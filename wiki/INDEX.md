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

## Status (2026-05-01 — session 38)

| Project | Sorries | Status |
|---|---|---|
| `jepa-learning-order` | **3 (bernoulli_laurent_bound h_gronwall + h_laurent + laurent_separation_dominates)** | **Job J `b94c82bd` cherry-picked (`62392e4`).** `bernoulli_laurent_bound` proved structurally: Gronwall comparison (sorry'd) + Laurent (named sorry) + triangle inequality. **`JEPA_dynamics_ordering` assembled (`4d3c920`)**: composes `actual_critical_time` × 2 + `laurent_separation_dominates` (new named sub-lemma) + `linarith`. **Aristotle Job K `47230570` in flight** — `laurent_separation_dominates` (ε-asymptotic algebra). Build clean (8035 jobs). See OQ-17. |
| `stochastic-search-bounds` | **0** ✅ | **18pp paper.tex, compiles clean (session 23). Aristotle fc0719d6 merged. lake build 8034 jobs.** arXiv-ready. |
| `simplicial-latent-geometry` | **3 dead-code only** ✅ | 16pp paper.tex done. **arXiv held — Cook requested pre-arXiv expansion (OQ-16): optimality + sparse regime.** |
| `stochastic-proofs-handbook` | n/a | Scripts only |

---

## Open Questions

### OQ-14: JEPA — Job B `pd_lower_from_offDiag` ✅ DONE (session 28)

Job `53f7f1b1` landed. Proof via Frobenius submultiplicativity + Gershgorin det ≠ 0.
Key finding: hypothesis strengthened from `δ*√d < c_w/2` to `δ*(d-1) < c_w`.
PDLowerHelpers.lean added with 6 helper lemmas. Build clean.
paper.tex already reflects `δ(d-1) < c_w` at lines 661 and 1593. No further action.

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

### OQ-16: simplicial — pre-arXiv expansion (Cook request, 2026-04-30)

Nick Cook wants two extensions before arXiv:
1. **Low-degree optimality** of τ_f (BB24-style for the simplicial setting).
2. **Sparse regime** `p → 0` / `p = p(d)` (LMSY 2111.11316 model).

Roadmap: `simplicial-latent-geometry/my_theorems/roadmap_pre_arxiv.md`.

**Track A — DONE pen-and-paper (session 31).** `analytic_decay_rate.md`:
- `\phi(1/3 - \epsilon) = 1 - 36\epsilon^2` *exactly* on `[0, 1/12]` (Stevens 1939).
- `1 - fillingP(p,d) = 4\log(3/2)\,|\log p|\,\eta^2(1+O(\eta))`, `\eta = 1 - d/d^*(p)`.
- 8-term `geomCov` collapse: `geomCov = (1-q)\gamma^d + 3p^3[(7r/2)^d - q]`. Wedge term vanishes by 1D Helly.
- Final rate: `geomCov ≍ (1-q)\gamma(r)^d ≍ (3/4)^d p^2` deep in regime.
- Sparse threshold: `p_n \gg n^{-3/4}` for fixed `d`.

**Status (session 31, end):**
- ✅ 5 Lean stubs landed in `SimplicialDetection.lean` (lines 691–820), build clean.
- ✅ **Aristotle Job 1 (sim-A5-primitives) IN FLIGHT: `43761387-672d-4007-9a74-aefd8efb068d`.** Targets `wedge_implies_fill`, `gamma_pow_eq`, `mu_e_pow_eq`, `fillingProb_eq_low_r`. Email-on-completion.
- ✅ Paper deltas drafted in `my_theorems/paper_delta_OQ16.md` (§5.1 quantitative decay, §5.2 sparse corollary, §5.3 low-degree, §5.4 sub-regime open problem, Stevens 1939 bib entry).
- ⚠️ **Decision Point 2 hit (Track C C3, session 31).** Pure-fill pair statistic `τ_ff = ∑_{shared-edge t,t'} (F_t-q)(F_{t'}-q)` appears to beat `τ_f` by `n^{1/2} · 2.07^d` in the deep regime — see `fourier_setup.md` §C3-C4. If correct, **τ_f is NOT low-degree optimal**; the paper's planned §5.3 "Theorem 6.1: τ_f optimal" must be reframed to "there exists a strictly better test". Calculation needs independent verification before telling Cook.

**Next (when Aristotle returns):**
1. `python ../stochastic-proofs-handbook/scripts/retrieve.py` for job `43761387`.
2. Cherry-pick PASS into `SimplicialDetection.lean`, `lake build`, commit.
3. Submit Job 2 (sim-A5-assembly: `geometricCov_eq_deep`, `geometricCov_decay_rate_le`).
4. **Verify τ_{ff} > τ_f finding** — check arithmetic in `fourier_setup.md` §C3-C4 by hand, then numerically.
5. If verified, draft revised §5.3 + send Cook a note describing the new test.

---

### OQ-6: simplicial — `volumeFill_div_le_one'` forward-reference sorry (line 2296)

Forward reference to `volumeFill_div_volumeEmpty_le_one` (line 3479) — Lean 4 rejects. Fix: move `incBeta_*` block earlier in the file (Option A) or duplicate inline (Option B). Not an Aristotle job.

---

### OQ-1: Paper submission venue for `jepa-learning-order`

Strategic advice in `jepa-learning-order/CLAUDE.md` recommends submitting soon — "first machine-checked learning-dynamics result" claim has time value. One named sorry (`bootstrap_consistency`) is a strong position.

---

### OQ-17: JEPA — close conceptual gap (dynamics-level ordering) — **NEW (session 31)**

User's goal: prove that the *actual* JEPA training dynamics obey the
$\rho^*$-ordering, not just the formula-level ordering. Audit of Section 6
of the paper draft against Littwin 2024 (`literature/2407.03475v1.pdf`,
Theorem 4.5) revealed the previous formula
$\tilde t^* \approx L/(\lambda\rho^{2L-2}\varepsilon^{1/L})$ is the n=1
Laurent term (not leading); leading is $L/((2L-1)\lambda\varepsilon^{(2L-1)/L})$,
$\rho$-independent. Ordering enters at the n=1 term as predicted.
Section 6 rewritten to drop Prediction 6.1 in favour of four target
theorems. Five Lean stubs added; full proof plan in
`jepa-learning-order/my_theorems/strongest_result_roadmap.md`. Aristotle
Jobs E, F.1, F.2, F.3, G + assembly form the path to closing it.

**Session 35 update:** Job G's first proof (`862881a0`) was witness-K-vacuous —
`K = (|E|+1)/ε^{-(L-2)/L}`. Path (1) chosen: lemma signature refactored to hoist
`K` outside `∀ ε, ∀ Wbar` so K depends only on `(dat, eb, L, t_max, p, r, C)`.
Sorry restored. **Aristotle Job H `b1224de3` submitted** with the genuine
monotone-sandwich strategy (`my_theorems/job_H_sandwich_prompt.md`).

**Session 36 update: Job H retrieved — TWO NEW EVASION PATTERNS caught, DO NOT cherry-pick.**
1. **Wrong exponent**: Job H changed `-(L-2)/L` → `-(2L-1)/L` to make triangle inequality work.
   This breaks `JEPA_dynamics_ordering` (error no longer `o(ε^{-(2L-2)/L})` separation).
2. **`hWbar` never used**: proof is `|T̂ - T*| ≤ |T̂| + |T*|` (triangle inequality), no dynamics.
   Fingerprint: K has no C in it.
3. **Root cause identified**: statement with `-(L-2)/L` is FALSE without initial-condition
   hypothesis. Counterexample: Wbar=0 satisfies hWbar trivially (F(0)=0 for L≥2), T*(ε)~ε^{-(2L-1)/L}→∞ >> K*ε^{-(L-2)/L}.

**Fix**: Add `hwbar_init : diagAmplitude dat eb (Wbar 0) r = epsilon` to `actual_critical_time` signature.
With this, Step 1 (Grönwall: |T̂-T₀|) and Step 2 (Laurent: |T₀-T_Laurent|) both close.
Step 2 may be left as a named `sorry` (`h_bernoulli_laurent`).

**Aristotle Job I `d9d21ce9` — RETRIEVED AND CHERRY-PICKED (session 37, commit `1e52e17`).**
`actual_critical_time` proved: Gronwall sandwich delegated to `bernoulli_laurent_bound` (named sorry).
Build clean (8035 jobs).

**Aristotle Job J `b94c82bd` — RETRIEVED AND CHERRY-PICKED (session 38, commit `62392e4`).**
`bernoulli_laurent_bound` proved structurally: `h_gronwall` (Picard-Lindelöf existence + Gronwall) and `h_laurent` (Littwin 2024 Thm 4.5) as internal named sorries; Step 3 closes via triangle inequality + exponent comparison + K = K₁ + K₂. Audit pass on all 8 fingerprints.

**`JEPA_dynamics_ordering` ASSEMBLED (session 38, commit `4d3c920`).** Refactored signature with `hinit_r/s` (diagonal-amplitude initial conditions) + `hode_r/s` (perturbed Bernoulli ODE bounds). Proof composes `actual_critical_time` × 2 + `laurent_separation_dominates` (new named sub-lemma) + `linarith`.

**Aristotle Job K `47230570` submitted (session 38)** — `laurent_separation_dominates`. Strategy: drop all but n=2L-2 summand (each nonneg via λ_s ≤ λ_r and ρ_s < ρ_r); rewrite ε^{-(2L-2)/L} = ε^{-1} · ε^{-(L-2)/L}; choose ε_0 = min(1/2, M/(K_r+K_s)) where M = L·(1/(λ_s ρ_s) − 1/(λ_r ρ_r))/(2L−2). Prompt: `my_theorems/job_K_laurent_separation_dominates_prompt.md`.

Decision rationale: the project's stated goal is to *close*
the gap, not document it open. Also note: `jepa_critical_time_diag` (Job F)
is also vacuous — K = (|LHS|+1)/|log ε|, depends on ε. Do not build on it.

---

*Resolved: OQ-15 (uniform_pd_lower_from_compactness Job C, session 30), OQ-14 (pd_lower_from_offDiag Job B, session 28), OQ-13 (Job A offDiag_ftc + tracking_bound, session 26), OQ-10 (chebyshev_ratio, session 19), OQ-9 (geomCov, session 11), OQ-8 (fillingProb, session 9), OQ-5 (frozen_encoder_convergence, session 20), OQ-3 (matchRadius, session 6), OQ-2 (SSB sorry count, session early) — see session-log for details.*

---

## Next Priorities

1. **JEPA — retrieve Job K `47230570`** when Aristotle emails. `cd jepa-learning-order && python ../stochastic-proofs-handbook/scripts/retrieve.py 47230570-5153-479f-8da9-7ea657f8dca2`
2. **JEPA — audit Job K** before cherry-pick: (a) `ε_0` built only from `(dat, eb, L, r, s, K_r, K_s)` — no ε in witness, (b) both `hrho` and `hlam` actually consumed, (c) n=2L-2 summand extraction is genuine (not a witness trick), (d) no `decide`/`native_decide`. If genuine, cherry-pick into `MainTheorem.lean`, `lake build`, commit. JEPA sorries drop to 2.
3. **JEPA — close `bernoulli_laurent_bound` internals** (decision needed): submit jobs for `h_gronwall` (Picard-Lindelöf + Gronwall) and `h_laurent` (Littwin 2024 Thm 4.5), or accept as named "Mathlib infrastructure missing" placeholders for the paper.
4. **JEPA — paper.tex audit:** Ensure Section 6/7 reflects the assembled `JEPA_dynamics_ordering` (Theorem 6.1) signature: it takes `hinit_r/s` + `hode_r/s` + `hrho` + `hlam`.
5. **JEPA — Aristotle job D:** Derive `hDrift_bound` from chain rule on `quasiStaticDecoder` + `hWbar_slow`. (Lower priority.)
6. **JEPA — wire `hPhaseA`:** Apply `frozen_encoder_convergence` inside `JEPA_rho_ordering'`. (Lower priority.)
7. **Stochastic-search-bounds — arXiv upload:** 18pp ready. Confirm OQ-7 (ITP/CPP 2026 deadline) first.
8. **Simplicial — OQ-16 expansion (pre-arXiv):** see roadmap. Start with Track A (geomCov decay rate, A1–A3 pen-and-paper) + Track C steps C1–C2 in parallel.
9. **Simplicial — RSA submission:** PDF via Wiley ScholarOne after OQ-16 lands and arXiv ID assigned.
10. **Forward-cites triage (SSB):** Boige-Boumaza-Scherrer, Ito-Suzuki 2024, Chrestien-Pevný-Edelkamp 2023 flagged.

## Pickup notes for fresh agent (2026-05-01, after session 38)

**Context to load on session start:**
- This file (`wiki/INDEX.md`) — status + open questions + next priorities.
- `wiki/session-log.md` top entry — session 38 wrap (Job J cherry-picked; `JEPA_dynamics_ordering` assembled; Job K submitted).
- `jepa-learning-order/my_theorems/strongest_result_roadmap.md` — full proof plan.
- `jepa-learning-order/my_theorems/job_K_laurent_separation_dominates_prompt.md` — Job K prompt.
- Aristotle id in flight: `47230570` (Job K `laurent_separation_dominates`, ε-asymptotic algebra).

**Mathematical context to know:**
- **Witness-K vacuity pattern:** when `∃ K` (or `∃ ε_0`) sits inside the ε-parameterised body, the witness can absorb the bound. Always hoist outside `∀ ε`. For Job K, `ε_0` MUST be built only from `(dat, eb, L, r, s, K_r, K_s)`.
- **`bernoulli_laurent_bound` structure (session 37–38):** Gronwall step (`h_gronwall` sorry; K₁ genuine, contains C_ode) + Laurent step (`h_laurent` named sorry — Littwin 2024 Thm 4.5) + triangle on hitting times. K = K₁ + K₂ is ε-free.
- **`JEPA_dynamics_ordering` assembly (session 38):** Composes `actual_critical_time` × 2 + `laurent_separation_dominates`. Key identity: ε^{-(2L-2)/L} = ε^{-1} · ε^{-(L-2)/L}, so the Laurent gap dominates the perturbation error iff ε < M/(K_r+K_s).
- **`jepa_critical_time_diag` is vacuous:** K = (|LHS|+1)/|log ε| — K depends on ε. Do not use it as a genuine black box.

**Current sorry inventory (3 total, all intentional, all named):**
1. `JEPA.lean` `bernoulli_laurent_bound` — internal `h_gronwall` (Picard-Lindelöf + Gronwall + hitting time comparison).
2. `JEPA.lean` `bernoulli_laurent_bound` — internal `h_laurent` (Littwin 2024 Thm 4.5 — pure calculus).
3. `MainTheorem.lean` `laurent_separation_dominates` — Job K in flight (`47230570`); ε-asymptotic algebra over finite Laurent sum.

`JEPA_dynamics_ordering` itself is **structurally proved** — body has no `sorry`.

**Build status:** `lake build` succeeds (8035 jobs).

A Sonnet agent can run the workflow autonomously: retrieve → audit → cherry-pick → commit → repeat.
