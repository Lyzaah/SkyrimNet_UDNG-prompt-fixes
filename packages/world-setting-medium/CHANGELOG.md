# Changelog

All notable changes to this package are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [3.3.8] - 2026-09-07

### Fixed
- `0761_vibrator_remote.prompt` edge-count loop called
  `contains(format_event(event, "compact"), ...)` directly; a malformed
  event can make `format_event` return non-string, and `contains({}, "...")`
  behaves like the classic `{} != ""` Inja trap. Now binds the result and
  guards it with `isString()` first. Ported from a hand-built release
  published outside this repo — see `world-setting-aio` CHANGELOG 3.3.10.

## [3.3.7] - 2026-09-02

### Changed
- `0730_kink_experimental` is no longer in this package. Install
  `packages/kink-experimental` (see `EXPERIMENTAL.md`) if you want
  arousal bands / follower remote play.

## [3.3.6] - 2026-09-01

### Changed
- Same combat no-go as Hard 3.3.6: lock/vibe/strip **prompt omitted** while
  `_fighting`, not listed-then-forbidden. Arms-first no longer leaks during
  a fight. Selector hides `BDSMLOCK` on a dressed+bound strip line.

## [3.3.5] - 2026-09-01

### Added
- Same follower/friend ungag-to-drink as Hard 3.3.5 (SunHelm ≥ 70, gagged,
  close NPC, `BDSMUNLOCK` gag, belt stays).

## [3.3.4] - 2026-09-01

### Fixed
- Same dressed+bound-hands strip-wins occupancy gate as Hard 3.3.4, still
  only for predator/shady/arrest. Clothes/Arms hide the empty-slot BDSMLOCK
  catalog so gag/bra cannot beat `change_outfit_target`.

## [3.3.3] - 2026-09-01

### Changed
- Same behind-the-back pick as Hard 3.3.3 (not a forced armbinder).

## [3.3.2] - 2026-09-01

### Changed
- Same looser idea as Hard 3.3.2 (arms, clothes, silence last).

## [3.3.1] - 2026-09-01

### Changed
- Same bind-then-cut order as Hard 3.3.1, still only for predator/shady/arrest.

## [3.3.0] - 2026-09-01

### Added
- Strip-then-lock for predator/shady/arrest cases when the female target is
  still in armor — same SexLab `change_outfit_target` undress as Hard 3.3.0,
  not on ordinary greetings. See Hard CHANGELOG for the action shape.

## [3.2.5] - 2026-09-01

### Fixed
- Same women-only lock-target gate and catalog-SKU speech translation as `world-setting-hard`
  3.2.5 — see that CHANGELOG. Applied to this variant's `0010_setting`, `0710_gender_speech`,
  `0720_player_devices`, `0760_bdsm_lock_action`, `0761_vibrator_remote`, and
  `native_action_selector`.

### Fixed (corrects 3.2.4)
- Same correction as `world-setting-hard` 3.2.5 — see that CHANGELOG for the full story (3.2.4
  wrongly blocked BDSMLOCK/BDSMUNLOCK/ActivateVibratorOnActor for NPC targets entirely; reworked
  into a generalized `_lockTargetUUID`/`_lockTargetName` that correctly targets whoever the line
  is actually addressed to, player or NPC). Validated clean via `validate_prompt`.

## [3.2.4] - Unreleased

### Fixed
- Same `_addressingPlayer` mislock fix as `world-setting-hard` 3.2.4 — see that CHANGELOG for the
  live-confirmed root cause (Gorr's hallucinated narration about a different NPC, Daegon, ending
  in a real `BDSMLOCK` firing on the player instead). Applied to this variant's
  `native_action_selector.prompt`, `0760_bdsm_lock_action.prompt`, and
  `0761_vibrator_remote.prompt`. Validated live via `validate_prompt`.

## [3.2.3] - Unreleased

### Fixed
- `0760_bdsm_lock_action.prompt`'s player-facing slot-word map, same occupancy-filtered rewrite as
  `world-setting-hard` 3.2.3 — see that CHANGELOG and `bdsmlock-and-vibrations-fix` 2.5.2 for the
  live-confirmed root cause. Re-validated live via `validate_prompt` once MCP/game came back —
  passed clean.

## [3.2.2] - Unreleased

### Fixed
- `native_action_selector.prompt`'s `ActivateVibratorOnActor` guidance still said "Strength and
  duration are filled by the game" — stale since the params became dynamic. This file is the
  active action-selection path when "Embed Actions in Dialogue" is off, so the stale text was
  directly misleading whichever model handles it. Now matches `0761_vibrator_remote.prompt`'s
  current guidance: plain-digit vibStrength (1-5) and duration, with the same "never a word/
  placeholder/non-English text" reminder that mitigated the live TBD/garbled-token bug.

## [3.2.1] - Unreleased

### Fixed
- `0761_vibrator_remote.prompt`: added an explicit "plain digits only" reminder directly next to
  the `ACTION:` line template. Confirmed live via `openrouter_output.log`: the dynamic
  `vibStrength`/`duration` params (new in `bdsmlock-and-vibrations-fix` 2.2.0) occasionally came
  back malformed — non-English tokens (`普遍的`, `布4`) or the literal placeholder string `"TBD"`
  instead of a number, all observed during one long, dense escalation scene, suggesting
  context-length/generation-quality fatigue as a contributing factor rather than pure prompt
  ambiguity. This is a mitigation (stronger, closer-to-the-generation-point instruction), not a
  guaranteed fix — the underlying cause is LLM output reliability under long context, which prompt
  wording can reduce but not eliminate. Worth monitoring for recurrence.

## [3.2.0] - Unreleased

