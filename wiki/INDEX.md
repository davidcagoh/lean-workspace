# Wiki Index — lean-projects

## Files

| File | When to read |
|---|---|
| `INDEX.md` (this file) | Start of every session — status, open questions, next priorities |
| `session-log.md` | Start of every session — top entry for latest state |
| `decisions.md` | Before making architectural or proof-strategy choices |
| `lean4-reference.md` | Before writing any Lean — type conventions, Mathlib API, pitfalls, termination patterns |
| `aristotle-strategy.md` | Before submitting to Aristotle — sizing, statement quality, merging, domain patterns |

> **Rule:** all project state (sorry counts, open Aristotle jobs, next steps) lives in this file.
> Project CLAUDE.md files contain architecture and pitfalls only — not status.

### Handbook
`stochastic-proofs-handbook/` is scripts-only. All knowledge is in this wiki.

### Paper drafts — naming convention
Each lean project has a canonical paper draft at `my_theorems/paper_draft.md`. Supporting docs sit alongside it.
- `jepa-learning-order/my_theorems/paper_draft.md` — "Conditional" title, 767L source (v2)
- `jepa-learning-order/my_theorems/paper.tex` — LaTeX, **14pp, compiles clean (session 24); `\leanverified{…}` catalog + Appendix B axiom status**
- `stochastic-search-bounds/my_theorems/paper_draft.md` — Manuscript v6 source
- `stochastic-search-bounds/my_theorems/paper.tex` — LaTeX, **18pp, compiles clean (session 23: Winston-star rewrite); Appendix A Lean verification catalog + Appendix B Lean signatures**
- `simplicial-latent-geometry/my_theorems/paper_draft.md` — Strategy 2 draft, §5 updated
- `simplicial-latent-geometry/my_theorems/paper.tex` — LaTeX, **16pp (session 20); all `\lean{}`/`\leanverified{}` pointers resolve to sorry-free lemmas; compiles clean**
- `simplicial-latent-geometry/my_theorems/proof_strategy.md` — active proof strategy (481L)

### Workspace repo
`lean-projects/` is now `davidcagoh/lean-workspace` (private) — tracks wiki/, scripts/, stochastic-proofs-handbook/, CLAUDE.md. The three proof projects are excluded (.gitignore) and remain independent repos.

---

## Status (2026-04-30 — session 29)

| Project | Sorries | Status |
|---|---|---|
| `jepa-learning-order` | **0** ✅ | **15pp paper.tex, compiles clean. 0-sorry language, Sobal2022+Lejepa2025 citations added. Aristotle job C (`b061ab0f`) in flight for uniform hPD_lower.** arXiv-ready. |
| `stochastic-search-bounds` | **0** ✅ | **18pp paper.tex, compiles clean (session 23). Aristotle fc0719d6 merged. lake build 8034 jobs.** arXiv-ready. |
| `simplicial-latent-geometry` | **3 dead-code only** ✅ | Unchanged from session 20. 16pp paper.tex ready for arXiv. |
| `stochastic-proofs-handbook` | n/a | Scripts only |

---

## Open Questions

### OQ-15: JEPA — Job C `b061ab0f` uniform_pd_lower_from_compactness (session 29)

Submitted 2026-04-30. Target: `uniform_pd_lower_from_compactness` in `BootstrapLemmas.lean` — compactness argument giving uniform c₀ over [0, t_max] from `pd_lower_from_offDiag`. On success: integrate and remove `hPD_lower` as named hypothesis from `JEPA_rho_ordering`.
Retrieve: `python ../stochastic-proofs-handbook/scripts/retrieve.py`

---

### OQ-14: JEPA — Job B `pd_lower_from_offDiag` ✅ DONE (session 28)

Job `53f7f1b1` landed. Proof via Frobenius submultiplicativity + Gershgorin det ≠ 0.
Key finding: hypothesis strengthened from `δ*√d < c_w/2` to `δ*(d-1) < c_w`.
PDLowerHelpers.lean added with 6 helper lemmas. Build clean.
**Action needed:** update paper.tex Appendix B hypothesis statement.

---

