# Changelog

All notable changes to this package are documented here.
Format loosely follows [Keep a Changelog](https://keepachangelog.com/).

## [RETIRED] - Unreleased

This standalone package is retired. Its component (`components/gagged_speech/`, unchanged) now
ships permanently inside [`bdsmlock-and-vibrations-fix`](../bdsmlock-and-vibrations-fix/) 2.0.0+,
which became the one mechanics package (BDSMLOCK, vibrator remote, gagged-speech, and worn-device
physics together). No further versions of this standalone package will be built or tagged.

If you have this package installed on its own: remove it and install
`bdsmlock-and-vibrations-fix` 2.0.0+ instead — it's not an optional add-on to that package
anymore, its content is bundled in. Nothing else in this package's behavior changed; only where
it ships from did.

## [1.1.1] - Unreleased

### Changed
- Docs only: clarified pairing with World Setting Medium/Hard now that
  neither bundles this package internally (Medium used to, as of its 2.0.0
  it no longer does) — see the new AIO packages if you want a pre-combined
  convenience zip instead.

## [1.1.0] - Unreleased

### Changed
- Ported into the mod-dev monorepo. No content changes from the original
  shipped `05 SkyrimNet Gagged Speech.zip` — verified byte-identical via
  `diff -r` against the extracted original after build.
- Content now lives in shared component `components/gagged_speech/`, the
  same source that `world-setting-medium`/`world-setting-hard` pull in, so
  the two copies that used to drift independently are now one file each.
