# Changelog

All notable changes to this package are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [2.7.7] - 2026-09-07

### Fixed
- **Material preference never worked, for any NPC, ever.** The drilldown's
  material-preference check read `decnpc(npc.UUID).background` /
  `.personality` — those fields don't exist on the actor decorator, so the
  check silently always came up empty. Switched to
  `get_world_knowledge(npc.UUID)` (guarded `isString`), so a per-NPC World
  Knowledge entry now actually drives the Steel/Chain/Ebonite/Leather pick.
  See `HOWTO_NPC_PREFERENCES.md` (ships with `world-setting-aio`) for setup.
- **Vibrator remote param order.** All five vibe action YAMLs
  (`vibehornify(long)`, `vibejab`, `vibepunish`, `vibetease`) had the
  dynamic `teaseOnly` param mapped before the static `vibStrength`/
  `duration` params — reordered to match the actual
  `zadLibs.VibrateEffectAsync` call shape.
- Ported from a hand-built release published outside this repo (no git
  remote exists) — see `world-setting-aio` CHANGELOG 3.3.10 for the full
  story of how these were found.

## [2.7.6] - 2026-09-01

### Changed
- Combat no-go is structural omission: selector + drilldown **hide**
  BDSMLOCK / EQUIP_* / EXTCMDUNEQUIP* / vibe from Eligible Actions while
  `is_in_combat` is true on speaker or target. No "pick None" combat
  paragraph. Device occupancy sets also skip that turn.

## [2.7.5] - 2026-09-01

### Added
- Gagged-listener (`0935`) and overlay selector: if the player is gagged and
  SunHelm thirst/hunger ≥ 70, a follower/friend who can work a buckle
  `BDSMUNLOCK`s the gag so she can drink/eat. Overrides "do not ungag because
  she asked." Belt stays.

## [2.7.4] - 2026-09-01

### Fixed
- Overlay selector occupancy-gates strip: dressed + bound hands MUST
  `change_outfit_target`, not another BDSMLOCK (overrides a spoken gag/bra).
  Dressed + free hands: behind-the-back first. Empty device catalog is hidden
  until she is out of the armor.

## [2.7.3] - 2026-09-01

### Changed
- Overlay selector: behind-the-back pick (`armbinder` / `butterfly` / `elbow binder`).

## [2.7.2] - 2026-09-01

### Changed
- Overlay selector: one-line idea (armbinder → undress → gag/hood last).

## [2.7.1] - 2026-09-01

### Changed
- Overlay selector: bind hands first, then cut clothes. Bound-hand speakers
  never re-dress (`GetDressed`/`EquipArmor`/`change_outfit`).

## [2.7.0] - 2026-09-01

### Added
- Overlay `native_action_selector`: if the female lock-target is still in armor
  and this is spoils/arrest/she asked to be stripped, pick SexLab
  `change_outfit_target` (`stripped` / `forcefully` / `undresses`) this line
  instead of BDSMLOCK. Hood/mask maps to `hood`.

## [2.6.0] - 2026-09-01

### Fixed
- **Women-only device targeting, confirmed live** (`SkyrimNet - Kopie.log`, 2026-09-01):
  Belethor (Male) received real locks (`gag Belethor`, chastity belt, catsuit) because
  drilldown and the overlay selector followed `responseTarget` with no gender check.
  `native_action_selector_drilldown.prompt` and the overlay `native_action_selector.prompt`
  now share the same `_lockWomenOnly` gate as world-setting 3.2.5: retarget onto a
  `responseTarget` only if she is female; a male addressee does not fall back onto the
  player; otherwise pick `None` for `BDSMLOCK`/`EQUIP_*`/`BDSMUNLOCK`/Vibe*.
- `0722_worn_truth.prompt`: catalog SKUs in the physics sheet (`Steel Chastity Bra (Padded)`,
  `Female Chastity Bra (Padded)`, parenthetical slot tags) were being copied into TTS.
  Added an explicit translate-into-ordinary-speech instruction after the physics block.

### Added
- `gagged_speech`'s `0935_player_gagged_listener.prompt` — the rich per-line reaction guidance
  (gag-type flavor, layered gag+hood tier, elapsed-time escalation, blind/deaf handling,
  relationship-scaled comprehension chance) — was still hardcoded to `player.UUID` despite
  `event_history.prompt`/`event_history_compact.prompt` already being generalized to any gagged
  actor. Practical effect: an NPC talking directly to a gagged NPC (not the player) got no live
  reaction guidance at all, just the generic history line. Generalized with the same
  `_gaggedUUID`/`_gaggedName` pattern as BDSMLOCK's `_lockTargetUUID`/`_lockTargetName` —
  `responseTarget` if it exists and isn't the player or the speaking NPC itself, else the player.
  Filename kept as `0935_player_gagged_listener.prompt` for history; content is no longer
  player-specific. Motivated directly by confirming BDSMLOCK now genuinely works NPC-on-NPC
  (Gorr gagging/binding Daegon) and asking whether the gagged-speech reaction layer keeps up —
  it didn't, until this. **Not yet re-validated live** — MCP was disconnected when this landed;
  run `validate_prompt` before calling this closed.