### Added
- `native_action_selector.prompt` previously had **zero** mention of `BDSMUNLOCK` — a narrated
  device removal had no positive instruction requiring the action line at all. Added the same
  enforcement line as Hard's copy, plus the negative gate Hard already had. Pairs with
  `bdsmlock-and-vibrations-fix` 2.4.0's new `BDSMUNLOCK` drilldown leaf-action mapping — see that
  package's CHANGELOG for the full root-cause writeup (a live in-game hood-removal that never
  actually fired).

## [3.1.3] - Unreleased

### Changed
- `0761_vibrator_remote.prompt`: same render_mode-guard-ordering best-practice fix as
  `bdsmlock-and-vibrations-fix` 2.2.3 (moved the guard above the header comment, no behavior
  change). Full validation sweep of every file in this package completed and confirmed clean.

## [3.1.2] - Unreleased

### Fixed
- No changes to this package's own content this round — bump tracks
  `bdsmlock-and-vibrations-fix` 2.2.2's real parse-error fix (infix `contains` → function form) in
  the shared `gagged_speech` component this package's narrative reacts to. See that package's
  CHANGELOG.

## [3.1.1] - Unreleased

### Fixed
- `0761_vibrator_remote.prompt`: the same `get_recent_events(N, [player.UUID])` parse error fixed
  in `bdsmlock-and-vibrations-fix` 2.2.1 also existed here (edge-count/last-presser detection) —
  fixed the same way (bare UUID, no brackets). Also rescaled the combat-intensity RNG check from
  `random < 0.5` (float, wrong) to `random < 50` (the real 0-100 integer scale, confirmed live via
  MCP). This affected every render of this file, i.e. every vibrator-remote-eligible turn.

## [3.1.0] - Unreleased

### Added
- `0761_vibrator_remote.prompt` deepened: multi-toy narration (names the
  specific worn device(s), though the underlying action is actor-wide with
  no per-device targeting), edge-count tracking across the session,
  orgasm-as-payoff guidance for `teaseOnly:false`, public-vs-hidden
  bystander awareness via `vrtedd_worn_visible`, predator-faction captor
  tone, and an RNG-gated (50%) combat-intensity suggestion via
  `is_in_combat`. Pairs with `bdsmlock-and-vibrations-fix` 2.2.0's new
  dynamic `vibStrength`/`duration` action params — required at that version
  or newer for the new guidance to reference real dynamic params. See that
  package's own CHANGELOG for full detail and the caveats (unverified
  `is_in_combat` and event-detection assumptions, deferred movement-state
  granularity, deferred real orgasm-completion event).

## [3.0.0] - Unreleased

### Changed (BREAKING)
- **Renamed** from "NEFARAM World Setting - Medium" to "World Setting - Medium"
  (`name`/`mo2_mod_name` — slug was already `world-setting-medium`, unchanged).
  This is a universal SkyrimNet+DD tool, not tied to the NEFARAM modlist, and
  most users of this package don't run NEFARAM. Because MO2 tracks mods by
  folder name, this is a **new mod folder for anyone upgrading** — remove the
  old "NEFARAM World Setting - Medium" install and install this one, it is
  not an in-place upgrade the way a same-name version bump would be.
- No longer includes `world_setting_shared` (the old `0722_worn_truth.prompt`
  physics file). Worn-device physics moved entirely into the required
  `bdsmlock-and-vibrations-fix` package (2.0.0+), now powered by a
  third-party addon's decorators instead of our own keyword list, and richer
  for it. This package is narrative/tone only now, full stop — see the repo
  root README's "core + addon, not bundle + bundle" note for why physics
  ownership belongs with the mechanics package, not the tone package.
- `bdsmlock-and-vibrations-fix` is required at **2.0.0+** specifically (not
  just "installed") — earlier versions of that package don't include the
  physics file this package's own tone content (`0720_player_devices.prompt`)
  assumes is rendering elsewhere in the prompt tree.

## [2.0.0] - Unreleased

### Changed (BREAKING)
- No longer bundles `bdsmlock_vibrations_fix` (BDSMLOCK drilldown + vibrator
  remote actions) or `gagged_speech` internally. Both are now separate
  companion installs — see this package's README for the new install order.
  Existing installs of the 1.3.0 all-in-one zip will lose the fix/gag
  functionality on upgrade unless the companion packages are installed too.
- If you want the old single-zip experience back, install
  `world-setting-medium-aio` instead — same combined content, new package.
- Own narrative content (`0010_setting`, `0710_gender_speech`,
  `0720_player_devices`, `0760_bdsm_lock_action`, `0761_vibrator_remote`,
  `0765_player_arrest`, `native_action_selector.prompt`) is unchanged —
  promoted into component `world_setting_medium_narrative` so the AIO
  package can reuse it without duplication.
- `0722_worn_truth.prompt` moved to shared component `world_setting_shared`
  (unchanged from 1.3.0's move).

## [1.3.0] - Unreleased

### Changed
- Ported into the mod-dev monorepo. No content changes from the original
  shipped `04.a NEFARAM World Setting - Medium.zip` — verified byte-identical
  via `diff -r` against the extracted original after build (see repo root
  README's verification steps).
- Vibrator-remote/drilldown logic and gagged-speech logic are now shared
  components (`bdsmlock_vibrations_fix`, `gagged_speech`) instead of
  hand-copied files, so future fixes to either apply here automatically.
- Occupancy physics sheet (`0722_worn_truth.prompt`) moved to shared
  component `world_setting_shared` after porting Hard confirmed it's
  byte-identical between the two variants.
- `native_action_selector.prompt` stays in this package's own `overlay/`
  (not shared) — porting Hard revealed the two variants' selector prompts
  genuinely disagree on when BDSMLOCK should fire, so they can't be one
  shared file.
