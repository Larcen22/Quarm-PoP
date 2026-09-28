import sys, re, glob, os
from bs4 import BeautifulSoup

def extract(path):
    soup = BeautifulSoup(open(path,encoding='utf-8',errors='replace').read(),'html.parser')
    for t in soup(['script','style','noscript']): t.decompose()
    blocks = soup.find_all('div', class_='et_pb_text_inner')
    out=[]
    def emit(line):
        line=re.sub(r'\s+',' ',line).strip()
        if not line: return
        if out and out[-1]==line: return
        out.append(line)
    for b in blocks:
        for el in b.find_all(['h1','h2','h3','h4','h5','p','li','td','th','img']):
            if el.name=='img':
                src=el.get('src') or el.get('data-src') or ''
                alt=(el.get('alt') or '').strip()
                s=str(src)
                if s.startswith(('http','/')) and not any(x in s for x in ['logo','paypal','youtube-pic','contact-me','404.png']):
                    emit(f"[IMG] {s} | alt={alt}")
                continue
            txt=' '.join(el.get_text().split())
            if not txt: continue
            tag={'h1':'# ','h2':'## ','h3':'### ','h4':'#### '}.get(el.name,'')
            prefix='- ' if el.name=='li' else ''
            emit(f"{tag}{prefix}{txt}")
    return '\n'.join(out)

if __name__=='__main__':
    total=0
    for f in sorted(sys.argv[1:] or glob.glob('html/*.html')):
        base=os.path.basename(f).replace('.html','')
        txt=extract(f)
        open(f"md/{base}.md",'w').write(txt)
        total+=len(txt)
    print("TOTAL", total, "files:", len(glob.glob('md/*.md')))
