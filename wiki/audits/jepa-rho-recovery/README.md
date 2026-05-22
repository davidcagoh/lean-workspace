# jepa-rho-recovery audits

The spinoff from `jepa-learning-order`. Structurally better than the parent — same total LOC but distributed across coherent files with no god-module.

## Tier 1 — import graph

[`jepa-rho-recovery_import_tier1.svg`](jepa-rho-recovery_import_tier1.svg) — 17 files, 5429 LOC. **No god-module.** Largest file is `SignedRecovery.lean` (798 LOC) but it's a *synthesis* file, not a hidden god-module.

Findings:
- `Basic.lean` is the real foundation (125 LOC, fan-in 13). Compare to learning-order's `Basic.lean` which is a stub.
- `Concentration.lean` is a true orphan (not imported by anything) — **intentional** per session log: staged placeholder for paper-3 with named axiom `matrix_bernstein_subgaussian`.
- `EarlySlopeGronwall.lean` used only by `SignedRecovery` — intentional v-transform extraction.
- `Corrected.lean` is the deprecation-policy landing pad — intentional.

## Tier 3b — not yet run

No file in rho-recovery crosses the god-module threshold (largest legitimate file is 798 LOC, below the rule-of-thumb 800). Tier 3b would surface low-value here.

## Tier 3a — not yet run

Would catch `_ORIGINAL` cleanup candidates and any stale `Corrected.lean` content. Worth running before paper submission.

For methodology, see [`../_methodology/tier1-import.md`](../_methodology/tier1-import.md).
