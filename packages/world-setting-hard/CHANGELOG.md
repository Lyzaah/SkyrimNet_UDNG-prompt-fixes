# Changelog

All notable changes to this package are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [3.3.9] - 2026-09-07

### Fixed
- A speaker whose own hands are bound (armbinder, elbow tie, butterfly binder,
  yoke, straitjacket, arm cuffs, or bondage mittens) could still be instructed
  to `BDSMLOCK` a device onto someone else, or narrate the behind-the-back
  "Arms first" restraint — `_speakerHandsBusy` existed but only ever gated
  the dressing/stripping branch, never the actual lock menu. Both
  `native_action_selector.prompt` and `0760_bdsm_lock_action.prompt` now
  short-circuit the whole BDSMLOCK/BDSMUNLOCK/Vibe*/change_outfit_target
  section when the speaker's own hands are busy, and the native selector's
  eligible-actions list drops those actions from the menu entirely in that
  case (not just the instruction text) so the model can't reach for them
  even off the generic "prefer an action over None" bias.

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
- Combat is a no-go for our scripts. `_fighting` is
  `is_in_combat(speaker) or is_in_combat(target)` — native SkyrimNet combat
  flag, not the DD addon. While it is true the lock/vibe/strip **prompt is
  omitted** (no `## Combat` Do-Not block, no occupancy sheet, no BDSMLOCK
  in Eligible Actions). Talk is fine. After-fight spoils stay with other
  Devious mods (and with us once `is_in_combat` drops, including the usual
  un-hostile flee window). Removed the mid-fight `VibePunish` nudge. Plug
  visibility (`vrtedd_worn_visible`) still gates *public vs hidden* out of
  combat. Dressed + bound hands: selector hides `BDSMLOCK` so strip is the
  listed option, not a listed-then-forbidden one.

## [3.3.5] - 2026-09-01

### Added
- Follower/friend ungag-to-drink: if the player is gagged and SunHelm thirst
  or hunger is ≥ 70, a close NPC (follower or rank ≥ 1) who can work a buckle
  MUST `BDSMUNLOCK` the gag this line so she can drink/eat. Belt stays. Live:
  Tina thirst 98, gagged, Daegon follower+friend — and the AIO never told her
  to take it off because that block lived only in `0730` (not bundled). Also
  punches through 0935's "do not ungag because she asked" (mmph is not a
  request; parched is visible).

## [3.3.4] - 2026-09-01

### Fixed
- Dressed + bound hands no longer keeps stacking toys. Live (`SkyrimNet.log`):
  Daegon addressing Evelyn got `## Clothes` with the exact
  `change_outfit_target` ACTION, then still `BDSMLOCK`'d gag and chastity bra
  because the occupancy sheet above it listed those slots as "legal to lock
  this line" and the section title was still `BDSMLOCK`. Arms/Clothes now
  replace that catalog: clothes-on + hands bound → strip only; clothes-on +
  free hands → behind-the-back only. Selector occupancy-gates the same way
  (`MUST change_outfit_target`, overrides a spoken gag/bra). 0710/0720 stop
  telling the model to "tease the next empty piece" while she is still
  dressed.

## [3.3.3] - 2026-09-01

### Changed
- First lock is any empty behind-the-back restraint (armbinder, butterfly,
  elbow tie) — not a hardcoded armbinder.

## [3.3.2] - 2026-09-01

### Changed
- Less script, more idea: arms behind the back, then clothes, gag/hood last so
  she can still complain. Numbered punishment ladder and "prefer hood now"
  removed. Occupancy map and ACTION shapes stay as tools.

## [3.3.1] - 2026-09-01

### Changed
- Bind-then-cut: a dressed female target gets armbinder/arm cuffs **first**, then
  `change_outfit_target` undress with cutting-clothes narration once her hands
  are locked. Bound hands never pick `GetDressed`/`EquipArmor`/`change_outfit`.
  Evelyn already stripped stays skipped (`ArmorCuirass`/`ClothingBody` absent).

## [3.3.0] - 2026-09-01

### Added
- **Strip-then-lock for female targets.** A mouthy adventuress still in
  `ArmorCuirass`/`ClothingBody` (not a locked catsuit) gets her clothes taken
  this line via SexLab `change_outfit_target` (`stripped`, `style: forcefully`,
  `how: undresses`) — like a defeat — and BDSMLOCK waits until she is actually
  out of the armor. `Undress`/`change_outfit` only strip the speaker; never those.
  Speaker must not be in combat or have bound hands (matches SexLab eligibility).
- Punishment hood/mask is now the default public claim when hood is empty and
  she did not name another slot. Bondage heels are no longer preferred.

