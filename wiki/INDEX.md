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
- `jepa-learning-order/my_theorems/paper.tex` — LaTeX, **12pp, full rewrite (session 40, Bubeck-style); Theorem-1 cluster (a)(b)(c) on p.~3; consolidated §1.1 related work (deep-linear lineage / JEPA 2024–2026 incl. Maes2026 LeWM springboard / implicit bias / formal verification); Lean record isolated to App.~C; named axioms in App.~D**
- `stochastic-search-bounds/my_theorems/paper_draft.md` — Manuscript v6 source
- `stochastic-search-bounds/my_theorems/paper.tex` — LaTeX, **18pp, compiles clean (session 23: Winston-star rewrite); Appendix A Lean verification catalog + Appendix B Lean signatures**
- `simplicial-latent-geometry/my_theorems/paper_draft.md` — Strategy 2 draft, §5 updated
- `simplicial-latent-geometry/my_theorems/paper.tex` — LaTeX, **16pp (session 20); all `\lean{}`/`\leanverified{}` pointers resolve to sorry-free lemmas; compiles clean**
- `simplicial-latent-geometry/my_theorems/proof_strategy.md` — active proof strategy (481L)

### Workspace repo
`lean-projects/` is now `davidcagoh/lean-workspace` (private) — tracks wiki/, scripts/, stochastic-proofs-handbook/, CLAUDE.md. The three proof projects are excluded (.gitignore) and remain independent repos.

---

## Status (2026-05-01 — session 42)

> Session 42: simplicial Job 1b retrieved + cherry-picked (commit `72c3377`). 3 of 4 TorusIntegrals lemmas proved (`volume_closedBall_inter_T1`, `volume_triangleSet`, `volume_edgeFillSet`); Aristotle deferred `volume_fillSet` due to `dist = 2r` boundary. Job 1c (`0bc2c753`) submitted with strict-inequality + Fubini-ignores-measure-zero strategy. Build clean (8030 jobs).

## Status (2026-05-01 — session 41)

> Session 41 was workspace housekeeping + scoping. JEPA `my_theorems/` reorganized (`notes/`, `rho_recovery/`, `archive/` subdirs; LaTeX artifacts deleted; duplicate `.env` removed). Aristotle job prompts H/I/J/K moved out of `my_theorems/` to project-level `jepa-learning-order/requests/` alongside the existing 37 submission records. Paper-writing scripts (`verify_refs.py`, `forward_cites.py`) consolidated under `stochastic-proofs-handbook/scripts/` with documentation. Read the `rho_recovery/` handoff docs and recorded a feasibility verdict (OQ-17 below). Lean state unchanged.

## Status (2026-05-01 — session 40)

| Project | Sorries | Status |
|---|---|---|
| `jepa-learning-order` | **2 (bernoulli_laurent_bound h_gronwall + h_laurent)** | **paper.tex full rewrite (session 40, Bubeck-style).** 1686 → 1076 L, 18 → 12 pp. Crisp Theorem-1 cluster (a)(b)(c) on p. 3. Consolidated §1.1 related work into 4 thematic clusters: deep-linear lineage (now incl. PesmeFlammarion2023, BoixAdsera2023, SaxeNeuralRace2022), JEPA 2024–2026 (now incl. **Maes2026 / LeWM springboard**), implicit bias (Yang2021Tensor, Tian2021BYOL, Halvagal2023, Tian2024, Gunasekar2017), formal verification of learning theory (Bagnall2019, Tassarotti2021). Lean record isolated to App. C. Verified all 34 bib entries via verify_refs.py — 3 fixes applied (Bardes2024 V-JEPA actual title, Aristotle2024 IMO title, Tian2024 venue). Forward_cites only resolved Arora2019 (587 cites); 3 high-value additions surfaced. Build state unchanged (Lean: 8036 jobs, sorry inventory unchanged). |
| `stochastic-search-bounds` | **0** ✅ | **18pp paper.tex, compiles clean (session 23). Aristotle fc0719d6 merged. lake build 8034 jobs.** arXiv-ready. |
| `simplicial-latent-geometry` | **3 dead-code only** ✅ | 16pp paper.tex done. **arXiv held — Cook requested pre-arXiv expansion (OQ-16): optimality + sparse regime.** |
| `stochastic-proofs-handbook` | n/a | Scripts only |

