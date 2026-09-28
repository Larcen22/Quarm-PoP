import re, json, glob, os, time, urllib.request, urllib.parse

UA="Mozilla/5..0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
all_vids={}   # id -> {title?, author?, queries:[]}
order=[]
for f in sorted(glob.glob('yt/*.html')):
    q=os.path.basename(f).replace('.html','').replace('+',' ')
    html=open(f,encoding='utf-8',errors='replace').read()
    ids=re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
    seen=set()
    for vid in ids:
        if vid in seen or 'shorts' in vid.lower(): continue
        seen.add(vid)
        all_vids.setdefault(vid, {'queries':[]})['queries'].append(q)
        if vid not in order: order.append(vid)

print("unique videos:", len(order))
def oembed(vid):
    url=f"https://www.youtube.com/oembed?url={urllib.parse.quote(f'https://youtu.be/{vid}',safe='')}&format=json"
    try:
        req=urllib.request.Request(url, headers={'User-Agent':UA})
        d=json.load(urllib.request.urlopen(req, timeout=15))
        return d.get('title'), (d.get('author_name') or '')
    except Exception as e:
        return None, None

results=[]
for i,vid in enumerate(order):
    t,a=oembed(vid)
    if t is None and i<20:  # retry a few on failure
        time.sleep(1); t,a=oembed(vid)
    results.append({'id':vid,'title':t or '(unknown)','author':a,'queries':all_vids[vid]['queries'][:3]})
    if i%10==9: print(f"{i+1}/{len(order)} done")
json.dump(results, open('videos.json','w'), indent=1)
print("saved", len(results))
