# Experimental — SkyrimNet Kink overlay

Optional overlay. On the **FOMOD AIO** (`World Setting (AIO)` 3.3.1+) it is a checkbox, **off by default**. You can still install the standalone `packages/kink-experimental` zip on top of an older split Hard/Medium AIO.

Leave it off if you want lock/strip/vibe/ungag without SLO numbers in the prompt.

Package: `packages/kink-experimental/`  
Prompt: `components/kink_experimental/.../0730_kink_experimental.prompt`

## What it adds

`0730` concatenates into `user_final_instructions` (numeric prefix, unique filename). It does **not** overwrite 0720/0760/0761.

1. **Arousal bands** from `sla_Arousal` faction rank (SLO Aroused NG / SkyrimNet_Arousal). 0 dry, **20–60 the play window**, 70 already insane, 90–100 gone. After 60 it is too late to play it cool. Prints the number inside the band. Does **not** fire `ArousalChange` — SkyrimNet_Arousal owns that.
2. **Follower / friend remote play** if she is plugged, speaker arousal ≥ 20, not combat, speaker hands free. They may press without being asked. Prefer `teaseOnly` true.
3. **Ungag-to-feed** if close, gagged, and SunHelm thirst or hunger ≥ 70. Same beat the AIO already has in `0720` / `0935` — the gag is in the way of drinking; one ACTION; invent the rest. Harmless overlap: one action slot per line.

Combat: `{% if not _fighting %}` — same omit pattern as the AIO. No mid-fight remote from this file either.

## What it is not

- Not a world setting. Hard/Medium still own *when* civilians lock.
- Not occupancy physics. Occupied slots still come from 0760 / drilldown.
- Not a copy-me beat sheet. Invent it.
- The **follower contract** tick-boxes (`docs/templates/follower_contract.prompt`) are **not** in this zip. Paste those into a specific follower's bio if you want a signed house/dungeon contract. Safeword is three stomps.

## Requirements (on top of an AIO)

Required for the overlay to load:

- One of **World Setting Hard (AIO)** or **Medium (AIO)** (or the separate Fix + narrative stack)
- SkyrimNet, same as the AIO

Needed for the *content* to fire:

| Need | Mod | Link |
|---|---|---|
| Arousal numbers | **SLO Aroused NG** (faction `sla_Arousal`) | [Nexus 65454](https://www.nexusmods.com/skyrimspecialedition/mods/65454) (OSL Aroused family; SLO is the NG stack this load order uses) |
| Who owns ArousalChange | **SkyrimNet_Arousal** | [GitHub](https://github.com/GoodProvider/SkyrimNet_Arousal) |
| Ungag-to-feed meters | **SunHelm Survival** | [Nexus 39414](https://www.nexusmods.com/skyrimspecialedition/mods/39414) |

Missing SunHelm → globals are `0.0` → the feed beat never renders. Missing SLO → ranks read 0 → cold NPCs see nothing extra. The AIO still works.

SexLab Survival `sever_hunger` is the **wrong meter**. Do not use it here.

## Install

1. Install Hard AIO **or** Medium AIO first. Enable it.
2. Drop `SkyrimNet Kink Experimental-v*.zip` into MO2 as its **own** mod.
3. Enable it. Left pane: **above** the AIO is fine (0730 is a new file, so it concatenates either way).
4. **Restart the game.** New `.prompt` files are not always picked up on a save reload.
5. No ESP. No plugin.txt tick.

Do **not** also dump `0730` by hand into the AIO folder — that is the same file twice.

## Uninstall

Disable the Experimental mod in MO2. Restart. AIO behavior is unchanged.

## Version

**1.0.0** — first standalone zip. Same `0730` that used to ride inside standalone Hard/Medium `includes:` (never inside the AIO).
