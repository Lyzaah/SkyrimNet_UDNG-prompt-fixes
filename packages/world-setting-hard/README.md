# World Setting (HARD)

Tiny **SkyrimNet overlay** (no ESP). Prompts + two UDNG action YAML overrides.

This is the **meat-market** pack: NPCs talk like devices, sex, and public humiliation are *normal in this Skyrim* — and they **actually fire the lock / remote / arrest actions** instead of only dirty-talking.

Adult / BDSM / noncon-themed roleplay. All named people are adults. Do not use this on child NPCs.

This is a universal SkyrimNet + Devious Devices tool — it doesn't assume any particular modlist. (Formerly named "NEFARAM World Setting - Hard"; renamed because most people running this don't run that specific modlist.)

This package is the **world/personality narrative layer only**. **It requires [`bdsmlock-and-vibrations-fix`](../bdsmlock-and-vibrations-fix/) 2.0.0+ installed alongside it** — as of that version, the Fix package is the one mechanics package: the BDSMLOCK-drilldown and vibrator-remote mechanism, gagged/hooded player speech, and worn-device physics (what's actually on her body right now) all live there. This package owns none of that anymore.

If you want everything combined into a single zip instead of managing two mods, install [`world-setting-hard-aio`](../world-setting-hard-aio/) instead — same content plus gagged-speech, pre-bundled for convenience.

See [`docs/ENGINE_NOTES.md`](../../docs/ENGINE_NOTES.md) for the underlying merge mechanics, decorator gotchas, and DD keyword map.

## What this pack actually fixes (all of them)

Stock SkyrimNet + UDNG *can* lock Devious Devices. NPCs usually **don't**. They talk about a gag and fire `Outfit`, `RestrainNPC`, or a broken `BDSMLOCK` line.

This pack:

1. Puts a cruel world-law + adult-RP greenlight at the **front** of the system prompt (`0010_setting`).
2. Sets speech register and how they treat the **player's** worn DD (`0710`, `0720`) — reacting to physics the required Fix package already stated, not re-deriving it.
3. Forces `ACTION: BDSMLOCK PARAMS: {"intent": "..."}` with **intent as the only key** (`0760`). Extra keys (`target`, `targetName`, `device`) kill the nested picker.
4. Overlay of action-selector + drilldown so slot groups (`GAGS`, `HOODS`, `BOOTS`, `PLUGS`, `SUITS`, `CHASTITY_BRAS`, … ~20 live groups) resolve to `EQUIP_*`. Occupied slot → `None`, not a second collar.
5. Stops chaining locks after one just clicked. Talking about a worn leash is `None`.
6. Stops guards from "arresting" the player with `RestrainNPC` (that action only finds **other NPCs**). Real path is `Arrest` → `AddBountyToPlayer` then `ArrestPlayer` (`0765`).
7. Turns on the vibe **remote** after a plug/piercing is already on (`0761` + YAML), retargeted to **`zadLibs.VibrateEffectAsync`** on `zadQuest` (DD NG), not the stock `zadlibs_UDPatch`. As of Fix 2.2.0, strength and duration are **dynamic** — the LLM picks `vibStrength` (DD's 1-5 scale) and `duration` per press instead of a fixed 4/60s; PARAMS are `Actor` + `teaseOnly` + `vibStrength` + `duration`.

Unlock is still UDNG Papyrus (`ExtCmdUnequipGag` by slot). This pack does not replace VRTE (speaker's own gag/bind/blind) or UDNG `0799`.

**Live occupancy / worn-device physics** so NPCs don't narrate a phantom gag or binder is no longer part of this package at all — it's `0722_worn_truth.prompt`, component `vrtedd_worn_truth`, and it lives in the required Fix package now (see below).

## Hard vs. Medium — what's actually shared

Porting this into the monorepo surfaced that Hard and Medium diverge more than their READMEs originally implied — only some files are truly identical between them:

| Piece | Shared or per-variant? |
|---|---|
| `native_action_selector_drilldown.prompt`, `activatevibratoronactor.yaml`, `turnoffvibrators.yaml`, `0722_worn_truth.prompt` (worn-device physics) | **Shared with Medium** — but lives in the separate **required companion package** [`bdsmlock-and-vibrations-fix`](../bdsmlock-and-vibrations-fix/) 2.0.0+, not bundled here |
| `native_action_selector.prompt` | **Differs from Medium** — Hard's copy is noticeably more permissive about *when* BDSMLOCK fires ("ordinary manners... not too dramatic" vs. Medium's "never a random greeting or a quest hello"). Bundled in this package (component `world_setting_hard_narrative`), must win the left-pane fight over the Fix's own default copy |
| `0010_setting.prompt`, `0710_gender_speech.prompt`, `0720_player_devices.prompt`, `0760_bdsm_lock_action.prompt`, `0761_vibrator_remote.prompt`, `0765_player_arrest.prompt` | **Differs from Medium** — tone/register only, bundled in this package (component `world_setting_hard_narrative`) |
| gagged-speech | **Not included in Hard at all** (unchanged, always been the case) — it's bundled in the required Fix package now, not a separate optional install anymore; use [`world-setting-hard-aio`](../world-setting-hard-aio/) if you want one zip |

## Requirements

- Skyrim SE/AE + SKSE + **SkyrimNet**
- **[`bdsmlock-and-vibrations-fix`](../bdsmlock-and-vibrations-fix/) 2.0.0+** (required — see Install)
- The third-party **DD SkyrimNet AddOn** (Base component, ESP ticked) if you want the worn-device physics section to actually render — see the Fix package's own README
- **SkyrimNet_UDNG** + **Devious Devices NG** (lock/unlock/vibe)
- **SeverActions** (arrest path in `0765`; harmless if missing, those lines just won't match actions)
- MO2 (or any manager that USVFS-merges `SKSE/Plugins/SkyrimNet/`)

Optional: VRTE DD-ZaZ (physical constraints on a *speaking* NPC). Leave it. Don't clone it.

Do **not** install Unforgiving Devices just to make stock UDNG YAML happy. The remote is retargeted at DD NG.

## Install (MO2)

1. Install **[`bdsmlock-and-vibrations-fix`](../bdsmlock-and-vibrations-fix/) 2.0.0+** — required. This narrative layer's instructions do nothing without it.
2. Install this package's built zip. Put it **above** `bdsmlock-and-vibrations-fix`, so this package's own `native_action_selector.prompt` wins the left-pane fight and Hard's tone actually applies.
3. Put both **above** `SkyrimNet_b24`, UDNG, VRTE, SeverActions, and `SKSE Output` in the **left pane**. First enabled `+` in `modlist.txt` is **highest** priority.
4. Disable **Skyrim selfparody** if you have it. Same filename `0010_setting.prompt` — sitcom wins and eats the world law.
5. Disable any older Hard / Medium / Moderate World Setting, or the [`world-setting-hard-aio`](../world-setting-hard-aio/) convenience bundle — same filenames, highest left-pane wins the whole file, they will fight for no benefit. Pick the separate-mods stack *or* the AIO, not both.
6. UDNG MCM: **NPC can Equip Devices → on the player** = ON.
7. **Restart the game** after install (or after adding new `.prompt` / action YAML). SkyrimNet caches templates; new files are not always picked up on a save reload. YAML script-name changes **always** need a restart.

No ESP. No plugin.txt tick.

## Correct lock line (copy this)

Spoken dialogue first, then:

```
ACTION: BDSMLOCK PARAMS: {"intent": "gag PlayerName to shut her mouth"}
```

`intent` only. Slot words the drilldown understands: `gag`, `collar`, `hood`, `blindfold`, `heels`, `armbinder`, `shocking plug`, `nipple piercings`, `chastity belt`, `chastity bra`, `harness`, `catsuit`.

Then UDNG nested picker:

`BDSMLOCK` → `GAGS` / `HOODS` / `BOOTS` / `SUITS` / … → `EQUIP_GAGS_Black_Leather_Gag_Ball_Harness PARAMS: {"target":"PlayerName"}`

**Hood gotcha:** output `ACTION: HOODS`, never `ACTION: HOODS — Pick the hood to lock on a target`. The extra sentence is the description; the engine drops the call.

**Occupied slot:** do not restack. DD will refuse a second collar. Talking about a worn leash is `None`.

**Vibe remote** (plug or piercing already on — does **not** equip):

```
ACTION: ActivateVibratorOnActor PARAMS: {"Actor": "PlayerName", "teaseOnly": true, "vibStrength": 4, "duration": 60}
```

That is `zadLibs.VibrateEffectAsync` on `zadQuest` (DD NG, **not** `zadlibs_UDPatch`). `vibStrength` (DD's real 1–5 scale, integer) and `duration` (seconds) are picked per press as of Fix 2.2.0 — default to 3-4 strength here, go to 5 for real punishment. Do **not** add `vibrator_strength`, `vibration_duration`, or `intent`. Empty holes → `BDSMLOCK` a plug first.

**Player arrest:**

```
ACTION: Arrest PARAMS: {"intent": "add a contempt bounty on PlayerName then arrest her"}
```

Not `RestrainNPC` with the player's name.

## Punishment ladder (0760)

One lock per spoken line, first **missing** piece when it's punishment / "more":

1. Shocking plug
2. Nipple piercings
3. Chastity belt (she can't pull the plug)
4. Harness
5. Armbinder (no keys, no lockpicks)

If she **named** a slot (`hood`, `heels`, `catsuit`, `chastity bra`), that empty slot wins. Mouthy and still free → gag default. Already plugged and mouthy → remote, not a second gag.

## Logs if it still does nothing

`SKSE/Plugins/SkyrimNet/logs/openrouter_output.log` (often under MO2 **SKSE Output**). You want:

```
ACTION: BDSMLOCK PARAMS: {"intent": "..."}
[action_evaluation] ACTION: GAGS
[action_evaluation] ACTION: EQUIP_GAGS_...
```

`SkyrimNet.log` must **not** say `zadlibs_UDPatch` / `function does not exist`. That means an older YAML (stock UDNG or an old zip) is winning the left pane.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Zero `BDSMLOCK` | prompts / they picked Outfit / ArousalReaction / RestrainNPC instead |
| `BDSMLOCK` then `HOODS — Pick the hood…` | drilldown format issue — this pack's overlay is meant to stop that |
| `EQUIP_*` and still no item | DD `LockDevice` / slot conflict (hood vs gag harness) / quest item / MCM |
| Remote fires, no buzz | no vaginal/anal plug and no nipple/vaginal piercing (`VibrateEffect` returns `-2`) — lock a plug first |
| NPCs never mention worn-device physics at all | the third-party DD SkyrimNet AddOn isn't installed, or its ESP isn't ticked — that's a separate requirement from this package, see the Fix package's README |

`conversation_log.log` is speech only. It will not show whether the action fired.

## Conflicts / don'ts

- Do not enable **Skyrim selfparody** while this is on.
- Do not enable Medium / Moderate World Setting at the same time.
- Do not also install `world-setting-hard-aio` alongside this package + a separate Fix install — same filenames, pick one approach.
- Do not edit stock `SkyrimNet_b24` originals; this overlay is the point.
- Dashboard "Setting" editor writes **SKSE Output**, which **loses** to this mod if we sit higher in the left pane. Edit these files on disk.
- Device boolean in prompts: `worn_has_keyword(player.UUID, "zad_DeviousGag")`. Never test Papyrus names with `!= ""` (`{}` is truthy).
- Never lock devices on children.
- Do not point the remote at `zadLibsNG` unless you prove that script is the one on `zadQuest`. Classic `zadLibs` is the API.

## Version

**3.1.0** — `0761_vibrator_remote.prompt` deepened: multi-toy narration, edge-count tracking,
orgasm-as-payoff guidance, public-vs-hidden bystander awareness, predator-faction captor tone, and
an RNG-gated combat-intensity nudge. Requires `bdsmlock-and-vibrations-fix` **2.2.0+** for the
dynamic `vibStrength`/`duration` params this guidance now assumes (older 2.0.0+ Fix installs still
work, just against the previous fixed-strength behavior). See CHANGELOG.md.

**3.0.0** — **breaking.** Renamed from "NEFARAM World Setting - Hard" (new MO2 mod folder, not an in-place upgrade). No longer includes the worn-device physics file (`world_setting_shared`/`0722_worn_truth.prompt`, which was already shared byte-for-byte with Medium) — physics moved entirely into `bdsmlock-and-vibrations-fix` 2.0.0+, which now requires that in turn (and now bundles gagged-speech too). See CHANGELOG.md for the full breakdown.

2.0.0 — **breaking.** No longer bundles `bdsmlock-and-vibrations-fix` internally; it's now a required separate companion install (see Install, above). If you want the old single-zip experience, install [`world-setting-hard-aio`](../world-setting-hard-aio/) instead.

1.3.0 — ported into the mod-dev monorepo from the original hand-packaged `04.b NEFARAM World Setting - Hard.zip`. Content verified byte-identical (`diff -r`) against the extracted original after build. Shared logic (`bdsmlock_vibrations_fix`'s drilldown + vibrator actions, `world_setting_shared`'s occupancy sheet) was sourced from the same components Medium uses, bundled internally — everything else (the selector's tone, all six narrative prompts) was genuinely Hard-specific.
