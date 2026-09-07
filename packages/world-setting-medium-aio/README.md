# World Setting — Medium (AIO)

One MO2 zip. Prompt overlay, no ESP. Same **mechanics** as Hard (occupancy, women-only, combat omit, arms-then-clothes, baked vibe leaves). Softer **when**: a greeting is not a lock. Predators, shady types, real arrests, and "she asked" still fire.

Player-facing list: [`docs/SkyrimNet-DD-Features.md`](../../docs/SkyrimNet-DD-Features.md).

**Hard vs Medium:** Hard treats locking an adult woman as ordinary manners. Medium keeps shops, quests, and kind followers on the job unless the scene is spoils / a liberty / she asked. Occupancy physics is identical.

Arousal-band / follower-initiative overlay is **not** in this zip. That is [`SkyrimNet Kink Experimental`](../kink-experimental/) — see [`EXPERIMENTAL.md`](../../EXPERIMENTAL.md).

## What's in this zip

| Piece | Role |
|---|---|
| `bdsmlock_vibrations_fix` | Selector drilldown, vibe YAML leaves, occupancy |
| `gagged_speech` | Muffled TTS / listener / gag-lock trigger |
| `vrtedd_worn_truth` | What's on her **now** (`0722`) |
| `world_setting_medium_narrative` | World law, speech, lock ACTION, remote, arrest |
| `roleplay_guidelines` | NPC agency, SKU → ordinary speech |

Do **not** also enable `bdsmlock-and-vibrations-fix`, `world-setting-medium`, Hard AIO, or Hard narrative next to this. Same filenames. Pick **one** AIO.

## Requirements

### Required

| Need | Mod | Link |
|---|---|---|
| Game + extender | Skyrim SE/AE + **SKSE** | [skse.silverlock.org](https://skse.silverlock.org/) |
| SKSE address map | **Address Library** | [Nexus 32444](https://www.nexusmods.com/skyrimspecialedition/mods/32444) |
| NPC AI | **SkyrimNet** | [GitHub releases](https://github.com/MinLL/SkyrimNet-GamePlugin/releases) |
| Devices | **Devious Devices SE 5.2** + **DD NG** | [DD SE](https://www.loverslab.com/files/file/5878-devious-devices-se/) · [DD NG](https://www.loverslab.com/files/file/29779-devious-devices-ng/) |
| Lock API this overlay talks to | **SkyrimNet_UDNG** (DDUDNG) | [GitHub](https://github.com/naitro2010/SkyrimNet_UDNG) |
| Strip (`change_outfit_target`) | **SexLab Framework SE** | [LoversLab category](https://www.loverslab.com/files/category/228-sexlab-framework-se/) |

UDNG MCM: **NPC can equip devices on the player = ON**.

### Strongly recommended

| Need | Mod | Link |
|---|---|---|
| Worn-device physics (`vrtedd_*`) | **DD SkyrimNet AddOn** (mad72), **Base** component, **ESP ticked** | Third-party, not redistributed here. Without it, `0722` fails soft and the rest still runs. |
| Escape / extra devices | **Unforgiving Devices** 3.x | [LoversLab](https://www.loverslab.com/files/file/41829-unforgiving-devices/) |
| Papyrus helpers | **powerofthree's Papyrus Extender** | [Nexus 22854](https://www.nexusmods.com/skyrimspecialedition/mods/22854) |

### Optional (features degrade cleanly)

| Need | Mod | Link |
|---|---|---|
| Ungag-to-drink (thirst/hunger ≥ 70) | **SunHelm Survival** | [Nexus 39414](https://www.nexusmods.com/skyrimspecialedition/mods/39414) |
| Guard arrest path in `0765` | **SeverActions** | [GitHub](https://github.com/Severause/SeverActions) |
| Arousal bands / follower remote | **Kink Experimental** zip + SLO + SkyrimNet_Arousal | [`EXPERIMENTAL.md`](../../EXPERIMENTAL.md) |

Missing SunHelm → thirst/hunger read `0`. Missing SeverActions → arrest lines don't match.

Do **not** use SexLab Survival `sever_hunger` as the thirst meter.

## Install (MO2)

1. Install the required stack (SKSE, Address Library, SkyrimNet, DD SE + DD NG, SkyrimNet_UDNG, SexLab).
2. Install **DD SkyrimNet AddOn** (Base, ESP ticked) if you want worn-device physics.
3. Drop `World Setting - Medium (AIO)-v*.zip` into MO2. Enable it.
4. Left pane: **above** `SkyrimNet_b24`, DDUDNG, VRTE, SeverActions, and **SKSE Output**.
5. Disable Hard AIO / old Medium / the separate Fix+narrative pair — same filenames.
6. UDNG MCM: NPC can equip devices on the player = ON.
7. **Restart the game.**

No ESP of our own. No `plugins.txt` tick.

## Load order sketch

```
[required frameworks: SKSE / Address Library / SkyrimNet / DD / DD NG / UDNG / SexLab]
DD SkyrimNet AddOn (Base ESP on)
World Setting - Medium (AIO)        ← this zip, high in the LEFT pane
SkyrimNet Kink Experimental         ← optional, separate zip
```

## Version

**3.2.5** — README rewritten (current deps, current mechanics). Experimental is its own zip. Prompt occupancy / combat-omit / women-only as of Medium 3.3.6 + Fix 2.7.6.
