# Session-log two-tier format experiment

Sibling of `session-wrap/`. Not a skill — just a tracked experiment with
a pre-registered protocol and a rolling log.

## Files

- `DESIGN.md` — pre-registered hypothesis, protocol, decision criteria,
  risks, rollback plan. Read first.
- `LOG.md` — per-session record. Predictions written at session start
  (from `<summary>` lines only), expansion counts tracked during the
  session, summary line appended at wrap. Decision applied after
  3 sessions.
- `TEMPLATE-entry.md` — boilerplate for a single LOG.md entry. Copy in.

## Status

| | |
|---|---|
| Designed | 2026-05-22 (session 94) |
| Started | session 95 (next session) |
| Decision due | after session 97 |
| Current verdict | pending |

## Activation

The experiment runs prospectively at sessions 95, 96, 97. At each of
those wraps, write the session-log entry in the two-tier format:

```markdown
## YYYY-MM-DD (session N, <project>) — <headline>

<summary line: N-bullet outcome — state delta (flagged items)>

<details>

- <full narrative bullet>
- <full narrative bullet>

</details>
```

At each session START (96 onward), follow the protocol in `DESIGN.md`
§"Decision criteria" steps 1–4, recording in `LOG.md`.

## Rollback

After session 97, count expansions in `LOG.md`. Apply decision rule from
`DESIGN.md`. If reverting: unwrap `<details>` blocks in the 3
experimental session-log entries; the format change leaves no other
artifacts.
