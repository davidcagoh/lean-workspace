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

## Session 95 — 2026-05-22

### At session start (predictions from `<summary>` lines only)

| Prior session | One-line prediction | "I'll expand if…" |
|---|---|---|
| 94 | Cherry-picked Aristotle results: `saxe_gronwall_sandwich` proved via Lyapunov reroute; `saxe_exact_solution_exists` axiom-promoted (matching paper-2 triple); paper.tex Appendix D adds Axiom A3 (12→13pp); INDEX.md compacted 845→407L as 2-tier format experiment kickoff. | I need the exact axiom statement, the Lyapunov helper names, or the precise t_max_reach inequality form. |
| 93 | (flat format — no summary line) | n/a |
| 92 | (flat format — no summary line) | n/a |
| 91 | (flat format — no summary line) | n/a |
| 90 | (flat format — no summary line) | n/a |

Only one prior two-tier entry exists (session 94), so this pickup is a degenerate first data point — the experiment becomes meaningful once 3+ two-tier predecessors are stacked.

### During session (expansion tracking)

| Expanded session | Why | Was summary misleading? |
|---|---|---|
| 94 | Protocol-required verification of prediction at session start (step 1 of the experiment instructions). | No — prediction matched on all 5 elements (cherry-pick, sandwich proved, axiom-promoted, paper 12→13pp, INDEX compact). |

### At wrap

- **Expansion count this pickup:** 1 (the protocol-required predictive-accuracy check on session 94)
- **Organic expansions during work:** 0 — the JEPA.lean refactor did not require me to open session 94's `<details>` block. The summary line carried enough state ("Corrected.lean sorry-free, 1 new axiom, sandwich proved, paper 12→13pp") to know that paper-1's `Corrected.lean` is stable and the next surface area to touch is `JEPA.lean` itself (per next-step note from session 93/94).
- **Wrap-time cost vs flat format:** equal. Writing the `<summary>` line + `<details>` body took the same effort as a flat entry; no measurable overhead.
- **Predictive accuracy:** 5/5 on session 94 (matched cherry-pick, sandwich proof, axiom promotion, paper update, INDEX compaction).
- **Summary-line quality this session (post-write):** clean. Session 95's summary is well-compressed ("Split — JEPA.lean 2002L → 6 sub-modules ... 2 active sorries quarantined ... build 8038 → 8044 jobs"). A future session reading only this summary will know: which file got refactored, the LOC ratio, where the sorries live, and the build delta.

### Notes

The protocol-required initial expansion is arguably noise — it's not a "I needed to know this to do my work" signal, it's "the experiment design told me to expand." Honest signal: **0 organic expansions** this pickup. Strong evidence that the summary-line discipline is working at least for this session's pickup pattern. Need 2 more sessions to confirm.

**Running tally going into session 96:** 1 protocol expansion + 0 organic = 1 total expansion across 1 measured pickup. On track for ≤3-total adopt threshold.
