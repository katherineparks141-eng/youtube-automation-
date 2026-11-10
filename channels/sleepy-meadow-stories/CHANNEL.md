# Sleepy Meadow Stories

Original, zero-filming kids' bedtime-story channel — the second concept being tested
alongside Forgotten & Found. Full identity defined in Idea 9 of the Business Ideas
Playbook doc.

- **Format:** narrated original illustrated bedtime stories, soft painterly storybook
  art, consistent original characters (Pip the bunny is the first)
- **Narrator voice:** Piper `en_US-amy-medium` — warm
- **Postiz project key:** `forgotten-and-found` (shares the channel for now)
- **YouTube channel:** "Katie Tuell" (integration id `cmvy6plen09q6nk0750rg2fha`)
- **Made for kids:** Yes — this is a real compliance declaration, not a default; see
  CLAUDE.md hard rule #2.
- **Thumbnails:** keep calm and true-to-content, not exaggerated — kids-channel trust
  signal research shows exaggerated thumbnails actively hurt recommendations here,
  unlike in most adult niches.
- **Character consistency:** generate one reference image per character, then pass its
  Canva media id as `imageReferences` on every later image of that character.
- **Pip redesign (Katie, 2026-11-10):** the old look (brown bunny, blue top, burrow with
  round window, lantern, basket) was too close to Peter Rabbit. Use only the new design in
  `character-reference.json`, and check every image against its `doNot` list. Stories 01-03
  use the old look; Katie is reviewing them.
