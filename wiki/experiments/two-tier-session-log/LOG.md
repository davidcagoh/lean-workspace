# Two-tier format experiment — rolling log

Per-session entries. Newest at top. Copy from `TEMPLATE-entry.md`.

Decision rule (from `DESIGN.md`): after 3 sessions, sum the
"Expansion count this pickup" column.

- **Total 0–3 across 3 sessions** → adopt two-tier format permanently.
  Update `~/.claude-main/skills/session-wrap/SKILL.md` to make it the
  default.
- **Total 4–9** → tune. Refine `<summary>` content convention and re-run
  for 3 more sessions.
- **Total 10–15** → revert. Unwrap the experimental entries, delete this
  experiment dir.

---

<!-- Entries below this line; newest at top. Copy from TEMPLATE-entry.md. -->
