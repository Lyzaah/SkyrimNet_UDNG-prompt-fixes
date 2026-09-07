# BDSMLOCK_and_VIBRATIONS_Fix

Prompt-only MO2 overlay. No ESP of its own. This is the **mechanics package** — everything that
makes device locking, the vibrator remote, gagged-speech, and worn-device physics actually work
correctly against the DDUDNG plugin:

1. **BDSMLOCK selection.** A better two-tier category → drilldown action-selection prompt for locking Devious Devices, with correct slot-occupancy tracking (never restacks an occupied slot, never invents a group that doesn't exist).
2. **The vibrator remote.** `ActivateVibratorOnActor` / `TurnOffVibrators` wired correctly against DD NG's `zadLibs.VibrateEffectAsync` / `StopVibrating`. Strength and duration are picked by the LLM per press (DD's real 1-5 scale), not a fixed value — plus edge-count awareness, orgasm-as-payoff guidance, public-vs-hidden bystander logic, predator-faction captor tone, and an RNG-gated combat-intensity nudge.
3. **Gagged speech.** Open-mic and F1/F7-transformed player speech gets muffled to NPC listeners when she's gagged or hooded — NPCs hear mush, not her actual words. Narration is now tiered by device (ring/ball/muzzle/panel/harness-style, hood-only, or gag+hood layered), escalates with how long it's been locked, accounts for blindness stacked on top of a gag, handles a deafened player, and gives close-relationship NPCs a real weighted-RNG chance (not vibes) to catch an occasional fragment.
4. **Worn-device physics.** A ground-truth sheet of what's actually on the player's body right now — gag/blind/deaf/restraint state, with a positive-phrased "just came free" push for a few turns after a device is removed, so NPCs stop imitating stale gagged/bound turns out of habit.

This package holds **only the mechanical logic** — there is no world-setting or personality prompt
in here. Drop it over DDUDNG in your load order and it just works underneath *any* personality
prompt: your own favorite domme-NPC bio, or this repo's own [World Setting Medium](../world-setting-medium/) / [Hard](../world-setting-hard/) narrative layers.

**This is a required companion install**, not an optional one, if you're using World Setting Medium
or Hard — those packages ship *only* their narrative layer and rely on this package for everything
mechanical, physics included. (If you want everything pre-combined in one zip instead, see the
[Medium AIO](../world-setting-medium-aio/) / [Hard AIO](../world-setting-hard-aio/) convenience
bundles.)

**External requirement for the physics layer:** worn-device physics (`0722_worn_truth.prompt`) is
powered by decorators (`vrtedd_worn_devices`, `vrtedd_gag_name`, `vrtedd_blind`, `vrtedd_deaf`,
`vrtedd_all_bound`/`_arms_bound`/`_legs_bound`, and their recovery-countdown counterparts)
registered by a separate third-party mod, **"DD SkyrimNet AddOn"** (its Base component — a
compiled DLL, a small ESP, and Papyrus scripts). That mod isn't ours and isn't redistributed
here — install it separately, and make sure its ESP is ticked, or the physics section of this
package renders nothing (silently — everything else still works).

See [`docs/ENGINE_NOTES.md`](../../docs/ENGINE_NOTES.md) in this repo for the underlying BDSMLOCK category/drilldown mechanics and the DD NG keyword map this fix relies on.

## What it does, concretely

