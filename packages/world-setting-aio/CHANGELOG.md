# Changelog

All notable changes to this package are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [3.3.10] - 2026-09-07

### Context
- Versions 3.3.7–3.3.10 were published to Discord straight from a hand-edited
  build, never committed to this repo (no git remote exists to have pulled
  them from). This entry ports those real fixes back into `components/` so
  the pipeline is the source of truth again — diffed the published
  `Lyza's SkyrimNet_DDUDNG fixes-v3.3.10.zip` against a fresh build of this
  branch, file by file, and applied every substantive difference below.

### Fixed
- **Material preference never worked.** `native_action_selector_drilldown.prompt`
  read `decnpc(npc.UUID).background` / `.personality` for a stated material
  preference — those fields don't exist on the actor decorator at all, so
  the check silently always came up empty, for every NPC, since this
  feature was first written. Switched to `get_world_knowledge(npc.UUID)`
  (guarded with `isString`), so a per-NPC World Knowledge entry actually
  drives the pick now. New doc: `HOWTO_NPC_PREFERENCES.md` (ships in
  `common/`), also linked from `docs/SkyrimNet-DD-Features.md`.
- **Vibrator remote param order.** All five vibe action YAMLs
  (`vibehornify(long)`, `vibejab`, `vibepunish`, `vibetease`) had the
  dynamic `teaseOnly` param mapped *before* the static `vibStrength`/
  `duration` params instead of after — reordered to match the actual
  `zadLibs.VibrateEffectAsync` call shape.
- **Edge-count crash guard.** `0761_vibrator_remote.prompt` (Hard and
  Medium) called `contains(format_event(event, "compact"), ...)` directly;
  `format_event` can return a non-string for a malformed event, and
  `contains({}, "...")` behaves like the classic `{} != ""` Inja trap.
  Now binds the result to a variable and guards it with `isString()` first.

## [3.3.6] - 2026-09-07

### Fixed
- Experimental plugin's `<image />` in `ModuleConfig.xml` had no `path`
  attribute — Vortex's FOMOD installer throws on a bare `<image />`.
  Now points at `fomod/header.jpg` like every other plugin entry.

## [3.3.5] - 2026-09-02

### Changed
- Shipped `README.md` rewritten from scratch: explains the three actual
  mechanical fixes (occupancy-tracked locking, real-scale vibrator remote,
  structural gagged-speech history rewrite) and why each works, plus the
  optional arousal integration. Dropped the in-README version/changelog
  section and the "Skyrim selfparody" compat callout (kept the same
  same-filename warning without naming that mod). Added a "Suggestion"
  section and a dedicated "Credits" section for naitro2010 and telord.
  `CHANGELOG.md` (this file) remains the real history; it is not shipped
  in the zip (`build.py` skips it).

## [3.3.4] - 2026-09-02

### Changed
- Mod renamed to **Lyza's SkyrimNet_DDUDNG fixes** (`package.yaml` name +
  `mo2_mod_name`, FOMOD `moduleName`, `info.xml` Name). Old name kept as
  "(formerly ...)" in the README for continuity.
- FOMOD `info.xml` `<Website>` now points at the Discord support thread:
  https://discord.com/channels/1287232260617015336/1544716621610877018

### Added
- `Features.md` (copy of `docs/SkyrimNet-DD-Features.md`) now ships in
  `common/` — always installed, sits next to `README.md`.
- New final FOMOD install step ("Finish") reminding the player to open
  `Features.md`, since a declarative FOMOD can't launch a file itself.

## [3.3.3] - 2026-09-02

### Added
- FOMOD hard-requires **SkyrimNet_UDNG** by **naitro2010**
  (`SkyrimNetUDNG.esp` Active). New Requirements-page entry with
  credit, GitHub, and releases links:
  https://github.com/naitro2010/SkyrimNet_UDNG/releases
  The UDNG archive is **not** inside this zip.

## [3.3.2] - 2026-09-02

### Added
- FOMOD hard-requires telord **DD SkyrimNet AddOn V1.1-beta**
  (`DD SN AddOn.esp` Active) plus `Devious Devices - Integration.esm`.
  Discord: https://discord.com/channels/1287232260617015336/1541604450072793139/1543822052899815584
  The addon zip is **not** inside this archive.
- Installer header image (`fomod/header.jpg`).

## [3.3.1] - 2026-09-02

### Added
- FOMOD second page: optional Experimental (`0730`) — SLO arousal
  bands, follower remote if plugged, ungag-to-feed overlap. Off by
  default. Description in the wizard. Needs SLO / SkyrimNet_Arousal
  or the extra file is inert.

## [3.3.0] - 2026-09-02

### Added
- First unified AIO with MO2 FOMOD: radio choice Medium (RP-focused)
  vs Hard (being made a pet). Shared mechanics always install.
- Ungag-to-drink prose no longer says "belt stays" — one ACTION on
  the mouth; invent the rest.
