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
- `jepa-learning-order/my_theorems/paper_draft.md` — "Conditional" title, 767L source (v2)
- `jepa-learning-order/my_theorems/paper.tex` — LaTeX version, **13pp, compiles clean (session 21); `\leanverified{…}` catalog + Appendix B axiom status**
- `stochastic-search-bounds/my_theorems/paper_draft.md` — Manuscript v6 source
- `stochastic-search-bounds/my_theorems/paper.tex` — LaTeX version, **17pp, compiles clean (session 22: reframe + Thm 1 root-only weakening); Appendix A Lean verification catalog with paper-to-Lean map + Appendix B Lean signatures**
- `simplicial-latent-geometry/my_theorems/paper_draft.md` — Strategy 2 draft, §5 updated
- `simplicial-latent-geometry/my_theorems/paper.tex` — LaTeX version, **16pp (session 20: Def 2.3 aligned with Lean's nerve-only F, Thm 4.4(b) softened to statistic-level TV, §5 restructured into 3 clean subsections, 4 new refs, new covariance identity `geomCov = Cov(∏(A_e−p), F)` in §5.1); all `\lean{...}`/`\leanverified{...}` pointers resolve to sorry-free lemmas; compiles clean**
- `simplicial-latent-geometry/my_theorems/proof_strategy.md` — active proof strategy (481L)

### Workspace repo
`lean-projects/` is now `davidcagoh/lean-workspace` (private) — tracks wiki/, scripts/, stochastic-proofs-handbook/, CLAUDE.md. The three proof projects are excluded (.gitignore) and remain independent repos.

## Status (2026-04-29 — session 24)

| Project | Sorries | Status |
|---|---|---|
| `jepa-learning-order` | **1** in JEPA.lean + **3** in BootstrapLemmas.lean (Job A `697611e0` in flight) | **paper.tex 14pp, compiles clean. `bootstrap_consistency` decomposed into 3 sub-lemmas: `offDiag_ftc` + `tracking_bound_from_gronwall` (Job A pending) + `pd_lower_from_offDiag` (Job B, after A). Key insight: gradV is linear in V — off-diagonal bound needs no bootstrap, just FTC.** arXiv-ready. |
| `stochastic-search-bounds` | **0** ✅ | **paper.tex 18pp, compiles clean (session 23: Winston-star rewrite complete). Aristotle fc0719d6 merged. lake build 8034 jobs. references.bib (40 entries).** arXiv-ready. |
| `simplicial-latent-geometry` | **3 dead-code only** ✅ | Unchanged from session 20. 16pp paper.tex ready for arXiv. |
| `stochastic-proofs-handbook` | n/a | Scripts only |

## Next Priorities

1. **JEPA — retrieve Job A** (`697611e0-f2b0-4bd1-9520-c61cb8bcd447`): `aristotle result 697611e0` — cherry-pick `offDiag_ftc` + `tracking_bound_from_gronwall` if genuine.
2. **JEPA — submit Job B** (`pd_lower_from_offDiag`): prompt in `help_from_aristotle/21_bootstrap_request.md`.
3. **Stochastic-search-bounds — arXiv upload:** 18pp ready. Confirm OQ-7 (ITP/CPP 2026 deadline) first.
4. **Simplicial — arXiv upload:** 16pp ready.
5. **JEPA — arXiv upload:** 14pp ready. Ship as "conditional"; Jobs A+B landing would strengthen the story.
6. **Simplicial — RSA submission:** PDF via Wiley ScholarOne after arXiv ID assigned.
7. **Forward-cites triage (stochastic-search-bounds):** Boige-Boumaza-Scherrer, Ito-Suzuki 2024, Chrestien-Pevný-Edelkamp 2023 flagged.
8. **OQ-7:** Venue targets for all three papers still open.
9. **JEPA long-term:** `bootstrap_consistency` in JEPA.lean stays sorry'd until Jobs A+B land and are wired in.
