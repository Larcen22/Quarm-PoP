# Supplemental Research — Plane of Time (all 6 phases) + cross-checks

## Primary new source: Rasper's Realm (raspersrealm.com)

**URL:** https://www.raspersrealm.com/Everquest/PoP/raidTime.html
- Old-school EQ fan site with a complete, phase-by-phase Plane of Time raid guide.
- Site is live and reachable via curl (browser UA). Full PoP section exists:
  index, gearSummary, gearVisibleArmor, miscSpells, miscProgression, openPoJ/I/D/N/S/V/CoD/T/BoT/HoH/PoTact/SolRo/W/E/A/F, raidTime.
- All pages downloaded to `html/raspers-*.html`; PoT maps to `imgs/maps_potimea.txt`, `imgs/maps_potimeb.txt`.
- Extracted text: `md/raspers-pot-full.txt` (14,371 chars).

### Cross-check vs eqprogression.com
- Phase 1 boss names match exactly: Neimon of Air, Terlok of Earth, Kazrok of Fire, Anar of Water, Rythor of the Undead.
- Phase 5 (Major Gods) matches: Cazic-Thule, Bertoxxulous, Rallos Zek details consistent with eqprogression phase-5 file (Bertoxxulous resist/ooze emote mechanic, Rallos power gains at 75/50/25%).
- Two independent sources agree → high confidence.

## Plane of Time — full raid structure (Rasper's Realm)

**Overview:** Final zone. Raid consists of **6 phases**; after each phase you get extra time to complete the raid. Start in "Plane of Time A"; portals: Z = zone in/out, A = Undead, B = Fire, C = Earth, D = Water, E = Air.

### Phase 1 — The Five Trials
- 5 events, max **18 people per event**, all 5 must complete within **1 hour** to advance script. Lockout: 12 hours.
- Each event drops 1 loot from: Mask of Conceptual Energy, Pulsing Emerald Hoop, Ring of Force, Smooth Onyx Torque, Wristguard of Keen Vision.

