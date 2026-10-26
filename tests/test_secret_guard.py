"""Check the scanner's clean and credential-shaped fixture paths without real credentials."""
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("check_public_secrets", ROOT / "scripts/check-public-secrets.py")
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)


class PublicSecretGuard(unittest.TestCase):
    def test_clean_and_synthetic_credential(self):
        with tempfile.TemporaryDirectory(prefix="www-ch-scanner-") as directory:
            repo = Path(directory)
            def git(*args):
                return subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", *args], cwd=repo, check=True, capture_output=True)
            git("init", "-b", "main")
            target = repo / "fixture.txt"
            target.write_text("Public notary identifier: 1499\n")
            git("add", "fixture.txt")
            git("commit", "-m", "Clean fixture")
            previous_root = scanner.ROOT
            try:
                scanner.ROOT = repo
                self.assertEqual(scanner.scan_history()["findings"], [])
                # A recognisable format assembled at runtime; never a real key.
                target.write_text("ghp" + "_" + "A" * 36 + "\n")
                git("add", "fixture.txt")
                git("commit", "-m", "Synthetic scanner fixture")
                found = scanner.scan_history()["findings"]
                self.assertTrue(any(x["rule"] == "github-token" for x in found))
                self.assertTrue(all(set(x) == {"location", "rule"} for x in found))
            finally:
                scanner.ROOT = previous_root
