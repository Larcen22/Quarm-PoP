# BUILD BRIEF — EverQuest Planes of Power Guide Site

You are building ONE page of a static fan-guide website. Follow these rules exactly.

## 1. GitHub Pages compatibility (hard requirement)
- Pure static HTML/CSS/JS. Relative paths only (`assets/style.css`, `img/...`, sibling `.html` files). No build step, no absolute `file://` or `http://localhost` references. Must work when the repo is served from any subdirectory via GitHub Pages.

## 2. Page skeleton
Read `/home/larcen/Code/PoP/assets/page-template.html`. Copy its structure verbatim into your page: `<head>` (fonts + style.css), particles canvas, nav bar, footer, particles script. Then:
- Replace `[PAGE TITLE]` and the subtitle with the values from your assignment.
- Mark EXACTLY ONE link in `nav.topbar` with `class="active"` — the one matching your page.
- Keep the `<footer>` text exactly as in the template.

## 3. CSS classes available (in assets/style.css)
- `.page-header` (h1 + p.subtitle) for inner pages; home uses `<header class="hero">`.
- `section`, `section.narrow`, `.section-title`, `.section-sub`, `h2.subhead` (gold left-border subheading).
- `.encounter` > `.enc-head` (`<h3>` boss name + `<p class="enc-meta">` level/zone line) + `.enc-body` — one per boss/event.
- `.phase-block` (h3 + .phase-meta) for Plane of Time phases; put encounters inside.
- `table.stats` — rows: Level / HP / Hits / Resistances / Special Abilities / Procs.
- `ul.checklist` — flag items with gold diamond bullets.
- `figure.guide-img` > img + figcaption.
- `.video-grid` > `.video-card` (iframe + .video-caption).
- `.source-note` — attribution box.

## 4. Content fidelity (hard requirement)
Include ALL text from your assigned source files — every paragraph, step, list item, warning, and loot entry. No summarizing, no omitting, no rewriting mechanics. Convert markdown to HTML: `#`/`##` headings → h3/h4 inside sections; `**bold**` → `<strong>`; bullet lists → `<ul>`, numbered → `<ol>`.

## 5. Image rule
A source line like `[IMG] https://www.eqprogression.com/wp-content/uploads/<PATH> | alt=<TEXT>` becomes:
```html
<figure class="guide-img"><img src="img/<PATH>" alt="<TEXT>"><figcaption><TEXT></figcaption></figure>
```
Before writing the page, batch-check every image path you plan to use exists under `/home/larcen/Code/PoP/img/` (one bash command listing them). Omit any figure whose file is missing.

## 6. PQDI stats tables (hard requirement — user explicitly asked for special abilities)
Read `/home/larcen/Code/PoP/research/pqdi_bosses.json` (keyed by NPC id string). For EACH boss on your page, add a `<table class="stats">` inside its encounter block with rows:
- Level; HP (format with commas); Hits (as listed)
- Resistances — only if present in JSON (`MR/CR/FR/DR/PR`)
- Special Abilities — the FULL comma-separated list from the JSON. Include every single ability, never truncate or abbreviate.
- Procs / Spells — list them; if absent, omit the row (do not fabricate).
Add a caption line under each table: `Cross-referenced from pqdi.cc (Project Quarm Database Interface)`.

## 7. Video embeds
```html
<div class="video-card">
  <iframe src="https://www.youtube.com/embed/<ID>" title="<TITLE>" allowfullscreen></iframe>
  <div class="video-caption"><strong><TITLE></strong> — <CHANNEL></div>
</div>
```
Wrap in `<div class="video-grid">`. Embed ONLY the video IDs listed in your assignment.

## 8. Source note (end of page content)
A `.source-note` box listing the exact sources used: eqprogression.com guide pages, raspersrealm.com (Plane of Time only), pqdi.cc for stats.

## 9. Verify before finishing
- `bash ls` every img path you included.
- Confirm internal links match real filenames in `/home/larcen/Code/PoP/`.
- Write the final file with the write tool to your assigned output path.

