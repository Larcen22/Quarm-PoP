import sys, re
from bs4 import BeautifulSoup

def extract(path):
    with open(path, encoding='utf-8', errors='replace') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    for t in soup(['script','style','noscript']):
        t.decompose()
    # find main content container (WordPress)
    main = None
    for sel in ['article','main','#content','.entry-content','.post']:
        el = soup.select_one(sel)
        if el:
            main = el; break
    if not main: main = soup.body or soup
    out=[]
    def walk(el, depth=0):
        name = el.name
        if name in ('h1','h2','h3','h4'):
            txt=' '.join(el.get_text().split())
            lvl=int(name[1])
            out.append('\n'+'#'*lvl+' '+txt)
        elif name=='li':
            txt=' '.join(el.get_text().split())
            if txt: out.append('- '+txt)
        elif name in ('p','div'):
            # only direct text blocks to avoid dupes from nested divs
            kids=[c for c in el.children if getattr(c,'name',None) and c.name not in ('h1','h2','h3','h4','li','ul','ol','table')]
            txt=' '.join(el.get_text().split())
            if len(txt)>0: out.append(txt)
        elif name=='img':
            src=el.get('src') or el.get('data-src') or ''
            alt=el.get('alt','')
            if src and not src.startswith('data:'):
                out.append(f'[IMG] {src} | alt={alt}')
    for el in main.find_all(['h1','h2','h3','h4','p','li','img']):
        txt=' '.join(el.get_text().split()) if el.name!='img' else ''
        if el.name=='img':
            src=el.get('src') or el.get('data-src') or ''
            alt=el.get('alt','')
            if src and not str(src).startswith('data:'): out.append(f'[IMG] {src} | alt={alt}')
        elif txt:
            tag={'h1':'# ','h2':'## ','h3':'### ','h4':'#### '}.get(el.name,'')
            prefix='- ' if el.name=='li' else ''
            line=f"{tag}{prefix}{txt}"
            # dedupe consecutive
            if not out or out[-1]!=line: out.append(line)
    return '\n'.join(out)

if __name__=='__main__':
    for p in sys.argv[1:]:
        print(f"===== {p} =====")
        print(extract(p))
