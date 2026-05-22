# Tier 3a — Per-theorem math build-up

Lemma-level view. For each headline theorem, three rows:

1. **DEFINITIONS** (bottom) — what the theorem is built on (types, key concepts, helper lemmas).
2. **LEMMA** (middle) — the load-bearing intermediate result, if any.
3. **THEOREM** (top) — the headline result, with its actual mathematical statement.

Reads bottom-to-top. Every cross-file edge here corresponds to an `import` line in the importing file.

## Start with the combined view

[`ssb_math_tier3a_combined.svg`](ssb_math_tier3a_combined.svg) — all four SSB theorems on one canvas with a shared foundation row. Best single picture for "project at a glance, math-side."

Then drill into individual theorems for legibility:

| Theorem | File | What this view surfaces |
|---|---|---|
| Theorem 1 — hitting-time upper bound | [`ssb_math_tier3a_hitting_time_upper_bound.svg`](ssb_math_tier3a_hitting_time_upper_bound.svg) | Theorem rests on one lemma plus four definitions. **`isProvable` declared as hypothesis but never used in the proof.** |
| Theorem 2 — policy improvement | [`ssb_math_tier3a_policy_improvement.svg`](ssb_math_tier3a_policy_improvement.svg) | **The only cross-file proof-step edge in SSB**: `NNReal.weighted_sum_mono` (Defs) → `successProb_mono` (T2). Visible as a long red arrow. |
| Theorem 3 — AND-branching lower bound | [`ssb_math_tier3a_and_branching.svg`](ssb_math_tier3a_and_branching.svg) | **Theorem uses no lemma** — invokes `hpmax` hypothesis directly. Two declared T3 helpers (`successProb_andNode_eq`, `andNode_successProb_le`) are dead. |
| Theorem 4 — sequential ≤ parallel | [`ssb_math_tier3a_sequential_parallel.svg`](ssb_math_tier3a_sequential_parallel.svg) | **Uses no Defs symbol** — yet `Theorem4.lean` imports `Defs`. And `Defs.sum_prod_erase_le_one` is a near-duplicate of T4's local lemma, sitting dead. |

## Encoding

| Channel | Meaning |
|---|---|
| Node fill — blue | from `Defs.lean` |
| Node fill — yellow | from a `Theorem*.lean` |
| Node fill — gray | external (Mathlib) |
| Hexagon shape | type or structure |
| Rectangle | lemma or theorem |
| Bold + thick border (top row) | headline theorem |
| Edge — **red, thick** | proof-step (lemma applied in a proof body) |
| Edge — blue, thin | definitional dependency (appears in signature or conclusion) |
| Edge — dashed gray | external (Mathlib) dependency |
| Node or edge — dashed red | dead or unused |

## What tier 3a catches that tier 1 can't

| Finding (SSB) | Visible in tier 1? | Visible in tier 3a? |
|---|---|---|
| `Theorem1_Strong → Theorem1` import unjustified | ✗ | tier 3a doesn't show this for SSB (T1_Strong isn't a headline) |
| `T4 → Defs` import unjustified | ✗ | ✓ (T4 build-up has no Defs node feeding in) |
| `T4_Strong → Defs/Theorem4` imports unjustified | ✗ | partial |
| `T1.isProvable` hypothesis unused | ✗ | ✓ (red dashed edge) |
| `T3.successProb_andNode_eq`, `andNode_successProb_le` dead | ✗ | ✓ (red dashed nodes, no live edges in or out) |
| `Defs.sum_prod_erase_le_one` dead (T4 reinvents) | ✗ | ✓ (red dashed node, no edges) |
| `Defs.NNReal.prod_le_pow_of_le` only used by dead T3 helper | ✗ | ✓ (dashed, only edges go to a dashed node) |

## Caveat — read `session-log.md` before acting

The structural "dead" / "unused" findings are *facts*. Whether to remove them depends on intent (deliberate placeholder for paper-3 work? deprecation-policy artifact? archived `_WRONG` variant?). See top-level README of `wiki/audits/`.
