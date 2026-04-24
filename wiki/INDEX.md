# Wiki Index — lean-projects

## Files

| File | When to read |
|---|---|
| `INDEX.md` (this file) | Start of every session — check status block and next priorities |
| `session-log.md` | Start of every session — read the top (most recent) entry for project state |
| `decisions.md` | Before making architectural or proof-strategy choices |
| `open-questions.md` | When something seems ambiguous or undocumented; add new questions here |
| `lean4-reference.md` | Before writing any Lean — type conventions, Mathlib API, pitfalls, termination patterns |
| `aristotle-strategy.md` | Before submitting to Aristotle — sizing, statement quality, merging, domain patterns |

### Handbook
`stochastic-proofs-handbook/` is now scripts-only. Its `docs/`, `templates/`, and `archive/` directories have been deleted — all knowledge is in this wiki. The handbook README points here.

### Paper drafts — naming convention
Each lean project has a canonical paper draft at `my_theorems/paper_draft.md`. Supporting docs sit alongside it. Older versions are in `my_theorems/archive/`. This is the standard across all three projects:
- `jepa-learning-order/my_theorems/paper_draft.md` — "Conditional" title, 767L (v2)
- `stochastic-search-bounds/my_theorems/paper_draft.md` — Manuscript v6
- `simplicial-latent-geometry/my_theorems/paper_draft.md` — Strategy 2 draft, §5 updated
- `simplicial-latent-geometry/my_theorems/paper.tex` — LaTeX version, **14pp, §1 prose-first, Thm 4.2 rescoped to fixed d, variance-bound case analysis in Appendix B, 15 bib entries, 17 Lean pointers all verified, compiles clean**
- `simplicial-latent-geometry/my_theorems/proof_strategy.md` — active proof strategy (481L)

### Workspace repo
`lean-projects/` is now `davidcagoh/lean-workspace` (private) — tracks wiki/, scripts/, stochastic-proofs-handbook/, CLAUDE.md. The three proof projects are excluded (.gitignore) and remain independent repos.

## Status (2026-04-24 — session 18)

| Project | Sorries | Status |
|---|---|---|
| `jepa-learning-order` | **1** (`bootstrap_consistency` only) ✅ | Paper updated. Build clean. Ready for vet. |
| `stochastic-search-bounds` | **0** ✅ | Paper complete. LaTeX/bib pending (post-vet). |
| `simplicial-latent-geometry` | **6 in-flight** ⚠️ | `lake build` ✅ green (was 28 errors). 6 tactic-drift sorries sent to Aristotle (Jobs `ef4bf1ac`, `e9270000`, `986efbdd`). 16/17 paper pointers resolve; `paleyZygmund_cech_prob_tendsto_one` awaits Job C. New OQ-10 flagged: `chebyshev_ratio_tendsto_zero` Lean statement weaker than proof needs (paper fixed-`d` regime not captured in signature). |
| `stochastic-proofs-handbook` | n/a | Scripts only |

## Next Priorities

1. **Simplicial — retrieve Aristotle jobs:** run `python ../scripts/retrieve.py` when emails arrive for `ef4bf1ac` (Job A: `cechDoublySigned_triangle_integral` + `edgeProduct_integral_bounded'`), `e9270000` (Job B: `vertex_sharing_indepFun'`), `986efbdd` (Job C: `cech_complement_prob_bound` + `chebyshev_ratio_tendsto_zero` + `paleyZygmund_cech_prob_tendsto_one`). Cherry-pick filled bodies; do not wholesale replace.
2. **Simplicial — resolve OQ-10:** after Job C, reconcile `chebyshev_ratio_tendsto_zero`'s Lean hypothesis with the paper's fixed-`d` regime. Either tighten the signature (add `∃ c > 0, ∀ k, c ≤ geometricCov p (dSeq k)`) or specialise at the call site in `paleyZygmund_cech_prob_tendsto_one`. ~5 min work.
3. **Simplicial — arXiv upload:** `paper.tex` + `references.bib` (14pp) once sorries close.
4. **Simplicial — RSA submission:** PDF via Wiley ScholarOne after arXiv ID assigned.
5. **OQ-7:** JEPA and stochastic-search-bounds venue targets still open.
6. **JEPA:** Wire `frozen_encoder_convergence` into `JEPA_rho_ordering` (discharge `hPhaseA`) — low urgency.
