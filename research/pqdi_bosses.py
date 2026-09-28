#!/usr/bin/env python3
"""Fetch PQDI /npc/<id> pages for all PoP bosses and extract stats.

Output: research/pqdi_bosses.json  (structured) + research/html/pqdi/*.html (raw saves)
Captures: quick facts (level, HP, hits, resists), special abilities, procs/spells.
"""
import json, re, time, html as h, os, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
BASE = "https://www.pqdi.cc/npc/"
OUT_HTML = "/home/larcen/Code/PoP/research/html/pqdi"
os.makedirs(OUT_HTML, exist_ok=True)

BOSS_IDS = {
    # Tier 1
    205091: "Grummus",
    223002: "Terris-Thule",
    206046: "Manaetic Behemoth",
    206208: "Xanamech Nezmirthafen",
    201074: "The Seventh Hammer",
    # Tier 2
    208074: "Aerin'Dar",
    200226: "Bertoxxulous (SoV)",
    223005: "Bertoxxulous (PoT)",
    200232: "Carprin Deatharn",
    223003: "Saryrn",
    207015: "Keeper of Sorrows",
    # Tier 3
    209026: "Agnarr the Storm Lord",
    220020: "Lord Mithaniel Marr",
    223001: "Tallon Zek",
    999217: "Vallon Zek",
    223006: "Rallos Zek (PoT)",
    214312: "Rallos Zek the Warlord (Tier 3)",
    # Solusek Ro Tower
    212023: "Arlxir",
    212014: "Jiva",
    212026: "Rizlona",
    212408: "Protector of Dresolik",
    212055: "Xuzl",
    212025: "Solusek Ro",
    # Elementals — Air
    215056: "Xegony the Queen of Air",
    215054: "Baltaldor the Cursed",
    # Fire
    217440: "Fennin Ro the Tyrant of Fire",
    217050: "Guardian of Doomfire",
    217425: "Azobian the Darklord",
    217453: "Hebabbilys the Ragelord",
    217426: "Javonn the Overlord",
    217427: "Reaxnous the Chaoslord",
    217432: "Chancellor Kirtra",
    217433: "Chancellor Traxom",
    217429: "Omni Magus Crato",
    217428: "Warlord Prollaz",
    # Water
    216048: "Coirnav the Avatar of Water",
    216042: "Grioihin the Wise",
    216043: "Hydrotha",
    216041: "Krziik the Mighty",
    216040: "Ofossaa the Enlightened",
    # Earth A
    222040: "Avatar of Earth",
    218374: "Peregrin Rockskull Golem",
    218360: "A Monstrous Mudwalker",
    218363: "Derugoak Bloodwalker",
    218038: "Tantisala Jaggedtooth",
    218375: "Mystical Arbitor of Earth",
    # Earth B
    222037: "War Chieftan Awisano",
    222035: "War Chieftan Birak",
    222036: "War Chieftan Galronar",
    222038: "Warlord Gintolaken",
    # PoT Phase 1
    223044: "Neimon of Air",
    223032: "Terlok of Earth",
    223018: "Kazrok of Fire",
    223037: "Anar of Water",
    223029: "Rythor of the Undead",
    # PoT Phase 2
    223075: "Windshapen Warlord of Air",
    223072: "Earthen Overseer",
    223073: "Gutripping War Beast",
    223074: "War Shapen Emissary",
    223076: "Ralthos Enrok",
    # PoT Phase 3
    223084: "A Ferocious Warboar",
    223083: "Deathbringer Blackheart",
    223090: "Xeroan Xi`Geruonask",
    223091: "Kraksmaal Fir`Dethsin",
    223096: "A Deadly Warboar",
    223097: "Deathbringer Skullsmash",
    223105: "Sinrunal Gorgedreal",
    223101: "Herlsoakian",
    223108: "A Needletusk Warboar",
    223109: "Deathbringer Rianit",
    223116: "Dersool Fal`Giersnaol",
    223115: "Xerskel Gerodnsal",
    223123: "Dark Knight of Terris",
    223124: "Undead Squad Leader",
    223132: "Champion of Torment",
    223131: "Dreamwarp",
    223133: "Supernatural Guardian",
    223134: "Avatar of the Elements",
    # PoT Phase 5 (Major Gods)
    76600: "Innoruuk (SoV ref only)",
    223007: "Innoruuk (PoT)",
    223004: "Cazic Thule (PoT)",
    # Final
    223008: "Quarm",
}


