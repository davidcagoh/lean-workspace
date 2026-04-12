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

## Status (2026-04-12)

| Project | Sorries | Status |
|---|---|---|
| `jepa-learning-order` | 2 (`bootstrap_consistency` + `frozen_encoder_convergence`) | Aristotle job `f9906716` queued (non-existential reformulation). Check status next session. |
| `stochastic-search-bounds` | **0** ✅ | Focus project. Two submission blockers: .bib file + LaTeX conversion. |
| `simplicial-latent-geometry` | 13 | Option A chosen. OQ-6 (forward-ref) NOT yet fixed. Aristotle NOT yet submitted. |
| `stochastic-proofs-handbook` | n/a | Scripts only |

## Next Priorities

1. **simplicial OQ-6:** Fix forward-ref — move `incBeta_*` + `volumeFill_div_volumeEmpty_le_one_ge2` block before line 2296 in `SimplicialDetection.lean`, then `lake build`
2. **simplicial:** Submit Aristotle job for matchRadius chain (OQ-3) — use `my_theorems/proof_strategy.md` and prompt from OQ-3
3. **stochastic:** Create `references.bib` from 23 prose citations in `paper_draft.md` lines 430–467
4. **stochastic:** Convert `paper_draft.md` → `paper_draft.tex` with preamble + `\bibliography{references}`
5. **jepa:** Check `f9906716` status — if complete, cherry-pick + wire into `JEPA_rho_ordering` (OQ-5)
