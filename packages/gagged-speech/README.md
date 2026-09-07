# SkyrimNet Gagged Speech

> **RETIRED.** This standalone package is no longer built or tagged. Its content now ships
> permanently inside [`bdsmlock-and-vibrations-fix`](../bdsmlock-and-vibrations-fix/) 2.0.0+, the
> one mechanics package. If you have this package installed on its own, remove it and install
> that one instead — see its CHANGELOG.md for the full rationale. The rest of this README is kept
> for reference only.

Prompt-only MO2 overlay. No ESP. Adult / BDSM. Devices stay on adults.

Fully separate project — no dependency on [World Setting Medium](../world-setting-medium/) or [Hard](../world-setting-hard/). Pairs with either as an optional add-on (Medium never bundled it either, as of 2.0.0 — nor does Hard, which never bundled it even before). If you want everything pre-combined in one zip, see the [Medium AIO](../world-setting-medium-aio/) / [Hard AIO](../world-setting-hard-aio/) convenience bundles, which include this exact same content as a shared component (`gagged_speech`) so the copies never drift out of sync.

**1.1.0** — same speech split as 1.0, plus: listeners do **not** smear/thumb the gag every reply; one handling beat fires when the gag actually locks (`nefaram_gag_just_locked`, 180s cooldown).

When the player is **gagged or hooded**, two different mouths happen:

1. **Open mic / regular speech** — you still hear yourself. NPCs do **not** understand you. They comment on muffled *mmphs*, mock, imitate, joke-translate. They do not answer the sentence you said.
2. **F1 text input** (and F7 Voice Dialogue Transform / chat `/transform`) — the line is rewritten as **asterisk narration**. Chatterbox has nothing to read as spoken dialogue. You see what is going on. They still only heard mush.

Thoughts stay ungagged. A gag stops the mouth, not the inner monologue.

For *why* this split exists — the STT-vs-transform engine mechanics, the exact decorator gotchas, and how the merge system lets one file override another — see [`docs/ENGINE_NOTES.md`](../../docs/ENGINE_NOTES.md) in this repo. This README covers only what's in this package and how to install it.

---

## What you should feel in-game

**Worn:** a Devious Devices gag (`zad_DeviousGag`), a ZaZ gag (`zbfWornGag`), and/or a DD hood (`zad_DeviousHood`). A ballgag harness plus an extreme hood both count. A blindfold alone does **not** — that is eyes, not mouth.

**Open mic:** you talk. Your TTS still speaks the transcript. The guard does *not* quote "please release me." They go "mmph mmph? she says please," talk over you. That is the intended split: *you* know what you meant; *they* got cloth and drool.

**Just locked:** once, nearby NPCs get a short narration of the strap being thumbed. Then the room talks over her. They do **not** re-enact buckling it every line.

**F1 (text input):** you type. The model outputs something like:

```
*Lola jerks her chin against the harness, a wet sound trapped in her throat.*
```

No spoken line. Subtitles / chat show the body beat. NPCs react to a gagged girl, not to a request.

**Gag comes off:** speech returns.

---

## What this package ships

```
SKSE/Plugins/SkyrimNet/
├── config/triggers/
│   └── nefaram_gag_just_locked.yaml              # one smear beat when a gag locks (180s)
└── prompts/
    ├── player_dialogue.prompt                    # overlay (same name as stock)
    ├── components/
    │   ├── event_history.prompt                  # overlay (NPC verbose history)
    │   └── event_history_compact.prompt          # overlay (compact history)
    └── submodules/
        ├── system_head/
        │   └── 0011_gagged_player_task.prompt    # merge (new name)
        └── user_final_instructions/
            ├── 0905_gagged_player_tts.prompt      # merge, AFTER VRTE 0900
            └── 0935_player_gagged_listener.prompt # merge: you did not understand her
```

All of the above lives in this repo's `components/gagged_speech/` — this package's `overlay/` is empty; it ships that shared component as-is, standalone.

### What this pack does **not** own

| Job | Owner | Do not clone |
|---|---|---|
| Gagged *NPC* cannot form words | VRTE `0900_vrtedd_gag.prompt` | Leave it |
| NPC bind / blind / ungagged recovery | VRTE `0910–0930` | Leave it |
| DD bios / optional "treat player as muffled" one-liner | UDNG `0799` | Optional; 0935 is the social last word |
| World cruelty, BDSMLOCK, vibe remote, arrest | [World Setting Medium](../world-setting-medium/) / [Hard](../world-setting-hard/) | Separate package |

Thoughts: `render_mode == "thoughts"` is excluded everywhere in this pack. A gagged girl still thinks.

---

## Install (MO2)

1. Drop this folder (or the built zip) as a mod (or install the zip). Name it `SkyrimNet Gagged Speech`.
2. Enable it **above** `SkyrimNet_b24`. First `+` in the left pane wins same-filename fights (`player_dialogue.prompt`, `event_history*.prompt`).
3. Optional: install [World Setting Medium](../world-setting-medium/) or [Hard](../world-setting-hard/) next to it. They do not share filenames. Order between them does not matter.
4. Optional but useful: VRTE DD-ZaZ (NPC speaker gag), SkyrimNet_UDNG (device bios + lock event), Devious Devices NG (the keywords).
5. **Restart the game.** SkyrimNet caches templates. A save reload is not enough for new files **or new triggers**.
6. Dashboard: Dialogue transformation on if you want the F1/F7 narration path. Open-mic mmph-to-NPCs works even if that is off, because that path is history + 0935.

## Requirements

- Skyrim SE/AE + SKSE + **SkyrimNet**
- A gag/hood that carries `zad_DeviousGag`, `zbfWornGag`, and/or `zad_DeviousHood` (Devious Devices and/or ZaZ)
- Lock trigger needs **SkyrimNet_UDNG** (the `SkyrimNetDDUDNG_Event`). Speech muffling still works without it.

No plugin tick. Prompt merge only.

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| Open mic: NPCs quote your exact words | History overlay lost the same-filename fight, or you did not restart |
| F1 still speaks a full sentence | Transformation off, or `player_dialogue.prompt` not winning, or no gag keyword on the worn item |
| They smear/thumb the gag every sentence | An older `0935` still higher in the left pane — this version must win |
| No "just locked" smear beat | Trigger YAML not loaded (restart), or UDNG event name mismatch, or cooldown |
| Gagged NPC (not you) goes silent forever after the gag comes off | VRTE 0920 missing — not this pack |
| Everyone in the hold is "gagged" | Someone gated Papyrus with `!= ""` — see `docs/ENGINE_NOTES.md`. This pack does not. |
| Hood on, still understood | That hood has neither `zad_DeviousHood` nor a gag keyword (open-face / eyes-only). Blindfold is not a mouth. |
| Children | Do not. This pack never targets kids; keep adult toys on adults. |

## Version

1.1.0 — ported into the mod-dev monorepo. No content changes from the original standalone `05 SkyrimNet Gagged Speech.zip` — verified byte-identical via `diff -r` against the extracted original after build.
