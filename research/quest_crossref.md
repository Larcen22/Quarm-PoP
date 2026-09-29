# Quest / Event Cross-Reference — SecretsOTheP/quests Lua scripts

Repo cloned to `research/quests-lua/` (187 zone folders). Folders = zones; files usually named by NPC.
`encounters/` subfolders hold multi-mob event scripts; `#NPC.lua` = quest-giver/boss scripts; numeric `.lua` = instance controllers.

## Boss mobs on our site → Lua scripts

| Site boss | Page | Script(s) | Notes |
|---|---|---|---|
| Grummus | bosses-tier1 | `podisease/#Grummus.lua` (297 B) | death → Planar Projection loot container only |
| Terris-Thule | bosses-tier1 | `nightmareb/Terris_Thule.lua` | full encounter: defilers 79/69%, debuff 50%, gargoyles 40% |
| Manaetic Behemoth | bosses-tier1 | `poinnovation/encounters/Behemoth.lua` | wave controller; dormant until 10 device kills |
| Xanamech Nezmirthafen | bosses-tier1 | `poinnovation/#Xanamech_Nezmirthafen.lua` | dormant construct, wake signal, 30-min depop |
| Seventh Hammer | bosses-tier1 | `pojustice/The_Severh_Hammer.lua` → `The_Seventh_Hammer.lua` | dialogue challenge; Tribunal casts Verdict/Tremor |
| Aerin'Dar | bosses-tier2 | `povalor/#Aerin-Dar.lua` | adds wake at 85/65/45/25% HP |
| Bertoxxulous | bosses-tier2 | `codecay/encounters/Bertox.lua` | multi-stage summoning event (12 boss kills → Bertox) |
| Carprin Deatharn | bosses-tier2 | `codecay/#_Carprin_Deatharn.lua` | 3 named adds on engage; warp+heal hate-drop |
| Saryrn | bosses-tier2 | `potorment/Saryrn.lua` | Sorrowsong phases; servants at every HP threshold |
| Keeper of Sorrows | bosses-tier2 | `potorment/The_Keeper_of_Sorrows.lua` (150 B) | death → respawn #Tylis_Newleaf |
| Agnarr the Storm Lord | bosses-tier3 | `bothunder/Agnarr_the_Storm_Lord.lua` | adds at 75/50/25%; storm portals every 2 min |
| Lord Mithaniel Marr | bosses-tier3 | `hohonorb/Lord_Mithaniel_Marr.lua` | gated behind 3 named mobs |
| Rallos Zek (+Tallon/Vallon) | bosses-tier3 | `potactics/#Rallos_Zek_.lua` + `potactics/encounters/Rallos.lua` | multi-phase arena; Tallon+Vallon are phases of same event |
| Arlyxir | solusek-ro-tower | `solrotower/Arlyxir.lua` | 75 s rebirth heal; death → cauldron + 3 warders |
| Jiva | solusek-ro-tower | `solrotower/Jiva.lua` (+`encounters/JivaAdds.lua`) | 8-add rotation every 45 s |
| Rizlona | solusek-ro-tower | `solrotower/Rizlona.lua` + `#Rizlona.lua` | two-phase (form 1 death spawns form 2) |
| Protector of Dresolik | solusek-ro-tower | `solrotower/The_Protector_of_Dresolik.lua` | bounds check; 2.5 h depop paused in combat |
| Xuzl | solusek-ro-tower | `solrotower/Xuzl.lua` | bounds check + "conjurings" emote |
| Solusek Ro | solusek-ro-tower | `solrotower/Solusek_Ro.lua` | anti-cheat: Guardian of Fire teleport + 100K heal |
| Baltaldor the Cursed | plane-of-air | `poair/#Baltaldor_the_Cursed.lua` | warp+heal hate-drop only |
| Xegony | plane-of-air | `poair/encounters/Xegony.lua` | 6 named-add waves at HP thresholds; full reset on deaggro >120 s |
| Ring events (Wind/Smoke/Mist/Dust) | plane-of-air | `poair/encounters/Wind\|Smoke\|Mist\|Dust.lua` | controller islands → event boss → Avatar; 66 h success / 18 min fail repop |
| Tantisala Jaggedtooth | plane-of-earth | `poeartha/Tantisala_Jaggedtooth.lua` | warp+heal hate-drop only |
| Mystical Arbitor of Earth | plane-of-earth | `poeartha/A_Mystical_Arbitor_of_Earth.lua` (+`arbitor_guy.lua`) | +50-min depop; death → Planar Projection |
| War Chieftans Awisano/Birak/Galronar | plane-of-earth | `poearthb/#War_Chieftan_*.lua` | invisible-marker kill tracking (crash-safe) for Gintolaken gate |
| Warlord Gintolaken | plane-of-earth | `poearthb/#Warlord_Gintolaken.lua` | spawns only after 3 chieftans dead; bounds check; death → 84 h respawn |
| Avatar of Earth | plane-of-earth | `poearthb/#Avatar_of_Earth.lua` | death → Essence of Earth; Council respawns 5 d 18 h (fail: 15 min) |
| Fennin Ro | plane-of-fire (not built yet) | `pofire/encounters/Fennin.lua` (+`SnareImmunity.lua`) | 4-phase army event; fail timer ~4.9 h +2 h at phase 4 |
| Coirnav | plane-of-water (not built yet) | `powater/encounters/Coirnav.lua` (+`Fishlords.lua`, `Traps.lua`) | Guardian → 3 waves × 25 minions → trio (130K/120K/155K HP) → Coirnav 250K; 15-min fail → Banishment of the Pantheon |
| Quarm (final) | plane-of-time (not built yet) | `potimeb/encounters/Phase6.lua` + controller `potimeb/223077.lua` | QUARM_TYPE = 223008; "Quarm defeated. Remaining instance time set to 1 hour." |
| PoT phases 1–5 | plane-of-time (not built yet) | `potimeb/encounters/Phase1Air\|Earth\|Fire\|Undead\|Water.lua`, `Phase2-6.lua` | phase-level controllers, no per-boss files for P1 nameds |

## No script found (checked filenames across all 187 zones)
- Tallon Zek / Vallon Zek as standalone bosses — covered inside `potactics/encounters/Rallos.lua` event instead.
- PoEarth A: Peregrin Rockskull, Mudwalker, Derugoak Bloodwalker (only Tantisala + Arbitor scripted).
- PoWater: Grioihin, Hydrotha, Krziik, Ofossaa (Coirnav/Fishlords/Traps only; Fishlords.lua references Lezom/Craiyk types).
- Symbol of Torden quest NPC.

## Shared mechanics seen across scripts
- **Planar Projection**: loot container spawned at boss death + signaled with killer's ID (most bosses).
- **Bounds check**: `GMMove` back to spawn + wipe hate + cast 3230 "Balance of the Nameless" or 2830 "Annul Self".
- **Hate-drop anti-Memory-Blur**: on combat end, warp to guard point + heal 30% max HP; periodic timer reduces target hate to 5%.
- **Depop timers** paused while engaged (e.g. 2.5 h for tower bosses).
