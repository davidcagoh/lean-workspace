# jepa-learning-order audits

The project that motivated the audit framework. `JEPA.lean` was 2002 LOC; **the recommended 6-file split was executed in session 95** — see [`../REPORT-2026-05-23-jepa-split.md`](../REPORT-2026-05-23-jepa-split.md) for the before/after analysis, audit-prediction accuracy, and shim-importer migration coda. (Approach-evaluation reports live one level up at `audits/REPORT-*.md`.)

**Quick status:** largest active file now 606 LOC (was 2002); audit-predicted LOC matched actual within ~10% across all 6 sub-modules; the audit-surfaced 11-edge bond between FrobeniusHelpers and EncoderConvergence was respected; build green at 8044 jobs (was 8038); sorry inventory unchanged.

## Tier 1 — import graph

[`jepa-learning-order_import_tier1.svg`](jepa-learning-order_import_tier1.svg) — 12 files, 5051 LOC. **`JEPA.lean` is a god-module** (2002 LOC, 5× the 400-line threshold). Visually red, thick border, fan-in 6.

Other findings:
- `GronwallIntegral.lean` and `Basic.lean` are orphan/stub (dashed).
- Depth 5 chain (`Lemmas → OffDiag → JEPA → Bootstrap → Main`).

## Tier 3b — god-module zoom on JEPA.lean

**Start here:** [`jepa_cluster_summary.svg`](jepa_cluster_summary.svg) — the actionable view. 8 sub-cluster nodes showing what the import graph would look like if `JEPA.lean` were split.

Detail (52 declarations, 112 internal edges): [`jepa_lean_internal.svg`](jepa_lean_internal.svg) — confirms the cluster boundaries.

## Recommended split (informed by tier 3b)

```
JepaLearningOrder/JEPA/
├── Core.lean              (~110 LOC, 13 decls)  ← foundation
├── QuasiStatic.lean       (~235 LOC, 4 decls)
├── Bernoulli.lean         (~285 LOC, 10 decls)  ← merges Bernoulli + CriticalTime (low coupling)
├── DiagAmpODE.lean        (~250 LOC, 3 decls)
├── EncoderHelpers.lean    (~588 LOC, 16 decls)  ← merges FrobeniusHelpers + EncoderConvergence (11-edge bond)
└── OffDiagFinal.lean      (~494 LOC, 6 decls)   ← contains JEPA_rho_ordering (headline)
```

Largest file drops 2002 → 588 LOC (~3.4× editing-pain reduction on the active-work file).

**Key non-obvious finding:** `FrobeniusHelpers` and `EncoderConvergence` are tightly coupled (11 cross-edges). Splitting them would create 11 new import-line dependencies — likely a partition mistake. The audit prevents this by surfacing the coupling visually.

## Post-split snapshot (session 95)

[`jepa-learning-order_import_tier1_post-split.svg`](jepa-learning-order_import_tier1_post-split.svg) — 16 files (+5 net), no red nodes inside the active development surface, largest active file `JEPA/EncoderHelpers.lean` at 606 LOC. `Corrected.lean` (1066 LOC) is the only remaining ≥800-LOC file and stays large intentionally as a deprecation-sibling per the framework's structure-vs-intent caveat.

## Two methodological findings only surfaced post-split

1. **DAG depth increased 5 → 9** because the shim-based migration kept downstream importers pointing at `JEPA.lean`. Strategy doc should add a chain-depth check to the tier-1 reading order.
2. **Shim creates a fake fan-in hub.** `JEPA.lean` shim has fan-in 6 — backwards-compat artifact, not structural truth. Schedule a follow-up to migrate importers to narrow sub-module imports.

Both findings detailed in the report; both fed back into [`wiki/graph-audit-strategy.md`](../../wiki/graph-audit-strategy.md).

For methodology, see [`../_methodology/tier1-import.md`](../_methodology/tier1-import.md) and [`../_methodology/tier3b-god-module-zoom.md`](../_methodology/tier3b-god-module-zoom.md).
