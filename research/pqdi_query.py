import re, html as h, urllib.request, urllib.parse, http.cookiejar, sys

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def fetch(url, data=None):
    if data is not None:
        req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(), headers={"User-Agent": UA})
    else:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
    return opener.open(req, timeout=30).read().decode("utf-8", "replace")

def search_npc(name):
    page = fetch("https://www.pqdi.cc/npcs")
    m = re.search(r'name="csrf_token" type="hidden" value="([^"]+)"', page) or \
        re.search(r'id="csrf_token"[^>]*value="([^"]+)"', page)
    token = m.group(1) if m else ""
    data = {"npc_name": name, "csrf_token": token}
    for k in ["class_select","exp_select","gives_exp","hpmax_int","hpmin_int","max_lvl","min_lvl","race_select"]:
        data[k] = ""
    page2 = fetch("https://www.pqdi.cc/npcs", data=data)
    txt = re.sub(r'<script[^>]*>.*?</script>', '', page2, flags=re.S)
    body = txt[txt.find('<body'):]
    plain = h.unescape(re.sub(r'<[^>]+>', '|', body)).strip()
    return page2, plain

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "Quarm"
    raw, plain = search_npc(name)
    open(f"html/pqdi-npc-{name.lower().replace(' ', '-')}.html", "w").write(raw)
    print(plain[-3000:])
