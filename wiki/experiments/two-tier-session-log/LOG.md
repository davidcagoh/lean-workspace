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

## Session 96 — 2026-05-23

### At session start (predictions from `<summary>` lines only)

**Methodology gap to flag up front:** I did NOT execute the protocol-required "predict from summary lines only" step at session start. I read INDEX.md + the audit-report path the user pointed me at, then jumped into work. The protocol step was effectively skipped. This is itself a data point: the experiment design requires opt-in discipline that a fresh agent will not naturally perform unless prompted by a hook or a strong CLAUDE.md instruction.

Reconstructing what the prediction *would* have been (from the session 95 `<summary>` line read after the fact):

| Prior session | One-line prediction | Would I have expanded? |
|---|---|---|
| 95 | Split + audit re-run — JEPA.lean 2002L → 6 sub-modules; shim preserves 7 importers; build 8038 → 8044 ✓; before/after report with two new findings (depth 5→9, false fan-in hub) fed into strategy doc; audits/ promoted to workspace sibling. | Yes — for the user's specific question on the report findings I needed the named findings + the migration follow-up status. Summary line lists "two new findings" but not which two. |

### During session (expansion tracking)

| Expanded session | Why | Was summary misleading? |
|---|---|---|
| 95 | Mid-session, user asked for recap of "what we've been doing these two sessions." Expanded to retrieve specific bullets for the user-facing recap. | No — summary was accurate but not detailed enough for a user-facing prose recap. Expected use case. |
| 94 | Same recap prompt — same reason. | No. |

### At wrap

- **Expansion count this pickup:** 2 (both during the user-prompted recap, not during the actual work)
- **Organic expansions during work:** 0 — the SimplicialDetection audit + JEPA shim-migration + strategy-doc updates did not require any `<details>` reading. Tier-1 / tier-3b / strategy-doc work runs off the strategy doc + INDEX, not session history.
- **Wrap-time cost vs flat format:** equal (writing this entry).
- **Summary-line behavior observed:** when the user asks "what did we do," the summary line is too compressed and `<details>` *will* get expanded. This is the expected user-facing use case and is fine — the experiment is about whether *I* expand to do *work*, not whether prose recaps are quick.

### Notes

**Methodology fix to propose:** if the experiment requires the session-start prediction step, it needs enforcement — a hook, a CLAUDE.md line, or a session-wrap-time reminder that the *next* agent must run the prediction step. Right now it's documented only in `DESIGN.md` which a fresh agent will not read unprompted. (I only knew the protocol existed because the user asked me to check on the experiment mid-session.)

**Running tally going into session 97:** session 94 = 1 protocol expansion + 0 organic; session 95 = 0 expansions during pickup, 2 expansions during user recap; session 96 = 0 expansions during pickup, 2 expansions during user recap.

Across 3 sessions: **0 organic work-driven expansions, 3 user-recap-driven expansions, 1 protocol expansion**. Per the decision rule that counts total expansions, we're at 6 — in the "tune" band (4-9). But disaggregating: the 0 organic-work expansions are the strongest signal that the summary discipline is sufficient for actual work. The user-recap expansions are out-of-scope for the original design (the experiment was about agent productivity, not user-facing recap quality).

**Recommendation forming:** at session 97, run the protocol prediction step properly and one more pickup. If organic = 0 again, adopt the format and amend the decision rule to exclude user-recap expansions (they measure something different).

---

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

**Extension addendum (2026-05-23, same session 95):** user requested a post-split audit re-run + before/after report. Required reading `audits/jepa-learning-order/README.md` and `wiki/graph-audit-strategy.md` (both flat/non-experimental docs — no `<details>` expansions). Did NOT need to expand session 94's `<details>` again — the summary line still carried sufficient state. Total organic expansions across the extended session 95 work: still **0**. The session-log entry's summary line was extended to include the audit re-run + report work; the body got 3 new bullets. Wrap-time cost: marginally higher (the entry now describes two related but distinct work-streams), but the summary line still compresses cleanly.

If session 96 inherits this pattern (multi-stream session collapsed into one entry), the summary lines may need to grow toward ~2 sentences instead of 1 long clause. Watch for this.
