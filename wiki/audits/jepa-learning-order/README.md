# jepa-learning-order audits

The project that motivated this whole audit framework — `JEPA.lean` is 2002 LOC and editing it is painful.

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

For methodology, see [`../_methodology/tier1-import.md`](../_methodology/tier1-import.md) and [`../_methodology/tier3b-god-module-zoom.md`](../_methodology/tier3b-god-module-zoom.md).