### OQ-13: JEPA — Aristotle Job A `697611e0` ✅ DONE (session 26)

Both sorries proved and cherry-picked into `BootstrapLemmas.lean`:
- `offDiag_ftc` — proved via compactness on compact interval [0, t_max] (fun_prop + IsCompact.exists_bound_of_continuousOn)
- `tracking_bound_from_gronwall` — proved via `contractive_gronwall_decay` + `Real.rpow_sub` arithmetic

Note: `offDiag_ftc` proof uses a compactness bound (K may depend on ε); mathematically sufficient for the existential but K is not ε-independent. `hoff_small` can be derived in `JEPA_rho_ordering` once Job B (`pd_lower_from_offDiag`) also lands.

---

### OQ-12: stochastic-search-bounds — T2 `hcorrect_better` weakening (design-before-submit)

Before submitting to Aristotle, pick a concrete weaker sufficient condition. Candidates:
1. **Locality:** require ordering only at OR nodes on actual proof paths.
2. **Greedy-wrt-value:** require `π'` greedy wrt per-subtree `V(T) = successProb(π', T, ·)`.
3. **Zero-on-incorrect:** require `π'(nid, i) = 0` for incorrect children.

Option 2 is the cleanest research target. Action: pick one, formalise, scaffold, submit.

---

### OQ-11: stochastic-search-bounds — Aristotle Job `fc0719d6` (T4 sharp regime)

Submitted 2026-04-24 (session 22). Target: `sum_prod_erase_le_one_of_sum_le_one` and `sequential_le_parallel_sharp` in `Theorem4_Strong.lean`, replacing `q(i) ≤ 1/2` with sharp `∑ q(i) ≤ 1`.
Retrieve: `python scripts/retrieve.py`. On success: upgrade Prop 4.15 to sharp form.

---

### OQ-7: Publication strategy — venue targets for all three papers

1. **JEPA** → ICLR theory / COLT / TMLR (arXiv-ready; 1 sorry remaining in JEPA.lean)
2. **Stochastic-search-bounds** → ITP / CPP 2026 (0 sorries; confirm deadline first)
3. **Simplicial** → RSA via Wiley ScholarOne after arXiv ID assigned
4. **Methodology paper** ("Aristotle-Assisted Formalization") → NeurIPS / ITP (all three as case studies)

---

### OQ-6: simplicial — `volumeFill_div_le_one'` forward-reference sorry (line 2296)

Forward reference to `volumeFill_div_volumeEmpty_le_one` (line 3479) — Lean 4 rejects. Fix: move `incBeta_*` block earlier in the file (Option A) or duplicate inline (Option B). Not an Aristotle job.

---

### OQ-1: Paper submission venue for `jepa-learning-order`

Strategic advice in `jepa-learning-order/CLAUDE.md` recommends submitting soon — "first machine-checked learning-dynamics result" claim has time value. One named sorry (`bootstrap_consistency`) is a strong position.

---

*Resolved: OQ-10 (chebyshev_ratio, session 19), OQ-9 (geomCov, session 11), OQ-8 (fillingProb, session 9), OQ-5 (frozen_encoder_convergence, session 20), OQ-3 (matchRadius, session 6), OQ-2 (SSB sorry count, session early) — see session-log for details.*

---

## Next Priorities

1. **JEPA — retrieve Aristotle job `b061ab0f`** (uniform_pd_lower_from_compactness); integrate to remove `hPD_lower` from main theorem.
2. **JEPA — wire `hPhaseA`** via `frozen_encoder_convergence` (deferred mechanical step).
3. **JEPA — arXiv upload:** 15pp paper.tex compiles clean, 0 sorries. Ship now.
4. **Stochastic-search-bounds — arXiv upload:** 18pp ready. Confirm OQ-7 (ITP/CPP 2026 deadline) first.
5. **Simplicial — arXiv upload:** 16pp ready.
6. **Simplicial — RSA submission:** PDF via Wiley ScholarOne after arXiv ID assigned.
7. **Forward-cites triage (SSB):** Boige-Boumaza-Scherrer, Ito-Suzuki 2024, Chrestien-Pevný-Edelkamp 2023 flagged.
