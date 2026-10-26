"""Read-only heuristic secret scan, including Git history and embedded ZIP/HTML data.

Reports locations and rule names only, never matching values. Does not validate
credentials against any service. A clean result is not a full security audit.
"""
import base64
import io
import json
import re
import subprocess
import zipfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def git(*args):
    return subprocess.check_output(
        ["git", "-c", f"safe.directory={ROOT.as_posix()}", *args], cwd=ROOT
    )


RULES = {
    "private-key": rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
    "github-token": rb"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b",
    "aws-access-key": rb"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "bearer-credential": rb"\bBearer\s+[A-Za-z0-9_.~-]{25,}",
    "jwt": rb"\beyJ[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\.[A-Za-z0-9_-]{12,}\b",
    "literal-secret-assignment": rb"(?:password|passwd|passwort|client[_-]?secret|api[_-]?key|access[_-]?token|refresh[_-]?token)\s*[\"']?\s*[:=]\s*[\"'][^\"'\r\n]{6,}[\"']",
    "url-password": rb"https?://[^\s/@:\"']+:[^\s/@\"']+@",
}


def scan_history():
    findings, seen = [], set()
    stats = {"commits": len(git("rev-list", "--all").splitlines()), "git_blobs": 0,
             "decoded_html": 0, "zip_entries": 0, "skipped_decodes": 0}

    def inspect(data, location, depth=0):
        if depth > 3:
            stats["skipped_decodes"] += 1
            return
        for name, pattern in RULES.items():
            if re.search(pattern, data, re.I):
                findings.append({"location": location, "rule": name})
        for encoded in re.findall(rb"[A-Za-z0-9+/]{200,}={0,2}", data):
            try:
                decoded = base64.b64decode(encoded, validate=True)
            except ValueError:
                continue
            if decoded.startswith(b"PK\x03\x04"):
                with zipfile.ZipFile(io.BytesIO(decoded)) as archive:
                    for entry in archive.infolist():
                        if entry.is_dir():
                            continue
                        if entry.file_size > 10_000_000:
                            stats["skipped_decodes"] += 1
                            continue
                        stats["zip_entries"] += 1
                        inspect(archive.read(entry), location + "!" + entry.filename, depth + 1)
            elif b"<html" in decoded[:500].lower() or b"<!doctype html" in decoded[:500].lower():
                stats["decoded_html"] += 1
                inspect(decoded, location + "!embedded-html", depth + 1)

    rows = git("rev-list", "--objects", "--all").splitlines()
    if "--index" in sys.argv:
        rows.extend(line.split(b" ")[1] + b" " + line.split(b"\t", 1)[1]
                    for line in git("ls-files", "--stage").splitlines())
    paths = {}
    for row in rows:
        oid, _, path = row.partition(b" ")
        paths.setdefault(oid, path)
    requested = b"\n".join(paths) + b"\n"
    kinds = subprocess.check_output(["git", "-c", f"safe.directory={ROOT.as_posix()}",
                "cat-file", "--batch-check=%(objectname) %(objecttype)"], input=requested, cwd=ROOT)
    blobs = [line.split()[0] for line in kinds.splitlines() if line.endswith(b" blob")]
    payload = subprocess.check_output(["git", "-c", f"safe.directory={ROOT.as_posix()}", "cat-file", "--batch"],
                input=b"\n".join(blobs) + b"\n", cwd=ROOT)
    offset = 0
    for oid in blobs:
        end = payload.index(b"\n", offset)
        size = int(payload[offset:end].rsplit(b" ", 1)[1])
        data = payload[end + 1:end + 1 + size]
        offset = end + 2 + size
        if oid in seen:
            continue
        seen.add(oid)
        stats["git_blobs"] += 1
        inspect(data, oid.decode()[:12] + ":" + paths[oid].decode("utf-8", "replace"))
    return {"scope": "all locally fetched Git refs, embedded archives" + (", staged index" if "--index" in sys.argv else ""), "stats": stats, "findings": findings}


if __name__ == "__main__":
    result = scan_history()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(1 if result["findings"] else 0)
