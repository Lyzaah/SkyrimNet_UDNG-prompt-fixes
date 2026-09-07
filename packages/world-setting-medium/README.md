# World Setting — Medium

Drop-in MO2 overlay. **Devices actually equip.** The world is not a 24/7 meat market.

This package is the **world/personality narrative layer only** — setting greenlight, gendered speech tone, device-awareness, BDSMLOCK/vibrator-remote/arrest instruction blocks, and its own tone-specific action-selector prompt. Same narrative machinery family as Hard. Softer **when**.

This is a universal SkyrimNet + Devious Devices tool — it doesn't assume any particular modlist. (Formerly named "NEFARAM World Setting - Medium"; renamed because most people running this don't run that specific modlist.)

**This does not work standalone.** It requires [`bdsmlock-and-vibrations-fix`](../bdsmlock-and-vibrations-fix/) **2.0.0+** installed alongside it — as of that version, the Fix package is the one mechanics package: BDSMLOCK-drilldown, the vibrator remote, gagged/hooded player speech, *and* worn-device physics (what's actually on her body right now) all live there. This package owns none of that anymore — it only reacts to it.

If you want everything combined into a single zip instead of managing two mods, install [`world-setting-medium-aio`](../world-setting-medium-aio/) instead of this package — same content, pre-bundled for convenience.

See [`docs/ENGINE_NOTES.md`](../../docs/ENGINE_NOTES.md) for the underlying merge mechanics, decorator gotchas, and DD keyword map.

## What you should feel

- **Camilla / innkeepers / quest NPCs:** do their jobs. May notice gear you already wear. Will **not** lock from hello. If you *ask* and they agree, they still fire `BDSMLOCK`.
- **Bandits / forsworn / warlocks / vampires / hostiles:** after the fight, they may lock **one** empty slot as spoils, with a reason, out loud.
- **Guards:** real arrest only, not street sarcasm. `RestrainNPC` is never used on the player.
- **Already gagged/blind/deaf/bound** (physics from `bdsmlock-and-vibrations-fix` 2.0.0+): NPCs know, they do not understand her, they do not restack a worn slot, and they stop narrating her as still-restrained a few turns after a device actually comes off. As of the Fix's 2.1.0, gagged narration is also tiered by device/layering, escalates with time-locked, and a close NPC gets a real (weighted, not guaranteed) chance to catch a fragment.
- **Remote** (needs `bdsmlock-and-vibrations-fix` 2.2.0+): `ActivateVibratorOnActor` on DD NG (`zadLibs.VibrateEffectAsync`). Needs a plug/piercing already on. LLM sends `Actor` + `teaseOnly` + `vibStrength` (DD's real 1-5 scale) + `duration` — strength/duration are picked per press now, not fixed. Also aware of edge-count, who's nearby and whether they'd actually notice, and escalates (sometimes) if she's mid-fight.

## Install

This is a 2-mod stack, not one zip:

1. Install **[`bdsmlock-and-vibrations-fix`](../bdsmlock-and-vibrations-fix/) 2.0.0+** — required. This narrative layer's instructions (fire BDSMLOCK, use the remote, react to gagged/blind/bound state) do nothing without it.
2. If you want the worn-device physics section to actually render, also install the third-party **DD SkyrimNet AddOn** (Base component, ESP ticked) — see the Fix package's own README for details. Without it, everything else here still works; NPCs just won't get the physics ground-truth sheet to react to.
3. Install **this package** (`world-setting-medium`). Put it **above** `bdsmlock-and-vibrations-fix` and above `SkyrimNet_b24` in the left pane, so its own `native_action_selector.prompt` wins the file-path fight over the Fix's default copy.
4. **Disable** `world-setting-hard` if it is on. Same filenames — highest left-pane wins the whole file, they will fight.
5. Disable **Skyrim selfparody** if you have it.
6. UDNG MCM: NPC can equip devices on the player = ON.
7. **Restart the game.**

## Do not also enable

`world-setting-hard`, or the [`world-setting-medium-aio`](../world-setting-medium-aio/) convenience bundle at the same time as this package + the Fix installed separately — pick the 2-mod stack *or* the AIO, not both (same filenames, they'll fight for no benefit).

## What this package contains vs. what it needs alongside it

| Piece | Where it lives |
|---|---|
| Setting greenlight, gendered speech tone, device-awareness narrative, BDSMLOCK/vibrator/arrest instruction blocks, this variant's own `native_action_selector.prompt` | **in this package** — component `world_setting_medium_narrative` |
| Worn-device physics (what's actually on her body, right now) | **required companion** — [`bdsmlock-and-vibrations-fix`](../bdsmlock-and-vibrations-fix/) 2.0.0+, component `vrtedd_worn_truth`, powered by a third-party addon's decorators |
| BDSMLOCK drilldown, vibrator remote, gagged/hooded player speech | **required companion** — [`bdsmlock-and-vibrations-fix`](../bdsmlock-and-vibrations-fix/) 2.0.0+, install separately |

`native_action_selector.prompt` is **not** shared with Hard, or with the Fix package's own default copy — porting both World Setting variants into this repo showed their selector prompts genuinely disagree on *when* BDSMLOCK should fire (Medium: "never a random greeting or a quest hello"; Hard: locking is "ordinary manners... not too dramatic"). This package's copy must win the left-pane fight for Medium's tone to actually apply.

This package's own `0720_player_devices.prompt` assumes the Fix package's physics section already rendered ground truth elsewhere in the prompt tree — it reacts to that, it does not re-derive it (Jinja variables don't carry across separately-rendered `.prompt` files, so its local `worn_has_keyword` checks are for its own tone branches only, not a second copy of ground truth).

## Version

**3.1.0** — `0761_vibrator_remote.prompt` deepened: multi-toy narration, edge-count tracking,
orgasm-as-payoff guidance, public-vs-hidden bystander awareness, predator-faction captor tone, and
an RNG-gated combat-intensity nudge. Requires `bdsmlock-and-vibrations-fix` **2.2.0+** for the
dynamic `vibStrength`/`duration` params this guidance now assumes (older 2.0.0+ Fix installs still
work, just against the previous fixed-strength behavior). See CHANGELOG.md.

**3.0.0** — **breaking.** Renamed from "NEFARAM World Setting - Medium" (new MO2 mod folder, not an in-place upgrade). No longer includes the worn-device physics file (`world_setting_shared`/`0722_worn_truth.prompt`) — physics moved entirely into `bdsmlock-and-vibrations-fix` 2.0.0+, which now requires that in turn. See CHANGELOG.md for the full breakdown.

2.0.0 — **breaking.** No longer bundles `bdsmlock-and-vibrations-fix` or `gagged-speech` internally; both were separate companion installs as of this version (gagged-speech has since been folded into the Fix package too, see 3.0.0 above). If you were running the old 1.3.0 all-in-one zip, either install the pieces separately going forward, or switch to [`world-setting-medium-aio`](../world-setting-medium-aio/) for an equivalent single-zip experience.

1.3.0 — ported into the mod-dev monorepo from the original hand-packaged zip, bundled the Fix and gagged-speech internally as shared components.