---

## Open Questions

### OQ-17: JEPA — $\rho^*$-recovery extension (feasibility verdict, session 41)

Roadmap (`jepa-learning-order/my_theorems/paper2_recovery/roadmap.md`, March 2026 by David; moved from `rho_recovery/` mid-session 41) defines 5 layers and 9 gaps from the current $\rho^*$-ordering paper to a full recovery theorem (sign + magnitude + finite-sample rates). Honest assessment after a session-41 read:

**Likely tractable (Layers 1–2):**
- **1.1 / 1.2** — quasi-static ODE rigorous statement + non-vacuous feature ordering. These overlap heavily with what's already in `paper.tex` and the `actual_critical_time` / `JEPA_dynamics_ordering` / `bernoulli_laurent_bound` lineage (Jobs G/I/J/K). The math is in hand; mostly Lean-engineering. **High odds.**
- **2.1** — generalised diagonal ODE in the $(\mathbf{u}_r^*, \mathbf{v}_r^*)$ basis. Already informally in the proof lecture; reduces to Lemma 3.1 + Theorem 7.3 + Arora 2019 balancedness. **Medium-high odds** (likely a single Aristotle job once 1.1/1.2 are clean).
- **2.2** — identifiability / inversion formula. Algebraic inversion of Corollary 6.2. **High odds** as a paper result; Lean formalisation requires the leading-order asymptotic, which is the same flavour as `laurent_separation_dominates`.

**Plausible with effort (Layer 3):**
- **3.1** — Davis–Kahan / Wedin perturbation for the *non-symmetric* generalised eigenproblem under sample noise. Standard but Mathlib's coverage of generalised / non-self-adjoint perturbation theory is limited. **Medium odds** for paper-level; **low odds** for Lean within a reasonable horizon — would likely need new Mathlib infrastructure (which David should not block on).
- **3.2** — end-to-end finite-sample rate. Combines 2.2 + 3.1 by union bound. **Medium odds** as paper; depends on 3.1.

**Hard / structurally novel (Layers 4–5):**
- **4.1** — signed-$\rho$ ODE analysis. The $\rho^* < 0$ case changes the qualitative picture: Bernoulli ODE coefficient flips sign, fixed-point analysis is different. Genuinely new dynamics work. **Medium odds** as paper, **low odds** for Lean (the existing `bernoulli_laurent_bound` would not transfer; need a separate suppression-timescale argument).
- **4.2 / 5.1** — signed-$\rho$ recovery + mixed-sign ordering. Statement (iii) of 4.2 already concedes $|\rho^*|$ for negative features is *not* recoverable from JEPA dynamics alone; it falls back to direct covariance estimation. So the headline "JEPA recovers $\rho^*$" is qualified — half the result is just classical covariance estimation, not a JEPA result. This weakens the framing.

**Verdict.** Layers 1–2 are the natural next paper after the current $\rho^*$-ordering submission; **strong probability of getting it done within a session arc** (likely 4–8 sessions, assuming Aristotle keeps cooperating on the leading-order asymptotic lemmas). Layer 3 is reasonable as a paper but the Lean version stalls on Mathlib gaps. Layer 4 is genuinely new mathematics — feasible but a real research project, not formalisation. Layer 5 is mostly bookkeeping after 4.

**Strategic call.** Treat the current paper as one deliverable; treat **Layers 1–2 of recovery as the natural sequel** (a targeted second paper, "$\rho^*$-Recovery for Linear JEPA"). Layers 3–5 should be flagged as future work in that paper's discussion, not promised. Don't conflate the recovery roadmap into the current submission — the ordering result stands on its own and is what's actually proved.

**Action:** none yet. Revisit after the current paper is on arXiv. When ready, draft a new request prompt deriving Theorem 2.2 (identifiability via leading-order $\tilde t_r^*$ inversion) — likely the smallest new Aristotle target that yields a publishable advance.

---

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

