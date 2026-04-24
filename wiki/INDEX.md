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
- `simplicial-latent-geometry/my_theorems/paper.tex` — LaTeX version, **16pp (session 20: Def 2.3 aligned with Lean's nerve-only F, Thm 4.4(b) softened to statistic-level TV, §5 restructured into 3 clean subsections, 4 new refs, new covariance identity `geomCov = Cov(∏(A_e−p), F)` in §5.1); all `\lean{...}`/`\leanverified{...}` pointers resolve to sorry-free lemmas; compiles clean**
- `simplicial-latent-geometry/my_theorems/proof_strategy.md` — active proof strategy (481L)

### Workspace repo
`lean-projects/` is now `davidcagoh/lean-workspace` (private) — tracks wiki/, scripts/, stochastic-proofs-handbook/, CLAUDE.md. The three proof projects are excluded (.gitignore) and remain independent repos.

## Status (2026-04-24 — session 20)

| Project | Sorries | Status |
|---|---|---|
| `jepa-learning-order` | **1** (`bootstrap_consistency` only) ✅ | Paper updated. Build clean. Ready for vet. |
| `stochastic-search-bounds` | **0** ✅ | Paper complete. LaTeX/bib pending (post-vet). |
| `simplicial-latent-geometry` | **3 dead-code only** ✅ | Build unchanged from session 19. **Paper expository pass completed** — Def 2.3 realigned to Lean's nerve-only F (fixing a genuine definitional mismatch), Thm 4.4(b) scope softened to statistic-level, §5 restructured 3→3 cleaner subsections, new `geomCov = Cov(∏(A_e−p), F)` identity derived, 4 new citations added (Brennan-Bresler-Huang, Litvak, Perkins, Yu-Zadik-Zhang). 16pp, compiles clean. |
| `stochastic-proofs-handbook` | n/a | Scripts only |

## Next Priorities

1. **Simplicial — typography skim:** one visual pass through rendered 16-page PDF for any lingering indent/spacing inconsistencies before arXiv upload.
2. **Simplicial — arXiv upload:** `paper.tex` + `references.bib` (16pp) ready.
3. **Simplicial — RSA submission:** PDF via Wiley ScholarOne after arXiv ID assigned.
4. **Simplicial — optional power-comparison evaluation:** worth one focused session to verify above-`d*` dominance of edge-only statistic numerically for small `d`? Would strengthen §5.1.
5. **OQ-9 (geomCov decay rate):** still the bottleneck for sharp-threshold and quantitative power comparison. Referenced in new §5.3.
6. **OQ-7:** JEPA and stochastic-search-bounds venue targets still open.
7. **JEPA:** Wire `frozen_encoder_convergence` into `JEPA_rho_ordering` (discharge `hPhaseA`) — low urgency.