def fetch(url, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            return urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")
        except Exception as e:
            if attempt == retries - 1:
                print(f"FAIL {url}: {e}")
                return None
            time.sleep(2 + attempt * 3)


def strip_tags(s):
    s = re.sub(r'<[^>]+>', ' ', s)
    s = h.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def extract(raw):
    """Parse the PQDI NPC page into a stats dict."""
    d = {"url_ok": True}

    # Title / name
    m = re.search(r'<title>([^<]+)</title>', raw)
    if m:
        d["page_title"] = strip_tags(m.group(1))

    # Quick Facts table — grab the whole main content area text
    body = raw[raw.find('<body'):]
    plain = strip_tags(body)

    def find(pattern):
        mm = re.search(pattern, plain)
        return mm.group(1).strip() if mm else None

    d["expansion"] = find(r'Expansion:\s*([A-Za-z ]+?)\s+(?:Zone:|Level)')
    d["zone"] = find(r'Zone:\s*(.+?)\s+Level\s+\d+')
    m = re.search(r'Level\s+(\d+)\s+', plain)
    if m:
        d["level"] = int(m.group(1))
    m = re.search(r'Hits for\s*([\d,\-\s]+?)(?:\s+Has|\s*\|)', plain)
    if m:
        d["hits"] = strip_tags(m.group(1)).strip()
    m = re.search(r'Has\s+([\d,]+)\s+hitpoints', plain)
    if m:
        d["hp"] = int(m.group(1).replace(",", ""))

    # Resist table (MR CR FR DR PR) — appears as header row then values
    m = re.search(r'MR\s*CR\s*FR\s*DR\s*PR\s+([\d\s,]+)', plain)
    if m:
        vals = [int(x.replace(",", "")) for x in m.group(1).split()]
        if len(vals) >= 5:
            d["resists"] = {"MR": vals[0], "CR": vals[1], "FR": vals[2], "DR": vals[3], "PR": vals[4]}

    # Special abilities — <h5>Special Abilities : </h5><p>comma, list</p>
    m = re.search(r'Special Abilities\s*:\s*</h5>\s*<p>(.*?)</p>', raw, re.S)
    if m:
        d["special_abilities"] = [x.strip() for x in strip_tags(m.group(1)).split(',') if x.strip()]

    # Can cast these spells — everything up to the next <h5> (usually 'Can proc:')
    m = re.search(r'Can cast these spells\s*:\s*</h5>(.*?)(?=<h5)', raw, re.S)
    if m:
        seg = m.group(1)
        pairs = re.findall(r'<a href="/spell/(\d+)"[^>]*>([^<]+)</a>', seg)
        seen, uniq = set(), []
        for sid, name in pairs:
            key = (sid, strip_tags(name))
            if key not in seen:
                seen.add(key)
                uniq.append({"id": int(sid), "name": strip_tags(name)})
        if uniq:
            d["cast_spells"] = uniq

    # Procs / spells — spell links inside <dd> blocks after '<h5>Can proc:</h5>',
    # ending at the closing </article> of that section.
    m = re.search(r'Can proc:</h5>(.*?)</article>', raw, re.S)
    if m:
        seg = m.group(1)
        pairs = re.findall(r'<a href="/spell/(\d+)"[^>]*>([^<]+)</a>', seg)
        # de-dup preserving order
        seen, uniq = set(), []
        for sid, name in pairs:
            key = (sid, strip_tags(name))
            if key not in seen:
                seen.add(key)
                uniq.append({"id": int(sid), "name": strip_tags(name)})
        if uniq:
            d["procs"] = uniq
    else:
        m2 = re.search(r'Can proc:\s*(.+?)(?:No clue|Database version|$)', plain, re.S)
        if m2:
            d["procs_raw"] = strip_tags(m2.group(1))[:3000]

    return d


def main():
    results = {}
    for nid, label in BOSS_IDS.items():
        url = BASE + str(nid)
        fname = f"npc-{nid}.html"
        path = os.path.join(OUT_HTML, fname)
        if not os.path.exists(path):
            raw = fetch(url)
            if raw is None:
                results[str(nid)] = {"label": label, "error": "fetch failed"}
                continue
            open(path, "w", encoding="utf-8").write(raw)
            time.sleep(0.4)  # be polite
        else:
            raw = open(path, encoding="utf-8").read()
        if len(raw) < 5000:
            results[str(nid)] = {"label": label, "error": f"unexpectedly small page ({len(raw)})"}
            continue
        d = extract(raw)
        d["label"] = label
        results[str(nid)] = d
        print(f"{nid:>7}  {label:35s}  hp={d.get('hp')}  hits={d.get('hits')}  lvl={d.get('level')}")

    out = "/home/larcen/Code/PoP/research/pqdi_bosses.json"
    json.dump(results, open(out, "w"), indent=1)
    print(f"\nWrote {out} ({len(results)} bosses)")


if __name__ == "__main__":
    main()
