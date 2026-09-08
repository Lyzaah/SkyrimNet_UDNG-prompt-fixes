# Lyza's SkyrimNet_DDUDNG fixes

A SkyrimNet + Devious Devices prompt overlay. No ESP of its own — it's plain text (`.prompt`/`.yaml`)
that drops on top of your load order and changes how NPCs reason about Devious Devices.

Feedback / support thread: https://discord.com/channels/1287232260617015336/1544716621610877018

Full player-facing feature list ships inside the mod as `Features.md` (next to this file — the
FOMOD's last page reminds you to open it). Same content lives in-repo at
[`docs/SkyrimNet-DD-Features.md`](../../docs/SkyrimNet-DD-Features.md).

Want a specific NPC to actually prefer a material when she locks something on someone? See
`HOWTO_NPC_PREFERENCES.md`, also shipped next to this file.

## What's actually broken, and what this fixes

Stock SkyrimNet talking to SkyrimNet_UDNG *can* lock and unlock Devious Devices, but three things
go wrong in practice, and this overlay is built specifically against those three:

**1. Locking doesn't track what's already worn.** The stock action selector has no real concept of
occupied slots, so an NPC can "lock a gag" on a mouth that already has one, or invent a slot group
that doesn't exist. This overlay splits locking into two passes — a category pick, then a
cheap-model drilldown that maps the intent to one of ~20 real slot groups (gags, collars, hoods,
belts, bras, harnesses, corsets, catsuits, armbinders, elbow ties, butterfly binders, yokes,
straitjackets, arm/leg cuffs, gloves, piercings, plugs, boots) — and only picks an `EQUIP_*` leaf
action if that exact slot reads empty via `worn_has_keyword` right now. Occupancy is read live every
line, not remembered from a diary entry or an old bio note, because those go stale the moment a
device comes off.

**2. The vibrator remote sends nonsense values.** `zadLibs.VibrateEffectAsync` takes a 1–5 strength
scale; a naive integration lets the model send whatever number it wants (`vibStrength: 80`,
`duration: 99999`) or hardcodes one value for every press. This overlay wires the actual DD NG scale,
lets the LLM pick strength/duration per press within it, tracks edge-count from event history so a
tenth press reads different from a first, and gates the whole thing off during combat.

**3. Gagged speech doesn't actually gag anything.** By default, a gagged player's exact typed or
spoken words still show up in what NPCs are told happened, because the mute is cosmetic (TTS/subtitle
only), not structural. SkyrimNet has two separate player-speech paths — open-mic/STT never touches an
LLM at all, so nothing can filter it at the source — and this overlay's actual fix lives downstream:
`event_history` / `event_history_compact` substitute a "muffled struggle" description for
NPC-listener-facing history whenever the speaker is wearing a gag/hood keyword, tiered by device type
and how long it's been locked, with a real weighted-RNG chance for a close relationship to catch a
fragment. Thoughts (`render_mode == "thoughts"`) are explicitly excluded from all of this — a gag
stops the mouth, not the inner monologue.

On top of those three mechanical fixes, a **world-tone layer** decides *when* any of this fires at
all: **Medium** keeps shops, quests, and friendly followers acting like shops, quests, and followers
unless she asked or the NPC is a predator/shady/mid-arrest; **Hard** treats locking an adult woman as
ordinary manners, culture rather than a special occasion. Same occupancy rules, same out-of-combat
gate, same women-only targeting either way — the difference is purely the trigger condition, not the
mechanics underneath.

## Arousal integration (optional)

The base install has **no arousal numbers in the prompt at all** — lock/strip/vibe/ungag work
without any horniness meter. If you're already running **SLO Aroused NG** and **SkyrimNet_Arousal**,
the optional **Experimental** page adds a layer on top: it reads the `sla_Arousal` faction rank and
prints a named band (dry / play-window / already-past-it / gone) so the model has a number to react
to, and lets followers or friends who are close to a plugged-in toy choose to press the remote on
their own — without you asking, weighted toward tease-and-deny. It does not fire `ArousalChange`
itself (`SkyrimNet_Arousal` owns that meter); it only reads it. Off by default, and completely inert
without both of those mods installed.

## What the installer copies

Always installed (`common/`):

| Piece | Role |
|---|---|
| BDSMLOCK selector + drilldown, vibrator remote | Fix #1 and #2 above |
| Gagged speech (history rewrite, listener logic) | Fix #3 above |
| Worn-device physics | Ground-truth "what's on her right now" sheet the other pieces read from |
| Roleplay guidelines | NPC agency framing, SKU-name-to-speech conversion (never TTS an inventory string) |

Then a "Vibrator script" page with one checkbox, greyed out and locked either way — not a real
choice, just a readout of what the installer found:

| State | What it means |
|---|---|
| Checked (locked) | `UnforgivingDevices.esp` — the actual **Unforgiving Devices NG** patch mod by naitro2010, a *different* plugin from `SkyrimNet_UDNG`'s `SkyrimNetUDNG.esp` (already a hard requirement above) — was detected active. The seven vibrator actions call `zadLibs_UDPatch` instead of base `zadLibs`, so pressing the remote actually drives UDNG's own custom vibrator render scripts when she's wearing one of UDNG's custom devices. |
| Unchecked (locked) | `UnforgivingDevices.esp` wasn't detected active. The actions keep calling base `zadLibs` — nothing changes. |

Nothing to click here; the installer decided from what's actually in your load order, because
leaving it as a manual choice was pointless — one answer is always right.

Then **exactly one** world tone:

| Choice | What it changes |
|---|---|
| Medium | RP-focused *when*. A greeting is not a lock. |
| Hard | Being made a pet. Locking is ordinary manners. |

Optional checkbox:

| Choice | What it adds |
|---|---|
| Experimental | Arousal bands + follower/friend remote play, described above. Off by default. |

## Requirements

| Need | Mod | Link |
|---|---|---|
| Game + extender | Skyrim SE/AE + **SKSE** | [skse.silverlock.org](https://skse.silverlock.org/) |
| SKSE address map | **Address Library** | [Nexus 32444](https://www.nexusmods.com/skyrimspecialedition/mods/32444) |
| NPC AI | **SkyrimNet** | [GitHub releases](https://github.com/MinLL/SkyrimNet-GamePlugin/releases) |
| Devices | **Devious Devices SE 5.2** + **DD NG** | [DD SE](https://www.loverslab.com/files/file/5878-devious-devices-se/) · [DD NG](https://www.loverslab.com/files/file/29779-devious-devices-ng/) |
| Lock API | **SkyrimNet_UDNG** by **naitro2010** — ships `SkyrimNetUDNG.esp` | [GitHub](https://github.com/naitro2010/SkyrimNet_UDNG) · [Releases](https://github.com/naitro2010/SkyrimNet_UDNG/releases). **Hard requirement.** Not bundled — FOMOD checks the ESP. |
| Strip | **SexLab Framework SE** | [LoversLab](https://www.loverslab.com/files/category/228-sexlab-framework-se/) |
| Vibrator render scripts (optional) | **Unforgiving Devices NG** by **naitro2010** — ships `UnforgivingDevices.esp`. A *different* mod from SkyrimNet_UDNG above, despite the similar name. | Not bundled, not a hard requirement — the FOMOD's "Vibrator script" page shows a locked checkbox reading whatever it autodetects. |
| Worn-device physics (`vrtedd_*`) | **DD SkyrimNet AddOn V1.1-beta** by **telord** — tick **Base** so `DD SN AddOn.esp` is active | [Discord](https://discord.com/channels/1287232260617015336/1541604450072793139/1543822052899815584). **Hard requirement.** Not bundled — FOMOD checks the ESP. |

Optional, for the pieces described above: [SLO Aroused NG](https://www.nexusmods.com/skyrimspecialedition/mods/65454), [SkyrimNet_Arousal](https://github.com/GoodProvider/SkyrimNet_Arousal) (arousal bands), [SunHelm](https://www.nexusmods.com/skyrimspecialedition/mods/39414) (ungag-to-drink fail-softs to 0 without it), [SeverActions](https://github.com/Severause/SeverActions).

UDNG MCM: NPC can equip devices on the player = ON.

## Install (MO2)

1. Install **SkyrimNet_UDNG** (naitro2010). Enable `SkyrimNetUDNG.esp`.
2. Install **DD_SkyrimNet_AddOn_V1.1-beta.zip** (telord). Enable `DD SN AddOn.esp`.
3. Drop `Lyza's SkyrimNet_DDUDNG fixes-v*.zip` on MO2. The FOMOD wizard should open — it will
   complain if either ESP above is missing.
4. Requirements page: acknowledge both plugins.
5. Vibrator script page: a locked, greyed-out checkbox — checked if it detected
   `UnforgivingDevices.esp` (Unforgiving Devices NG) active, unchecked if not. Nothing to click.
6. World tone page: pick **Medium — RP-focused** or **Hard — being made a pet**.
7. Optional: tick **Experimental** only if you're running SLO Aroused NG + SkyrimNet_Arousal and
   want arousal bands and follower remote play.
8. Last page: a reminder to open `Features.md` (ships in this mod's own folder) for the full
   feature rundown.
9. Enable the mod. Left pane **above** `SkyrimNet_b24`, DDUDNG, VRTE, SKSE Output.
10. Disable any other mod that ships its own `0010_setting.prompt` or an older split
    Hard/Medium/Fix install — same filenames, last one in the left pane wins the whole file.
11. **Restart the game.**

If MO2 installs without showing a wizard, the zip has no `fomod/ModuleConfig.xml` at its root —
re-download. Do not extract by hand unless you copy `common/` plus **one of** `medium/` or `hard/`
(and optionally `experimental/`) into the same Data tree.

## Suggestion

Start with **Medium**, no Experimental — it's the tone this overlay was tuned against and it plays
fine without touching your existing shops-and-quests roleplay. Turn **Experimental** on only once
you're already running SLO Aroused NG + SkyrimNet_Arousal for other reasons; it adds nothing on its
own. Switch to **Hard** once you know you want locking to be ambient rather than occasional — it's a
different *when*, not a different mechanic, so nothing about occupancy, combat-gating, or the remote
changes when you do.

## Credits

- **naitro2010** — [SkyrimNet_UDNG](https://github.com/naitro2010/SkyrimNet_UDNG), the lock/unlock
  Papyrus and mod-event this whole overlay is built against. Hard requirement, not bundled. Also
  supplied the working UDNG-compatible vibrator action definitions the "UDNG-patched" install
  choice is based on.
- **telord** — DD SkyrimNet AddOn, the worn-device physics decorators. Hard requirement, not bundled.