| Trial | Mobs → Boss | Notes (Rasper's) |
|---|---|---|
| Air | 4x An Air Phoenix Noble (~900 hits) → 4x Servitor of Xegony (~1k, mez-immune, rootable) → **Neimon of Air** | Neimon: 1100 hits, flurries, AE rampage, 125pt DS, AE slow/spell-slow/550dd. (eqprogression adds: Caustic Aura dispel, Caustic Atmosphere PBAE) |
| Earth | 3x a pile of living rubble (~1k, mez/root immune; each death spawns 1–4 rock shaped assassins, 800 hits, mezz+root) → after 10 kills **Terlok of Earth** | Terlok: quads for 1100, no tricks. (eqprogression: 290K HP) |
| Fire | fire mephits until **Kazrok of Fire** | Kazrok: 1150 hits, flurries, AE rampages, 75pt DS, AE spell-slow + 225 DoT. (eqprogression: Pyrokinetic Aura dispel, Black Pyre PBAE, adds at 75/50/25%) |
| Water | **Anar of Water** up with 2x a triloun gatherer; at 90% & 50% AE snare/slow/850dd + summons 2x a deepwater triloun (~1k, rootable) | Anar: 1150 hits, flurries, AE rampages. (eqprogression phase-1 file covers this trial too) |
| Undead | 3x an undead guardian (900ish, mezz+root) → 4 more (harder) → 3rd wave (harder, mez-immune) → **Rythor of the Undead** | Rythor: 1150 hits, flurries, AE spell-cost-increase + 350 DoT + 575dd, plus 1k dd w/ stun on tank. |

### Phase 2 — The Three Branches
- After phase 1 each area portals into the phase 2 area. Split into **3 branches**: Earth+Air together, Water+Fire together, Undead alone. Each branch: trash chunk → second wave + boss at end. Time: 1 hour (+ leftover). Lockout from here on: **5.5 days**.
- Bosses (one per branch area):
  - **Windshapen Warlord of Air** — hits 1200, pure melee.
  - **Earthen Overseer** — hits 1200, flurries, immune to slow, pure melee.
  - **Gutripping War Beast** — hits 1500, pure melee.
  - **War Shapen Emissary** — hits 1200 and rampages.
  - **Ralthos Enrok** — hits 1100, flurries, casts Shadowknight spells.
- Each boss drops one loot from: Cloak of Ferocity, Hoop of the Enlightened, Cudgel of Wrecking, Shield of the Vortex, Wand of the Vortex, Veil of Warmth, Tiny Jade Ring, Gauntlets of Disruption, Glowing Chains, Drape of the Unending, Girdle of Restoration.

### Phase 3 — The Trash Clear
- Branches reunite; **8 waves**, each with trash (pure melee) + 2 bosses = 16 bosses:
  - W1: A Ferocious Warboar (≤2k, flurries, procs 200dd+stun); Deathbringer Blackheart (≤2k, rampages, procs 2–3.5k dd)
  - W2: Xeroan Xi`Geruonask (≤2k, AE DoT + mana drain proc); Kraksmaal Fir`Dethsin (≤2k, flurries, 667 DoT proc)
  - W3: A Deadly Warboar (≤2k, rampages, AE 1200dd+stun proc); Deathbringer Skullsmash (≤2k, 2k dd + 500 DoT + stun proc)
  - W4: Sinrunal Gorgedreal (≤2k, AE silence proc); Herlsoakian (≤2k, AE attack+armor debuff proc)
  - W5: A Needletusk Warboar (≤2k, flurries, AE 500 DoT proc); Deathbringer Rianit (≤2k, rampages, 1600dd-on-tank proc)
  - W6: Dersool Fal`Giersnaol (≤2k, rampages, AE 600dd+stun proc); Xerskel Gerodnsal (≤2k, unslowable, AE 1500 mana drain + Cleric spells)
  - W7: Dark Knight of Terris (≤2k, AE slow + small DoT, 36 disease counters); Undead Squad Leader (≤2k, rampages, 400pt lifetap proc)
  - W8: Champion of Torment (≤2k, flurries, AE 800dd+flux proc); Dreamwarp (≤2k, AE 1500dd proc)
- Each of the 16 bosses can drop **Time Phased Quintessence** (backflag for Plane of Time) + up to one of: Elemental Greaves Mold, Elemental Chain/Leather/Silk Pant Pattern, Cloak of Wishes, Dagger of Distraction, Necklace of Celestial Energy, Ossein of Limitless Time, Protective Sleeves, Time Traveler's Abandoned Notebook.
- After wave 8 bosses die: **two massive rock golems** spawn at the portal; total time for phase = 75 min (+ leftover).
- Final bosses:
  - **Supernatural Guardian** — hits ≤1700, flurries, unslowable, procs 200dd+stun.
  - **Avatar of the Elements** — hits ≤1700, fairly resistant, procs AE snare + 1100dd.
- Both rock bosses drop Time Phased Quintessence + one of: Earring of Xaoth Kor, Pauldrons of Purity, Ethereal Destroyer, Faceguard of Frenzy, Fiery Crystal Guard, Mask of Strategic Insight, Timeless Coral Greatsword.

### Phase 4 — The Lesser Gods
- Clear central-area trash, then defeat **Saryrn, Terris Thule, Vallon Zek, Tallon Zek** in any order; time = 4 hours (+ leftover). (eqprogression phase-4 file covers these too.)

- **Saryrn** — up to 2500 single-target rampage. Spells:
  - Torrent of Agony: 1500dd, 60% aggro reduction + 40% slow on tank; 20 disease counters.
  - Horrifying Affliction: 375-range AE, drains 500 mana then 175/tick, reduces spell damage; overwrites KEI line.
  - Torrential Torment: 125-range AE, 45 mana/tick drain; 9 curse counters; overwrites Ranger's self-buff.
  - Summons four adds at 90/50/10%: random mix of A Mouth of Insanity (unrootable), A Mouth of Dementia (rootable, procs root), A Tormentor (unrootable/unmezzable, backstabs), A Twisted Tormentor (rootable). Adds have decent HP and do not despawn.
  - Drops 3 from: Shroud of Provocation, Time`s Antithesis, Veil of Lost Hopes, Gloves of the Unseen, Runewarded Belt, Symbol of the Planemasters, Edge of Eternity, Ring of Evasion, Cap of Flowing Time, Girdle of Intense Durability.
- **Terris Thule** — up to 2500 single-target rampage. Spells:
  - Quivering Nightmares: 375-range AE reducing all primary stats by 200 (overwrites Beastlord Ferocity etc.).
  - Phantasmal Torment: 375-range AE, 200 DoT + 150/tick mana drain; overwrites Enchanter KEI line.
  - Adds at 90/50/10%: A Nightmare Knight of Terris (mana-drain+mez proc), A Phantasm of Terris (mana-drain+mez proc), A Summoned Guardian of Terris, A Summoned Knight of Terris (both unmezzable/unrootable). Do not despawn.
  - Drops 3 from: Earring of Corporeal Essence, Talisman of Tainted Energy, Hammer of Hours, Armguards of the Brute, Cape of Endless Torment, Cudgel of Venomous Hatred, Orb of Clinging Death, Coif of Flowing Time, Vanazir Dreamer`s Despair.
- **Tallon Zek** — hits 3000, single-target rampage. Spells: Tallon's Balance (−300 resists); Planeshift (375-range AE, +50% spell cost); Strategic Blow (2k dd + 500 DoT + short stun on tank); Barb of Tallon ×4 variants (ice AE snare/slow/2k; fire AE 2500dd; disease AE 300 DoT + AC/hate debuff; poison AE 2650dd).
  - Drops 3 from: Cloak of the Falling Skies, Serpent of Vindication, Hopebringer, Winged Storm Boots, Band of Prismatic Focus, Amulet of Crystal Dreams, Tactician`s Shield, Mantle of Deadly Precision, Bracer of Precision, Circlet of Flowing Time.
- **Vallon Zek** — hits 3000, single-target rampage. Spells: Blade of Vallon (4–6k dd on tank ~1/min); Vallon's Precision (93-range AE increasing aggro generation); Tactical Strike (30s stun + FD on tank). At 50% spawns **two clones** (~1800 hits, unmezzable, very root-resistant, lower HP — kill first; do not despawn).
  - Drops 3 from: Earring of Temporal Solstice, Cord of Potential, Hammer of Holy Vengeance, Wand of Temporal Power, Shinai of the Ancients, Globe of Mystical Protection, Shoes of Fleeting Fury, Bow of the Tempest, Helm of Flowing Time, Temporal Chainmail Sleeves.

### Phase 5 — The Major Gods
- Clear central-area trash, then defeat **Bertoxxulous, Innoruuk, Cazic Thule, Rallos Zek** in any order; time = 4 hours (+ leftover). (eqprogression phase-5 file covers these too.)

- **Bertoxxulous** — up to 3000 hits at fight end, AE rampage. Nearly spell-immune at start; resists drop while melee damage scales as HP drops. Spells: Rain of Bile (975dd + 275 mana drain, up to 3x if you don't move); Black Plague (AE snare + 700 DoT, 18 disease counters).
  - Drops 3 from: Collar of Catastrophe, Veil of the Inferno, Eye of Dreams, Celestial Cloak, Belt of Temporal Bindings, Timeless Leather Tunic Pattern, Symbol of Ancient Summoning, Timespinner Blade of the Hunter, Boots of Despair, Greatblade of Chaos, Pulsing Onyx Ring, Leggings of Furious Might.
- **Innoruuk** — up to 3500 hits, AE rampages, flurries. Barrier of Hatred (225 DS + 1800pt rune); Seething Hatred ×2 (200-range 325dd+aggro debuff; 125-range 550 DoT+aggro debuff+fear). Intended to spawn 3 adds at 66% and 4 at 20% — "may be broken" per source.
  - Drops 3 from: Earring of Celestial Energy, Necklace of Eternal Visions, Mantle of Pure Spirit, Shroud of Survival, Timeless Chain Tunic Pattern, Serrated Dart of Energy, Songblade of the Eternal, Jagged Timeforged Blade, Barrier of Freezing Winds, Gloves of Airy Mists, Girdle of Stability, Bracer of Timeless Rage.
- **Cazic Thule** — up to 3000 hits, AE rampages. Aura of Fear (375-range AE 2k dd + 550 DoT + stun); Call of the Faceless (375-range AE 200 DoT + snare + 30s silence); Timeless Panic (100-range AE 1k dd + fear).
  - Drops 3 from: Timestone Adorned Ring, Cloak of Retribution, Wand of Impenetrable Force, Belt of Tidal Energy, Timeless Silk Robe Pattern, Staff of Transcendence, Earring of Unseen Horrors, Mask of Simplicity, Padded Tigerskin Gloves, Greaves of Furious Might, Zealot`s Spiked Bracer, Wristband of Echoed Thoughts.
- **Rallos Zek** — quads up to 3500, flurries, AE rampages; damage scales down as HP drops (eqprogression: power gains at 75% harder hits + AE rampage, 50% +flurries, 25% increased attack). Vindictive Strike (3500 dd + 20s stun on tank); Rage of Zek (250-range AE 400 DoT + 50 mana DoT, 9 curse counters). Adds at 90/75/50/25% (weak; eqprogression: dispel Blind Rage self-buff every 7 min out of combat).
  - Drops 3 from: Ring of Thunderous Forces, Platinum Cloak of War, Timeless Breastplate Mold, Ton Po`s Mystical Pouch, Darkblade of the Warlord, Greatstaff of Power, Visor of the Berserker, Band of Primordial Energy, Shield of Strife, Pants of Furious Might, Pauldrons of Devastation, Sandals of Empowerment.

### Phase 6 — Quarm
- Time = 2 hours (+ leftover). **Quarm**: hits up to 4k, flurries, AE rampages. Starts with **4 heads and 8 AEs**: Infernal Flames (fire 3k), Glacier Blast (cold 3k), Plague Seism (magic 3k), Venom Blast (poison 3k), Glacier Breath (cold 100 DoT + snare), Epoch Conviction (magic attack/spell-damage debuff + 100 DoT + 50 mana DoT, 36 curse counters), Plagued Earth (disease 500 DoT + 50 mana DoT, 36 disease counters), Venomed Mist (poison 500 DoT + 50 mana DoT, 36 poison counters).
- Every **25%** one head explodes and it loses some AEs. Self-dispels/cures → re-debuff constantly. Little elementals spawn (low damage but proc slow/spell-slow, 36 disease counters).
- Drops 3 from: Silver Hoop of Speed, Earring of Influxed Gravity, Talisman of the Elements, Shroud of Eternity, Cord of Temporal Weavings, Timeless Chain Tunic Pattern, Timeless Breastplate Mold, Timeless Leather Tunic Pattern, Timeless Silk Robe Pattern, Spool of Woven Time, Bracer of the Inferno, Hammer of the Timeweaver, Stone of Flowing Time, Prismatic Ring of Resistance, Whorl of Unnatural Forces, Ethereal Silk Leggings, Shawl of Eternal Forces, Earthen Bracer of Fortitude, Wristband of Icy Vengeance.

### Finale
- After loot: break the prison holding **Zebuxoruk** → scene with **Druzzil Ro** → "resetting the timeline" → raid ports to **Plane of Knowledge**.

## Other Rasper's Realm pages (downloaded, for cross-checking)
All at https://www.raspersrealm.com/Everquest/PoP/<page>:
- index.html (1.4K — JS-driven hub), gearSummary.html (212K — big gear tables), gearVisibleArmor.html, miscSpells.html, miscProgression.html (47K)
- Plane guides: openPoJ (Justice 26K), openPoI (Innovation), openPoD (Disease), openPoN (Nightmare), openPoS (Storms), openPoV (Valor), openCoD (Crypt of Decay), openPoT (Torment), openBoT (Bastion of Thunder), openHoH (Halls of Honor), openPoTact (Tactics), openSolRo (Tower of Solusek Ro)
- Elemental planes: openPoW (Water), openPoE (Earth), openPoA (Air), openPoF (Fire)

## Notes / caveats
- Rasper's Realm is a contemporaneous fan site (era-appropriate, pre-current-expansion data). Numbers are "hits" estimates from parses; eqprogression gives HP estimates. Both agree on mechanics/names where they overlap.
- Innoruuk add mechanic flagged as possibly broken by the source itself — present as-is with attribution.
- PoT maps: `imgs/maps_potimea.txt` (phase 1 area, ASCII map data rendered via JS), `imgs/maps_potimeb.txt` (phase 2 branches). These are text-map sources for the site's own map renderer; may need conversion or can be cited as-is.