## [2.5.2] - Unreleased

### Fixed
- `native_action_selector_drilldown.prompt`'s `BDSMLOCK` category-drilldown group list ("Live
  groups are ONLY: GAGS, COLLARS, ...") was a static enumeration of all 18 groups every single
  turn, with only prose telling the model not to pick an occupied one. Confirmed live even with
  **Claude Sonnet 4.6** as the Action Evaluation model (an explicit test ruling out "needs
  a stronger model" as the fix): Gorr and Daegon both independently fired `BDSMLOCK {"intent":
  "gag Tina"}` within seconds of each other despite the mouth already being occupied, triggering
  9+ wasted `EQUIP_GAGS_*` leaf attempts. Direction taken: stop telling the model "don't pick
  the occupied one" and instead never list it at all. Rewritten to build the group list from a
  dynamically-populated `_emptyGroups` array (reusing the same occupancy booleans already computed
  for the lock-side "currently wears" text) and render only `join(_emptyGroups, ", ")` — an
  occupied group is structurally absent from the prompt, not just discouraged. Mirrors the same
  structural-omission pattern already applied to `BDSMUNLOCK` in 2.5.0. Companion fix to
  `world-setting-hard` 3.2.3 / `world-setting-medium` 3.2.3, which apply the identical dynamic
  treatment to the player-facing slot-word map in `0760_bdsm_lock_action.prompt`. Re-validated live
  once MCP/game came back: `validate_prompt` passed on all three edited files, and `render_template`
  against Tina's real worn equipment (gag, hood, blindfold, belt, hand-restraint device) confirmed
  `_emptyGroups` correctly excludes GAGS and the whole hand-restraint group
  (ARMBINDERS/ELBOW_BINDERS/BUTTERFLY_BINDERS/YOKES/STRAITJACKETS) while still listing
  COLLARS/BOOTS/PIERCINGS/CHASTITY_BRAS/HARNESSES/SUITS/ARM_CUFFS/LEG_CUFFS/GLOVES/CORSETS.

## [2.5.1] - Unreleased

### Fixed
- `native_action_selector_drilldown.prompt`'s BDSMUNLOCK hand-restraint detection treated
  armbinder/elbow-tie/straitjacket/yoke/heavy-bondage/butterfly as mutually exclusive — they are
  not. Confirmed live via `get_worn_equipment`: a single worn butterfly binder carries
  `zad_DeviousArmbinder`, `zad_DeviousHeavyBondage`, AND `zad_DeviousButterfly` simultaneously
  (broader category tags riding on the same item as its specific type tag). The independent
  `{% if %}` checks from 2.5.0 would have rendered contradictory lines for one physical item
  ("armbinder → EXTCMDUNEQUIPBINDER" AND "butterfly, no unequip action exists" both at once).
  Rewritten as a priority `elif` chain — most specific real device type wins, generic "armbinder"
  is the last-resort fallback only when none of the more specific tags are present. Re-confirmed
  live: the actual worn item now correctly resolves to butterfly-only, no armbinder line.

## [2.5.0] - Unreleased

### Changed
- `native_action_selector_drilldown.prompt`'s `BDSMUNLOCK` leaf mapping is now generated
  dynamically from the same `worn_has_keyword` occupancy checks the lock side already computes,
  instead of a static 21-line catalog shown every time regardless of what's actually worn.
  Call made: the model only ever needs to know what it could plausibly remove, not memorize a
  full command catalog on every single BDSMUNLOCK turn — fewer tokens, less room to invent an
  action that doesn't apply. Confirmed live via `render_template` against the current player
  character (wearing gag/hood/blindfold/belt/armbinder): the list correctly showed exactly those
  five options, nothing else. Also confirmed the underlying assumption first via `render_template`:
  `{% set %}` values assigned inside an `{% if %}` block remain readable for the rest of the
  template after `{% endif %}` in this engine — this is what makes reusing the lock-side occupancy
  booleans for the unlock section safe.

## [2.4.0] - Unreleased

### Added
- `native_action_selector_drilldown.prompt`: real leaf-action mapping for `BDSMUNLOCK` — 21 of the
  25 `EXTCMDUNEQUIP*` actions now have an explicit slot-word → action mapping, mirroring the
  existing `BDSMLOCK` slot table. Previously there was zero drilldown guidance for unlocking at
  all, only a one-line negative gate on the category selector ("do not pick BDSMUNLOCK unless...").
  Confirmed live in-game: an NPC narrated removing a hood ("*unlocks the mask, letting it fall
  away*") with no `ACTION:` line at all, `openrouter_output.log` confirmed no action ever fired —
  the device stayed locked despite the narration. Root cause: our own prompt content only
  positively enforced the LOCK path ("talking about it without the action leaves her free" appears
  many times); nothing equivalent existed telling the model an unlock narration also requires its
  own action line. Also flagged: no unequip action exists for boots/heels in the confirmed 25-item
  catalog, and `EXTCMDUNEQUIPANKLESHACKLES` is a distinct action from `EXTCMDUNEQUIPLEGCUFFS` on
  the unlock side — asymmetric with the lock side, where ankle shackles fold into `LEG_CUFFS` with
  no separate group. Documented as-is rather than guessed around.
- `native_action_selector.prompt` (both variants): added the missing positive enforcement line —
  "if your own line narrates removing a device, you MUST end with the BDSMUNLOCK action line this
  same turn." Medium's selector previously had **zero** mention of BDSMUNLOCK at all (Hard at
  least had the one negative gate); both now have the same instruction.

## [2.3.0] - Unreleased

### Added
- `native_action_selector_drilldown.prompt`: device material picks (Black Leather/Iron/Padded/
  Steel/Chain/Ebonite) are now weighted-RNG (`random`, confirmed 0-100 integer scale) instead of
  defaulting to "Black Leather" out of habit — a real bug reported by a tester and confirmed live
  in `openrouter_output.log` (two independent chastity-belt locks in the same session both landed
  on `Black_Leather_Chastity_Belt` despite the drilldown trying `Iron` and `Padded` as candidates
  first). NPCs with a stated material preference in `decnpc().background`/`.personality` (e.g. an
  NPC written as liking "steel" or "chain" gear) now prefer that material instead of rolling,
  falling back to the random pick if no matching item exists for that slot. Confirmed live via
  `render_template` against two real nearby NPCs (empty bios fall through to the random branch
  correctly, no crash).

## [2.2.3] - Unreleased

### Changed
- Best-practice fix per `~/SkyrimNet/modding/WORKFLOW_PROMPTS.md` Step 4.6 ("define render mode
  perspective once at the top of submodules"): `0935_player_gagged_listener.prompt` and
  `0722_worn_truth.prompt` had grown long header comments that pushed their `render_mode` guard
  past the first 5 lines — the same class of dashboard warning as
  "`0410_equipment` is not following best practices ... may be causing response delays" seen
  live in-game (that specific file isn't ours, but the same lint would likely flag these). Fixed
  by moving the guard `{% if %}` to the top and the explanatory comment inside it — no behavior
  change, purely reordering.
- Full validation sweep completed this round: every `.prompt` file, both action YAMLs, and both
  trigger YAMLs in this package (and its sibling narrative/AIO packages) confirmed `valid: true`
  via live `validate_prompt`/`validate_custom_action`/`validate_custom_trigger` — not just the
  files touched in earlier 2.x rounds. See [[mod-dev-mcp-validated-bugs]] in project memory.

## [2.2.2] - Unreleased

### Fixed
- **Second real render-breaking parse error, found live in-game after 2.2.1 shipped** (2.2.1 fixed
  one bug but didn't re-validate the full file afterward, so this one was still hiding behind it):
  `X contains "Y"` used as an infix expression (e.g.
  `event.data.str_arg contains "locked"`, `_gagName contains "ring"`) is not valid syntax — `inja`
  reported `malformed expression` at the point it gave up parsing the compound condition.
  `contains` is a **function**, confirmed via `get_decorators`: `contains(x, "y")`, and negation is
  `not contains(x, "y")`. Fixed all 11 occurrences across `player_dialogue.prompt` and
  `0935_player_gagged_listener.prompt` (the gag-lock-time scan condition, and every gag-type
  name-matching branch). Confirmed via full-file `validate_prompt` this time, not a shortened
  snippet — see [[mod-dev-mcp-validated-bugs]] in project memory for the process lesson.

## [2.2.1] - Unreleased

### Fixed
- **Real render-breaking parse error**, confirmed live via `validate_prompt` once MCP was
  connected: `get_recent_events(N, [npc.UUID])` / `get_recent_events(N, [player.UUID])` — an
  inline single-element array literal wrapping a UUID — fails to parse
  (`json.exception.parse_error.101`, "invalid literal; last read '[np'"/'[p''). Fixed in
  `player_dialogue.prompt` and `0935_player_gagged_listener.prompt` by dropping the brackets
  (`get_recent_events` accepts a bare UUID directly per its own docs — confirmed via
  `get_decorators`). This affected every render of both files, i.e. every gagged-player transform
  line and every NPC reacting to a gagged player — very likely the actual source of the "prompt
  errors" reported after the 2.1.0 gagged-speech round.
- Relationship-scaled comprehension chance in `0935_player_gagged_listener.prompt` used threshold
  guesses (`_rank >= 25/50/75`) against `get_relationship_rank`'s real scale, which is **-4 to +4**
  (Archnemesis..Lover), not 0-100 — confirmed via live `get_decorators`. The old thresholds could
  never be reached, so the comprehension-chance feature was dead code since it shipped. Rescaled to
  `_rank >= 1/2/3` (Friend/Confidant/Ally-or-better) mapping to the same 8%/20%/35% odds.
- `random < 0.5`-style float comparisons (vibration combat-intensity nudge) assumed a 0-1 float;
  the real `random` decorator returns an **integer 0-100**, confirmed live. Rescaled to
  `random < 50` in both `0761_vibrator_remote.prompt` variants (also fixed there, see
  `world-setting-medium`/`world-setting-hard` 3.1.1).
- Everything else checked against the newly-connected live MCP came back clean: `vrtedd_*` calls
  fail soft (render as `{}`, guard pattern works as designed) whether or not the third-party addon
  is loaded, `append`/`join`/`contains`/`isString` all confirmed real and working, `is_in_faction`
  and `is_in_combat` both confirmed real.

## [2.2.0] - Unreleased

### Added
- `ActivateVibratorOnActor`'s `vibStrength` and `duration` are now dynamic
  parameters the LLM picks per call (DD's real 1-5 scale, plus a seconds
  duration) instead of a hardcoded 4/60s — the action description points at
  `0761_vibrator_remote.prompt` for guidance on what each level should mean.
  An intensity-ladder (separate Increase/DecreaseVibrator actions) was
  considered and rejected: there's no readback of the toy's current running
  strength, so a relative stepper would have no state to step from. Absolute
  per-call control avoids that problem entirely.
- `0761_vibrator_remote.prompt` (both variants) deepened:
  - Narration now names the specific worn device(s) — vaginal plug, anal
    plug, nipple piercings, vaginal piercings — independently, though the
    underlying `VibrateEffectAsync` call is actor-wide with no per-device
    slot, so "multi-toy targeting" is narrative accuracy only, not
    mechanical dispatch. Documented as a real constraint, not glossed over.
  - Edge-count tracking: scans event history for prior remote presses this
    session and lets dialogue reference the escalating count.
  - Orgasm-as-payoff guidance: when `teaseOnly:false` lands, the acting NPC
    is told to narrate the payoff inline, since nothing else reacts to it
    automatically. A real cross-NPC "everyone reacts independently" version
    would need a confirmed orgasm-completion mod-event from DD/zadLibs —
    not confirmed live, flagged in `mod-dev/IDEAS.md` rather than guessed at.
  - Public-vs-hidden tension: bystander NPCs (not the one who last pressed
    the remote) get their awareness gated by `vrtedd_worn_visible`.
  - Faction-flavored captor tone: predator factions (Bandit/Forsworn/
    Warlock/Vampire, matching the factions already used for BDSMLOCK
    spoils-of-war elsewhere) get distinct captor-not-partner guidance via
    `is_in_faction`.
  - Combat-linked intensity: `is_in_combat` gates an RNG-weighted (50%)
    suggestion to escalate strength when she's mid-fight, so it doesn't fire
    every combat turn. Finer running/walking/sitting granularity was
    requested but deferred — no movement-state decorator is confirmed to
    exist yet (see `mod-dev/IDEAS.md`).

### Changed
- `is_in_combat(player.UUID)` and the event-history "press" detection are
  both unverified against live MCP — flagged in the file's own header
  comment, not just here.

## [2.1.0] - Unreleased

### Added
- `gagged_speech` deepened: gag narration is now tiered instead of one flat
  "muffled struggle" — differentiates hood-only vs gag-only vs gag+hood
  layered (max helplessness), flavors the gag-only case by device name via
  `vrtedd_gag_name` (ring/ball/muzzle/panel/harness-style heuristics), and
  escalates the description the longer a gag has been locked (derived from
  the existing `SkyrimNetDDUDNG_Event` lock event's timestamp).
- Blind+gag sensory stacking: when `vrtedd_blind` and a gag are both active,
  listener guidance now notes eye contact is also gone.
- New deaf-player handling: when `vrtedd_deaf` is active, listener guidance
  tells the responding NPC to get her attention physically first instead of
  assuming normal comprehension.
- New relationship-scaled comprehension chance: NPCs with a high
  `get_relationship_rank` toward the player get a weighted `random` roll
  (0%/8%/20%/35% by rank tier) each render; only a passed roll renders the
  "caught a fragment" prose, so this is real RNG deciding when the
  plausible outcome gets to happen, not prose asking the model to act
  "rare." A mage/spellcaster comprehension bonus was considered but
  deferred (see `mod-dev/IDEAS.md`) pending a confirmed detection
  mechanism — it should use the same weighted-roll shape when it lands.
- `event_history.prompt`/`event_history_compact.prompt`: the gagged-speaker
  muffling substitution is generalized from "only the player" to any gagged
  NPC speaker, for background multi-NPC gagged scenes.
- New `mod-dev/IDEAS.md` backlog doc capturing the fuller gagged-speech and
  vibration brainstorm this round drew from.

### Fixed
- The gag-lock trigger only fired its one-time handling beat on
  `str_arg contains "Gag"` — a hood-only lock never got it. Added a sibling
  trigger (`hood_just_locked.yaml`) matching hood locks the same way.

### Changed
- Renamed the gag-lock trigger file and its internal `name:` field from
  `nefaram_gag_just_locked` to `gag_just_locked` — leftover branding from
  before this repo's NEFARAM-name purge, missed at the time. No behavior
  change from the rename itself.

## [2.0.0] - Unreleased

### Changed (BREAKING)
- This package's scope grew from "BDSMLOCK + vibrator fix" to the one mechanics
  package. `includes:` gained `gagged_speech` and the new `vrtedd_worn_truth`
  component — `mo2_mod_name`/slug are unchanged, so this upgrades in place for
  existing installs (same MO2 mod folder, no manual reinstall needed).
- The standalone `gagged-speech` package is **retired** as of this version.
  Its component now lives here permanently. Anyone with the standalone
  gagged-speech package installed should remove it and install this package
  instead — see `packages/gagged-speech/CHANGELOG.md` for the closing note.

### Added
- `vrtedd_worn_truth` component (`0722_worn_truth.prompt`): a worn-device
  physics ground-truth sheet for the player — gag/blind/deaf/restraint state
  plus a positive-phrased "just came free" push for a few renders after a
  device is removed. Powered by decorators (`vrtedd_worn_devices`,
  `vrtedd_gag_name`, `vrtedd_blind`, `vrtedd_deaf`, `vrtedd_all_bound`/
  `_arms_bound`/`_legs_bound`, and their recovery-countdown counterparts)
  registered by a separate third-party mod, "DD SkyrimNet AddOn" — **new
  external requirement**, its Base component with ESP ticked, or this
  section renders nothing (silently; nothing else in the package is
  affected). Ported from that addon's own NPC-facing pattern, retargeted
  from `npc.UUID` to `player.UUID`, consolidated into one file since we
  don't need that addon's FOMOD-style granular install choice for our own
  always-on package.
- This is deliberately kept **functionality-only, no tone** — physics moved
  out of the World Setting tone packages (see their own 2.0.0 changelogs)
  specifically so tone stays swappable/editable independent of ground truth.

## [1.0.1] - Unreleased

### Changed
- Docs only: clarified that World Setting Medium/Hard (2.0.0+) require this
  package as a separate companion install rather than bundling it — see
  those packages' own changelogs for the corresponding breaking change.

## [1.0.0] - Unreleased

### Added
- Initial port into the mod-dev monorepo. Combines what was previously the
  standalone BDSMLOCK selector-prompt fix and the vibrator-remote fix into
  one logic-only package (`components/bdsmlock_vibrations_fix/`), renamed
  `BDSMLOCK_and_VIBRATIONS_Fix` to reflect the combined scope.
- No world/personality prompt content — this package is meant to sit under
  any personality prompt (including NEFARAM World Setting, which now
  includes it as a shared component instead of a hand-copied duplicate).
- `native_action_selector.prompt` ships in this package's own `overlay/`
  (Medium's tone) rather than the shared component — porting the Hard
  variant showed the two real World Setting variants' selector prompts
  genuinely disagree on when BDSMLOCK should fire, so only the drilldown
  and the two vibrator action YAMLs are truly selector-tone-neutral and
  shared. If your own personality prompt wants different lock pacing than
  this default, swap this one file.
