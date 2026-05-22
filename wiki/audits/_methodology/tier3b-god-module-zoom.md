# Tier 3b — God-module zoom

When a single `.lean` file is large enough that tier 1 cannot say anything about its internals (it's just one node), tier 3b drops one level and looks at the **declarations inside the file** as if it were its own project.

Output is two complementary views per file:

1. **Cluster summary** — "if we split this file, what would the import graph look like?" 8 sub-cluster nodes, edges weighted by how many lemma-level math edges cross each boundary. Direct answer to "where to split."
2. **Lemma detail** — every declaration as its own node, grouped by proposed sub-cluster. Lets you verify the cluster boundaries.

## Index

| File audited | LOC | Cluster summary | Lemma detail | Key finding |
|---|---|---|---|---|
| `jepa-learning-order/JepaLearningOrder/JEPA.lean` | 2002 | [`jepa_cluster_summary.svg`](jepa_cluster_summary.svg) | [`jepa_lean_internal.svg`](jepa_lean_internal.svg) | 52 declarations split cleanly into 8 sub-clusters. Single tight-coupling pair: EncoderConvergence ↔ FrobeniusHelpers (11 edges) — these want to merge. All other non-Core couplings ≤ 4 edges — clean split candidates. |

## Methodology

- Parse declarations with regex (`^theorem|lemma|noncomputable def|...`).
- For each declaration's body, regex-match every other declaration's name as a "uses" reference.
- Classify each declaration into a sub-cluster by topic (read line ranges + naming).
- Count intra-cluster vs inter-cluster edges to validate the partition.
- Edges between **non-Core** clusters are the "real" coupling signal — edges *into* Core are expected (Core is the foundation).

## Encoding (cluster summary)

| Channel | Meaning |
|---|---|
| Node size | ∝ LOC of the proposed split file |
| Node thick border | foundation (Core) or headline-bearing (OffDiagFinal) |
| Edge thickness | ∝ # lemma-level math edges that would cross this boundary |
| Edge color — blue | edge points into Core (the foundation pull — expected, not a concern) |
| Edge color — dark gray | non-Core coupling (the "real" signal) |
| Edge style — dashed | single-edge connection (probably proof-incidental, not structural) |

## What this view delivers

For JEPA.lean specifically:

- **Confirms the 8-cluster hypothesis** — declarations partition cleanly along topic boundaries.
- **Surfaces one tight non-Core coupling**: `EncoderConvergence ↔ FrobeniusHelpers` has 11 edges. These two clusters want to stay in one file (~588 LOC combined; still above the 400 target but defensible).
- **Validates that other couplings are sparse** (≤ 4 edges between any other non-Core pair) — those splits are essentially free.
- **Quantifies the foundation pull** — Core has 68 incoming edges. After splitting Core out, those become 68 import-justified references in 7 sibling files. Healthy star pattern.

## Proposed split (informed by this audit)

```
JepaLearningOrder/JEPA/
├── Core.lean              (~110 LOC, 13 decls)  ← foundation
├── QuasiStatic.lean       (~235 LOC, 4 decls)
├── Bernoulli.lean         (~285 LOC, 10 decls)  ← merges Bernoulli + CriticalTime (low coupling makes merger viable)
├── DiagAmpODE.lean        (~250 LOC, 3 decls)
├── EncoderHelpers.lean    (~588 LOC, 16 decls)  ← merges FrobeniusHelpers + EncoderConvergence (11-edge bond)
└── OffDiagFinal.lean      (~494 LOC, 6 decls)   ← contains headline theorem JEPA_rho_ordering
```

Result: largest file 588 LOC (vs 2002 today). Editing pain drops by ~3×. Foundation file (Core) stays small (~110 LOC) so its high fan-in is cheap. EncoderHelpers stays large but its internal connectivity justifies it.
