# SkyrimNet engine notes

Reusable mechanics and gotchas for anyone building Devious Devices prompt/trigger/action
content against SkyrimNet. This is reference material, not a changelog — package READMEs
link here instead of re-explaining the engine each time.

See also SkyrimNet's own modding documentation for the general Prompts/Triggers/Actions/Mod
Integration workflow this repo builds on top of.

## The "two mouths" — why gagged speech works the way it does

SkyrimNet does **not** send every player line through an LLM:

| How the player talks | Event type | Hits a prompt? | What TTS speaks |
|---|---|---|---|
| Open mic / STT | `dialogue_player_stt` | **No** | Raw transcript, unmuffleable by any prompt |
| F1 text input, F7 Voice Dialogue Transform, chat `/transform` | `dialogue_player_text` → transform | **Yes** — `player_dialogue.prompt`, `render_mode == "transform"` | Whatever the LLM returns |
| Chat `/think` (`~`) | thoughts | No — and must never be gagged | Nothing (internal) |

Since open-mic can't be touched at the source, the only lever is hiding the transcript from
**NPC-facing** event history: `event_history.prompt` / `event_history_compact.prompt` check
`not is_player(npc.UUID)` (the listener) plus a gag keyword on the speaker, and if both are
true, substitute a "muffled struggle" description instead of printing the actual STT/typed
words. That's the real fix — not a keyword filter on the transcript itself. Thoughts
(`render_mode == "thoughts"`) must always stay excluded from any gag logic — a gagged
character still thinks in full sentences.

## Key native decorators/functions

- `worn_has_keyword(uuid, "KeywordEditorID")` — boolean, native, not a Papyrus round-trip.
  **Gotcha:** never test a Papyrus-backed decorator with `!= ""`. An empty Papyrus return
  comes back as JSON `{}`, and `{} != ""` evaluates true — so the block fires on *everyone*.
  Guard with `isString(x) and x != ""`.
- `is_player(npc.UUID)` — correct player-check; never compare UUID strings manually.
- `is_hostile_to_actor(a, b)`, `is_in_faction(uuid, "FactionEditorID")`, `is_in_combat(uuid)`,
  `is_guard_or_authority(uuid)`, `get_relationship_rank(a, b)`.
- `random` — a bare context value (not a function call), re-rolled per render. **Integer
  0–100 inclusive, not a 0–1 float.** Write thresholds as plain percentages: `random < 50`
  for 50%, `random < 35` for 35%. Wherever a prompt uses prose to ask the model to act
  "rarely" or "sometimes" — prose standing in for a probability slider — replace it with an
  actual `random < weight` roll instead; the prose still describes what a *passed* roll looks
  like, the roll decides whether that prose renders at all.
- `get_relationship_rank(a, b)` — returns **-4 to +4**, not 0–100. Named levels: 4=Lover,
  3=Ally, 2=Confidant, 1=Friend, 0=Acquaintance, -1=Rival, -2=Foe, -3=Enemy, -4=Archnemesis.
  Returns 0 if no relationship exists.
- `get_recent_events(count, entityUUIDs)`'s second argument must be a bare UUID or a
  variable holding an array — never an inline array literal wrapping an identifier, like
  `[npc.UUID]`. That exact shape fails to *parse* (not just "returns empty") and breaks
  every render of the file containing it. A multi-UUID filter must be built as a variable
  first: `{% set f = [] %}{% set f = append(f, x) %}` ... `get_recent_events(n, f)`.
- `append(arr, x)` / `join(arr, sep)` / `contains(container, x)` / `isString(x)` — all real
  template-engine base functions, not SkyrimNet-registered decorators, so they won't appear
  in a decorator dump. Absence from a decorator listing is not proof of non-existence for
  base functions — only actually rendering/validating a template proves real behavior.
- No movement-state decorator (running/walking/sneaking/sitting) is confirmed anywhere.
  Only `is_in_combat` is reliable for activity-based gating. An unrecognized *native*
  decorator name can hard-error rather than silently no-op — don't guess a name into a
  shipped file, look it up first.
- `is_narration_enabled()` — gates whether asterisk-narration output is allowed at all
  (falls back to "one short muffled sound, no words" when off).
- `get_recent_events(n, [uuids])`, `format_event(event, "compact"|"verbose"|"recent_events")`,
  `get_event_history_count(uuid)`. `format_event` can return a non-string for a malformed
  event — guard with `isString()` before passing its result to `contains()`.
