#!/usr/bin/env python3
"""Run in an environment with access to the original website. No dependencies."""
from pathlib import Path
from urllib.request import urlopen, Request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
import hashlib, json, concurrent.futures

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://christmann-heise.de/'
PAGES = ['', 'rechtsanwaeltinnen/', 'notarinnen/', 'mediatorin/', 'kontakt/', 'impressum/', 'datenschutz/']
KNOWN = {
 'christmann.jpg': ORIGIN+'wp-content/uploads/2018/08/RechtsanwaeltinnenSC-e1534960103594.jpg',
 'heise.jpg': ORIGIN+'wp-content/uploads/2018/08/RechtsanwaeltinnenHH-e1534960135173.jpg'
}
class Assets(HTMLParser):
    def __init__(self): super().__init__(); self.urls = set()
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag=='img' and a.get('src'): self.urls.add(a['src'])
        if tag=='link' and a.get('rel')=='stylesheet' and a.get('href'): self.urls.add(a['href'])

def download(url, target, image=False):
    try:
        with urlopen(Request(url,headers={'User-Agent':'Christmann-Heise-Website-Migration/1.0'}),timeout=20) as r:
            b=r.read(20_000_001); typ=r.headers.get('Content-Type','')
        if len(b)>20_000_000: raise ValueError('Datei größer als 20 MB')
        if image and not b.startswith((b'\xff\xd8\xff',b'\x89PNG\r\n\x1a\n')): raise ValueError('Kein gültiges JPEG/PNG')
        target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
        return {'url':url,'path':str(target.relative_to(ROOT)),'status':'downloaded','sha256':hashlib.sha256(b).hexdigest(),'content_type':typ}
    except Exception as e:
        return {'url':url,'status':'failed','reason':str(e)}

def main():
    records=[]; discovered=set()
    for page in PAGES:
        target=ROOT/'sources/original-html'/((page.strip('/') or 'startseite')+'.html')
        record=download(urljoin(ORIGIN,page),target);records.append(record)
        if record['status']=='downloaded':
            p=Assets();p.feed(target.read_text(errors='replace'))
            discovered.update(urljoin(ORIGIN,u) for u in p.urls)
    jobs=[(u,ROOT/'assets'/name,True) for name,u in KNOWN.items()]
    for url in discovered:
        if urlparse(url).hostname not in ('christmann-heise.de','www.christmann-heise.de') or url in KNOWN.values():continue
        name=hashlib.sha256(url.encode()).hexdigest()[:10]+'-'+Path(urlparse(url).path).name
        jobs.append((url,ROOT/'sources/original-assets'/name,False))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        records.extend(pool.map(lambda a:download(*a),jobs))
    (ROOT/'sources/download-manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
    for r in records:print(r['status'],r['url'])
    print('Originale prüfen, Bildzuordnung und Markenfarbe bestätigen; danach python3 scripts/build.py ausführen.')
if __name__=='__main__': main()
