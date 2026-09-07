# Lyza's SkyrimNet_DDUDNG fixes

Devious Devices prompt/trigger/action overlays for **[SkyrimNet](https://github.com/MinLL/SkyrimNet-GamePlugin)**. 

No ESP, no Papyrus of its own — plain text (`.prompt` / `.yaml`) that drops into your MO2/Vortex load order and teaches NPCs to actually *use* the Devious Devices already installed, instead of just talking about them.

## ✨ What it actually does

- 🔒 **Real locking, real occupancy.** NPCs check what's actually worn — live, every single line — before locking anything. No phantom gag, no second collar stacked on an already-occupied slot.
- 🙊 **Gagged speech that's actually enforced.** Not cosmetic muting — NPCs perceive a muffled struggle, not your real words, tiered by device (ring / ball / muzzle / panel / hood) and how long it's been locked.
- 📳 **A vibrator remote with a real scale.** Devious Devices' actual 1–5 strength range, picked per press by the NPC, with memory of how many times it's already been pressed — not a fixed buzz or an invented 1–100 number.
- 🙆 **Arms first, then clothes.** Free hands get bound behind the back before anything comes off. Hands already bound → stripped instead. Never both at once, never in the wrong order.
- 🚺 **Women only, always.** Male NPCs are never a lock target — no exceptions, no falling back onto the player.
- ⚔️ **Out of combat, always.** Every lock / strip / vibe / ungag instruction is structurally omitted the moment anyone's fighting. Talk mid-fight is fine — the kit just stays holstered until it's over.
- 🎭 **Two tones, one install.** Pick **Medium** (shops and quests stay shops and quests, unless she asked or the NPC's a predator) or **Hard** (locking is just how this world works) — same mechanics underneath either way.
- 💧 **Ungag to drink.** A follower who can see she's parched notices the gag is in the way — she never has to ask for it.
- 🎯 **NPCs can have an actual material preference.** Set one up once and she'll reach for cold ebonite or steel instead of a random pick every time — see [`docs/HOWTO_NPC_PREFERENCES.md`](docs/HOWTO_NPC_PREFERENCES.md).
- 🔥 **Optional arousal integration.** Off by default — flip it on if you're already running SLO Aroused NG + SkyrimNet_Arousal, and followers may start pressing the remote on their own.

Full writeup: [`docs/SkyrimNet-DD-Features.md`](docs/SkyrimNet-DD-Features.md).

## 📦 What's in this repo

| Package | What it is |
|---|---|
| [`world-setting-aio`](packages/world-setting-aio/) | **Start here.** One FOMOD zip — pick Medium or Hard at install, plus an optional Experimental page. |
| [`bdsmlock-and-vibrations-fix`](packages/bdsmlock-and-vibrations-fix/) | Core mechanics only: locking, the remote, gagged speech, worn-device physics. No tone/personality of its own. |
| [`world-setting-medium`](packages/world-setting-medium/) / [`world-setting-hard`](packages/world-setting-hard/) | Tone-only overlays, for anyone who'd rather install the Fix and the tone separately. |
| [`world-setting-medium-aio`](packages/world-setting-medium-aio/) / [`world-setting-hard-aio`](packages/world-setting-hard-aio/) | Older single-tone convenience bundles, superseded by `world-setting-aio`'s FOMOD — kept for anyone already using them. |
| [`kink-experimental`](packages/kink-experimental/) | The arousal-integration overlay as its own zip (also available as a checkbox inside the AIO installer). |
| [`gagged-speech`](packages/gagged-speech/) | Retired — folded permanently into `bdsmlock-and-vibrations-fix`. Kept for history. |

`components/` is shared source: every package above composes its zip from pieces in there, so a fix made once is a fix made everywhere that piece is used. Each package's own README has its exact requirements and install steps.

## 🔨 Build it yourself

Ready-made zips are on the [Releases page](../../releases) — grab one and drop it in MO2/Vortex, no Python needed. If you'd rather build from source (testing a change, or just don't want to wait for a release):

```bash
pip install --user pyyaml
python3 scripts/package_zip.py world-setting-aio   # or any other package slug, or --all
```

Drops a ready-to-install MO2 mod folder in `dist/<slug>-v<version>/` and a zip in `dist/zips/`.

## 📋 Requirements

Every package needs 
- [SkyrimNet](https://github.com/MinLL/SkyrimNet-GamePlugin/releases)
- [Devious Devices NG](https://www.loverslab.com/files/file/29779-devious-devices-ng/). 
- [**SkyrimNet_UDNG**](https://github.com/naitro2010/SkyrimNet_UDNG) by **naitro2010** — the lock/unlock Papyrus this overlay is built against
- [Devious Device type awareness AND reminder for NPC](https://discord.com/channels/1287232260617015336/1541604450072793139/1543822052899815584) by **telord** — the worn-device physics decorators
- Optional: [Unforgiving Devices](https://www.loverslab.com/files/file/41829-unforgiving-devices/) enables NPC struggling and other nice immersive stuff

Full requirement tables (with versions and links) and install order live in each package's own README — start with [`packages/world-setting-aio/README.md`](packages/world-setting-aio/README.md).

## 📖 Docs

- [`docs/SkyrimNet-DD-Features.md`](docs/SkyrimNet-DD-Features.md) — the full player-facing feature writeup
- [`docs/HOWTO_NPC_PREFERENCES.md`](docs/HOWTO_NPC_PREFERENCES.md) — give a specific NPC a stated material preference
- [`docs/ENGINE_NOTES.md`](docs/ENGINE_NOTES.md) — SkyrimNet engine mechanics and gotchas, for anyone building their own prompt/trigger/action content

## 🙏 Credits

- **naitro2010** — [SkyrimNet_UDNG](https://github.com/naitro2010/SkyrimNet_UDNG)
- **telord** — [Devious Device type awareness AND reminder for NPC](https://discord.com/channels/1287232260617015336/1541604450072793139/1543822052899815584)

## 💬 Feedback

[Discord thread](https://discord.com/channels/1287232260617015336/1544716621610877018)
