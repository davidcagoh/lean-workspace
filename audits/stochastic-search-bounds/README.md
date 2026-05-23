# SSB audits

Reference shape — depth 3, no god-module, clean sibling fan-out. Use this project's tier 1 as the **target shape** for what other projects should aspire to.

## Tier 1 — import graph

[`stochastic-search-bounds_import_tier1.svg`](stochastic-search-bounds_import_tier1.svg) — 8 files, 1199 LOC total, largest file 280 LOC. No structural issues at the file level.

## Tier 3a — math build-up (all four headline theorems)

**Start here:** [`ssb_math_tier3a_combined.svg`](ssb_math_tier3a_combined.svg) — all four theorems on one canvas, sharing the Defs foundation row.

Then drill in:

| Theorem | File | What it surfaces |
|---|---|---|
| Theorem 1 — hitting-time upper bound | [`ssb_math_tier3a_hitting_time_upper_bound.svg`](ssb_math_tier3a_hitting_time_upper_bound.svg) | **`isProvable` declared as hypothesis but unused in proof.** |
| Theorem 2 — policy improvement | [`ssb_math_tier3a_policy_improvement.svg`](ssb_math_tier3a_policy_improvement.svg) | **The only cross-file proof-step edge in SSB**: `NNReal.weighted_sum_mono` → `successProb_mono`. |
| Theorem 3 — AND-branching lower bound | [`ssb_math_tier3a_and_branching.svg`](ssb_math_tier3a_and_branching.svg) | **Theorem uses no lemma**; two declared T3 helpers are dead. |
| Theorem 4 — sequential ≤ parallel | [`ssb_math_tier3a_sequential_parallel.svg`](ssb_math_tier3a_sequential_parallel.svg) | **Uses no Defs symbol** — yet `Theorem4.lean` imports `Defs`. `Defs.sum_prod_erase_le_one` is a dead near-duplicate of T4's local lemma. |

## Summary findings

| Layer | Verdict |
|---|---|
| File structure (tier 1) | ✓ Reference quality |
| Math content (tier 3a) | Partial — 4 unjustified imports (T1_Strong→T1, T4_Strong→T4, T4→Defs, T4_Strong→Defs), 4 dead lemmas (1 in Defs, 2 in T3, 1 in T4_Strong), 1 unused hypothesis (`isProvable` in T1) |

Tier-3a findings are code-quality smells that don't affect editing pain but are worth cleaning before paper submission.

For encoding conventions, see [`../_methodology/tier1-import.md`](../_methodology/tier1-import.md) and [`../_methodology/tier3a-build-up.md`](../_methodology/tier3a-build-up.md).
