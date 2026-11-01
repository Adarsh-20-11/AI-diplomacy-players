# needle-ai knowledge vault

Open this `notes/` folder as a vault in Obsidian.

- One concept per note, copied from `_templates/concept.md`
  (Obsidian: Settings > Core plugins > Templates > set template folder to `_templates`).
- Link notes with `[[wiki links]]`; the Graph view shows how concepts connect.
- Write the "What it is" section in your own words. Don't paste explanations.
- Mark `status: solid` once you can answer all quiz questions without looking.

## Review and quiz loop
1. Write a concept note. The "What it is" section is in your own words.
2. Ask Claude to review it. Claude appends a block under "Reviews (Claude)" with a
   1-5 score, what was right, what was wrong, and a corrected version. Claude also
   updates `score` and `last_reviewed` in the frontmatter and the row in
   [[_progress]]. Claude never edits your sections.
3. Say "quiz me". Claude picks concepts with low or falling scores first, asks,
   grades your answer, and updates the tracker.
4. A concept becomes `status: solid` after a 4+ on two reviews.

## Phase 0 notes to write
- [[Src Layout]]
- [[pyproject.toml]]
- [[Virtual Environments]]
- [[Linting vs Type Checking]]
- [[Continuous Integration]]