**Status (2026-05-01, session 34):**
- ✅ 5 Lean stubs landed in `SimplicialDetection.lean`, build clean.
- ✅ **Job 1 (`43761387`) RETRIEVED + cherry-picked (commit `902914e`).** All 4 target lemmas closed via new helper `TorusIntegrals.lean` (410L: transpose measure-preservation, indicator algebra, R-line integrals 3r²/7r²). Build clean (8030 jobs).
- ✅ **Job 1b (`b28b078b`) RETRIEVED + cherry-picked (commit `72c3377`, session 42).** 3 of 4 lemmas closed: `volume_closedBall_inter_T1`, `volume_triangleSet`, `volume_edgeFillSet`. `volume_fillSet` deferred due to `dist = 2r` codim-1 boundary issue. TorusIntegrals.lean grew 478 → 814L with `fill_fiber_*` helper infrastructure.
- 🔄 **Job 1c (`0bc2c753-143e-4e3a-8f7d-15993f793148`) IN FLIGHT (session 42).** Targets `fill_fiber_volume_lt` (strict `b < 2r`) and `volume_fillSet`. Strategy: closedBall sandwich on strict subdomain + Fubini-ignores-measure-zero on `{dist = 2r}`. New helper `integral_4r_minus_abs_2r` for outer integral `12r²`. Email-on-completion.
- ✅ Paper deltas drafted in `my_theorems/paper_delta_OQ16.md` (§5.1 quantitative decay, §5.2 sparse corollary, §5.3 low-degree, §5.4 sub-regime, Stevens 1939 bib).
- ⚠️ **Decision Point 2 still open (Track C C3).** Pure-fill pair statistic `τ_ff` appears to beat `τ_f` by `n^{1/2} · 2.07^d` deep in regime — see `fourier_setup.md` §C3-C4. If verified, paper §5.3 must be reframed. Needs hand + numerical verification before telling Cook.

**Next (when Job 1b returns):**
1. `python ../stochastic-proofs-handbook/scripts/retrieve.py b28b078b-543c-46cd-a341-a0126251d735`.
2. Cherry-pick PASS into `TorusIntegrals.lean`, `lake build`, commit.
3. Submit Job 2 (sim-A5-assembly: `geometricCov_eq_deep`, `geometricCov_decay_rate_le`).
4. **Verify τ_{ff} > τ_f** — check `fourier_setup.md` §C3-C4 by hand, then numerically (try `(n,p,d)=(1000, 0.01, 3)`).
5. If verified, draft revised §5.3 + draft Cook note (DO NOT email autonomously).

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

**Aristotle Job K `47230570` — RETRIEVED AND CHERRY-PICKED (session 39, commit `05adbd0`).**
`laurent_separation_dominates` proved. New file `LaurentHelpers.lean` (5 helpers: `projectedCovariance_pos`, `projCov_mul_rho_strict_lt`, `projCov_mul_rho_pow_le`, `Finset.sum_sub_ge_single`, `rpow_two_L_minus_two_split`). Audit pass: ε_0 from `(dat, eb, L, r, s, K_r, K_s)` only; both `hrho` and `hlam` consumed; n=2L-2 extracted via `Finset.single_le_sum`; no `decide`/`native_decide`/`admit`.

**`JEPA_dynamics_ordering` chain is structurally complete.** Theorem 6.1 has no `sorry` in body. Two remaining sorries are both internal to `bernoulli_laurent_bound`: `h_gronwall` (Picard-Lindelöf + Gronwall + hitting time comparison) and `h_laurent` (Littwin 2024 Thm 4.5 — pure calculus). Both are standard ODE/Laurent facts left implicit in informal learning-theory papers — paper-ready under CompCert convention. Decision pending on whether to submit Aristotle jobs for them or document as named axioms.

Decision rationale: the project's stated goal is to *close*
the gap, not document it open. Also note: `jepa_critical_time_diag` (Job F)
is also vacuous — K = (|LHS|+1)/|log ε|, depends on ε. Do not build on it.

---

