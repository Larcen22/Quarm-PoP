import sys, re
from bs4 import BeautifulSoup

def extract(path):
    soup = BeautifulSoup(open(path,encoding='utf-8',errors='replace').read(),'html.parser')
    for t in soup(['script','style','noscript']): t.decompose()
    # main content: largest div containing the post title text; fallback body
    best=None; blen=0
    for d in soup.find_all('div'):
        L=len(d.get_text())
        if L>blen and L<200000: blen=L; best=d
    main = best or soup.body or soup
    out=[]
    seen=set()
    def emit(line):
        line=line.strip()
        if not line: return
        key=(line[:80])
        if key in seen and len(out)>2: 
            # allow repeats of list items but skip exact dupes within 3 lines
            pass
        out.append(line)
    for el in main.find_all(['h1','h2','h3','h4','h5','p','li','td','th','img','a']):
        if el.name=='img':
            src=el.get('src') or el.get('data-src') or ''
            alt=(el.get('alt') or '').strip()
            if str(src).startswith(('http','/')) and 'logo' not in str(src) and 'paypal' not in str(src):
                emit(f"[IMG] {src} | alt={alt}")
            continue
        txt=' '.join(el.get_text().split())
        if not txt: continue
        tag={'h1':'# ','h2':'## ','h3':'### ','h4':'#### ','h5':'##### '}.get(el.name,'')
        prefix='- ' if el.name=='li' else ''
        emit(f"{tag}{prefix}{txt}")
    # collapse consecutive duplicates
    res=[]
    for l in out:
        if res and res[-1]==l: continue
        res.append(l)
    return '\n'.join(res)

if __name__=='__main__':
    import glob, os
    total=0
    for f in sorted(sys.argv[1:] or glob.glob('html/*.html')):
        base=os.path.basename(f).replace('.html','')
        txt=extract(f)
        open(f"md/{base}.md",'w').write(txt)
        total+=len(txt)
        print(f"{len(txt):7d}  {base}")
    print("TOTAL", total)
