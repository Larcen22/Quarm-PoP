#!/usr/bin/env python3
"""Audit eqprogression loot lists against PQDI (master source).

For every boss guide md file with a Loot section:
  1. Parse the item names from the md (list line + individual name lines).
  2. Fetch the boss's pqdi.cc /npc/<id> page and extract its /item/ drop links.
  3. Classify each loot item:
       ON-PAGE   : listed on that boss's PQDI page        -> link to that id
       TABLE     : exists in PQDI items table, not on this boss page -> keep + flag
       PHANTOM   : nowhere in PQDI                        -> REMOVE from our site
  4. Report extras: items on the boss's PQDI page we don't list (owner decides).

Outputs research/pqdi_drops.json and prints a per-boss report.
"""
import json, re, time, urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
ITEMS_JSON = "/home/larcen/Code/Axiom-DKP2/items.json"
OUT = "/home/larcen/Code/PoP/research/pqdi_drops.json"

BOSS_MAP = {
    "npc-aerin-dar.md": ("Aerin'Dar", 208074),
    "npc-agnarr-the-storm-lord.md": ("Agnarr", 209026),
    "npc-arlyxir.md": ("Arlyxir", 212023),
    "npc-avatar-of-earth.md": ("Avatar of Earth", 222040),
    "npc-bertoxxulous.md": ("Bertoxxulous", 223005),
    "npc-carprin-deatharn.md": ("Carprin Deatharn", 200232),
    "npc-grummus.md": ("Grummus", 205091),
    "npc-jiva.md": ("Jiva", 212014),
    "npc-lord-mithaniel-marr.md": ("Lord Mithaniel Marr", 220020),
    "npc-manaetic-behemoth.md": ("Manaetic Behemoth", 206046),
    "npc-rallos-zek-the-warlord.md": ("Rallos Zek", 214312),
    "npc-rizlona.md": ("Rizlona", 212026),
    "npc-saryrn-potorment.md": ("Saryrn", 223003),
    "npc-solusek-ro.md": ("Solusek Ro", 212025),
    "npc-tallon-zek-potactics.md": ("Tallon Zek", 223001),
    "npc-terris-thule-nightmare.md": ("Terris-Thule", 223002),
    "npc-the-keeper-of-sorrows-plane-of-torment-event.md": ("Keeper of Sorrows", 207015),
    "npc-the-protector-of-dresolik.md": ("Protector of Dresolik", 212408),
    "npc-vallon-zek-potactics.md": ("Vallon Zek", 999217),
    "npc-xanamech-nezmirthafen.md": ("Xanamech Nezmirthafen", 206208),
    "npc-xuzl.md": ("Xuzl", 212055),
}

def norm(s):
    s = re.sub(r"\s+", " ", s).strip().lower()
    for a, b in (("\u2019", "'"), ("\u2018", "'"), ("\u201c", '"'), ("\u201d", '"')):
        s = s.replace(a, b)
    return s

def variants(s):
    n = norm(s)
    return {n, n.replace("'", ""), n.replace("-", " "), n.replace("'", "").replace("-", " ")}

def parse_md_loot(path):
    """Return (list_line, [individual names]) from the Loot section."""
    lines = open(path).read().split("\n")
    try:
        start = next(i for i, l in enumerate(lines) if l.strip() == "Loot")
    except StopIteration:
        return None, []
    end = len(lines)
    for j in range(start + 1, len(lines)):
        s = lines[j].strip()
        if re.match(r"^(Fight Info|Random Loot|Note)", s):
            end = j; break
    section = [l.strip() for l in lines[start + 1:end]]
    list_line = None
    names = []
    for s in section:
        if not s or s.startswith("[IMG]"):
            continue
        if list_line is None and " " in s:      # first text line = concatenated list
            list_line = s; continue
        if re.match(r"^[A-Z]", s) and not s.endswith(".") and "**" not in s:
            names.append(s)
    return list_line, names

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")

def main():
    items = json.load(open(ITEMS_JSON))
    table = {}   # normalized name (+ apostrophe-stripped) -> largest id
    for row in items["rows"]:
        if not isinstance(row.get("id"), int) or not isinstance(row.get("NAME"), str):
            continue
        base = norm(row["NAME"])
        for key in {base, base.replace("'", "")}:
            prev = table.get(key)
            if prev is None or row["id"] > prev:
                table[key] = row["id"]

    drops_out = {}
    report = []
    for md, (boss, nid) in BOSS_MAP.items():
        list_line, names = parse_md_loot(f"md/{md}")
        if not names and not list_line:
            continue
        page = fetch(f"https://www.pqdi.cc/npc/{nid}")
        time.sleep(0.4)
        drops = {}   # normalized name -> (id, display)
        for m in re.finditer(r'<a[^>]*href="/item/(\d+)"[^>]*>([^<]*)</a>', page):
            iid, label = int(m.group(1)), m.group(2).strip()
            key = norm(label)
            if key not in drops or iid > drops[key][0]:
                drops[key] = (iid, label)
        drops_out[md] = {"boss": boss, "npc_id": nid,
                          "drops": [{"id": v[0], "name": v[1]} for k, v in sorted(drops.items(), key=lambda x: x[1][1])]}

        # tokenize the concatenated list line against known individual names
        pool = sorted(set(names), key=len, reverse=True)
        toks, rest = [], list_line or ""
        changed = True
        while changed and rest.strip():
            changed = False
            for k in pool:
                kn = norm(k)
                idx = norm(rest).find(kn)
                if idx != -1:
                    # map back to original casing span
                    start = len(rest) - len(norm(rest)) + idx if False else None
                    rest2 = re.sub(re.escape(k), " ", rest, count=1, flags=re.I)
                    toks.append(k); rest = rest2; changed = True; break
        remainder = re.sub(r"\s+", " ", rest).strip(" -–")

        rows = []
        for item in sorted(set(names)):
            iv = {norm(item), norm(item).replace("'", "")}
            hit_page = next(((d[0], d[1]) for k, d in drops.items() if k in iv or (k.replace("-", " ") in iv)), None)
            hit_table = next((table[k] for k in iv if k in table), None)
            status = "ON-PAGE" if hit_page else ("TABLE" if hit_table else "PHANTOM")
            rows.append({"item": item, "status": status,
                          "id": hit_page[0] if hit_page else hit_table,
                          "pqdi_name": hit_page[1] if hit_page else None})
        report.append({"md": md, "boss": boss, "npc_id": nid, "rows": rows, "remainder": remainder})

    json.dump(drops_out, open(OUT, "w"), indent=2)
    for r in report:
        print(f"\n===== {r['boss']} ({r['md']}, /npc/{r['npc_id']}) =====")
        if r["remainder"]:
            print(f"  LIST-LINE REMAINDER (unparsed): {r['remainder']}")
        for row in r["rows"]:
            tag = {"ON-PAGE": "OK ", "TABLE": "tbl", "PHANTOM": "XXX"}[row["status"]]
            extra = f" -> /item/{row['id']}" if row["id"] else ""
            pqdi_name = f" [pqdi: {row['pqdi_name']}]" if row["pqdi_name"] and norm(row["pqdi_name"]) != norm(row["item"]) else ""
            print(f"  [{tag}] {row['item']}{extra}{pqdi_name}")

if __name__ == "__main__":
    main()
