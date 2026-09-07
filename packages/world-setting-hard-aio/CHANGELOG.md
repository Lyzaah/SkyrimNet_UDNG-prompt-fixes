# Changelog

All notable changes to this package are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [3.2.6] - 2026-09-07

### Fixed
- Material preference never worked (dead `decnpc().background`/`.personality`
  read) — now sourced from `get_world_knowledge`. See
  `HOWTO_NPC_PREFERENCES.md`. Also picks up the reordered vibe-YAML params
  and the `0761` edge-count `isString` guard. Ported from a hand-built
  release published outside this repo — see `world-setting-aio` CHANGELOG
  3.3.10 for the full story.

## [3.2.5] - 2026-09-02

### Changed
- README rewritten: current requirements with links, install order,
  Hard-vs-Medium, combat omit, baked vibe leaves. Stale 2.x history
  and freeform `vibStrength` docs removed from the zip README.
- Experimental (`0730`) stays **out** of this AIO. Separate zip:
  `SkyrimNet Kink Experimental` — see `EXPERIMENTAL.md`.

## [3.2.4] - 2026-09-01

### Changed
- Combat no-go for lock/strip/vibe is omit-the-prompt, not a Do-Not list.
  Inherited from Hard 3.3.6 / Fix 2.7.6.

## [3.2.3] - 2026-09-01

### Added
- Mistress/follower ungag when the player is parched or starving (SunHelm
  ≥ 70). Inherited from Hard 3.3.5 / Fix 2.7.5. `0730` still not bundled.

## [3.2.2] - 2026-09-01

### Fixed
- Strip actually wins: dressed + bound hands → `change_outfit_target`, not
  another BDSMLOCK. Live miss was Daegon stacking gag/bra on still-clothed
  Evelyn after Clothes already rendered. Inherited from Hard 3.3.4 / Fix 2.7.4.

## [3.2.1] - 2026-09-01

### Changed
- First lock is armbinder, butterfly, or elbow tie — actor picks.

## [3.2.0] - 2026-09-01

### Removed
- `kink_experimental` (`0730_kink_experimental.prompt`) is no longer bundled in
  the AIO. Drop it in yourself as a separate overlay if you want it.

## [3.1.2] - 2026-09-01

### Changed
- Arms, clothes, let her complain. Gag/hood last. Less beat-sheet, same tools.

## [3.1.1] - 2026-09-01

### Changed
- Bind-then-cut: armbinder/cuffs first, then cut the armor off a helpless girl.
  Bound hands do not re-equip. Inherited from Hard 3.3.1 / Fix 2.7.1.

## [3.1.0] - 2026-09-01

### Added
- Strip-then-lock: mouthy female adventurers still in armor get
  `change_outfit_target` undressed like a defeat, then BDSMLOCK. Punishment
  hood/mask is the public claim; heels are no longer the default. Inherited
  from `world-setting-hard` 3.3.0 / `bdsmlock-and-vibrations-fix` 2.7.0.

## [3.0.2] - 2026-09-01

### Fixed
- Women-only lock targets: `BDSMLOCK`/`BDSMUNLOCK`/vibe never act on men. Live (`SkyrimNet - Kopie.log`): Belethor was getting gags/catsuits/chastity because `responseTarget` had no gender check. Daegon (Female) still lockable. Inherited from `world-setting-hard` 3.2.5 / `bdsmlock-and-vibrations-fix` 2.6.0.
- Catalog SKUs (`Steel Chastity Bra (Padded)`, `Female Chastity Bra (Padded)`) no longer get recited in dialogue/TTS — translate to ordinary speech.

## [3.0.1] - 2026-09-01

### Removed
- `sla_Arousal` numbers from Hard 0710/0720/0761. SkyrimNet_Arousal owns
  bio + ArousalChange; dumping 0–100 at the LLM was noise.

## [3.0.0] - 2026-09-01

### Changed
- Feature-freeze snapshot of `grok/prompt-readability`: Hard shape-instruction
  rewrite (no copy-me filth scripts), baked vibe leaves, SLO Arousal numbers as
  facts in 0710/0720/0761. ArousalChange stays with SkyrimNet_Arousal.

## [2.7.0] - Unreleased

### Added
- Inherits the generalized `0935_player_gagged_listener.prompt` reaction guidance
  (`bdsmlock-and-vibrations-fix` 2.6.0) — see that CHANGELOG. Not yet re-validated live.

## [2.6.4] - Unreleased

### Fixed (corrects 2.6.3)
- Inherits the `_lockTargetUUID`/`_lockTargetName` generalization (`world-setting-hard` 3.2.5) that
  corrects the previous fix's wrong assumption that BDSMLOCK could only target the player — see
  that CHANGELOG. Also inherits that version's women-only lock-target gate (no BDSMLOCK on men)
  and catalog-SKU speech translation.

## [2.6.3] - Unreleased

### Fixed
- Inherits the `_addressingPlayer` mislock fix (`world-setting-hard` 3.2.4) — see that CHANGELOG.

## [2.6.2] - Unreleased

### Fixed
- Inherits the occupancy-filtered BDSMLOCK group/slot-map fix (`bdsmlock-and-vibrations-fix`
  2.5.2, `world-setting-hard` 3.2.3) — see those CHANGELOGs, now re-validated live.

## [2.6.1] - Unreleased

### Fixed
- Inherits the BDSMUNLOCK priority-chain fix (`bdsmlock-and-vibrations-fix` 2.5.1) and the stale
  vibrator-param text fix (`world-setting-hard` 3.2.2) — see those CHANGELOGs.

