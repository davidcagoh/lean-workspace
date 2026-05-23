# Graph audits

Per-project import-graph and math-graph audit artifacts (the worked examples). For the methodology — when to audit, what commands to run, how to read the output — see [`../graph-audit-strategy.md`](../graph-audit-strategy.md).

## Layout

Organized **by project**. Each project folder contains all of its audit artifacts (tier 1 imports, tier 3a build-ups, tier 3b god-module zooms — whichever apply).

| Project | Folder | Status |
|---|---|---|
| stochastic-search-bounds | [`stochastic-search-bounds/`](stochastic-search-bounds/) | tier 1 + tier 3a (all four theorems) |
| jepa-learning-order | [`jepa-learning-order/`](jepa-learning-order/) | tier 1 + tier 3b on `JEPA.lean` |
| jepa-rho-recovery | [`jepa-rho-recovery/`](jepa-rho-recovery/) | tier 1 only |

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

## Why this lives in `wiki/`, not `stochastic-proofs-handbook/`

The handbook is for shared **scripts**; results live in the wiki. When the audit becomes automated (a `graph_audit.py` script in the handbook), it will write results back into these per-project folders.
