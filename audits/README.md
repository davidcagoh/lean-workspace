# Graph audits

Per-project import-graph and math-graph audit artifacts (the worked examples), plus **approach-evaluation reports** at this root tracking how the methodology performed on each executed refactor. For the methodology itself — when to audit, what commands to run, how to read the output — see [`../wiki/graph-audit-strategy.md`](../wiki/graph-audit-strategy.md).

## Approach-evaluation reports (root level)

These capture **how the audit framework actually performed** on a real refactor: predictions vs. actuals, what the audit caught, what it missed, what the methodology should learn. Kept separate from per-project artifacts so the meta-evaluation arc is readable end-to-end.

| Report | Subject | Outcome |
|---|---|---|
| [`REPORT-2026-05-23-jepa-split.md`](REPORT-2026-05-23-jepa-split.md) | `JEPA.lean` 2002 LOC → 6-file split | Predictions ≤10% off; 11-edge bond respected; two methodology gaps fed back into strategy doc (depth blindness, shim false fan-in). Both gaps closed in shim-migration coda. |
| [`REPORT-2026-05-23-simplicial-split.md`](REPORT-2026-05-23-simplicial-split.md) | `SimplicialDetection.lean` 5606 LOC → 15-file split | Generated session 96; same-report format. |

## Per-project worked examples

Organized **by project**. Each folder holds tier-1 / tier-3a / tier-3b artifacts and a pre-split recommendation README.

| Project | Folder | Status |
|---|---|---|
| stochastic-search-bounds | [`stochastic-search-bounds/`](stochastic-search-bounds/) | tier 1 + tier 3a (all four theorems) |
| jepa-learning-order | [`jepa-learning-order/`](jepa-learning-order/) | tier 1 + tier 3b on `JEPA.lean` — **split executed** |
| jepa-rho-recovery | [`jepa-rho-recovery/`](jepa-rho-recovery/) | tier 1 only |
| simplicial-latent-geometry | [`simplicial-latent-geometry/`](simplicial-latent-geometry/) | tier 1 + tier 3b on `SimplicialDetection.lean` — **split executed (session 96)** |

Methodology docs (what each tier is, how to read it, encoding conventions) live in [`_methodology/`](_methodology/).

## The minimal workflow

For diagnosing **editing pain** on large `.lean` files:

```
1. Generate tier 1 (import graph) for the project.
   → Are any files > 800 LOC, or any node visually dominant?
2. If yes: generate tier 3b on the largest file.
   → What sub-clusters does the math graph reveal?
   → Where are the tight non-Core couplings (would-be split breakers)?
3. Split the file along sub-cluster boundaries, keeping tight pairs together.
4. Re-run tier 1 to verify (largest file should drop significantly).
```

This is ~90% scriptable — see `_methodology/` for the parser approach used.

**When also to run tier 3a:** before paper submission, or when reviewing for code quality. Tier 3a catches dead lemmas and unused hypotheses that the structural tiers can't see. Distinct lens, distinct cost.

## Tiers, briefly

- **Tier 1 — import graph.** File-level. Nodes = files, edges = imports. Size ∝ LOC, border ∝ fan-in.
- **Tier 3a — math build-up.** Lemma-level. Per headline theorem: definitions → lemma → theorem build-up, with dead/unused code surfaced.
- **Tier 3b — god-module zoom.** Lemma-level inside a single file. Shows internal sub-clusters; outputs a split recommendation.

(Tier 2 — red-edge annotation on tier 1 — was considered but superseded by tier 3a, which gives the same info with more context.)

## Caveat — structure ≠ intent

Structural facts (orphans, dead lemmas, unjustified imports) are facts. Whether to act on them depends on intent: staged future work, deprecation policy, archived `_WRONG` variants. **Always read `wiki/session-log.md` before acting on a finding.**

## Why `audits/` lives at the workspace root

Audits are operational artifacts (like `scripts/`), not pedagogical wiki content. Promoted from `wiki/audits/` to workspace-root `audits/` in session 95 once the framework was validated and started accumulating per-refactor reports.
