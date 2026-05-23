# Experiment: two-tier `<details>` format for session-log

**Status:** proposed, not yet adopted.
**Author:** davidgoh (designed 2026-05-22, session 94).

## Hypothesis

A two-tier session-log entry — one-line headline visible by default, full
narrative collapsed inside `<details>` — reduces session-pickup time without
losing recall.

Specifically: when re-entering a project, you can scan the last 5 sessions in
~5 lines of text instead of ~150, expanding only the entries you actually
need.

## Background

Current format (after session 94 cleanup) is flat: one `##` header + 3-7
narrative bullets per session. Active log carries 5 sessions = ~150 lines.
Pickup requires scanning all of it because there's no summary layer.

Two-tier version:

```markdown
## YYYY-MM-DD (session N, <project>) — <headline>

<details>
<summary>3-bullet outcome: action / decision / state-delta</summary>

- <full narrative bullet>
- <full narrative bullet>
- ...

</details>
```

The `<summary>` line is GitHub/Markdown-rendered as visible-by-default; the
`<details>` body collapses. In a plain-text editor (vim, terminal) the
distinction is just structural and a human can skim summaries.

## Decision criteria (pre-registered)

Run for **3 consecutive wraps** (sessions 95, 96, 97). At each session
start, BEFORE expanding any `<details>` block:

1. **Read the last 5 summaries** (one line each).
2. **Predict what you'd need from each session.** Write a single sentence
   per session: "I think session N did X; I'll need to expand if Y."
3. **Open the project, start work.**
4. **Track expansions.** Each time you expand a `<details>` block during
   the session, note which session and what you needed.

After 3 sessions:

- **Expansions per pickup: 0–1** → **adopt.** Summary layer is sufficient;
  detail layer is rare-reference, not pickup-critical.
- **Expansions per pickup: 2–3** → **tune.** Summary content is missing
  something; refine what goes in `<summary>` and re-run.
- **Expansions per pickup: 4–5** → **revert.** First line is just
  overhead; flat format wins.

Also track:
- **Wrap-time cost.** Does writing the two-tier format take noticeably
  longer than flat? If yes, that's a tax against adoption.
- **Predictive accuracy.** Did your one-sentence prediction from the
  summary match what was actually in the detail? Mismatches mean the
  summary is misleading.

## What goes in `<summary>` (proposed convention)

A single line of the form:

```
N-bullet outcome — <one-line state delta> (<flagged items: refusal / disproof / decision>)
```

Examples:

- `Cherry-pick — Corrected.lean sorry-free; 1 new axiom (saxe_*) (axiom-promote decision)`
- `Built graph-audit framework — no proof work; methodology codified to wiki/`
- `Sandwich proved + exact_solution disproved — 5→3 sorries (paper-2 alignment realization)`

Rule of thumb: if you can't compress the session to one sentence containing
(a) what changed, (b) the state delta, and (c) any flagged decisions or
refusals, the session was either too big to be one session or the wrap
isn't capturing the right thing.

## Risks

1. **Markdown rendering dependency.** `<details>` renders nicely on GitHub
   and most Markdown viewers but is just literal HTML in `cat`/`less`/vim.
   If pickup happens in a terminal, the collapse benefit evaporates.
   *Mitigation:* the `<summary>` line is human-readable as a regular
   sentence even without rendering, so no information is hidden in CLI
   contexts — just no visual collapse.
2. **Summary drift.** Tempting to write the summary first, then write
   detail that says different things. *Mitigation:* write detail first,
   compose summary as the last step at wrap.
3. **Reflex to expand everything.** If you instinctively open all
   `<details>` "just to be safe," the format provides zero value.
   *Mitigation:* enforce step 2 of the protocol (predict first, then
   expand only when prediction is insufficient).
4. **Confounding with content quality.** A bad week of sessions could
   make any format feel worse. *Mitigation:* run for 3 sessions, not 1.

## Rollback plan

If criteria say revert: take the 3 experimental entries, unwrap the
`<details>` blocks (delete the `<details>`/`<summary>` tags, keep the
bullets), update SKILL.md to remove the two-tier instructions. Total cost
~10 minutes. No structural lock-in.

## Out of scope

- Don't tier INDEX.md. Compact-table format is already at the right level.
- Don't tier decisions.md. Decisions are read in full or not at all.
- Don't apply retroactively to archived sessions. Format change is
  prospective only.
