# SkyrimNet × Devious Devices — What You're Actually Getting

*Every NPC in your game just got a mouth, a memory, and a key. Here's what happens when you hand them all three.*

This is the player-facing feature list for **Lyza's SkyrimNet_DDUDNG fixes** (formerly "World Setting AIO"). Mechanics match the live prompts, not older marketing.

Feedback / support thread: https://discord.com/channels/1287232260617015336/1544716621610877018

---

## Gagged Speech — Your Mouth Isn't Yours Anymore

Stuff a gag in and the AI doesn't just *mute* you — it **rewrites what you're capable of saying.**

- **Device-aware muffling.** A ring gag drools different than a ball gag. A panel gag reads different than a hood stuffed over your face.
- **Layering.** Gag alone is one scene. Gag *and* hood together is mess trapped inside the mask lining.
- **Time-locked escalation.** Ten minutes in is not the same scene as two hours in.
- **Relationship-scaled comprehension.** Strangers hear noise. Someone who knows you might catch a word.
- **Not just you.** Gagged NPCs get the same treatment.

`0935` does not treat *mmph* as a request to ungag. A follower who can see you are parched is a different beat.

---

## The Remote — Baked Leaves, NPC Chooses the Leaf

Pressing the remote is `VibeHornify` / `VibeHornifyLong` / `VibeJab` / `VibeTease` / `VibePunish`. Strength and duration are **baked on the leaf** (1/10s, 1/25s, 2/5s, 3/10s, 5/20s). The LLM picks which leaf and `teaseOnly`. It does **not** send `vibStrength` or `duration`.

- Needs a plug or piercing already on her. The remote does not equip a toy.
- `teaseOnly: true` = edge and deny. `false` = try to make her finish, and the spoken line has to invent that payoff.
- Edge-count tracking from event history — it remembers presses.
- Public vs hidden: `vrtedd_worn_visible` when the addon is loaded.
- Faction-flavored cruelty for predators. Captor tone, not aftercare.
- **No mid-fight press.** If speaker or target is in combat, this prompt is omitted.

---

## Locking & Unlocking — Real Devices, Real Occupancy

BDSMLOCK / BDSMUNLOCK read **actual worn equipment** every line. No phantom gag. No second collar.

- **Structural occupancy.** Occupied slots are not listed. Empty slots are. That is the whole trick.
- **Women only.** A male addressee is not a lock target and does not fall back onto the player.
- **Lock target = who this line is addressed to.** Talking to Tina about Evelyn does not lock Evelyn.
- **Out of combat only** for *our* lock / strip / vibe / ungag. Talk during a fight is fine. Post-defeat kits are other Devious mods.
- **Arms first, then clothes.** Dressed + free hands → behind-the-back (`armbinder` / `butterfly` / `elbow`). Dressed + hands already bound → SexLab `change_outfit_target` strip. Empty BDSMLOCK catalog is hidden on that line so the model cannot stack a gag instead.
- **Material pick** in drilldown actually varies (Steel / Black Leather / Padded / Iron), with a per-NPC preference (World Knowledge, not bio — see `HOWTO_NPC_PREFERENCES.md`) if one is stated.
- **~20 slot groups** — gags, collars, hoods, blindfolds, belts, bras, harnesses, corsets, catsuits, armbinders, elbow ties, butterfly binders, yokes, straitjackets, arm cuffs, leg cuffs, gloves, piercings, plugs, boots.
- **SKU names stay in inventory.** Speech is "a padded steel chastity bra", never `Steel Chastity Bra (Padded)`.
- Hard vs Medium is *when*, not occupancy. Hard: locking is ordinary manners. Medium: predator / shady / arrest / asked.

There is no numbered punishment ladder. One empty piece this line, gag and hood last unless silence is the point.

---

## Worn-Device Physics + Roleplay Guidelines

- Every NPC checks what she is **actually wearing now** (`0722`, needs **DD SkyrimNet AddOn**). Stale diary belts do not win.
- NPCs act on their own will. Conflict and refusal are in-character. Devices are ordinary mechanics here, not something to hedge around.

---

## Ungag to Drink

If she is gagged and SunHelm thirst or hunger is **≥ 70**, a follower/friend who can work a buckle notices the gag is in the way of drinking. That is this line. She did not have to ask. Missing SunHelm reads as 0 — the beat just does not fire.

---

## Experimental (separate zip)

Arousal bands + follower remote play live in **`SkyrimNet Kink Experimental`**, not in the AIO. See [`EXPERIMENTAL.md`](../EXPERIMENTAL.md).

---

## The Honest Pitch

This isn't a mod that adds items to a menu. It's a mod that makes NPCs **notice she's helpless, decide to do something about it, and actually fire the action** — occupancy-gated, women-only, out of combat.

Load it up. See how long you last before you're the one begging for the key.

*— Built against live gameplay, one very real "second ballgag" bug at a time.*