## [2.6.0] - Unreleased

### Changed
- Inherits the dynamic BDSMUNLOCK leaf-mapping change from `bdsmlock-and-vibrations-fix` 2.5.0 —
  see that CHANGELOG.

## [2.5.1] - Unreleased

### Fixed
- Inherits the "plain digits only" vibrator-parameter mitigation from `world-setting-hard` 3.2.1 —
  see that CHANGELOG.

## [2.5.0] - Unreleased

### Added
- Inherits the BDSMUNLOCK fix from `bdsmlock-and-vibrations-fix` 2.4.0 and `world-setting-hard`
  3.2.0 — narrated device removal now actually requires and maps to a real `EXTCMDUNEQUIP*`
  action instead of only being spoken. See those CHANGELOGs.

## [2.4.0] - Unreleased

### Added
- Inherits the device-material RNG + bio-preference fix from `bdsmlock-and-vibrations-fix` 2.3.0
  (`native_action_selector_drilldown.prompt` no longer defaults to "Black Leather" every lock).
  See that package's CHANGELOG.

## [2.3.3] - Unreleased

### Changed
- Inherits the render_mode-guard-ordering best-practice fix (0935/0761/0500/0722, no behavior
  change) from `bdsmlock-and-vibrations-fix` 2.2.3 and `world-setting-hard` 3.1.3. Full
  validation sweep of every file in this bundle completed and confirmed clean this round.

## [2.3.2] - Unreleased

### Fixed
- Inherits the second real parse-error fix (infix `contains` → function form, found live in-game
  after 2.3.1) from `bdsmlock-and-vibrations-fix` 2.2.2 — see that CHANGELOG. Update if you
  installed 2.3.1, it still had this bug.

## [2.3.1] - Unreleased

### Fixed
- Inherits the `get_recent_events` parse-error fix and RNG/relationship-rank rescaling from
  `bdsmlock-and-vibrations-fix` 2.2.1 and `world-setting-hard` 3.1.1 — see those CHANGELOGs. This
  was a real render-breaking bug hitting every gagged-speech and vibrator-remote render; update if
  you installed 2.3.0.

## [2.3.0] - Unreleased

### Added
- New `roleplay_guidelines` component (`guidelines/0500_roleplay_guidelines.prompt`), adapted from
  the shipped NEFARAM prompt-mod's version of this file — same shared component as
  `world-setting-medium-aio` 2.3.0, content is tone-neutral so no Hard-specific fork was needed.
  Deliberately does not restate `0010_setting.prompt`'s adult-fiction greenlight (different prompt
  slot, same message would just be redundant) — adds NPC agency/non-omniscience, anti-melodrama
  register, an explicit sexual-language bar, and a bridge sentence telling the model that
  devices/locking/kink are already live, mechanically-backed world texture elsewhere in this same
  prompt tree.

## [2.2.0] - Unreleased

### Added
- Inherits the deepened `0761_vibrator_remote.prompt` (multi-toy narration,
  edge-count tracking, orgasm-as-payoff guidance, public-vs-hidden tension,
  faction-flavored captor tone, RNG-gated combat intensity) and the new
  dynamic `vibStrength`/`duration` action params — see
  `bdsmlock-and-vibrations-fix` 2.2.0's own CHANGELOG for full detail.

## [2.1.0] - Unreleased

### Added
- Inherits `gagged_speech`'s deepened gag narration (device/layering tiers,
  time-locked escalation, blind+gag stacking, deaf-player handling,
  relationship-scaled comprehension chance) and the generalized multi-NPC
  gagged-speaker handling in `event_history`/`event_history_compact` — see
  `bdsmlock-and-vibrations-fix` 2.1.0's own CHANGELOG for full detail.

### Fixed
- Inherits the new `hood_just_locked` trigger closing the hood-lock gap in
  the gag-lock trigger, and the `gag_just_locked` rename (was
  `nefaram_gag_just_locked`).

## [2.0.0] - Unreleased

### Changed (BREAKING)
- **Renamed** from "NEFARAM World Setting - Hard (AIO)" to "World Setting -
  Hard (AIO)" — new MO2 mod folder, not an in-place upgrade. This is a
  universal SkyrimNet+DD tool, not tied to the NEFARAM modlist.
- `includes:` updated to match the underlying pieces' own 2.0.0/3.0.0
  restructure: dropped `world_setting_shared`, added `vrtedd_worn_truth`
  (worn-device physics, now powered by a third-party addon's decorators —
  see `bdsmlock-and-vibrations-fix`'s own CHANGELOG for detail). Content is
  otherwise the same combination as before, just current with what
  `world-setting-hard` and `bdsmlock-and-vibrations-fix` ship today.
- **New external requirement:** the third-party "DD SkyrimNet AddOn" (Base
  component, ESP ticked) for the worn-device physics section to render.
  Everything else in this bundle works without it.

## [1.0.0] - Unreleased

### Added
- New convenience-bundle package: `bdsmlock_vibrations_fix` +
  `world_setting_shared` + `world_setting_hard_narrative` + `gagged_speech`
  combined into one zip, for users who want a single-mod experience instead
  of managing the separate `world-setting-hard` + `bdsmlock-and-vibrations-fix`
  + `gagged-speech` packages individually.
- Unlike the original shipped `04.b NEFARAM World Setting - Hard.zip`, this
  AIO variant includes gagged-speech (the original never bundled it).
  Content otherwise verified against the extracted original — differences
  are exactly the added gagged-speech files, confirmed via `diff -r`.
