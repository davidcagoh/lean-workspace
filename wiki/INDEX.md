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

## Status (2026-04-24 — session 21)

| Project | Sorries | Status |
|---|---|---|
| `jepa-learning-order` | **1** (`bootstrap_consistency` only) ✅ | **paper.tex 14pp, compiles clean; references.bib (22 entries, +11 from citation triage); forward_cites audit done (14,546 cites reviewed); Phase C+D complete — 4 INCLUDE + 7 DISCUSS integrated, §1.2 vs §9 coherent; all 17 `\leanverified{…}` resolve to axiom-clean lemmas; `JEPA_rho_ordering` `#print axioms` = `[propext, Classical.choice, Quot.sound]`.** arXiv-ready. |
| `stochastic-search-bounds` | **0** ✅ (+2 sorries in pending-Aristotle `Theorem4_Strong.lean`) | **paper.tex 17pp, compiles clean (session 22: reframed + restructured 2 thm + 2 prop; pop-motivation paragraph grounded in Aletheia whitepaper §2.2 compute-plateau quote; Thm 1 weakened to root-only via `Theorem1_Strong.lean`). Aristotle job `fc0719d6` submitted for T4 sharp regime (`∑ q ≤ 1` in place of uniform `q ≤ 1/2`); retrieve when done. references.bib (40 entries).** arXiv/ITP-ready; pending upgrade from Aristotle. |
| `simplicial-latent-geometry` | **3 dead-code only** ✅ | Unchanged from session 20. 16pp paper.tex ready for arXiv. |
| `stochastic-proofs-handbook` | n/a | Scripts only |

## Next Priorities

1. **Simplicial — arXiv upload:** paper.tex + references.bib (16pp) ready.
2. **Stochastic-search-bounds — arXiv upload:** paper.tex + references.bib (13pp) ready. Venue (OQ-7) still open.
3. **JEPA — arXiv upload:** paper.tex + references.bib (13pp) ready. Ship as "conditional" per session-21 verification report; Mathlib ODE infrastructure not blocking. Venue (OQ-7) still open.
4. **Simplicial — RSA submission:** PDF via Wiley ScholarOne after arXiv ID assigned.
5. **Forward-cites triage (all three projects):** review reports, add any high-value citations authors decide to incorporate. Stochastic-search-bounds candidates flagged: Boige-Boumaza-Scherrer "AlphaBeta is not as good as you think", Ito-Suzuki 2024 AND-OR tree equilibria, Chrestien-Pevný-Edelkamp 2023 NeurIPS planning heuristics.
6. **OQ-7:** Venue targets for all three papers still open.
7. **OQ-9 (geomCov decay rate):** still the bottleneck for simplicial sharp-threshold.
8. **JEPA long-term:** `bootstrap_consistency` remains named regularity hypothesis. Picard-Lindelöf infrastructure in Mathlib would let it be closed; separate project.
