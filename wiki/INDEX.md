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
- `simplicial-latent-geometry/my_theorems/paper_draft.md` — early draft (133L)
- `simplicial-latent-geometry/my_theorems/proof_strategy.md` — active proof strategy (481L)

### Workspace repo
`lean-projects/` is now `davidcagoh/lean-workspace` (private) — tracks wiki/, scripts/, stochastic-proofs-handbook/, CLAUDE.md. The three proof projects are excluded (.gitignore) and remain independent repos.

## Status (2026-04-19 — session 3)

| Project | Sorries | Status |
|---|---|---|
| `jepa-learning-order` | **1** (`bootstrap_consistency` only) ✅ | `frozen_encoder_convergence` proved genuinely (Aristotle `f9906716`, 5 helpers, cherry-picked). Paper updated. |
| `stochastic-search-bounds` | **0** ✅ | Paper complete. `.bib` and LaTeX conversion pending (post-vet). |
| `simplicial-latent-geometry` | 13 | Paper rewritten (Strategy 2). OQ-6 resolved (already fixed). Aristotle job `069b1a71` submitted (matchRadius chain). |
| `stochastic-proofs-handbook` | n/a | Scripts only |

## Next Priorities

1. **Vet all three papers** — user review of three markdowns before preprint submission.
2. **simplicial:** When `069b1a71` Aristotle email arrives, cherry-pick `matchRadius_tendsto_half` into `SimplicialDetection.lean`.
3. **jepa:** Wire `frozen_encoder_convergence` into `JEPA_rho_ordering` (discharge `hPhaseA`) — mechanical, low urgency.
4. **stochastic:** Create `references.bib` from paper lines 430–467 (for LaTeX step, after vet).
5. **OQ-7:** Decide venue targets for all three papers.
