# How To: Give an NPC a Material Preference

*Why your favorite NPC keeps picking random locks, and how to make her actually have a taste.*

## What this is

When an NPC locks a device on someone (`BDSMLOCK` → drilldown → `EQUIP_*`), the drilldown also
picks a **material** — Steel, Black Leather, Padded, or Iron, rotated at random each time. If the
*locking NPC* has a stated preference, that preference wins instead, and the random rotation becomes
the fallback only for slots where her preferred material doesn't have a matching item.

Preferences are read live, every single lock — there's nothing to "set once and forget" beyond the
one-time setup below, and nothing that goes stale the way a diary entry would.

## Why this isn't in her bio

Earlier builds tried to read a preference off the NPC's own character bio — her `background` and
`personality` text. **That never worked**, for any NPC, in any version before 3.3.8: those fields
don't exist on the engine's actor decorator at all (confirmed against the live decorator schema —
`decnpc()` only exposes combat/skill/faction/state data, no bio text). Writing "she loves ebonite"
into a character's personality block did precisely nothing except read nicely in her dialogue.

As of **3.3.8**, preferences are read from **World Knowledge** instead — the same condition-scoped
fact system SkyrimNet already uses for lore ("A dragon attacked Helgen", "The player is Thane of
Whiterun"), just scoped to one NPC instead of a faction or location.

## Set one up

You need the SkyrimNet web dashboard at `localhost:8080` (or the MCP server, if you've got Claude
or another tool wired up to it — same fields, `create_world_knowledge`).

1. Open **World Knowledge** on the dashboard and create a new entry.
2. **Content:** one sentence, naming **only the material you want her to prefer** — see *The one
   gotcha* below for why that matters.
3. **Condition:** `get_name(actorUUID) == "HerExactName"` — the name as it actually displays in
   dialogue. If two NPCs in your game happen to share that exact name, use her UUID instead:
   `actorUUID == 801582357244708787` (grab the UUID from the MCP `get_npcs`/`get_nearby_actors`
   tools, or ask your assistant to look it up if you've got one wired to the MCP server).
4. **Always inject:** **on**. This is a standing trait, not something that should depend on whether
   the current conversation happens to be about locks.
5. **Type:** `KNOWLEDGE` is fine.
6. Save. No game restart needed — World Knowledge is read fresh on every render, unlike editing a
   `.prompt` file (which does need a reload/restart to be picked up).

That's it. Next time she locks something, the drilldown line will read "shows a preference for
`<Material>` gear" instead of falling back to a random pick.

## Worked example: Daegon

Daegon (Altmer, Mehrunes Dagon's daughter, general air of "I was raised on forbidden magic and
mild despair") gets an entry like this:

| Field | Value |
|---|---|
| Content | *"Daegon has a strong, stated preference for cold black ebonite restraints and devices — it matches her Daedric heritage and dark aesthetic. Anything softer feels like a compromise to her, and she'll say so."* |
| Condition | `get_name(actorUUID) == "Daegon"` |
| Always inject | on |
| Type | KNOWLEDGE |

Confirmed live: before this entry existed, her drilldown line read *"No stated material preference
for Daegon — pick [random] this time."* After it, the same line reads *"Daegon's own
background/personality shows a preference for Ebonite gear — pick a Ebonite item for this lock..."*
— no reload of any prompt file required, no bio edit, just the knowledge entry.

## The one gotcha: name only what you want

The check is a plain, unglamorous substring match, tested in this fixed order and stopping at the
first hit: **Steel → Chain → Ebonite → Leather**. It does not understand "prefers X over Y" — it
just looks for whichever of those four words shows up in her knowledge text, in that priority order,
full stop.

So this first draft of the Daegon entry was wrong:

> "...prefers cold black ebonite... over leather, steel, or chain."

That sentence contains all four words. `steel` is checked before `ebonite` in the fixed order above,
so the drilldown picked **Steel** — the exact opposite of the intent — and never even got to
`ebonite`. The fix was to drop the rejected materials from the sentence entirely and name only the
one preference:

> "...strong, stated preference for cold black ebonite restraints and devices..."

**Rule of thumb:** one entry, one material, never mention the other three by name in the same text
block.

## Valid materials

`Steel`, `Chain`, `Ebonite`, `Leather` — matched case-insensitively, in that priority order. `Padded`
and `Iron` exist as random-fallback materials but aren't currently checkable as a stated preference
(the drilldown's keyword list doesn't include them — extend the four `{% elif contains(...) %}`
lines in `native_action_selector_drilldown.prompt` if you want to add one).

## No preference set?

Nothing breaks — the drilldown just falls back to its normal random rotation (Steel / Black Leather
/ Padded / Iron) for that NPC, same as before any of this existed. Preferences are additive flavor,
not a requirement.