- `decnpc(uuid).isFemale / .isChild / .isVirtualPrivate / .isDead`, `is_summoned(uuid)`,
  `is_reanimated(uuid)`, `units_to_meters(dist)`, `get_name(uuid)`, `get_location(uuid)`,
  `short_time(str)`. Note: `decnpc()` does **not** expose bio text (`.background`,
  `.personality` don't exist) — for a stated NPC fact/preference, use
  `get_world_knowledge(uuid)` instead.
- `embed_actions_in_dialogue` + `eligible_actions` (array) — the guard every
  action-embedding instruction block checks (`length(eligible_actions) > 0`) before
  rendering at all.

## Arousal — SLO Aroused NG + SkyrimNet_Arousal (do not dump numbers)

A raw 0–100 arousal number without a gated behavior is noise — don't print it at the LLM.

**Who owns what:**

| Piece | Job |
|---|---|
| SLO Aroused NG | Source of truth. Writes `sla_Arousal` faction rank 0–100. Ships `SexLabAroused.esm`. |
| SkyrimNet_Arousal | Adaptor. Bio block (`short_inline` only) + Papyrus action `ArousalChange`. |
| SkyrimNetArousalBridge | Triggers on the SLO arousal-updated mod events. |

`ArousalChange` is **the speaker's** arousal, not the player's — don't teach it in your own
selectors/actions, the adaptor already registers it. Don't overlay `SkyrimNet_Arousal`'s own
bio prompt file.

Read it live: `get_faction_rank(uuid, "sla_Arousal")` — integer 0–100, `-1` = untracked (not
in the faction). Do **not** use `get_arousal_state(uuid)` — that's a different decorator
talking to the OSL Aroused DLL, which SLO NG doesn't implement; it returns
`{"available":false,...}` and missing keys render as unexpanded `{{ a.arousal }}`.

If you gate *behavior* on arousal (cold NPCs don't take liberties, hot ones do): snapshot
`get_faction_rank` once per render and **omit** the relevant prose unless the band matches.
Don't dump the number, and don't write an elaborate scripted reaction ladder — one gated
paragraph beats an 8-beat scripted escalation.

Suggested bands (print the rank *inside* the band, omit the whole block under 20): 0 dry →
20–39 warming → 40–59 deep in the window → 60–69 too late to play it cool → 70–89 far gone →
90–100 gone. 20–60 is the useful "magic" range for gating extra prose.

Ungag-to-drink/feed pattern: SunHelm's `get_global_value("_SHCurrentThirstLevel")` /
`"_SHCurrentHungerLevel"` are floats, higher = worse, gate at ≥ 70. (SexLab Survival's
`sever_hunger` is a different, unrelated meter — don't use it here.)

## Devious Devices NG keyword map (confirmed `zad_*` slot keywords)

| Slot | Keyword(s) |
|---|---|
| Mouth | `zad_DeviousGag`, `zbfWornGag` (ZaZ) |
| Head/eyes | `zad_DeviousHood`, `zad_DeviousBlindfold` |
| Neck | `zad_DeviousCollar` |
| Chastity (cunt) | `zad_DeviousBelt` |
| Chastity (chest) | `zad_DeviousBra` |
| Feet | `zad_DeviousBoots` |
| Internal | `zad_DeviousPlugVaginal`, `zad_DeviousPlugAnal` |
| Piercings | `zad_DeviousPiercingsNipple`, `zad_DeviousPiercingsVaginal` |
| Torso | `zad_DeviousHarness`, `zad_DeviousCorset` |
| Hands/arms (one group) | `zad_DeviousArmbinder`, `zad_DeviousYoke`, `zad_DeviousHeavyBondage`, `zad_DeviousElbowTie`, `zad_DeviousArmbinderElbow`, `zad_DeviousButterfly`, `zad_DeviousStraitJacket` |
| Arm cuffs | `zad_DeviousCuffs` / `zad_DeviousArmCuffs` / `zad_DeviousCuffsFront` |
| Leg cuffs | `zad_DeviousLegCuffs` / `zad_DeviousAnkleShackles` — **there is no separate "ankle shackles" group, it's LEG_CUFFS** |
| Gloves | `zad_DeviousGloves`, `zad_DeviousBondageMittens` |
| Full-body | `zad_DeviousSuit`, `zad_DeviousPetSuit` |
| Catch-all | `zad_Lockable` (has *any* lockable DD item) |

## BDSMLOCK: the two-tier category/drilldown action pattern

`BDSMLOCK` is a native category action:

1. **First pass** (an `native_action_selector.prompt`-style file): the LLM picks category
   `BDSMLOCK` and must output `PARAMS: {"intent": "<slot word> <target name>"}` — `intent`
   is the *only* allowed key; extra keys make it fail silently.
2. **Drilldown pass** (a second, cheaper-model prompt): maps the intent text to one fixed
   slot-group token — `GAGS, COLLARS, HOODS, BLINDFOLDS, BOOTS, PLUGS, PIERCINGS,
   CHASTITY_BRAS, CHASTITY_BELTS, HARNESSES, SUITS, ARMBINDERS, ELBOW_BINDERS,
   BUTTERFLY_BINDERS, YOKES, ARM_CUFFS, LEG_CUFFS, GLOVES, CORSETS, STRAITJACKETS` (no
   `ANKLE_SHACKLES` — that's `LEG_CUFFS`) — then, only if that slot reads empty via
   `worn_has_keyword` occupancy, picks one specific `EQUIP_*` leaf action, filling `target`
   with the target's exact display name.
3. **Occupancy is physics, not memory.** Every layer (bio, dialogue guidance, action
   selector, drilldown) independently recomputes "what's worn right now" from
   `worn_has_keyword` — old memories/diaries/bios claiming a slot is worn/free are stale
   and must be ignored in favor of the live check. Never restack an occupied slot. Never
   lock a child.

The vibrator remote is a companion custom action (not BDSMLOCK, no `intent`):
`ActivateVibratorOnActor` — `questEditorId: zadQuest`, `scriptName: zadLibs`,
`executionFunctionName: VibrateEffectAsync` — dynamic `Actor` + `teaseOnly` (edge vs.
finish) + dynamic `vibStrength` (DD scale is **1–5, not 1–100**) and `duration` (seconds),
each picked by the LLM per call. Needs a plug/piercing already worn; does not equip
anything. `TurnOffVibrators` is the same quest/script with `executionFunctionName:
StopVibrating`.

**Hard constraint:** `VibrateEffectAsync` takes exactly one `Actor` param — there's no
per-device-slot parameter. Pressing the remote buzzes *everything* currently active on that
actor at once; there's no way to fire just the plug and leave nipple piercings alone, and no
confirmed way to read back a toy's current running strength (so a relative +/- stepper has
nothing to step from). Absolute per-call control (`vibStrength`/`duration` above) sidesteps
both problems. "Multi-toy targeting" in the prompt layer is narrative-accuracy only (name
what's actually worn), never real per-device dispatch — the mechanism can't do that.

Occasional PARAMS corruption (a corrupted numeric field, or stray unrelated tokens leaking
into a value) has been observed across models/providers and currently kills the whole PARAMS
object if it hits a required field. Mitigation: keep `vibStrength`/`duration` genuinely
optional in the action YAML with sane defaults, and only instruct the model to fill them in
when the scene clearly calls for a specific number — this reduces how often the model
generates a number at all, which reduces exposure. It doesn't fix the root cause (that looks
like an inference/routing-layer issue, not something fixable from prompt wording).

## Arrest wiring

`RestrainNPC` **cannot target the player** (fails silently, only finds other NPCs) — the
player-arrest path is `AddBountyToPlayer` → `ArrestPlayer` (or the `Arrest` category with
`{"intent": "..."}` if no bounty exists yet), never `RestrainNPC` / `KidnapNPC` / `ArrestNPC`
on the player.

## "Predator" faction IDs

Used to detect bandits/hostiles who may lock devices as spoils after a fight:
`BanditFaction`, `BanditFriendFaction`, `ForswornFaction`, `WarlockFaction`, `VampireFaction`.

## Third-party worn-device-physics decorators (`vrtedd_*`)

A third-party addon ("DD SkyrimNet AddOn") registers a family of decorators for worn-device
ground truth, always guarded `isString(x) and x != ""` (Papyrus-backed, fails soft to `{}`):

- `vrtedd_worn_devices(uuid)` / the individual bound/blind/deaf flags — the physics sheet:
  what's actually on someone right now.
- `vrtedd_gag_name(uuid)` — flavors muffled-speech narration by device (ring/ball/muzzle/
  panel/harness-style), matched by a lowercased name-string heuristic — best-effort, not a
  real keyword classification, since no `zad_*` keyword distinguishes gag sub-types.
- `vrtedd_blind(uuid)` / `vrtedd_deaf(uuid)` — sensory-stacking (blind+gag) and
  deaf-listener handling.
- `vrtedd_worn_visible(uuid)` (layer-filtered onlooker view) — public-vs-hidden bystander
  logic for things like the vibrator remote.

## `responseTarget` — who a line is actually addressed to

The context object `responseTarget` (with `.UUID`, same shape as `player`/`npc`) holds
whoever the CURRENT dialogue line is addressed to — not always the player. `player` is
always the real player character regardless of who's talking to whom; `npc` is always the
current speaker. Guard access with `exists("responseTarget") and existsIn(responseTarget,
"UUID")` before reading it.

This matters for any action that targets a specific actor (locking, unlocking, vibrating):
compute a target once, near the top of the file, rather than hardcoding the player:

```
{% set _lockTargetUUID = player.UUID %}
{% set _lockTargetName = player_name %}
{% set _lockWomenOnly = decnpc(player.UUID).isFemale %}
{% if exists("responseTarget") and existsIn(responseTarget, "UUID") and responseTarget.UUID != player.UUID %}
{% if decnpc(responseTarget.UUID).isFemale %}
{% set _lockTargetUUID = responseTarget.UUID %}
{% set _lockTargetName = responseTarget.name %}
{% set _lockWomenOnly = true %}
{% else %}
{% set _lockWomenOnly = false %}
{% endif %}
{% endif %}
```

Then use `_lockTargetUUID` everywhere occupancy was hardcoded to `player.UUID` (all the
`worn_has_keyword` checks, the child guard, any press-history/visibility/combat tracking),
and `_lockTargetName` everywhere prose named the player directly. This makes the whole
lock/unlock/vibrate apparatus correct for both the player and whichever NPC is actually
being addressed, and a male addressee correctly does **not** fall back onto locking the
player instead.