## [3.2.5] - 2026-09-01

### Fixed
- **Women-only lock targets, confirmed live** (`SkyrimNet - Kopie.log`, 2026-09-01):
  Belethor (Male) was a real `BDSMLOCK` target — intents `gag Belethor`, `chastity belt Belethor`,
  `catsuit Belethor` fired because `_lockTargetUUID` followed `responseTarget` with no gender
  check. Daegon is Female so NPC-on-NPC locking her stays legal. `0760` / `0761` /
  `native_action_selector` now retarget onto `responseTarget` only if `decnpc(...).isFemale`;
  a male addressee does not fall back onto the player (that was the 3.2.4 mislock). When
  `_lockWomenOnly` is false the lock/unlock/vibe instructions are omitted and replaced with
  "pick no lock." Same gate in `0010_setting` and `0710_gender_speech`.
- **Catalog SKUs leaking into spoken narration, confirmed live:** TTS and thoughts recited
  inventory names (`Steel Chastity Bra (Padded)`, `Steel Cuffs (Padded) (Arms)`). `0500`,
  `0720`, `0722`, and `0760` now tell the model to translate SKUs into ordinary speech and
  never say "Female" as a product prefix.

### Fixed (corrects 3.2.4)
- **3.2.4's fix was wrong and regressed a working feature.** It assumed BDSMLOCK/BDSMUNLOCK/
  ActivateVibratorOnActor could only ever target the player, and blocked them entirely whenever
  a line addressed a different NPC. Caught immediately: `EQUIP_ARMBINDERS_Black_Leather_Armbinder
  PARAMS: {"target":"Daegon"}` had already fired successfully earlier in the SAME log session —
  NPC-on-NPC locking genuinely works (`ACTION: BDSMLOCK PARAMS: {"intent": "armbinder Daegon"}`
  correctly drilled down to a real lock on Daegon, not the player). The actual bug was narrower:
  the model sometimes writes the WRONG name into `intent`/`target`/`Actor` (naming the player when
  the scene is about a different NPC), not that locking an NPC is structurally impossible.
  Reworked properly: `native_action_selector.prompt`, `0760_bdsm_lock_action.prompt`, and
  `0761_vibrator_remote.prompt` now compute a generalized `_lockTargetUUID`/`_lockTargetName`
  (the actual `responseTarget` if one exists and differs from the player, else the player) and use
  it everywhere occupancy was previously hardcoded to `player.UUID`/`player_name` — including the
  vibrator's press-history/visibility/combat tracking. This makes locking/unlocking/buzzing correct
  for BOTH the player and any other NPC being addressed, and keeps the ACTION line's named target
  in sync with who the scene is actually about, instead of either blocking NPC targets (3.2.4) or
  leaving the name un-grounded (pre-3.2.4). Confirmed live via `render_template`: with Gorr
  addressing Daegon, `_lockTargetName` resolves to "Daegon" and occupancy correctly reads Daegon's
  real worn gear (gag=true, hood=false), not the player's. Validated clean via `validate_prompt`.

## [3.2.4] - Unreleased

### Fixed
- **Real mislock bug, confirmed live:** `native_action_selector.prompt`, `0760_bdsm_lock_action.prompt`,
  and `0761_vibrator_remote.prompt` offered `BDSMLOCK`/`BDSMUNLOCK`/`ActivateVibratorOnActor` even
  when the current dialogue line was addressed to a DIFFERENT NPC, not the player — because these
  actions only ever have one valid target (the player), any device word mentioned about another
  NPC could get mechanically redirected onto the player instead. Observed live: Gorr narrated
  binding/gagging **Daegon** (an NPC-on-NPC scene, confirmed via memory summaries: "black leather
  armbinder and gag" on Daegon, no hood anywhere), then hallucinated "that leather hood" onto
  Daegon in a later line with no mechanical backing — and the action selector then fired
  `ACTION: BDSMLOCK PARAMS: {"intent": "hood Tina"}`, locking a real hood onto the PLAYER (Tina)
  based on a scene that was never about her. Root cause: nothing checked whether the actual
  conversation target of the current line was the player before allowing these actions to render.
  Fixed with a new `_addressingPlayer` guard — `responseTarget.UUID == player.UUID` (confirmed live
  via `render_template`: evaluates `false` when Gorr addresses Daegon, `true` when addressing Tina;
  defaults to `true` when no `responseTarget` exists at all, e.g. single-actor renders) — that
  structurally omits all three device-action instructions when the line isn't addressed to the
  player, replacing them with a short "these actions can't act on anyone but {{ player_name }}"
  note. Same structural-omission pattern as the occupancy-filtering fix in 3.2.3/2.5.2. Validated
  live via `validate_prompt` (all three files clean).

## [3.2.3] - Unreleased

### Fixed
- `0760_bdsm_lock_action.prompt`'s player-facing slot-word map (gag/collar/hood/.../corset →
  group token) listed all 16 lines unconditionally, same shape as the drilldown bug fixed in
  `bdsmlock-and-vibrations-fix` 2.5.2 — see that CHANGELOG for the live-confirmed root cause (a
  real double-gag attempt even with Claude Sonnet 4.6 as Action Evaluation model). Each line is
  now wrapped in `{% if not _<slot> %}` so an occupied slot's line is never rendered at all, plus
  a new closing block: if every slot is occupied, the map is replaced with an explicit "nothing
  left to name, do not BDSMLOCK, tease a worn piece or use the remote instead" instruction.
  Re-validated live via `validate_prompt` once MCP/game came back — passed clean.

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
- `0761_vibrator_remote.prompt`: same "plain digits only" mitigation as `world-setting-medium`
  3.2.1 — see that CHANGELOG for the full root-cause writeup (malformed `vibStrength`/`duration`
  values observed live: non-English tokens and a literal `"TBD"` placeholder instead of a number).

