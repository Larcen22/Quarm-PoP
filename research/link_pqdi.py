#!/usr/bin/env python3
"""Link a guide page's loot items and boss names to pqdi.cc.

Usage:
  link_pqdi.py <page.html> --bosses "Grummus=205091,Terris-Thule=223002" [--dry-run]

- Loot: any <li>NAME</li> whose full text matches a name in Axiom-DKP2's
  items.json (PQDI items table dump) becomes
    <li><a class="pqdi-item" href="https://www.pqdi.cc/item/<id>" target="_blank"
           rel="noopener" data-pqdi-id="<id>">NAME</a></li>
  Ambiguous names (same name, multiple ids) use the LARGEST id — same owner
  convention as Axiom-DKP2.
- Bosses: the first <h2 class="section-title">NAME</h2> and first <h3>NAME</h3>
  are wrapped in an anchor to https://www.pqdi.cc/npc/<id>.

Idempotent: already-linked items/headings are skipped (detected by data-pqdi-id /
existing anchors). Prints a summary of matches + misses.
"""
import json, re, sys

ITEMS_JSON = "/home/larcen/Code/Axiom-DKP2/items.json"
ALIAS_JSON = "/home/larcen/Code/PoP/research/pqdi_item_aliases.json"  # guide spelling -> pqdi id
PQDI_BASE = "https://www.pqdi.cc"


def norm(s):
    """Normalize for matching: curly quotes -> straight, collapse whitespace."""
    s = re.sub(r"\s+", " ", s).strip().lower()
    for a, b in ("\u2019", "'"), ("\u2018", "'"), ("\u201c", '"'), ("\u201d", '"'):
        s = s.replace(a, b)
    return s

def load_items():
    data = json.load(open(ITEMS_JSON))
    by_name = {}   # normalized name -> largest id
    for row in data["rows"]:
        if not isinstance(row.get("id"), int) or not isinstance(row.get("NAME"), str):
            continue
        base = norm(row["NAME"])
        if not base:
            continue
        # PQDI often stores names without apostrophes ("Innovators Hammer")
        for key in {base, base.replace("'", "")}:   # register both spellings
            prev = by_name.get(key)
            if prev is None or row["id"] > prev:
                by_name[key] = row["id"]
    # aliases: our guide text spelling -> pqdi id (verified on the boss's pqdi page)
    try:
        for name, iid in json.load(open(ALIAS_JSON)).items():
            key = norm(name)
            prev = by_name.get(key)
            if prev is None or iid > prev:
                by_name[key] = iid
    except FileNotFoundError:
        pass
    return by_name


def link_loot(html, items):
    linked, missed = 0, []

    def repl(m):
        nonlocal linked
        inner = m.group(1).strip()
        if not inner or "<" in inner:            # only plain-text li's
            return m.group(0)
        cands = [inner]
        for sep in ("–", "-"):                  # fallback: "Item – annotation" → bare name
            if sep in inner:
                part = inner.split(sep)[0].strip()
                if len(part) > 3:
                    cands.append(part)
        iid = None
        for cand in cands:
            for key in (norm(cand), norm(cand).replace("'", "")):
                iid = items.get(key)
                if iid is not None:
                    break
            if iid is not None:
                break
        if iid is None:
            missed.append(inner)
            return m.group(0)
        linked += 1
        return (f'<li><a class="pqdi-item" href="{PQDI_BASE}/item/{iid}" target="_blank"'
                f' rel="noopener" data-pqdi-id="{iid}">{inner}</a></li>')

    # match simple single-line <li>TEXT</li> blocks (not nested lists)
    return re.sub(r"<li>([^<]+)</li>", repl, html), linked, missed


def link_bosses(html, bosses):
    done = []
    for name, nid in bosses.items():
        pat_h2 = rf'<h2 class="section-title">{re.escape(name)}</h2>'
        pat_h3 = rf"<h3>{re.escape(name)}</h3>"
        anchor = (f'<a class="pqdi-npc" href="{PQDI_BASE}/npc/{nid}" target="_blank"'
                  f' rel="noopener">{name}</a>')
        new, n2 = re.subn(pat_h2, rf"<h2 class=\"section-title\">{anchor}</h2>", html, count=1)
        new, n3 = re.subn(pat_h3, rf"<h3>{anchor}</h3>", new, count=1)
        if n2 or n3:
            done.append(name)
        html = new
    return html, done


def main():
    args = sys.argv[1:]
    page = None
    bosses_arg = None
    dry = False
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--bosses":
            bosses_arg = args[i + 1]; i += 2; continue
        if a == "--dry-run":
            dry = True; i += 1; continue
        page = a; i += 1
    if not page:
        print(__doc__); sys.exit(1)

    bosses = {}
    if bosses_arg:
        for pair in bosses_arg.split(","):
            n, v = pair.strip().split("=")
            bosses[n] = int(v)

    html = open(page).read()
    items = load_items()
    html, linked, missed = link_loot(html, items)
    if bosses:
        html, done = link_bosses(html, bosses)
    else:
        done = []

    if not dry:
        open(page, "w").write(html)

    print(f"loot linked: {linked}")
    print(f"boss headings linked: {done or 'none'}")
    uniq_missed = sorted(set(missed))
    print(f"li's with no PQDI item match ({len(uniq_missed)} unique):")
    for s in uniq_missed[:40]:
        print("  -", s)


if __name__ == "__main__":
    main()
