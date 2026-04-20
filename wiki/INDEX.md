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
- `simplicial-latent-geometry/my_theorems/paper.tex` — LaTeX version, compiles clean (11pp, 12 BibTeX entries)
- `simplicial-latent-geometry/my_theorems/proof_strategy.md` — active proof strategy (481L)

### Workspace repo
`lean-projects/` is now `davidcagoh/lean-workspace` (private) — tracks wiki/, scripts/, stochastic-proofs-handbook/, CLAUDE.md. The three proof projects are excluded (.gitignore) and remain independent repos.

## Status (2026-04-19 — session 5)

| Project | Sorries | Status |
|---|---|---|
| `jepa-learning-order` | **1** (`bootstrap_consistency` only) ✅ | Paper updated. Build clean. Ready for vet. |
| `stochastic-search-bounds` | **0** ✅ | Paper complete. LaTeX/bib pending (post-vet). |
| `simplicial-latent-geometry` | **5 active** | paper.tex compiles clean (11pp). `069b1a71` results extracted — cherry-pick `matchRadius_tendsto_half` next session. |
| `stochastic-proofs-handbook` | n/a | Scripts only |

## Next Priorities

1. **Simplicial:** Cherry-pick `matchRadius_tendsto_half` from `069b1a71_extracted/` into `SimplicialDetection.lean` (line 1277 sorry).
2. **Simplicial:** Submit `geometricCov_tendsto_zero` (line 1650) + `fillingProb_nonneg` (line 3371) to Aristotle as one job.
3. **OQ-7:** Decide venue targets for all three papers.
4. **Vet papers:** User review of paper_draft.md (JEPA, stochastic) before preprint submission.
5. **JEPA:** Wire `frozen_encoder_convergence` into `JEPA_rho_ordering` (discharge `hPhaseA`) — mechanical, low urgency.