*Resolved: OQ-15 (uniform_pd_lower_from_compactness Job C, session 30), OQ-14 (pd_lower_from_offDiag Job B, session 28), OQ-13 (Job A offDiag_ftc + tracking_bound, session 26), OQ-10 (chebyshev_ratio, session 19), OQ-9 (geomCov, session 11), OQ-8 (fillingProb, session 9), OQ-5 (frozen_encoder_convergence, session 20), OQ-3 (matchRadius, session 6), OQ-2 (SSB sorry count, session early) — see session-log for details.*

---

## Next Priorities

1. **JEPA — paper.tex rewritten (session 40).** 12 pp, Bubeck-style. Theorem-1 cluster up front, consolidated related work, Maes2026 LeWM integrated as springboard, Lean record in App. C, named axioms in App. D per CompCert. Verified all 34 bib entries; 3 high-value forward-cite additions integrated. **Ready for arXiv.**
2. **JEPA — arXiv submission.** Paper ready. Confirm OQ-7 venue (ICLR theory / COLT / TMLR) before upload.
3. **JEPA — Aristotle job D:** Derive `hDrift_bound` from chain rule on `quasiStaticDecoder` + `hWbar_slow`. (Lower priority — not required for arXiv.)
4. **JEPA — wire `hPhaseA`:** Apply `frozen_encoder_convergence` inside `JEPA_rho_ordering'`. (Lower priority — not required for arXiv.)
6. **Stochastic-search-bounds — arXiv upload:** 18pp ready. Confirm OQ-7 (ITP/CPP 2026 deadline) first.
7. **Simplicial — OQ-16 expansion (pre-arXiv):** see roadmap. Start with Track A (geomCov decay rate, A1–A3 pen-and-paper) + Track C steps C1–C2 in parallel.
8. **Simplicial — RSA submission:** PDF via Wiley ScholarOne after OQ-16 lands and arXiv ID assigned.
9. **Forward-cites triage (SSB):** Boige-Boumaza-Scherrer, Ito-Suzuki 2024, Chrestien-Pevný-Edelkamp 2023 flagged.

## Pickup notes for fresh agent (2026-05-01, after session 41)

**Context to load on session start:**
- This file (`wiki/INDEX.md`) — status + open questions + next priorities.
- `wiki/session-log.md` top entry — session 41 wrap (JEPA my_theorems reorg; paper-writing scripts moved to handbook).
- `jepa-learning-order/my_theorems/notes/strongest_result_roadmap.md` — full proof plan (note: now under `notes/` after session 41 reorg).
- No Aristotle jobs in flight.

**Mathematical context to know:**
- **Witness-K vacuity pattern:** when `∃ K` (or `∃ ε_0`) sits inside the ε-parameterised body, the witness can absorb the bound. Always hoist outside `∀ ε`. For Job K, `ε_0` MUST be built only from `(dat, eb, L, r, s, K_r, K_s)`.
- **`bernoulli_laurent_bound` structure (session 37–38):** Gronwall step (`h_gronwall` sorry; K₁ genuine, contains C_ode) + Laurent step (`h_laurent` named sorry — Littwin 2024 Thm 4.5) + triangle on hitting times. K = K₁ + K₂ is ε-free.
- **`JEPA_dynamics_ordering` assembly (session 38):** Composes `actual_critical_time` × 2 + `laurent_separation_dominates`. Key identity: ε^{-(2L-2)/L} = ε^{-1} · ε^{-(L-2)/L}, so the Laurent gap dominates the perturbation error iff ε < M/(K_r+K_s).
- **`jepa_critical_time_diag` is vacuous:** K = (|LHS|+1)/|log ε| — K depends on ε. Do not use it as a genuine black box.

**Current sorry inventory (2 total, both intentional, both named):**
1. `JEPA.lean` `bernoulli_laurent_bound` — internal `h_gronwall` (Picard-Lindelöf + Gronwall + hitting time comparison).
2. `JEPA.lean` `bernoulli_laurent_bound` — internal `h_laurent` (Littwin 2024 Thm 4.5 — pure calculus).

`JEPA_dynamics_ordering` (Theorem 6.1) and `laurent_separation_dominates` are **fully proved** — bodies have no `sorry`.

**Build status:** `lake build` succeeds (8036 jobs).

A Sonnet agent can run the workflow autonomously: retrieve → audit → cherry-pick → commit → repeat.