## 10. Exclusions (hard requirement)
- Do NOT include any "Random Loot Server(s)" sections from the source files — they are omitted site-wide by user decision.
- Do NOT use `img/PoP_Planar_Flagging/PoP-Menu-EQProg.png` anywhere — banned site-wide; our own text covers it.
- Do NOT place per-item icon figures/images in Loot lists (the `[IMG]` item-icon screenshots that follow loot `<ul>` blocks). Loot items are linked to PQDI with hover tooltips instead (rule 12) — the link + tooltip replaces the image. Contextual quest-item screenshots inside narrative text (e.g. key-quest walkthroughs) are still fine.

## 12. PQDI links + item tooltips (hard requirement)
- Boss names link to their PQDI page: wrap BOTH the `<h2 class="section-title">NAME</h2>` and the encounter's `<h3>NAME</h3>` in `<a class="pqdi-npc" href="https://www.pqdi.cc/npc/<id>" target="_blank" rel="noopener">`. Boss IDs come from /home/larcen/Code/PoP/research/pqdi_bosses.json (also listed in each page's brief).
- Loot items link to their PQDI item pages with hover tooltips. AFTER writing the page, run:
  `python3 /home/larcen/Code/PoP/research/link_pqdi.py <page.html> --bosses "BossName=id,Boss2=id2"`
  It auto-wraps matching loot `<li>` names (matched against PQDI's items table) in `<a class="pqdi-item" ... data-pqdi-id="...">` and links the boss headings. Idempotent — safe to re-run. Review its "no match" output: if a missed li is genuinely a loot item that exists on PQDI under a different name, fix it manually.
- The page template already includes `<script src="assets/pqdi-tooltip.js"></script>` (hover tooltips) and the image-sizing script — keep both when copying the skeleton.

## 11. Write incrementally (hard requirement — pages exceed single-output limits)
Never try to generate the whole page in one tool call. Build it in chunks:
1. `write` the full skeleton: head, particles canvas, nav, page-header, FIRST section only, then a placeholder line `<!-- APPEND-HERE -->`, then footer + scripts (particles script and the image-sizing script copied from flagging.html).
2. Repeat: use `edit` to replace `<!-- APPEND-HERE -->` with the next chunk of sections PLUS a fresh `<!-- APPEND-HERE -->`. Keep each chunk under ~6 KB of generated HTML.
3. Final edit: remove the last `<!-- APPEND-HERE -->` placeholder (replace it with empty text).
4. Verify no `APPEND-HERE` remains and all planned sections are present before finishing.

## 13. PQDI is the master source for stats (hard requirement)
When eqprogression's fight-info text gives HP or hit numbers for a boss that has a PQDI entry, **replace them with the PQDI values** from /home/larcen/Code/PoP/research/pqdi_bosses.json and note the original estimate in parentheses. Pattern used on bosses-tier1.html:
- `<li>1,100,000 HP (PQDI; eqprogression estimated 500K MoTM)</li>`
- `<li>Hits 661–1801</li>` (when the original claim is far off) or `<li>Hits 221–1179 (PQDI; eqprogression estimated 1500+)</li>`
Rules:
- Only normalize claims about THE BOSS itself. Claims about adds, trash, or other zone mobs stay verbatim. /home/larcen/Code/PoP/research/stats_discrepancies.md lists every claim with its context line — check which mob each refers to before replacing.
- The PQDI stats table (rule 6) already carries the authoritative values; the fight-info bullets must not contradict it.
- Bosses/mobs with NO PQDI entry (e.g. the six Plane of Justice trial mobs): keep eqprogression numbers verbatim — there is no master to compare against.

## 14. Spell links + tooltips (hard requirement)
In each boss's stats table, list the PQDI spells as linked tooltips:
`<a class="pqdi-spell" href="https://www.pqdi.cc/spell/<id>" target="_blank" rel="noopener" data-pqdi-spell="<id>">Name</a>`
Rows (data from /home/larcen/Code/PoP/research/pqdi_bosses.json, keyed by npc id):
- `Special Abilities` — plain comma list (`special_abilities`).
- `Can Cast` — the boss's active spells (`cast_spells`, each linked).
- `Procs` — on-hit procs (`procs`, each linked).
Omit a row the boss doesn't have. The shared tooltip script (assets/pqdi-tooltip.js, already in the template) handles `data-pqdi-spell` automatically: it fetches pqdi.cc's `/api/v1/spell/<id>` JSON and shows name + effects + recast/target/resist in a hover panel — no extra per-page JS needed.