- `native_action_selector.prompt` — first-pass action selection. Teaches the model the BDSMLOCK category, the occupied-slots concept (never re-lock a worn slot), and the correct params shape (`{"intent": "<slot word> <name>"}`, `intent` is the *only* key).
- `native_action_selector_drilldown.prompt` — second pass (cheaper model). Maps the chosen intent to one of the fixed slot-group tokens (GAGS, COLLARS, HOODS, ... — no invented `ANKLE_SHACKLES`, that's `LEG_CUFFS`) and picks a concrete `EQUIP_*` leaf action, generic-named (Black Leather / Iron / Padded / Steel), only if that slot reads empty.
- `activatevibratoronactor.yaml` — the remote. Calls `zadLibs.VibrateEffectAsync` on `zadQuest`. Needs a plug/piercing already worn; does not equip anything. `teaseOnly` true = edge and deny, false = let her finish. `vibStrength` (DD's real 1-5 scale) and `duration` (seconds) are dynamic params the LLM picks per call — there's no per-device targeting (the function is actor-wide, not per-slot), so multi-toy awareness in the prompt is narrative naming, not mechanical dispatch.
- `turnoffvibrators.yaml` — calls `zadLibs.StopVibrating`. Not a mercy button mid-punishment; only for when the scene is actually over.
- `player_dialogue.prompt` / `event_history.prompt` / `event_history_compact.prompt` / `0011_gagged_player_task.prompt` / `0905_gagged_player_tts.prompt` / `0935_player_gagged_listener.prompt` / `gag_just_locked.yaml` / `hood_just_locked.yaml` — gagged-speech: hides the player's real words from NPC-facing event history when she's gagged/hooded (generalized to any gagged NPC speaker, not just the player), and suppresses her TTS line, without touching open-mic audio at the source (it can't be — the fix is downstream, in what NPCs are shown). Narration tiers by device/layering, elapsed lock time, blind+gag stacking, deaf-listener handling, and relationship-scaled comprehension chance all live in `player_dialogue.prompt` and `0935_player_gagged_listener.prompt`.
- `0722_worn_truth.prompt` — worn-device physics, powered by the third-party decorators described above. Functionality only, no tone.

## Install

1. Drop this folder (or the built zip) into MO2 / copy into `mods/`.
2. Enable it **above** `SkyrimNet_b24` and above **DDUDNG**, and **below** World Setting Medium/Hard if you're running one of those (so its tone-specific `native_action_selector.prompt` wins the left-pane fight over this one's default copy).
3. Install and enable **DD SkyrimNet AddOn** (Base component, ESP ticked) if you want the physics section to actually render — everything else in this package works without it.
4. **Restart the game.**

## Requirements

- Skyrim SE/AE + SKSE + SkyrimNet
- Devious Devices NG (for the `zad_*` keywords and `zadLibs` functions)
- SkyrimNet_UDNG (device bios + lock events) recommended, though the selector/remote logic here works without it
- **DD SkyrimNet AddOn** (third-party, Base component, ESP ticked) — required only for the worn-device physics section; everything else in this package works without it

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| NPC talks about locking a device but nothing happens | Talking about a lock is not the ACTION line — check `embed_actions_in_dialogue` is on and this pack is winning the file-path fight for `native_action_selector.prompt` |
| Second collar/gag gets "locked" on an already-occupied slot | An older/other action-selector prompt is winning the left-pane fight — this pack must be higher |
| Remote does nothing | No plug/piercing worn yet — the remote presses an existing toy, it does not equip one |
| Everyone gets locked from a hello | You want the [World Setting Medium](../world-setting-medium/) / [Hard](../world-setting-hard/) narrative layer installed *and winning the left-pane fight* over this pack's own selector copy — this pack alone has only a light default opinion about *when* to lock |
| NPCs still describe the player as gagged/bound a turn or two after it comes off | Expected for up to 3 renders — the recovery-countdown push in `0722_worn_truth.prompt` needs that long to overwrite the LLM's own recent turns. Persisting past that means DD SkyrimNet AddOn's ESP isn't ticked, so the physics section isn't rendering at all |
| Physics section (gag/blind/deaf/restraint facts) never appears | DD SkyrimNet AddOn isn't installed, or its ESP isn't ticked — check its own log per that mod's README |
| Gag narration never mentions the device by name (ring/ball/muzzle/etc.) | Falls back to generic muffled-struggle text when `vrtedd_gag_name` returns empty or an unrecognized name — needs DD SkyrimNet AddOn installed, and only flavors devices whose name matches a known heuristic word |
| A close NPC never seems to catch a fragment of gagged speech | Working as intended most of the time — it's a real weighted roll (0-35% by relationship tier), not guaranteed; low relationship rank gets 0% |
| Remote never gets stronger over a fight | The combat-intensity nudge is also a real 50% roll via `is_in_combat`, not automatic every combat turn |

## Version

2.2.0 — vibration deepened: `vibStrength`/`duration` are now dynamic per-call params instead of a
fixed 4/60s, plus multi-toy narration, edge-count tracking, orgasm-as-payoff guidance,
public-vs-hidden bystander logic, predator-faction captor tone, and RNG-gated combat intensity.
See CHANGELOG.md.

2.1.0 — gagged-speech deepened: device/layering-tiered narration, time-locked escalation,
blind+gag stacking, deaf-listener handling, and a real weighted-RNG comprehension chance for
close relationships (replacing an earlier prose-only draft — RNG replaces prose wherever prose was
only standing in for a probability slider). Also fixed a hood-lock trigger gap and purged leftover
`nefaram_`-branded file/trigger naming. See CHANGELOG.md.

2.0.0 — merged into the one mechanics package: gagged-speech folded in permanently (the standalone
gagged-speech package is retired), plus a new worn-device physics file powered by a third-party
addon's decorators. See CHANGELOG.md for the full breaking-change rationale.

1.0.1 — clarified in docs that World Setting Medium/Hard (2.0.0+) require this package as a separate install rather than bundling it.

1.0.0 — initial port into the mod-dev monorepo, combining the selector-prompt fix and the vibrator-remote fix (both previously shipped/patched separately against DDUDNG) into one logic-only package.
