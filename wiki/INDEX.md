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
- `simplicial-latent-geometry/my_theorems/paper.tex` — LaTeX version, **14pp, Thm 4.2 pointer now `detection_lower_bound_fixed_d` (exact match for fixed-`d` claim); all 18 `\lean{...}`/`\leanverified{...}` pointers resolve to sorry-free lemmas with clean `#print axioms`; compiles clean**
- `simplicial-latent-geometry/my_theorems/proof_strategy.md` — active proof strategy (481L)

### Workspace repo
`lean-projects/` is now `davidcagoh/lean-workspace` (private) — tracks wiki/, scripts/, stochastic-proofs-handbook/, CLAUDE.md. The three proof projects are excluded (.gitignore) and remain independent repos.

## Status (2026-04-24 — session 19)

| Project | Sorries | Status |
|---|---|---|
| `jepa-learning-order` | **1** (`bootstrap_consistency` only) ✅ | Paper updated. Build clean. Ready for vet. |
| `stochastic-search-bounds` | **0** ✅ | Paper complete. LaTeX/bib pending (post-vet). |
| `simplicial-latent-geometry` | **3 dead-code only** ✅ | `lake build` clean (8029 jobs, 0 errors). Jobs A/B/C cherry-picked. OQ-10 **resolved** — added `hNG : n·g → ∞` throughout, new `detection_lower_bound_fixed_d` matches paper's Thm 4.2 verbatim. `#print axioms` on all main-chain theorems: `[propext, Classical.choice, Quot.sound]` only, no `sorryAx`. 3 remaining sorries are in `@[deprecated]` Strategy 1 blocks, not in the active chain. |
| `stochastic-proofs-handbook` | n/a | Scripts only |

## Next Priorities

1. **Simplicial — arXiv upload:** `paper.tex` + `references.bib` (14pp). All Lean verification cleanly defensible.
2. **Simplicial — RSA submission:** PDF via Wiley ScholarOne after arXiv ID assigned.
3. **Simplicial — optional cleanup:** remove the 3 dead-code sorries at lines 385, 440, 649 (deprecated Strategy 1). Low priority.
4. **OQ-7:** JEPA and stochastic-search-bounds venue targets still open.
5. **JEPA:** Wire `frozen_encoder_convergence` into `JEPA_rho_ordering` (discharge `hPhaseA`) — low urgency.