## [3.2.0] - Unreleased

### Added
- `native_action_selector.prompt`: added a positive enforcement line requiring the BDSMUNLOCK
  action whenever a line narrates removing a device — previously only the negative gate existed
  ("do not pick BDSMUNLOCK unless..."), nothing said the reverse was equally required. Pairs with
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
- **Renamed** from "NEFARAM World Setting (HARD)" / "NEFARAM World Setting -
  Hard" to "World Setting (HARD)" / "World Setting - Hard" (`name`/
  `mo2_mod_name` — slug was already `world-setting-hard`, unchanged). This is
  a universal SkyrimNet+DD tool, not tied to the NEFARAM modlist, and most
  users of this package don't run NEFARAM. Because MO2 tracks mods by folder
  name, this is a **new mod folder for anyone upgrading** — remove the old
  "NEFARAM World Setting - Hard" install and install this one, it is not an
  in-place upgrade the way a same-name version bump would be.
- No longer includes `world_setting_shared` (the old `0722_worn_truth.prompt`
  physics file, which was already shared byte-for-byte with Medium). Worn-
  device physics moved entirely into the required `bdsmlock-and-vibrations-fix`
  package (2.0.0+), now powered by a third-party addon's decorators instead
  of our own keyword list, and richer for it. This package is narrative/tone
  only now, full stop.
- `bdsmlock-and-vibrations-fix` is required at **2.0.0+** specifically (not
  just "installed") — earlier versions of that package don't include the
  physics file this package's own tone content (`0720_player_devices.prompt`)
  assumes is rendering elsewhere in the prompt tree. That same 2.0.0+ also
  now bundles gagged-speech, which this package still doesn't include
  directly (unchanged — it never has).

## [2.0.0] - Unreleased

### Changed (BREAKING)
- No longer bundles `bdsmlock_vibrations_fix` (BDSMLOCK drilldown + vibrator
  remote actions) internally. Now a separate required companion install —
  see this package's README for the new install order.
- If you want the old single-zip experience back, install
  `world-setting-hard-aio` instead — same combined content, new package.
- Still does not bundle `gagged_speech` (unchanged from 1.3.0 — confirmed
  from the original shipped zip's own README that it never did).
- Own narrative content (`0010_setting`, `0710_gender_speech`,
  `0720_player_devices`, `0760_bdsm_lock_action`, `0761_vibrator_remote`,
  `0765_player_arrest`, `native_action_selector.prompt`) is unchanged —
  promoted into component `world_setting_hard_narrative` so the AIO
  package can reuse it without duplication.

## [1.3.0] - Unreleased

### Added
- Ported into the mod-dev monorepo from the original shipped
  `04.b NEFARAM World Setting - Hard.zip`. No content changes — verified
  byte-identical via `diff -r` against the extracted original after build.
- Confirmed via the original zip's own README that Hard does **not** bundle
  gagged-speech (unlike Medium, which did at the time) — `includes:` in
  `package.yaml` reflected this.
- Porting this surfaced that Hard and Medium's `native_action_selector.prompt`
  and all six `user_final_instructions`/`system_head` narrative files
  genuinely differ in tone/logic (not just cosmetic wording) — only
  `native_action_selector_drilldown.prompt`, the two vibrator action YAMLs,
  and `0722_worn_truth.prompt` were truly identical between the two variants.
