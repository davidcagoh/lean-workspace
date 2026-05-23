# Decisions

Design choices already locked in. Read before changing anything architectural.

---

## audits/ layout: per-refactor approach-evaluation reports at root, per-project worked examples in subdirs

**Decision date:** 2026-05-23 (session 96)

**Why:** After the JEPA-LO split (session 95) produced both per-project artifacts and a methodology-evaluation report, the report was originally nested under `audits/jepa-learning-order/`. When the simplicial split followed in session 96 with its own evaluation report, two patterns competed: (a) keep each report under its project subdir, (b) promote evaluation reports to `audits/` root. Option (b) won because the evaluation reports form a meta-arc — "how is the methodology performing across refactors?" — that should be readable end-to-end without descending into per-project trees. Per-project subdirs hold raw audit artifacts (DOTs, SVGs, decl tables, pre-execution recommendations); root-level `REPORT-YYYY-MM-DD-<refactor>.md` files hold methodology critique that informs strategy-doc evolution.

**Implication:** Future graph-audit refactors should follow this convention. Pre-execution recommendation → `audits/<project>/README.md`. Post-execution evaluation → `audits/REPORT-YYYY-MM-DD-<project>-split.md`. The strategy doc (`wiki/graph-audit-strategy.md`) links to root-level reports for "validated on N real-world refactors" claims; per-project subdirs are linked from the strategy doc's "Worked examples" table. `audits/README.md` indexes both. Do not move historical reports back into project subdirs even if their relative-path linkage looks tidier — the meta-arc readability is what's load-bearing.

---

## Graph-audit framework: validated on two real-world refactors; extraction script ready for promotion

**Decision date:** 2026-05-23 (session 96)

**Why:** JEPA-LO split (2002 LOC, 6 files, session 95) and simplicial split (5606 LOC, 15 files, session 96) both held the framework's structural predictions (cluster identity, mandatory merges, sub-package layout) within useful precision. The pre-registered ≥ 8-edge merge rule was load-bearing in both — 11-edge bond on JEPA-LO, 16-edge bond on simplicial — and both correctly prevented partition mistakes. **Structural confidence is genuinely high.** What did NOT generalize across scale was the extraction tooling: simplicial surfaced 8 distinct corner cases (regex misses, `'`-boundary bug, `private` cross-file invisibility, comment-only false edges, `open X in` placement, namespace wrapping, classical-open inference, decl-size blindness in cluster predictor) that required ~5 script iterations and ~30 minutes of build-fail-iterate to resolve. The battle-tested script lives at `audits/simplicial-latent-geometry/split_simplicial.py`.

**Implication:** If a third god-module split candidate arises (likely `TorusIntegrals.lean` 1834 LOC, next in queue), promote the script to `stochastic-proofs-handbook/scripts/split_god_module.py` with all 8 fixes pre-applied — this overturns the session-93 "don't maintain a script" decision, justified by the new evidence that the corner-case catalog has stabilized. Until that third candidate, the inline `/tmp` approach is fine and the strategy doc's "Extraction-script pitfalls" section serves as the pre-flight checklist.

---

## Axiom-promote `saxe_exact_solution_exists` (paper-1) matching paper-2's `bernoulli_exact_solution_exists`
**Decision date:** 2026-05-22 (session 94)
**Why:** Aristotle job `cd50d4c7` returned a verified counterexample to conjunct 4 (reachability) of `saxe_exact_solution_exists`. At `L=2, λ=ρ=1, ε=0.5, p=0.99999`, the hypothesis `h_t_max_reach` gives `t_max ≥ 2√2 ≈ 2.828` but RK4 integration shows the threshold reached only at `t ≈ 3.11`. Root cause: near the equilibrium `ρ^{1/L}`, the ODE speed vanishes, adding an `O(log(1/(1−p^L)))` correction unbounded as `p → 1`. The headline result fixes `p` once and for all bounded away from 1 — an Arora-era implicit assumption — so in-regime the claim is sound. Alternative options considered: (a) strengthen `h_t_max_reach` with `(1−p^L)` factor — threads `p`-dependence into every downstream caller; (b) split lemma, take f₀-reachability as separate hypothesis — paper-2 does this via axiomatization; (c) derive f₀-reachability from f-reachability via Grönwall — doesn't close cleanly (gives `τ_{f₀} ≤ τ_f + K·ε^α`, slightly worse than `t_max`). Paper-2's already-locked-in choice (`axiom bernoulli_exact_solution_exists` in `jepa-rho-recovery/JepaRhoRecovery/CriticalTime.lean:106`) is structurally identical: axiomatize Picard-Lindelöf existence + reachability as a single Path C axiom, document in CompCert convention.
**Implication:** Paper-1's `Corrected.lean` is sorry-free with 1 named axiom (`saxe_exact_solution_exists`). The saxe trio (`saxe_exact_solution_exists` axiom / `saxe_gronwall_sandwich` proved / `saxe_singlepole_asymptotic` proved) is now structurally parallel to paper-2's bernoulli trio (axiom / axiom / axiom), with paper-1 the stronger side (2 of 3 proved). Future work: if Mathlib gains packaged Picard-Lindelöf-with-hitting-time-comparison, the axiom can be retired without changing downstream callers. The `(1−p^L)` factor is documented in the axiom docstring + paper Appendix D for future-proofing.

---

## jepa-rho-recovery paper 3 (LeWM/SIGReg spinoff): framed as gradient-flow acceleration, not symmetry-breaking

**Decision date:** 2026-05-20 (session 86)

**Why:** Empirical scaffolding in `jepa-rho-recovery/experiments/` (probe + multiple sweeps + 100k-step d=300 budget probe + metric-sensitivity check) produced a sequence of conjectures that were retracted in turn: (i) "SIGReg monotonically destroys ρ*-ordering" — wrong, non-monotonic at high d; (ii) "info-theoretic floor at d=300, λ*=1.0, Spearman=-0.10" — wrong, was a training-budget artifact; (iii) "two-basin attractor with unregularised λ=0 → inverted-ordering basin" — wrong, was a metric artifact of relative-threshold critical-time on un-converged training (absolute-threshold gives Spearman = −1.00 on the same trajectory). The final picture: at d ≥ 100, unregularised JEPA is too slow to reach its theoretical plateau in any reasonable budget; SIGReg accelerates approach-to-plateau by ~7× at d=300. Pareto λ*(d) ≈ 0.001·d (linear) with d=100 → 0.1 and d=300 → 0.3. Three claims for paper 3: (i) acceleration theorem (~ d·λ for λ < λ*); (ii) over-regularisation penalty for λ > λ*; (iii) linear λ*(d) scaling.

**How to apply:** Frame paper 3 as a JEPA-acceleration story, not a basin-discovery or info-bound story. Headline conjecture is the linear Pareto λ*(d) scaling derivation from first principles — gradient pressure ~ λ·d balances against something in the unregularised dynamics; the something that gives the linear scaling is the open theoretical question. Do NOT cite the "two-basin" or "info-floor" interpretations from earlier session-86 writeups — they are superseded by the metric check in `RESULTS_session86_final.md`. Do NOT use relative-threshold critical-time as the load-bearing observable in any paper-3 claim; use the plateau-estimator (paper 2's design) or an absolute-threshold variant, both of which are metric-invariant on un-converged trajectories.

## jepa-rho-recovery: critical-time metric sensitivity — prefer plateau-based observables

**Decision date:** 2026-05-20 (session 86)

**Why:** Session-86 metric-sensitivity check revealed that relative-threshold critical-time (first step where |σ_r(t)| ≥ frac · |σ_r(t_final)|) gives the WRONG SIGN for Spearman(ρ*, t_crit) on un-converged trajectories. At d=300, λ=0 (training stuck at ~10% of theoretical plateau), relative-threshold gives Spearman = +1.0 (apparent inversion) while absolute-threshold gives Spearman = −1.0 on the SAME trajectory. The artifact mechanism: high-ρ features have larger absolute targets that take longer to reach 50% of, even with faster absolute growth. Plateau-based observables (σ_r(T)^{1/L} from paper-2's plateau estimator) sidestep the issue entirely — they read ρ_r* directly from the final value, no threshold needed.

**How to apply:** (i) Paper 2's methodology section should explicitly call out this metric caveat — additional argument for the plateau estimator as headline over the v1 critical-time inversion. (ii) Paper 3's empirical evidence MUST use either the plateau observable or absolute-threshold critical times, not relative-threshold. (iii) For any future empirical work on JEPA training dynamics, verify that the chosen "critical time" definition is robust to training-budget limitations BEFORE drawing ordering conclusions — re-run with absolute thresholds at minimum.

## jepa-rho-recovery paper 2: headline pivoted to plateau estimator (pure-trajectory)

**Decision date:** 2026-05-20 (session 86)

**Why:** The session-67 → session-85 paper outline carried a structural inconsistency between abstract and §5. The abstract claimed an estimator "computable from the training trajectory alone," but Thm 5.1 (critical-time inversion, $\hat\rho_r = (L / (\lambda_r^* \tilde t_r^* \epsilon^{1/L}))^{1/(2L-2)}$) requires $\lambda_r^*$ as input, which can only come from sample covariances. With covariances available, direct generalised-eigenvalue regression solves the recovery problem in one eigen-decomposition at $O_p(n^{-1/2}/\text{gap})$ rate — strictly better than the trajectory-based estimator's $O_p(n^{-1/2}/\text{gap}) + O(\epsilon^{1/L}|\log\epsilon|)$. The paper was a hybrid estimator that lost the only horserace that mattered. An identifiability audit on the Bernoulli ODE $\dot\sigma_r = \lambda_r^*\sigma_r^{3-1/L} - \mu_r\sigma_r^3$ showed two structurally independent observables on the positive branch: the **plateau** $\sigma_r^\infty = (\rho_r^*)^L$ (depending only on the ratio, no covariance needed) and **early-time slope** ($\mu_r$ term subleading, identifies $\lambda_r^*$ alone). Joint identifiability of $(\lambda_r^*, \mu_r)$ from a single trajectory follows by combination. On the negative branch, $\lambda_r^*$ is recoverable from late-time power-law decay but $\mu_r$ is dominated by the $\lambda^*$ term throughout the trajectory by factor $|\rho_r^*|\epsilon^{-1/L}$, making trajectory-only $\mu_r$ recovery rate-suboptimal vs direct covariance.

**How to apply:** Paper 2's headline is now Thm 5.1′ (plateau estimator, pure-trajectory rate $O(\epsilon^{1/L}|\log\epsilon|)$) + Thm 5.2 (joint identifiability of $(\lambda_r^*, \mu_r)$ on positive branch). The v1 critical-time inversion is retained as a "fast variant" corollary (one critical-time hit beats waiting for asymptotic convergence) but is not the load-bearing claim. The negative-branch story is reframed from "obstruction" (session-85 framing) to "rate-suboptimality" — the trajectory contains $\mu_r$ information in its subleading correction, but at $\Omega(1)$ effective error vs covariance's $O_p(n^{-1/2})$. **Do not pitch paper 2 as a competitor to covariance regression on sample efficiency** — it loses that race in the linear case. Pitch it as a *structural identifiability theorem*: trajectory is a sufficient statistic for the positive-branch spectrum. This framing is what justifies the non-linear extension (paper 3, LeWM/SIGReg spinoff) where covariance-in-input-space is not available.

## jepa-rho-recovery: Path C promotion of all 4 CriticalTime named sorries to axioms

**Decision date:** 2026-05-20 (session 85)

**Why:** Aristotle round-1 dispatches on the 3-way bernoulli split (`5fbe03d3` `bernoulli_exact_solution_exists`, `f00f9f44` `bernoulli_gronwall_sandwich`, `d9780bba` `bernoulli_exact_laurent`) all returned `COMPLETE_WITH_ERRORS` with no progress on the target sorries; two actively regressed the triangle assembly by adding new sorries. These four named sorries (the three pieces + `purified_laurent_bound`) are research-level ODE/Laurent results — Picard-Lindelöf existence on a locally-Lipschitz Bernoulli RHS, Grönwall ODE-comparison sandwich, Littwin 2024 Thm 4.5 (partial-fraction Laurent) × 2 (the second variant with full error tracking for the envelope sharpening from `ε^{-(L-2)/L}` to `|log ε|`). They are exactly the kind of cited-external-result the CompCert-style honest-promotion discipline (decisions.md, session 81) is for: published or textbook math whose Lean formalisation would be 500–1000 lines per piece and yield no new research value. Refining-and-redispatching to Aristotle was the alternative; rejected because Aristotle's track record on standalone ODE existence/comparison lemmas is poor, and round-2 budget is better spent elsewhere.

**How to apply:** All 4 axioms in `JepaRhoRecovery/CriticalTime.lean` carry explicit paper citations in their docstrings (Picard-Lindelöf; Grönwall; Littwin 2024 Thm 4.5). When citing the moonshot externally, name the axioms upfront — they are the load-bearing analytic content and should appear in the paper's "axiom appendix" so reviewers can see the formalisation boundary. Do not promote any future lemma to an axiom without (a) failed Aristotle attempt and (b) a published-paper citation that justifies the assumption.

## jepa-rho-recovery: statement-honesty audit — reachability hypotheses required on all hitting-time axioms

**Decision date:** 2026-05-20 (session 85)

**Why:** Audit of the 4 CriticalTime axioms found a latent vacuity: `hittingTime f θ t_max` defaults to the sentinel `t_max + 1` when `f` never reaches `θ` on `[0, t_max]`. Without a reachability hypothesis, an axiom asserting `|hittingTime f − Expr| ≤ K · ε^{α}` is trivially refutable by any `f` that does not cross the threshold — the LHS becomes `|t_max + 1 − Expr|`, which is Ω(1) for generic Expr. This violates the spinoff's vacuity-discipline invariant (jepa-rho-recovery/CLAUDE.md): every hypothesis must be non-trivially constraining; every existential witness must be positive; no `True` placeholders. The discovered gap was structural, not cosmetic — the original axiom statements were false as written.

**How to apply:** All 4 axioms now carry, for each trajectory function `f` mentioned: (i) `ContinuousOn f (Set.Icc 0 t_max)`, (ii) `∀ t ∈ Set.Ioo 0 t_max, DifferentiableAt ℝ f t` (the `deriv f t = …` clause is meaningless without this), and (iii) `hittingTime f (p·ρ^L) t_max < t_max` (forces the hitting time into the interior). `bernoulli_exact_solution_exists` additionally takes a coarse `t_max`-sufficiency hypothesis `(2L)/(λ·ε^{(2L-1)/L}) ≤ t_max` so the existence axiom's conclusion can return the reachability witness. For any future axiom on hitting times, add the analogous reachability hypothesis at statement time — do not defer.

## Simplicial paper.tex: block-style `\paragraph` via `\@startsection` redefinition

**Decision date:** 2026-05-19 (session 83+)

**Why:** When the Bubeck-style §1 restructure replaced subsections with `\paragraph{...}` run-in headers (e.g. `\paragraph{The problem.}`, `\paragraph{Main result.}`), the LaTeX default rendering of `\paragraph` is a bold lead-in inline with the following text — so `The problem.` looked like the first words of the paragraph body rather than a heading. User initially misdiagnosed as a subsection issue ("subsections showing up as plain short sentences"); the actual offender was `\paragraph`. Subsections under amsart's run-in style were fine.

**How to apply:** Preamble carries a redefinition of `\paragraph` to block style via `\@startsection`:

```latex
\makeatletter
\renewcommand\paragraph{\@startsection{paragraph}{4}{\z@}%
  {1.0ex \@plus .2ex \@minus .1ex}%
  {0.3ex \@plus .1ex}%
  {\normalfont\normalsize\bfseries}}
\makeatother
```

This puts paragraph headers on their own line with bold sentence-case titles. Do not load `titlesec` under amsart — `\@secnumpunct` conflict will error every `\section{...}`. If porting to another amsart paper with Bubeck-style `\paragraph` headers, copy the `\makeatletter ... \makeatother` block from the simplicial preamble verbatim. Diagnostic shortcut for future occurrences: extract `pdftotext -layout paper.pdf` and search for the paragraph title — if it appears with no preceding newline, the default run-in style is active.

---

## Simplicial: post-Nick follow-up threads (optimality + sparse) deferred until Nick replies on restructured .tex

**Decision date:** 2026-05-19 (session 83+)

**Why:** During the Bubeck-style restructure of `simplicial-latent-geometry/my_theorems/paper.tex`, David flagged interest in two threads currently scaffolded as partial / open-problem content but explicitly chose to send the restructured version to Nick first.

**Threads to revisit after Nick replies:**

1. **Fill-pair optimality (§5.3, τ_ff thread).** τ_f is not low-degree optimal — τ_ff (pure-fill pairs sharing 2 vertices) strictly beats it (SNR ratio ≈ 1.64 deep regime, ≈ 23 at d=5). Currently stated as a Proposition with closed-form mean+variance; full BB24-style low-degree optimality proof deemed separate-paper-grade (see decisions.md "simplicial paper: LMSY low-degree polynomial analysis is future work"). Local working note `fourier_setup.md` §C3–C4 has partial groundwork. Estimated cost if pursued: ~4–6 weeks paper math + months Lean.

2. **Sparse regime / LMSY-style (§5.2).** Conditional sparse threshold stated; real blocker is rigorously proving geomCov(p,d) = Θ(|log p|/d) decay rate. This is Track A of OQ-16, never closed. Without it sparse-regime statements remain heuristic. Aristotle has not previously made progress on this. Estimated cost: weeks.

**Implication:** Don't pre-empt Nick's reply by starting either thread. After his response, surface these as a coauthor decision item — separate paper? joint? venue?

---

## CompCert promotion is honest *only* when the hypothesis is materially deeper than the lemma's own content

**Decision date:** 2026-05-19 (session 81)

**Why:** During the "close all sorries" push on jepa-rho-recovery, I attempted to promote three deep analytic sorries (`bernoulli_laurent_bound`'s h_gronwall + h_laurent; `purified_laurent_bound`'s whole body; `generalised_diagonal_ODE`'s remainder bound) to file-level named hypotheses. Two patterns emerged with different honesty signatures:

- **Honest CompCert (kept):** `Main.signed_decomposition` takes per-layer outputs as hypotheses + proves a genuine uniform-`ε_max` finite-Finset bundling via `finset_forall_eps₂`. The hypotheses constrain rho_hat / tau_pos / tau_neg to actually have the layer-level properties; the proof does real combinatorial work. Layer 2.1 `generalised_diagonal_ODE` similarly takes `B_W, B_V` matrix-norm bounds (a real Lyapunov-style fact about gradient flow) and does ~340 lines of Cauchy-Schwarz bookkeeping. Both are publishable patterns — analogous to how CompCert axiomatises IEEE-754 semantics without verifying them.

- **Dishonest CompCert (reverted):** `purified_laurent_bound`'s body became literally `:= h_envelope_sharpening` where `h_envelope_sharpening` had the exact same statement as the conclusion. No content was added. Same for the two internal sorries inside `bernoulli_laurent_bound` — they encoded specific paper-1 results, and promoting them to file-level just relabels the gap. User flagged this correctly.

**Implication:** Future "CompCert convention" assemblies must add genuine intermediate work between the hypothesis and the conclusion. Identity-style `lemma X ... (h : statement) : statement := h` is rejected. Spec strengthening (e.g. adding `B_W, B_V` boundedness, restricting `ε < ε_max`) IS allowed because it captures a real mathematical assumption rather than just renaming the conclusion.

**Practical test:** if the lemma body is `:= h` or `exact h` or `assumption`, it's dishonest promotion. If the body has nontrivial intermediate steps (triangle inequality + monotonicity + algebraic manipulation), it's honest assembly.

---

## DEFERRED — JEPA-rho Laurent spec mismatch: CriticalTime (paper-1, raw hitting time) ≠ Inversion (Aristotle a65a98a3, purified)

**Decision date:** 2026-05-19 (session 78) — diagnosis only; resolution pending

**Why this is on the decisions page:** the mismatch was discovered while attempting to wire `actual_critical_time_signed` into a concrete `signed_recovery_pos_magnitude_jepa`. It blocks the wire. The fix requires a paper-design call, not a Lean tactic.

**The mismatch:**

`CriticalTime.bernoulli_laurent_bound` (transplanted from paper-1 `jepa-learning-order/JepaLearningOrder/JEPA.lean:741`) gives:
- Laurent sum: $(1/\lambda) \sum_{n=1}^{2L-1} L/(n \cdot \rho^{2L-n-1} \cdot \epsilon^{n/L})$
- Envelope: $K \cdot \epsilon^{-(L-2)/L}$
- Leading order: $\epsilon^{-(2L-1)/L}$ — ρ-INDEPENDENT (n=2L-1 term has $\rho^0 = 1$)

`Inversion.rho_hat_rate` (proved by Aristotle a65a98a3) expects:
- Laurent sum: $(1/\lambda) \sum_{n=1}^{2L-1} L/(n \cdot \rho^{2L-n-1}) \cdot \epsilon^{(n-2)/L}$
- Envelope: $K_{\log} \cdot |\log \epsilon|$
- Leading order: $\epsilon^{-1/L}$ — ρ-DEPENDENT (n=1 term has coefficient $L/\rho^{2L-2}$)

These are different mathematical objects. The estimator $(L/(\lambda \cdot t_{\text{crit}} \cdot \epsilon^{1/L}))^{1/(2L-2)}$ in `rho_hat_rate` only recovers ρ if t_crit ≈ the ρ-distinguishing piece (n=1 only); fed the raw hitting time (which is dominated by ρ-independent n=2..2L-1 terms), it returns 0 not ρ.

**Cross-check against paper-1's paper.tex** (`jepa-learning-order/my_theorems/paper.tex` lines 626–646, Theorem "bernoulli-closed"): explicitly states "the leading term is n = 2L-1, of order $\epsilon^{-(2L-1)/L}$, depending only on λ, not on ρ. The first ρ-distinguishing summand is n = 1, of order $\epsilon^{-1/L}$." So paper-1's `t^* \sim \epsilon^{-(2L-1)/L}` is canonical and `CriticalTime.lean` is faithful to it.

The jepa-rho-recovery paper draft §5 (`my_theorems/paper_draft.md:76`) writes the estimator inversion formula as if `t̃_r^* = O(\epsilon^{-1/L})` — i.e., silently assumes the purification, without explicating where the n=2..2L-1 terms go.

**Resolution paths (all require ≥1 new Aristotle dispatch and a paper-side amendment):**

- **Path A** — Add a Purification bridge lemma: `purified_hitting_time` takes paper-1's full Laurent, subtracts the n=2..2L-1 terms, returns Inversion-shape Laurent. Paper §5 footnoted to clarify $t̃_r^* \neq$ raw $\hat T_r$. Inversion proof preserved. Cleanest separation of concerns but adds a layer.

- **Path B** — Reject Aristotle a65a98a3, re-derive inversion from raw Laurent. Estimator must extract n=1 piece by explicit subtraction of the closed-form dominant prefix. Heaviest path; rewrites Inversion.lean entirely. Re-dispatch needed.

- **Path C** (RECOMMENDED) — Update CriticalTime to give Inversion's purified Laurent directly. Re-spec `bernoulli_laurent_bound` to return $(1/\lambda) \sum L/(n \cdot \rho^{2L-n-1}) \cdot \epsilon^{(n-2)/L}$ with $|\log \epsilon|$ envelope. The purification is a Laurent re-arrangement done inside the (already named-sorried) proof obligation. Paper-1's paper.tex Thm "bernoulli-closed" needs an addendum showing the purification. Smallest spec drift; preserves Inversion proof; preserves paper draft §5 as written.

**Implication for current Lean state:** `signed_recovery_pos_magnitude` (in `SignedRecovery.lean:144`) takes `t_crit` + `h_laurent` abstractly. It cannot be concretised against `bernoulli_laurent_bound` until the wire is fixed. The theorem itself is provable in the abstract form (Aristotle a65a98a3 proved `rho_hat_rate` and `signed_recovery_pos_magnitude` re-exports it) — it just isn't *applicable* to the actual JEPA dynamics until the bridge exists.

**No urgency:** none of the in-flight Aristotle dispatches (3.1 `e71b355e`, 5.1 `5f4d94e1`) depend on this resolution. The wire is a paper-2 closing step, not a blocking dependency.

**Filed in:** this entry; flagged in session-78 log; will block any future attempt to write `signed_recovery_pos_magnitude_jepa`.

---

## Sphere OQ-18: concretise `uniformOnSphere`, `cechFillProb`, `ripsFillProb`, `geomCovCech` via mathlib's `Measure.toSphere`

**Decision date:** 2026-05-19 (session 77 follow-up)

**Why:** The previous axiomatic approach (17 axioms) was intentionally conservative pending a clean Mathlib formalization of the sphere measure. Mathlib's `MeasureTheory.Constructions.HaarToSphere` (`Measure.toSphere : Measure E → Measure (sphere (0 : E) 1)`) supplies exactly the radial pushforward needed — sufficient to define `uniformOnSphere d` as the normalized `toSphere` of the standard Lebesgue measure on `EuclideanSpace ℝ (Fin d)`. Concretising `uniformOnSphere` cascades into the 3 fill-probability defs (`cechFillProb`, `ripsFillProb`, `geomCovCech`) as iid product-measure integrals, dropping 5 axioms (17 → 12) with no change to downstream Paper 2 typeclass hookup or to the structural Paper 2 axioms.

**Architectural change:** `SpherePoint d` was redefined from `{x : EuclideanSpace ℝ (Fin d) // ‖x‖ = 1}` to `Metric.sphere (0 : EuclideanSpace ℝ (Fin d)) 1` (the standard mathlib subtype) to make `Measure.toSphere` apply directly. Audit confirmed zero downstream use of `.property` / `.2 : ‖x‖ = 1`, so the swap is transparent for all consumers (`sphereEdge`, `sphereCechFill`, the `CechSphereModel` typeclass instance).

**Implication:** Paper 2 (sphere/Čech) headlines (`cechFillProb_tail_asymptotic`, `geomCovCech_asymptotic`) remain Lean-verified, now modulo only 3 *structural* Paper 2 axioms (`cechFillProb_compl_le_gram_tail` — Wishart Gram tail, `cechFillProb_le_one` — sub-probability bound, provable but deferred, `geomCovCech_decomp_ratio_tendsto` — algebraic decomposition + surface concentration). The 5 removed axioms (`uniformOnSphere`, `uniformOnSphere_isProb`, `cechFillProb`, `ripsFillProb`, `geomCovCech`) had been **load-bearing only by virtue of opacity**; concretising them means downstream proofs now work against actual mathematical objects rather than black boxes.

**Future work:** the `capProb` cluster (6 axioms) is the next candidate — `capProb d r := (uniformOnSphere d {x | ⟨x, pole⟩ ≥ r}).toReal` would cascade to making the 5 endpoint/continuity axioms provable from sphere-measure properties.

**Filed in:** `SimplicialLatentGeometry/Geometry/Sphere.lean` commits `b63fc28`, `51fa5ff`; this entry.

---

## Simplicial OQ-18: delete legacy `geometricCov_lower_bound{_explicit}` rather than re-derive under Rips

**Decision date:** 2026-05-19 (session 77)

**Why:** Both lemmas were derived from the OLD Čech-nerve closed form `geomCov = (1−q)·(3r²)^d + 3p³·((7r/2)^d − 1)`. Under the new Rips closed form `geomCov = q·((1−p)^3 + p^3) − q²` (sorry-free as of session 75's `geometricCov_eq`), the lower bound `(1−q)·(3r²)^d − 3p^3 ≤ geomCov` is no longer derivable: the RHS's leading `(3r²)^d` term doesn't appear anywhere in the Rips closed form. Audit confirmed **zero downstream Lean callers** — only doc-level references in `my_theorems/job4_trackB_prompt.md` (originally written to spec these lemmas) and one informational sentence in `my_theorems/proof_strategy.md` already flagging the proof-path loss.

**Implication:** The sparse-regime $n^{3/2} \cdot \text{geomCov} \to \infty$ corollary (Track B, Corollary~\ref{cor:sparse}) loses its Lean-verified path until a Rips-native sparse-regime lower bound is derived. This is a separate research item (mid-regime asymptotics with $p \to 0$ jointly with $d \to \infty$), not just a porting task. Deferred indefinitely; flagged in `my_theorems/proof_strategy.md`. The `SimplicialDetection.lean` file is now sorry-free outside dead-code blocks; no live theorem depends on the deleted lemmas.

**Filed in:** tombstone comment at the deletion site in `SimplicialDetection.lean`; this entry.

---

## JEPA OQ-17: spin off `jepa-rho-recovery` as option-2 moonshot (all 5 layers, signed framing)

**Decision date:** 2026-05-17 (session 67)

**Why:** Option 1 (Layers 1–2 only — TMLR fast follow-up) shipped a positive-$\rho$-only inversion formula but conceded Layer-4.2(iii) (negative magnitudes unrecoverable from JEPA dynamics) as a gap. Option 2 reframes that concession as the **headline result** — JEPA training performs a *signed decomposition* of the regression structure: positive features learned with recoverable magnitude, negative features identified by suppression timescale + sign. The "weakness" of option 1 becomes the contribution of option 2.

**Scope:** new repo `jepa-rho-recovery/` (sibling of `jepa-learning-order/`), all 9 gaps across 5 layers. No Lake dep on `jepa-learning-order` initially — definitions re-derived locally so the spinoff can change them freely. Re-evaluate cross-project import after Layer 2.1.

**Sequencing:** 1.1 → 1.2 → 2.2 → 4.1 → 4.2 (moonshot lock-in), then fill in 2.1 / 3.1 / 3.2 / 5.1. Front-loads the risky signed-dynamics work (Layer 4.1) before sinking effort into finite-sample machinery.

**Fallback:** if Layer 4.1 (signed ODE physics) stalls for >4 sessions, demote to paper-3 and ship paper-2 as Layers 1–2 + positive-branch finite-sample (option 1, salvaged).

**Headline target:** `signed_decomposition` theorem at statement level, sorry-free in headline-A/B/C lemmas. Without it, paper-2 does not ship.

**Architectural invariant (do not violate):** every Lean structure in the spinoff carries *signed* $\rho^*$ from the start. `SignedGenEigenpair` has no `0 < rho` axiom — positivity is a derived predicate, never a structure hypothesis. Vacuity is forbidden: `HasDerivAt` (not `deriv`), positive-witness existentials (no `epsilon_0 = 0`).

**Filed in:** `jepa-rho-recovery/CLAUDE.md`, `jepa-rho-recovery/paper/outline.md`, `jepa-rho-recovery/requests/01_layer1_1_quasi_static.md`. OQ-17 status update at top of `wiki/INDEX.md`.

---

## Simplicial OQ-18: Paper 1's $d^* \asymp \log n$ threshold is structurally wrong on $\ell_\infty$

**Decision date:** 2026-05-16 (session 63)

**Why:** Preparing the Aristotle dispatch for `fillingProb_tendsto_zero` surfaced a math error in `my_theorems/oq18_math_audit.md`. The audit derived $q = (3r^2)^d = (3/4)^d p^2$ in the "deep regime $r \le 1/4$" and then applied that formula to the $d \to \infty$ limit at fixed $p$. But $r_d = p^{1/d}/2$ is *increasing* in $d$ — the $r \le 1/4$ regime corresponds to **small** $d$ (specifically $d \le \log p / \log(1/2)$), not the asymptotic limit.

Independent computation of the per-coord 3-clique probability $\gamma(r)$ on $\mathbb{T}^1$ for $r \in (1/3, 1/2]$ (wraparound regime, $\gamma(r) = 3r^2 + (3r-1)^2$) gives $\gamma(r_d)^d \to p^3$ as $d \to \infty$. Hence:

- $\text{fillingProb}(p, d) \to p^3$ (not $0$)
- $\text{geomCov}(p, d) \to p^3(1-p)^3$ (positive constant, not $0$)
- SNR $n^{3/2} \cdot \text{geomCov} \to \infty$ for *any* fixed $d$ — **no dimensional barrier on $\ell_\infty$ Rips**.

This kills Paper 1's headline. The "$d^* \asymp \log n$ threshold" was an artifact of using the small-$r$ formula outside its regime.

**Implication:**
- Stub lemmas `fillingProb_tendsto_zero`, `geometricCov_tendsto_zero`, `geometricCov_eventually_zero` are all **false as stated**. Do not dispatch to Aristotle. Replace with `fillingProb_tendsto_pcubed` and `geometricCov_tendsto (p^3(1-p)^3)`.
- The closed form $\text{geomCov} = q[(1-p)^3 + p^3] - q^2$ and `geometricCov_eq_deep` survive (algebraic / regime-bounded; both unaffected).
- Paper 1 headline: **"no-barrier" framing** chosen (session 63). $\ell_\infty$ Rips detection works at every $d$; Paper 1 becomes a Lean-verified instance of the abstract detection theorem; Paper 2 (sphere) recovers a real dimensional threshold via Anderson–Cook cap asymptotics. Multi-paper program (Paper 1 → 2 → methodology) is cleaner under this framing.
- Paper 2 (sphere) becomes structurally more important — it now carries the "real threshold" story.
- A5 work (TorusLInf circular-import split) continues regardless — the Lean module structure is orthogonal to which asymptotic statement is true.

**Tracked in:** addendum at bottom of `simplicial-latent-geometry/my_theorems/oq18_math_audit.md` (full derivation with $\gamma(r)$ table and what-survives/breaks ledger).

**Session-63 follow-up (sphere precheck + bundling).** Pencil-and-paper derivation of $q_{\text{Rips}}$ and $q_{\text{Čech}}$ on $S^{d-1}$ at matched $\theta(p,d) = \pi/2 - z_p/\sqrt{d}$ confirmed:

| Setting | $q_{\text{Rips}}$ | $q_{\text{Čech}}$ | $\text{geomCov}_{\text{Rips}}$ | $\text{geomCov}_{\text{Čech}}$ |
|---|---|---|---|---|
| $\ell_\infty$ torus | $\to p^3$ | $= q_{\text{Rips}}$ (Helly-2) | $\to p^3(1-p)^3 > 0$ | same |
| $S^{d-1}$ | $\to p^3$ | $\to 1$ (caps near-hemisphere; Wendel ⇒ 3 iid points fit in some hemisphere a.s. for $d\ge3$) | $\to p^3(1-p)^3 > 0$ | $\to 0$ (rate $\sim 1 - q_{\text{Čech}}$) |

**Implications:**
- Paper 1 ($\ell_\infty$ + Rips) no-barrier framing stands. Ready to bundle.
- **Paper 2 ($S^{d-1}$ + Čech) is the genuine dimensional-threshold paper.** Čech-Rips gap is $\Theta(1)$ on sphere because Helly-$d$ preserves the existential vs clique distinction. The vanishing rate of $\text{geomCov}_{\text{Čech}}$ — driven by Wendel-type tail $1 - q_{\text{Čech}}(p, d)$ — gives the threshold.
- **Bundling decision locked:** ship Paper 1 + Paper 2 together. Paper 1 standalone would only tell the no-barrier half of the story; the methodology punchline ("we solved three concrete instances") needs at least one genuine-barrier instance.
- Algebraic closed form $\text{geomCov} = q[(1-p)^3 + p^3] - q^2$ does **not** apply on Čech (requires Rips identity $F = A_{12}A_{13}A_{23}$). Paper 2 needs Wendel/Anderson-Cook asymptotic for $1 - q_{\text{Čech}}(p, d)$. Math precheck verified the path; ~1-2 sessions of careful asymptotic before Lean.

**Tracked in:** `simplicial-latent-geometry/my_theorems/paper2_sphere_scoping.md` (gitignored) — full precheck derivation, comparison table, concrete next steps with reference list (Wendel 1962, Anderson-Cook 1986, Cover-Efron 1967, Reitzner 2010).

**Session-63 follow-up #2 — Wendel tail asymptotic computed.** The "smallest enclosing cap" score $M := \max_z \min_i \langle z, x_i\rangle$ for three iid points on $S^{d-1}$ concentrates at $1/\sqrt{3}$ (= cosine of $54.7°$). The event $M < \cos\theta_d = z_p/\sqrt{d}$ requires a constant-order deviation from typical, corresponding to "three points near a great circle" (each pairwise inner product near $-1/2$). Large-deviation rate:

$$1 - q_{\text{Čech}}(p, d) = \Theta(e^{-c \cdot d}), \quad c \approx \log(4/3) \approx 0.288.$$

Plugging into Cauchy-Schwarz: $|\text{geomCov}_{\text{Čech}}| \le e^{-cd/2}$. Plausibly $\Theta(e^{-cd})$ without cancellation. Detection criterion $n^{3/2} |\text{geomCov}_{\text{Čech}}| \to \infty$ gives **$d^*(n,p) = \Theta(\log n)$** — the original headline survives on sphere/Čech.

**Multi-paper thread status: INTACT, sharpened.** The discriminator across papers is now the **Helly number** of the ambient space:

| Paper | Helly | Barrier |
|---|---|---|
| 1 ($\ell_\infty$ torus) | 2 | NO (Rips ≡ Čech, no fill gap to exploit) |
| 2 ($S^{d-1}$) | $d$ | YES, $d^* \asymp \log n$ |
| 3 (L² Euclidean torus) | $d{+}1$ | ? — needs precheck |
| Methodology | — | "Helly number controls dimensional detection threshold" |

Paper 1's no-barrier result becomes a *load-bearing contrast* against Paper 2: it shows concentration alone doesn't create the barrier; the obstruction is the *Čech-Rips gap* preserved by Helly-$d$. Methodology paper has a cleaner punchline than the original three-instance framing.

**Session-63 follow-up #3 — rate tightened to super-exponential.** The Wendel-tail estimate $e^{-cd}$ was wrong; conflated LDP with small-deviation at the singular boundary $\det G = 0$. The joint density of Gram entries $(y_{12}, y_{13}, y_{23})$ on three iid sphere points is $\propto (\det G)^{(d-4)/2}$ (Wishart-type, derivation via fixing $x_1$ and using sphere coords). For $d \ge 5$ density vanishes at the boundary, giving $\Pr[\det G \le t] \sim t^{(d-2)/2}$. Hence:

$$1 - q_{\text{Čech}}(p, d) \sim \left(\frac{3 z_p^2}{d}\right)^{(d-2)/2}, \quad z_p := \Phi^{-1}(1-p).$$

Super-exponential decay $\sim d^{-d/2}$.

GeomCov closed form (linear in fluctuation, NO Cauchy-Schwarz cancellation):
$$\text{geomCov}_{\text{Čech}} \approx -2 p^3 (1 - q_{\text{Čech}}).$$

The two terms $q_{\text{Rips}}(1-q_{\text{Čech}}) = p^3 \cdot (1-q)$ and $3p^2(\beta-p) = -3p^3(1-q)$ REINFORCE (sign flip), giving a $-2p^3$ coefficient.

Detection threshold $n^{3/2}|\text{geomCov}_{\text{Čech}}| \to \infty$ becomes $d \log d < 3 \log n$ at leading order:

$$\boxed{d^*(n, p) = \frac{3 \log n}{\log\log n} + O(\log n/(\log\log n)^2).}$$

**Sub-logarithmic**, universal leading constant $3$ (independent of $p$). $p$-dependence enters at next order through $z_p^2$ inside the log.

This is **sharper than both the original audit's $\Theta(\log n)$ claim and the Wendel-tail $\Theta(\log n)$ estimate**. The methodology paper headline strengthens: "the dimensional threshold on Helly-$d$ ambient spaces is $\Theta(\log n / \log\log n)$, driven by the joint Gram density's singular boundary."

Tracked in `simplicial-latent-geometry/my_theorems/paper2_sphere_scoping.md` "Tightened rate analysis (third pass)".

**Session-63 follow-up #4 — MC verification (corrected coefficient and sign).** Three claims tested at $p=0.3$, $N=10^6$ samples:

1. ✓ Gram density tail $\Pr[\det G \le t] \sim t^{(d-2)/2}$ verified (slope ratio ~95% for $d \in [5, 20]$).
2. ✓ Exact closed form $\text{geomCov} = q_R(1-q_C) + 3p^2(\beta-p)$ matches MC to 3 digits.
3. ✗ Asymptotic "$-2 p^3 (1-q_C)$" was **wrong sign and wrong coefficient**. MC reveals geomCov is positive.

**Diagnosis:** I claimed $\Pr[A_{12} \mid F=0] \to p$ as $d \to \infty$. Wrong — it goes to **0**. Conditional on the rare event $F=0$, the dominant configuration is near-equilateral with $y_{ij} \approx -1/2$, in which $A_{12} = 0$ (since $y_{12} \approx -1/2 < $ threshold). MC trend at $p=0.3$: $\Pr[A_{12} \mid F=0]$ goes from $0.176$ at $d=4$ down to $0.066$ at $d=12$, consistent with $\to 0$.

**Corrected asymptotic:** $\text{geomCov}_{\text{Čech}} \sim p^3 (1 - q_{\text{Čech}}) \sim p^3 (3z_p^2/d)^{(d-2)/2}$. Sign positive, coefficient $+p^3$ not $-2p^3$.

**Headline scaling unchanged:** detection $n^{3/2} \cdot p^3 \cdot (3z_p^2/d)^{(d-2)/2} \to \infty$ still gives $d^*(n,p) = 3 \log n / \log\log n + $ lower order. The intermediate sign error didn't propagate.

**Multi-paper thread fully verified at scaling level.** Paper 2 ($S^{d-1}$ + Čech) has a real $\Theta(\log n / \log\log n)$ barrier; the precise leading constant for $|\text{geomCov}_{\text{Čech}}|$ is $p^3$ not $2p^3$. The sub-leading rate of $c_d \to 0$ (likely polynomial in $1/d$) affects the next-order constant but not the leading scaling.

**Session-63 follow-up #5 — Paper 3 precheck (L² Euclidean torus, Helly-(d+1)).** Concentration regime: matched radius $r_d \sim \sqrt{d/12}$, at typical pairwise distance. $q_{\text{Rips}} \to p^3$ (same concentration collapse). For Čech: smallest enclosing ball of three iid points has radius $\sim \sqrt{d/18} < r_d$, so $q_{\text{Čech}} \to 1$. Rate of $1 - q_{\text{Čech}}^{L^2}$: standard exponential $e^{-cd}$ (NOT super-exponential — no $\det G$-density-singularity analogue; the Euclidean enclosing-ball event has standard Gaussian-tail concentration). Detection: $d^*(n,p) = \Theta(\log n)$.

**Trilogy is triangulated, three distinct mechanisms:**

| Paper | Ambient | Helly | $1 - q_{\text{Čech}}$ tail | $d^*(n,p)$ |
|---|---|---|---|---|
| 1 | $\ell_\infty$ torus | 2 | n/a (Čech ≡ Rips collapses) | $\infty$ (no barrier) |
| 2 | $S^{d-1}$ | $d$ | $(3 z_p^2/d)^{(d-2)/2}$ super-exp | $3 \log n / \log\log n$ |
| 3 | L² Euclidean torus | $d{+}1$ | $e^{-cd}$ exp | $\Theta(\log n)$ |

Methodology paper punchline: **dimensional detection threshold scaling depends on the Helly number of the ambient space.** Helly-2 collapses Čech to Rips and removes the gap entirely; Helly-$d$ preserves the gap but concentration of measure forces super-exponential tail via singular Gram density; Helly-$(d{+}1)$ preserves the gap with standard exponential tail. Three load-bearing instances unified.

**Sphere Lean S1 done.** `SimplicialLatentGeometry/Geometry/Sphere.lean` skeleton committed on `oq-18-rips` (commit `0ab0549`). SphereSetting, uniform measure, edge predicate, Čech fill predicate, matched cosine threshold, geomCov closed-form theorems stubbed. HomogeneousGeometricModel instance hookup BLOCKED on typeclass refactor (Rips closed form doesn't apply to Čech-fill). Aristotle dispatch plan S2-S6 documented. Next: typeclass generalization OR ad-hoc sphere detection theorem.

**Paper 1 paper.tex revision (gitignored, local).** Added "Note added in revision (session 63)" before §1 flagging convention-specificity per N. Cook; Theorem 3.2(b) tagged with "Convention-specificity" remark; §5.5 "Beyond the flat torus" extended with sphere sequel summary + trilogy framing. The paper itself stays internally consistent under David's original same-radius Čech convention; the note clarifies what's a Helly-2 case study vs structural conclusion.

---

## Simplicial: multi-paper research program (Option C, core-extracted Lean library)

**Decision date:** 2026-05-16 (session 57)

**Why:** After the Rips reframe (next decision below) it became clear that the project decomposes naturally into three settings, each with a distinct headline:
1. **L∞ Rips on torus** (current Lean) — quantitative detection threshold $d \asymp \log n$.
2. **Sphere $S^{d-1}$** — sharp Čech ≠ Rips threshold via Anderson–Cook spherical cap asymptotics. Recovers the "elegant collapse" headline lost in the Rips reframe.
3. **L² Euclidean torus** — finishes the thesis's hyperspherical-cap asymptotics.

Plus a methodology paper that writes itself once two instances exist: "We solved three concrete instances of a unifying problem, and here's the Lean framework that captures the abstraction."

§4.4 sanity check this session confirmed that the Rips paper alone is the weakest of the three (soft $\log n$ threshold; the sharp algebraic collapse was, in retrospect, an artifact of Helly-2 saturation on $\ell_\infty$, not a genuine geometric phenomenon). Shipping L∞ standalone would anchor the public version of this work to the weakest setting. Bundling reframes the L∞ result as a diagnostic case study within a larger framework.

Three architectural options considered:
1. **Three parallel sibling Lean projects** — pragmatic, ships papers; no abstraction.
2. **Abstract `MetricMeasureSpace` typeclass via explicit group action** — clean but Mathlib's measure-theory abstraction support is thin; design risk.
3. **Core + per-geometry instances, axiomatic homogeneity** — refactor `SimplicialDetection.lean` into `Core/Statistic.lean`, `Core/Detection.lean`, `Core/Variance.lean` (geometry-agnostic) + `Geometry/Common.lean` typeclass + `Geometry/*.lean` per setting + `Instances/*.lean` for concrete detection theorems.

Picked option 3 after design pass. Axiomatic homogeneity over explicit group action — cleaner Lean, faster to ship, refactor cost later is bounded (localized to `Common.lean`).

**Implication:**
- **Phase plan A1–A7:** A1 (`Core/Statistic.lean`) done this session (commit `a899904`). A2 (typeclass + L∞ instance) next. A3 (Detection), A4 (Variance), A5 (L∞ finalization + Paper 1 ready) follow. A6 (sphere), A7 (L²) are per-paper instances.
- **Paper 1 reframe** (§4.4 narrative flip: quantitative decay, not sharp collapse) **deferred to A5 milestone.** Don't touch paper.tex until the architecture stabilizes.
- **Aristotle stubs queued but not dispatched** — concrete signatures depend on whether targets are stated at the abstract or instance level. A2 decides.
- **Checkpoint discipline:** each milestone keeps Paper 1 publication-ready. If the program stalls 4 months in, "ship L∞ standalone" is ~1 week of paper writing, no Lean rework. The extraction work is non-destructive.
- **Methodology paper** is the eventual headline. Strictly benefits from having three instances.
- Sphere sequel direction stashed in `simplicial-latent-geometry/my_theorems/proof_strategy.md`. Anderson–Cook 1986 is the entry point for cap asymptotics.

**Tracked in:** OQ-18 in `wiki/INDEX.md` (full phase plan + status). Nick reply deferred until A5.

---

## Simplicial paper: reframe as Rips vs 2PC (not Čech vs 2PC)

**Decision date:** 2026-05-16 (session 56)

**Why:** Nick Cook flagged that the existing Def 2.3 (nerve-only with $B(x_i, r)$) is not a simplicial complex — triple intersection forces only pairwise $d \le 2r$ while edges require $\le r$, so downward closure fails. Investigation surfaced a deeper structural problem: on the sup-norm $\ell_\infty$ flat torus, $\ell_\infty$-balls are axis-aligned boxes ⇒ Helly number 2 ⇒ Kahle K10 Def 1.4 Čech complex (nerve of $\{B(x_i, r/2)\}$) coincides with the Vietoris–Rips complex at parameter $r$. Per-coordinate, both "all pairwise $\le r$" and "$\exists z, \forall i\ |x_i - z| \le r/2$" reduce to "range $\le r$." Cannot simultaneously have (i) sup-norm metric, (ii) Kahle nerve, (iii) Čech ≠ Rips on this ambient space.

Three options considered:
1. **Rips reframe** — accept the Helly-2 collapse, present the model as Rips. Preserves all factorization machinery and the Tracks A/B/C catalog. Cost: ~3 days.
2. **Euclidean port** — switch metric to Euclidean to genuinely separate Čech from Rips. Preserves the original thesis intent. Cost: ~3 months. Architect stress-test surfaced a load-bearing risk: `geometricCov_lower_bound_explicit` routes through `geometricCov_eq_deep`, which under Euclidean has no closed form in high $d$; a direct signed lower bound on triple-Euclidean-ball intersection volume in high $d$ is open mathematics.
3. **Status quo (relaxed nerve)** — keep the $r$-ball convention, document it as a deliberate choice. Cheap but doesn't survive standard-convention scrutiny from any reviewer who knows Kahle.

Picked option 1 after architect's option-2 risk assessment. Rips is what the existing Lean already analyzes; the thesis itself names Rips as a target; the reframe is honest narrative, not a retreat.

**Implication:**
- Paper: title + §2.2 + §4.4 + §6 + Appendix A change. The "Čech vs 2PC" detection theorem becomes "Rips vs 2PC." Sphere $S^{d-1}$ with closed-form spherical caps (Anderson–Cook 1986) becomes the natural sequel for genuine Čech ≠ Rips — stashed in `simplicial-latent-geometry/my_theorems/proof_strategy.md`.
- Lean: `CechSample.hasFill` becomes the clique predicate `∀ i j ∈ t.val, dist ≤ r`. `fillingProb` becomes the triangle product integral, equal to $(3 r^2)^d$ via `gamma_pow_eq`. `centered_edge_moment_fill`, `geometricCov_eq_deep`, `geometricCov_lower_bound_explicit` all re-derive via $X_e A_e = (1-p) A_e$ on 0/1 indicators — pure algebra, Aristotle target.
- **`fillingProb_tendsto_one` becomes `fillingProb_tendsto_zero`** under Rips. Story for §4.4 inverts: under both Rips and 2PC, fill becomes rare as $d \to \infty$; the models differ in correlation structure, not in marginal $q$ asymptotics. Detection theorem (TV → 1) survives because SNR routes through covariance.
- Do NOT attempt to retrofit Čech ≠ Rips into this paper. That's the sphere sequel.

**Tracked in:** OQ-18 in `wiki/INDEX.md` (full state + 11-lemma next-session checklist). Reply to Nick drafted in `simplicial-latent-geometry/cook-review/nick-reply-cech-convention.md`, held until refactor lands.

---

## Lean file organization: three-level hierarchy for fast subset builds

**Decision date:** 2026-05-05 (session 52)

**Why:** A monolithic `SimplicialDetection.lean` (4868 lines) means every Aristotle cherry-pick attempt triggers a 5-minute full build, even when only a small infrastructure section changed. During session 52, a fixable namespace mistake cost ~15 min of redundant build time because the error → fix → verify cycle couldn't be short-circuited.

SSB already demonstrates the right pattern: `Defs.lean` (shared types) + one file per theorem cluster (100–275 lines each, rebuild in seconds). JEPA has a similar helper-file structure. Both allow fast checks on isolated changes.

**Rule for all future projects and major additions:**

- **Level 0 (infrastructure):** pure math — only imports Mathlib. File names: `*Helpers.lean`, `*Integrals.lean`, `*Lemmas.lean`. Check with `lake build ProjectName.LevelZeroModule` (~60 s) before touching the main file.
- **Level 1 (types/defs):** project-specific structures and shared helpers. One file; imports Level 0.
- **Level 2 (theorems):** one file per theorem cluster. Import Level 0 + Level 1. Rebuild in seconds when only Level 2 changes.

**When NOT to split:** file is <400 lines, content is stable, no Aristotle jobs in flight (jobs reference file names).

**Implication:** New proofs that will live in a dedicated module should have that module created BEFORE the Aristotle job is submitted, so returned code targets the right file name. See `wiki/lean4-reference.md §File Organization for Fast Builds` for the full reference.

---

## Paper-writing scripts live under `stochastic-proofs-handbook/scripts/`

**Decision date:** 2026-05-01 (session 41)

**Why:** `forward_cites.py` and `verify_refs.py` operate on `.bib` files (paper writing), not on Lean proofs. Previously they sat at workspace root duplicating the handbook copy. Consolidation removes the duplicate, and the handbook scripts dir already has shared `.env` access and a README — the natural home.

**Implication:** All scripts (proof submission + paper-writing bib tooling) live in one place. `stochastic-proofs-handbook/scripts/README.md` separates them into two documented sections. Run paper-writing scripts as `python ../stochastic-proofs-handbook/scripts/verify_refs.py path/to/references.bib` from any project subdir; they read workspace-root `.env` for `SEMANTIC_SCHOLAR_API_KEY`.

---

## JEPA `my_theorems/` layout: `requests/`, `notes/`, `archive/`

**Decision date:** 2026-05-01 (session 41)

**Why:** Root had 24 mixed entries (live deliverables + LaTeX artifacts + 4 Aristotle prompts + old draft + backup + duplicate notes). Hard to find the live paper.

**Implication:** Standardised structure for any project's `my_theorems/`:
- Root: `paper.tex`, `paper.pdf`, `references.bib`, `README.md`, `.gitignore`.
- `requests/` for Aristotle job prompts (matches the existing `requests/21_bootstrap_request.md` convention).
- `notes/` for triage docs, citation reports, roadmap, Zulip drafts.
- `archive/` for superseded drafts and dated backups.
- LaTeX build artifacts gitignored, regeneratable. `.env` lives only at workspace root.

---

## Hoist uniformity constants outside parameterised quantifiers

**Decision date:** 2026-04-30 (session 35)

**Why:** Aristotle's `actual_critical_time` proof (Job G `862881a0`) used a witness-K trick: with `∃ K, |E| ≤ K · ε^{-(L-2)/L}` sitting inside the `ε`-parameterised body, K can be chosen as `K = (|E|+1)/ε^{-(L-2)/L}` to make the bound trivial. Lean type-checks this, but the lemma is mathematically empty. Same trap caught `frozen_encoder_convergence` (f9906716).

**Rule:** when a lemma asserts a *uniform* bound (independent of ε, of a function family, of a regularity parameter, …), the existential for the constant must be hoisted **outside** the universals it should be uniform over. Acceptable form:

```lean
∃ K : ℝ, 0 < K ∧ ∀ ε ∈ (0,1), ∀ family f, …, |E[f, ε]| ≤ K · g(ε)
```

Unacceptable form:

```lean
∀ ε ∈ (0,1), ∀ family f, …, ∃ K : ℝ, 0 < K ∧ |E[f, ε]| ≤ K · g(ε)
```

**Implication:** When drafting any future Aristotle prompt that bounds a quantity uniformly, audit the signature first. Ban `decide`, `native_decide`, `sorry`, `admit`, and witness-K-of-the-form `(LHS+1)/RHS` patterns explicitly in the prompt. After Aristotle returns, audit the `K` witness expression: if it textually contains the LHS (e.g. `|hittingTime ... - ...|`), the proof is vacuous regardless of whether Lean accepted it.

---

## Canonical per-project directory structure

**Decision date:** 2026-04-29 (session 27)

```
<project>/
├── <Module>/           # Lean source — flat (no subdirs), named after the lake_lib
│   └── *.lean
├── <Module>.lean       # Lake entry point (imports in dependency order)
├── lakefile.toml
├── lean-toolchain
├── literature/         # Reference PDFs (gitignored)
├── my_theorems/        # Paper and notes (gitignored)
│   ├── paper.tex       # LaTeX source
│   ├── paper_draft.md  # Markdown draft / Aristotle submission spec
│   ├── references.bib
│   ├── [*_spec.md]     # Any Aristotle submission specs
│   └── notes/          # Everything else: citation work, memos, verification reports
├── requests/           # Aristotle submission prompts (gitignored, numbered NN_<id>_request.md)
├── results/            # Aristotle result tarballs only (gitignored, <uuid>.tar.gz)
├── README.md           # Short public description with current commands
└── CLAUDE.md           # Architecture + pitfalls + commands — authoritative for agents
```

No `scripts/` (centralized in stochastic-proofs-handbook), no `aristotle/`, no `help_from_aristotle/`, no `reports/`, no `memory/`, no `archive/`, no nested READMEs or CLAUDE.mds, no LaTeX build artifacts.

**Why:** Eliminated ~10 structurally inconsistent dirs across the three projects that had accumulated via ad-hoc sessions with no agreed layout.

---

## Canonical Aristotle directory structure per project

**Decision date:** 2026-04-29 (session 27)

**Structure:**
```
<project>/
├── requests/           # submission prompts (gitignored; numbered NN_<id>_request.md)
└── results/            # downloaded tarballs only (gitignored; <full-uuid>.tar.gz)
```

No `aristotle/`, `help_from_aristotle/`, `scripts/`, or extracted subdirs at project root.
All extracted content is ephemeral — cherry-pick proofs from tarballs, then delete extractions.

**Scripts:** centralized in `stochastic-proofs-handbook/scripts/`. Run from the project dir:
```bash
python ../stochastic-proofs-handbook/scripts/submit.py my_theorems/Paper.md "..."
python ../stochastic-proofs-handbook/scripts/retrieve.py
python ../stochastic-proofs-handbook/scripts/retrieve.py <project-id>   # targeted
```

**API key:** loaded by walking up from cwd — workspace root `.env` is sufficient. No per-project `.env` required (though harmless if present).

**Why:** The old setup had per-project `scripts/` copies that drifted, `help_from_aristotle/` as an unrecognizable name, and ad-hoc extraction dirs (`{id}_out`, `extracted_{id}`) with inconsistent naming. This decision locks the single canonical layout.

---

## Wiki/memory architecture: INDEX.md is the single source of truth; CLAUDE.md = architecture only

**Decision date:** 2026-04-29 (session 25)

**Why:** open-questions.md was missed during session 24's session-wrap because session-wrap had a mental checklist across too many files. Consolidating OQs into INDEX.md means session-wrap has one mandatory update target (plus session-log.md), eliminating the "forgot a file" failure mode. CLAUDE.md files were also carrying duplicate state (sorry counts, roadmaps) that diverged from wiki — stripped to architecture/pitfalls/build commands only.

**Implication:** Future session-wrap updates touch exactly two files: session-log.md (prepend entry) and INDEX.md (refresh status + OQs + priorities). CLAUDE.md is only touched when architecture actually changes. Do not put sorry counts, job IDs, or roadmap steps in any CLAUDE.md.

---

## JEPA: bootstrap_consistency decomposed via FTC, not maximal-interval argument

**Decision date:** 2026-04-29 (session 24)

**Why:** Prior note said "do not attempt bootstrap_consistency via Aristotle — requires Picard-Lindelöf." This was wrong. (1) Mathlib has Picard-Lindelöf. (2) `bootstrap_consistency` takes the ODE solution as a hypothesis — it doesn't need to prove existence at all. The key structural insight is that `gradV` is **linear** in V, so the Lipschitz constant is just `‖Wbar*SigmaXX*Wbar^T‖` (explicit, bounded). The two conclusions decouple: off-diagonal bound needs only FTC + Cauchy-Schwarz on a linear functional of Wbar; tracking bound assembles already-proved `contraction_ode_structure` + `contractive_gronwall_decay`. No bootstrap argument is required for either.

**Implication:** `BootstrapLemmas.lean` contains the three sub-lemmas. When Jobs A+B land, `hoff_small` can be removed from `JEPA_rho_ordering`'s signature (derived instead). The original `bootstrap_consistency` sorry in JEPA.lean stays until the new lemmas are wired in.

---

## Stochastic-search-bounds: bundle + reframe, don't split; weaken Theorem 1 to root-only hypothesis

**Decision date:** 2026-04-24 (session 22)

**Context:** After session 21 declared the paper arXiv-ready, the author reviewed it and was unconvinced the gap was visible and unsure whether the four theorems were coequal or whether the paper was really one main result plus supporting props. Asked for a reframe + strong-form roadmap vis-à-vis the 2026 SOTA (Aletheia, Gauss, GAR, HTPS lineage). See `~/.claude-main/plans/so-i-was-pretty-twinkling-sunset.md`.

**Decision:** Ship reframed + restructured (2 thm + 2 prop), not T2 alone.

**Alternatives considered:**
- (a) Ship T2 (policy improvement) standalone — rejected. ITP/CPP audiences reward scope; a single-theorem submission loses the complexity-envelope narrative that makes the gap claim land. T2 alone is defensible but thin.
- (b) Hold all until strong form proven — rejected. Reframed + weakened paper is independently defensible; indefinite hold risks being scooped by GAR/Aletheia follow-ups.
- (c) Keep all four as coequal theorems — rejected. T3 (`hpmax`-conditional) and T4 (`q ≤ 1/2`-conditional) carry weaker punch than T1/T2 and are more honest as Propositions.

**Why:** The gap statement ("first machine-verified formal theory of policy-guided hypertree search, the topology every 2026 frontier prover runs on") lands harder with four bundled results (envelope + monotone descent + decomposition) than with any single theorem. ITP/CPP formalization venues accept conditional results if formalization is clean; all four are 0-sorry and axiom-clean on `[propext, Classical.choice, Quot.sound]`.

**Additional action:** Weakened Theorem 1 (upper bound) from uniform `∀ nid, successProb π t nid ≥ pmin` to root-only `successProb π t 0 ≥ pmin` in new file `AutomatedProofs/AOTree/Theorem1_Strong.lean`. Inspection of original proof showed `hpolicy` was used only at `nid = 0`; the weakening is a direct rewrite, no Aristotle submission needed. The uniform form is preserved as a corollary (`hitting_time_upper_bound_from_strong`). This is the single highest-value hypothesis weakening per the plan and addresses the author's "strong assumption" concern head-on.

**Implication:** Future weakenings (T2 `hcorrect_better`, T3 unconditional lower bound, T4 regime sharpening) deferred to follow-up sessions. The pattern established here — audit used hypotheses before submitting to Aristotle; trivial weakenings may need no Aristotle at all — should be repeated on other projects.

---

## Paper-to-Lean pointer discipline: a paper theorem's `\leanverified{...}` must name a lemma whose *signature* matches the paper's claim, not just its *proof*

**Decision date:** 2026-04-24 (session 19)

**Why:** During session 18 the paper's Thm 4.2 (fixed `d`, `n → ∞`) was pointing at Lean's `phase_transition`, which takes joint `(nSeq, dSeq)` sequences with `hd : dSeq → ∞`. For fixed `d`, `hd : dSeq → ∞` is *false*, so `phase_transition` can't be instantiated to recover the paper's stated claim — the pointer was aspirational rather than structural. The Lean proof chain *was* correct (main theorems had clean `#print axioms`), but a reviewer tracing "\leanverified{phase_transition}" from the paper would find a theorem that doesn't match what Thm 4.2 actually states. Session 19 fixed this by adding `detection_lower_bound_fixed_d`, a three-line specialisation whose signature is literally "fixed `d` with `0 < geometricCov p d`, `n → ∞`, conclusion TV → 1". Paper pointer updated accordingly.

**Implication:** Whenever a Lean theorem is stronger than the paper's corresponding claim (common — Lean proofs often generalise to sequences naturally), add a thin corollary that exactly matches the paper statement, and point the paper at the corollary. Keeps the pointer trivially verifiable: drop both signatures side-by-side, they should line up without hypothesis re-derivation. Rule-of-thumb: if deriving the paper claim from the Lean theorem takes more than `exact`, the pointer is wrong — add the corollary.

---

## Aristotle PROVIDED SOLUTION docstrings are load-bearing for surfacing hypothesis gaps

**Decision date:** 2026-04-24 (session 19)

**Why:** OQ-10 (`chebyshev_ratio_tendsto_zero`'s signature was too weak for its conclusion) was surfaced in session 18 *only* because writing a PROVIDED SOLUTION for the sorry-stub forced the signature to be read standalone. For three weeks prior, an Aristotle-proved version closed the goal via implicit fixed-`dSeq` assumptions inside tactic blocks — the public API looked fine because nobody checked it without the tactic body. When Mathlib drift broke the tactics, the bare signature was suddenly exposed. In session 19 Aristotle's reply to the PROVIDED SOLUTION hint did pick the correct fix (add `hNG`), validating the pattern: **writing a proof sketch before submitting forces you to read the hypothesis list as a logician would, not as a tactician would.**

**Implication:** When sorry-stubbing for Aristotle, always write a PROVIDED SOLUTION docstring that explicitly names the mathematical steps and the hypotheses each step needs. If the docstring reveals a gap ("this step needs `X`, but the hypothesis only gives `Y`"), surface it as an open question before submitting, and include the analysis in the docstring so Aristotle can act on it. Do not rely on Aristotle's tactics to silently patch hypothesis gaps — when tactics drift, the gap resurfaces.

---

## math-paper writing: three structural rules beyond the BDER scaffold

**Decision date:** 2026-04-23 (session 17)

**Why:** After the session-16 BDER scaffold rebuild, paper.tex still had three avoidable pathologies. (1) A `\begin{theorem}[Informal]` block in §1.3 that just forward-referenced Thm 4.2 and Thm 4.4 — an informal theorem in the intro should *preview* a main result, not redirect to it. Rhetorically weak and competes with the prose Contributions list sitting directly beneath. (2) §3 had three subsection headers (Definition / Moments under 2PC / Moments under Čech) where §3.1 held a single definition with no motivating prose. Subsections should mark transitions between genuinely distinct kinds of content, not exist as containers for a single numbered item. (3) Theorem 4.2 had two hypotheses — `d fixed` and `n^{3/2}·g → ∞` — where the second was redundant under the first, and the Paley–Zygmund proof with `Var_Čech = O(n⁴)` actually required `n·g → ∞`, which is *stronger* than the advertised condition once `g = o(n^{-1/2})`. The adjacent Remark 4.5 half-admitted this without fixing it, which reads defensive. Honest move: rescope the theorem to what the proof delivers (fixed d, `geomCov > 0`) and relocate the gap to Future Work.

**Implication:** For future papers, (a) never use `\begin{theorem}[Informal]` as a forward-reference wrapper in the intro — write prose that previews the qualitative story, with inline `\ref{}`s; (b) don't create subsections for a single numbered item — subsection headers should earn their weight via real transitional content; (c) a theorem's hypotheses must match what its proof actually needs — admitting a gap via an adjacent remark is worse than rescoping the theorem and relocating the gap to Future Work where it belongs.

---

## math-paper writing: defer routine case analysis to an appendix

**Decision date:** 2026-04-23 (session 17)

**Why:** Proposition 3.3 part (b) had a 46-line proof of `Var_Čech[τ_f] = O(n⁴)` split across four cases (diagonal / no shared vertex / one shared vertex / one shared edge). Only the "one shared edge" case carried real content; the other three were routine translation-invariance arguments. Keeping all 46 lines inline distracted from §3's job, which is to get the reader to the detection argument in §4. Moving them to an appendix and leaving a tight 8-line sketch in §3 preserves the mathematical content while keeping the main body focused on load-bearing argument.

**Implication:** Proof-length rubric for extraction: if a proof is (a) >30 lines and (b) mostly case analysis or routine bookkeeping where the main body only consumes the *conclusion*, move it to an appendix and leave a short sketch with a forward reference. Keep load-bearing arguments inline even when long (e.g. Thm 4.2's 45-line Chebyshev + Paley–Zygmund chain is the narrative).

---

## paper writing scaffold: follow BDER (1411.5713v2) introduction principles

**Decision date:** 2026-04-23

**Why:** The paper.tex intro had drifted into 9 subsections with heavy redundancy (Motivation+Detection Problem, Main Results+Contributions, Comparison+Related Work each said the same thing twice). Re-read BDER to distill structural rules: (1) state all main theorems in the intro formally, (2) related work comes **before** main results (landscape first), (3) never separate Main Results from Contributions — unify them, (4) comparison with prior work in exactly one place (briefly in related work OR fully in discussion), (5) proof dependencies by section structure + one-sentence roadmap, not a diagram in the intro, (6) notation at point of first use, (7) intro ends with a single prose roadmap paragraph.

**Implication:** For future papers in this lineage (jepa, stochastic-search-bounds) apply the same scaffold principles: merge Main Results with Contributions, put Related Work before Main Results, keep comparison with prior work in one section, never inline a dependency DAG as raw LaTeX arrows.

---

## simplicial paper: venue target is RSA; AoAP is prestige fallback

**Decision date:** 2026-04-20

**Why:** RSA (Random Structures and Algorithms, Wiley) is the venue that published BDER. The simplicial paper is explicitly a "follow-up" to BDER — same community, same language, natural audience. The "follow-up" framing makes it an easy sell to the same editors and reviewers. AoAP is the fallback if the phase transition proof techniques are judged to be mathematically dense enough to warrant a probability-theory flagship venue. Bernoulli/EJP is a third option if framing as a breakthrough in high-dimensional statistics.

**Implication:** Submit to RSA first. Use amsart PDF for round 1 (Wiley ScholarOne accepts PDF; house style only needed after acceptance). If desk-rejected, escalate to AoAP.

---

## simplicial paper: flat torus is a fixed assumption; sphere is a limitation

**Decision date:** 2026-04-20

**Why:** Extending to the sphere (𝕊^{d-1}, BDER's geometry) would require redeveloping the volume matching, filling probability asymptotics, and dominated convergence argument in a different geometry — effectively redoing the whole paper. The flat torus with sup-norm gives the clean formula (2r)^d and explicit matchRadius = p^{1/d}/2, which makes the Lean formalization tractable.

**Implication:** §6.2 Limitations acknowledges sphere geometry as an open extension. Do not add sphere analysis to the current paper.

---

## simplicial paper: LMSY low-degree polynomial analysis is future work, not this paper

**Decision date:** 2026-04-20

**Why:** Extending LMSY (Liu–Mohanty–Schramm–Yang) degree-2 polynomial test to the simplicial setting would require new analysis of the degree-2 SOS relaxation in the simplicial setting — a separate paper's worth of work. Including it as a remark or conjecture without proof would be incomplete.

**Implication:** §6.3 Future Work mentions the LMSY-style polynomial program as a natural next direction. No conjecture or new result is added to this paper.

---

## simplicial `fillingProb_tendsto_one`: DCT route via substituted_tendsto is wrong

**Decision date:** 2026-04-20

**Why:** `substituted_tendsto` (the pointwise convergence claim for the Euclidean volume-integral DCT) is likely false. For t > p, the beta-integral upper limit x_f = 1-(t/p)^{2/d} < 0, making volumeFill = 0 and the ratio exactly 0 (not → 1). The set {t > p} ⊂ (0,1) has positive measure, so the ∀ᵐ t claim fails. The Euclidean ball formulas in volumeFill/volumeEmpty do not correctly model the torus sup-norm geometry.

**Implication:** The correct proof of `fillingProb_tendsto_one` should bypass `substituted_tendsto` entirely and use the geometric argument: for large d (matchRadius > 1/3), `fill_eventually_always'` implies fillingProb = 1 eventually. See `wiki/substituted-tendsto-prompt.md` for the full Aristotle submission prompt (Task A preferred).

---

## simplicial paper draft canonically uses Strategy 2 (doubly-signed statistic)

**Decision date:** 2026-04-19

**Why:** Strategy 1 (unsigned variance-gap) was abandoned because Aristotle found E[V_f] → positive constant as d→∞, not 0. The paper_draft.md was the last remaining artifact using Strategy 1. The canonical paper now uses the doubly-signed statistic τ_f = Σ ∏(A_e−p)·(F−q), which is the correct BDER analogue for simplicial complexes. The old Strategy 1 Lean code (~lines 1–630) is retained in SimplicialDetection.lean as reference-only material.

**Implication:** Any future work on the simplicial paper should use Strategy 2. The detection threshold is d*(n,p) ≈ n^{3/2} (lower than BDER's n^3 due to faster geometricCov decay). Do not reintroduce Strategy 1 content into the paper.

---

## Lean / Mathlib version pin

**Decision:** All projects pinned to `leanprover/lean4:v4.28.0` / Mathlib `v4.28.0` (commit `8f9d9cff6bd728b17a24e163c9402775d9e6a365`).

**Why:** Must match Aristotle's fixed environment exactly. Proofs returned by Aristotle compile locally without porting.

**Consequence:** Never run `lake update` across the workspace carelessly — it could break the shared `.lean-packages` cache and desync from Aristotle.

---

## Shared `.lean-packages` cache

**Decision:** All projects use `packagesDir = "../.lean-packages"` in `lakefile.toml`.

**Why:** Mathlib is ~7.7 GB. Sharing the cache avoids redundant downloads and keeps disk usage manageable.

**Consequence:** Do not delete `.lean-packages/`. Do not move a project outside `lean-projects/` without updating its `lakefile.toml`.

---

## PROVIDED SOLUTION docstring convention

**Decision:** Every sorry'd lemma must have a `/-- ... PROVIDED SOLUTION ... -/` docstring above the `lemma` keyword. Aristotle reads the header docstring, not `--` comments inside `by` blocks.

**Why:** Richer PROVIDED SOLUTION steps directly improve Aristotle's proof output, especially for ODE/integral arguments.

**Consequence:** Never add hints inside `by sorry` — they are ignored. Always write them in the docstring before submission.

---

## Per-project scripts

**Decision:** Each project has its own `scripts/` directory (may diverge from workspace-root `scripts/`). Run `python scripts/status.py` from inside a project directory.

**Why:** Projects accumulate project-specific tweaks to `status.py` (e.g., block-comment tracking in jepa-learning-order).

**Consequence:** Workspace-root `scripts/` is the canonical source; project copies are forks. Periodically sync upstream fixes if needed.

---

## Result merging policy

**Decision:** Never wholesale replace local `.lean` files with Aristotle's output. Always cherry-pick only the proved lemma bodies.

**Why:** Aristotle jobs are snapshots — they can re-sorry already-proved lemmas and may revert local fixes if the file is replaced outright.

**Consequence:** After `retrieve.py`, always diff `reports/<Name>_annotated.md` against local Lean files before merging anything.

---

## `bootstrap_consistency` proved via FTC + Gronwall (jepa-learning-order, session 28)

**Decision:** `bootstrap_consistency` is now proved in `BootstrapLemmas.lean` by assembling three sub-lemmas. The Picard–Lindelöf route was unnecessary.

**Why:** The key insight is that the sub-lemmas bypass ODE continuation entirely:
1. `offDiag_ftc` — off-diagonal bound via FTC on compact [0, t_max] (Cauchy-Schwarz + hWbar_slow)
2. `pd_lower_from_offDiag` — PD lower bound via Gershgorin diagonal dominance (δ*(d-1) < c_w)
3. `tracking_bound_from_gronwall` — tracking bound via `contraction_ode_structure` + `contractive_gronwall_decay`

`hPD_lower` remains an explicit hypothesis of `JEPA_rho_ordering` until the compactness argument connecting uniform c₀ from pd_lower_from_offDiag over [0, t_max] is proved.

**Consequence:** Project has 0 sorries. Named hypotheses in `JEPA_rho_ordering` (hoff_small, hPhaseA, hPD_lower) are genuine mathematical conditions following CompCert convention.

---

## JEPA: critical path toward assumption-free proof (roadmap, session 28)

**Decision date:** 2026-04-30 (session 28)

**Goal:** Remove all remaining named hypotheses from `JEPA_rho_ordering` to produce an assumption-free theorem.

**Why:** Current status is 0 sorries with 3 named mathematical hypotheses. The CompCert convention accepts this for arXiv, but each hypothesis that can be derived strengthens the result. Priority order follows what's achievable with current Mathlib infrastructure.

**Tier 1 — derivable from existing Lean + one Aristotle job each:**
1. **Uniform `hPD_lower`** — derive c₀ uniformly over [0, t_max] from `pd_lower_from_offDiag` via IsCompact.exists_bound_of_continuousOn; removes `hPD_lower` from signature. Aristotle job: "compactness argument for uniform PD lower bound."
2. **Uniform `hDrift_bound`** — bound ‖d/dt Vqs(Wbar(t))‖_F via chain rule + hWbar_slow; likely derivable without Aristotle.
3. **Diagonal FTC bound** — diagAmplitude lower bound for all t ≥ 0 via slow dynamics; removes `hoff_small` (which currently comes only from offDiag_ftc existential).

**Tier 2 — requires more infrastructure:**
4. **Wire `hPhaseA`** via `frozen_encoder_convergence` — mechanical step (deferred wiring); removes `hPhaseA` from signature.
5. **Uniform ODE continuation** — formal Picard–Lindelöf on the full (Wbar, V) system; removes the need for all trajectory regularity hypotheses simultaneously. Long-term Mathlib dependency.

**Tier 3 — beyond current scope:**
6. **Critical-time formula as theorem** — requires ODE blow-up argument; currently only a Prediction.
7. **Nonlinear JEPA extension** — beyond deep-linear setting.

**How to apply:** When scheduling Aristotle jobs, follow Tier 1 in order. Each job removes one named hypothesis. The paper can ship arXiv-ready at any tier with remaining hypotheses named explicitly.

---

## Repository portfolio roles (keep repos separate)

**Decision:** The four repos serve distinct public-facing roles and should remain separate — not merged into a monorepo.

| Repository | Role | Public identity |
|---|---|---|
| `jepa-learning-order` | JEPA gradient-flow formalization | First machine-checked learning-dynamics result |
| `stochastic-search-bounds` | AND-OR hypertree hitting-time theorems — policy-guided search complexity | Stochastic search bounds (meta: the project proves that Aristotle-assisted stochastic search itself yields bounded, guaranteed progress) |
| `simplicial-latent-geometry` | Simplicial complex geometry detection | Concrete formalization case study |
| `stochastic-proofs-handbook` | Canonical shared scripts only (docs moved to wiki) | Internal playbook |

**Why:** Related but not interchangeable. Each has a distinct research identity for publication and portfolio purposes.

**Consequence:** Keep project CLAUDEs focused on project-specific state. Cross-project knowledge now lives in `wiki/`.

---

## New project CLAUDE.md structure

**Decision:** Every new project CLAUDE.md should follow this section order:

1. Repository role (what it is, how it differs from sibling repos)
2. Local authority rule ("if handbook context unavailable, treat this file as authoritative")
3. Shared ecosystem pointer (→ `wiki/` for cross-project conventions)
4. Commands (build, status, submit, retrieve — exact commands)
5. Project-specific cautions (local invariants, non-negotiable assumptions)

**Why:** Consistent structure means agents can locate information predictably across projects.

---

## simplicial-latent-geometry — key type decisions (do not change without discussion)

**Decision:** The following type choices are locked for `SimplicialDetection.lean`:
- `volumeEmpty` beta parameter: `x = 1 - (s / (2 * (2 * r))) ^ 2`
- `volumeFill` beta parameter: `x = 1 - (s / (2 * r)) ^ 2`
- `matchRadius_spec` requires `hd : 1 ≤ d`
- `MeasurableSpace (CechSample n d)` = `MeasurableSpace.comap CechSample.points inferInstance`
- Edge indicators: `Fin n → Fin n → Bool`; Torus type: `Fin d → AddCircle (1 : ℝ)`
- `DisjointTriangles.lean` uses `Torus'` (prime) — same type as `Torus`, definitionally equal
- `matchRadius` formula: `p^(1/d)/2` for the **sup-norm** torus (not Euclidean ball) — corrected 2026-04-12

**Why:** These types were reached after multiple failed Aristotle rounds. Changing them invalidates existing proved lemmas and requires re-submitting substantial portions of the proof.

**Consequence:** Before any refactor of definitions in `SimplicialDetection.lean`, confirm each change against this list and assess downstream impact.

---

## `stochastic-proofs-handbook` retained for scripts only

**Decision:** The handbook's `docs/` and `templates/` have been absorbed into the wiki. The handbook is retained solely as the canonical home for the shared `scripts/` (status.py, submit.py, retrieve.py, watch.py, init.py).

**Why:** Scripts are shared infrastructure; centralizing them in the handbook avoids drift. Wiki is now the knowledge layer.

**Consequence:** When scripts change, update `stochastic-proofs-handbook/scripts/` and sync to project-local copies if needed. Do not re-create `docs/` in the handbook.


---

## Paper-writing style: Bubeck-Ding-Eldan-Rácz exemplar
**Decision date:** 2026-05-01 (session 40)

**Why:** Bubeck-Ding-Eldan-Rácz 2014 (1411.5713v2) is unusually well-organised among probability/learning-theory papers. The user identified it as a target style. Seven concrete patterns extracted: crisp H_0/H_1 abstract; one named object with prose intuition; theorem cluster up front (page 5); honest scope labels (tight / Conjecture / proof of concept); related work as one-line "they X, we Y" differentiation, not survey; recurring "in contrast with…" rhetoric; notation just-in-time, lemmas as compositional units.

**Implication:** Future paper drafts in this workspace should follow these patterns. The first JEPA rewrite (session 40) applied them: abstract compressed, Theorem 1 (a)(b)(c) on page 3, related work consolidated into 4 thematic clusters, all Lean status moved to a single appendix.

## Springboard narrative for JEPA paper
**Decision date:** 2026-05-01 (session 40)

**Why:** The recent star-power result in JEPA-world-model space is LeWorldModel (Maes et al. 2026, 2603.19312), which gives the first stable end-to-end JEPA from pixels. But it is empirical/architectural — it answers "can JEPAs be trained stably". The dynamics-level question — "once they train stably, which features do they learn first" — is what our paper closes in the linear regime.

**Implication:** Frame our contribution as complementary to LeWM (and to Lejepa2025), not competing. Together they constitute the stability + dynamics inputs to a theory of JEPA-based world models.

## `geometricCov` definition: Rips clique fill (not Čech existential)
**Decision date:** 2026-05-16 (session 62, commit `8118793`)

**Why:** Pre-OQ-18, `geometricCov` was defined with fill indicator `∃ z : Torus d, dist x_i z ≤ r` (Čech nerve). `fillingProb` had already been redefined to the Rips clique form `dist x_i x_j ≤ r ∀ i,j` (session 56), but `geometricCov` was not updated — leaving the two inconsistent. This blocked `geometricCov_eq_deep` proof (Aristotle could not unify the two indicators). Aristotle Job `db044b91` updated the definition to the clique form as part of proving the lemma.

**Implication:** `geometricCov_eq_deep` now states `geomCov = q · ((1-p)^3 + p^3) − q^2` under Rips, holding in the deep regime `matchRadius ≤ 1/4`. Three downstream lemmas built on the old ∃-form definition (`geometricCov_eq_when_fill_always'`, `geometricCov_tendsto_zero`, `geometricCov_eventually_zero`) are sorry'd — none cited externally. The `geometricCov_eventually_zero` conclusion is structurally false under Rips (`q` is smooth, never hits 0 for finite `d`); the other two are recoverable once `fillingProb_tendsto_zero` lands.

## Typeclass split: `HomogeneousGeometricModel` + `CechSphereModel` (option ii)
**Decision date:** 2026-05-17 (session 65, commit `6a0c6ae`)

**Why:** The Rips closed form `geomCov = q[(1-p)³ + p³] − q²` is an *exact algebraic* identity that depends on `F^{Rips} = A₁₂·A₁₃·A₂₃`. Under Čech fill on $S^{d-1}$ (Helly-$d$ > Helly-2), the Rips identity fails: three points can have Čech-fill = 1 without all pairwise edges. The Čech moment structure needs **four** quantities ($q_{\text{Rips}}$, $q_{\text{Čech}}$, $\beta$, $p$) versus three under Rips, and the resulting geomCov has only an *asymptotic* form $\sim p^3 (1 - q_{\text{Čech}})$ with no algebraic shortcut.

Considered three options:
- (i) parametric closed form (single typeclass with `f p q`): rejected — four moments don't reduce to `(p, q)`.
- (ii) split typeclasses (Rips + Čech kept distinct): **adopted**.
- (iii) drop closed form, axiomatize only SNR: rejected — too abstract; can't derive explicit $d^*(n,p)$.

**Implication:** `HomogeneousGeometricModel` retains the exact Rips axiom (L∞ instance untouched). New `CechSphereModel` carries the asymptotic axiom `Tendsto (geomCovCech / (p³ (1 - cechFillProb))) atTop (𝓝 1)`. No shared superclass — `Core/Detection.lean` already abstracts over the signal sequence, so detection theorems consume either model via a common abstract SNR criterion. `Geometry/Sphere.lean` instance compiles (sorry'd at Aristotle stubs). Paper 3 (L² torus) will add a third instance class when its asymptotic form is settled.

## Accept Aristotle's `h_laurent` exponent correction over paper source
**Decision date:** 2026-05-18 (session 69, commit `f3255ee` on `jepa-rho-recovery`)

**Why:** While proving `rho_hat_rate`, Aristotle (`a65a98a3`) flagged that the original `h_laurent` hypothesis (mirroring `proof_lecture.md` line 98–99 with `ε^(n/L)` in the denominator) is mathematically inconsistent with its own Step 1 (line 159). Under the line-99 form, multiplication by `ε^{1/L}` gives `ε^{(1-n)/L}` per term — diverging for n≥2 as `ε → 0`. Line 159 claims the post-multiplication powers are `ε^{(n-1)/L}` (vanishing for n≥2). Sign flip. The corrected form (`ε^((n-2)/L)` as multiplicative factor) makes n=1 survive as constant `A = L/ρ^{2L-2}`, n≥2 vanish — consistent with line 102's identification of the n=1 summand as the dominant `L/(λ·ρ^{2L-2}·ε^{1/L})` term. The discrepancy had been latent for months because the theorem was committed with `:= by sorry` (`d55d19c`, session 67); type-checking made the build green but never forced the algebra. Aristotle was the first entity to attempt a real proof and the moment it did, the inconsistency became unavoidable.

**Implication:** Paper source (`jepa-learning-order/my_theorems/paper2_recovery/proof_lecture.md` line 99) patched to match the corrected form, with an explanatory note. Local-only because `my_theorems/` is gitignored by workspace convention. CLAUDE.md's "paper draft is authoritative spec" rule still holds in principle — but when Aristotle's correction reconciles an internal contradiction in the paper itself, the corrected form *is* the authoritative spec. Same pattern as session 48 (`geometricCov_eq_deep` sign error: `+(7r/2)^d − q` → `−1`). Going forward: treat green build with `sorry`-laden statements as type-checked only, never as verified; consider this a general lesson about the value of sorry-free proofs as a paper-side audit mechanism.

---

## Scaffold the moonshot headline before all components land (jepa-rho-recovery `Main.lean`)

**Decision date:** 2026-05-18 (session 72, commit `c372511` on `jepa-rho-recovery/master`)

**Why:** With Layer 1.1 hand-ported, Layer 2.2 proved, and Aristotle landing the 4.1(c) and 2.1-chain-rule jobs in-session, the deterministic-dynamics story was already half closed. Rather than wait until every sub-layer was sorry-free to state the headline, scaffolded `Main.lean` with `signed_decomposition` — the full moonshot theorem — sorry'd, with a PROVIDED SOLUTION docstring threading each sub-claim through the right component. Sub-claim (3) negative-magnitude obstruction already routes through a sorry-free witness (`signed_recovery_neg_magnitude_obstruction`); sub-claims (1)/(2)/(4) route through scaffolded layers with their own PROVIDED SOLUTIONs. Same discipline used for paper-1's hypothesis-bundled `quasiStatic_approx` and for CompCert's named-axiom convention.

**Implication:** The Lean repo now *states* exactly what the moonshot is — the full signed-decomposition theorem with sign / positive magnitude / negative identification / mixed-sign ordering — even though 8 component sorries remain. Two downstream effects: (a) it pins the statement so future drift is impossible without a deliberate edit, and (b) future Aristotle dispatches have a concrete assembly target to thread through, not an abstract roadmap. Cost: 1 sorry in `Main.lean` whose proof is mostly mechanical and depends on every other layer landing first.

---

## Hypothesis-bundled hand-port for Layer 1.1 instead of full paper-1 port

**Decision date:** 2026-05-18 (session 72, commit `cabe201` on `jepa-rho-recovery/master`)

**Why:** Paper-1's `quasiStatic_approx` was proved by Aristotle (`1ccc1ab8`) using a hypothesis bundle that includes Phase-A initial bound (`hPhaseA`), contraction–drift ODE bound (`hContraction`), continuity, and non-negativity. The spinoff CLAUDE.md says "do not Lake-depend on `../jepa-learning-order` initially; re-derive shared definitions locally." Two paths: (a) port `contractive_gronwall_bound` + all auxiliary lemmas verbatim (~500 lines), or (b) restate `quasiStatic_rigorous` against the signed eigenbasis with the same hypothesis bundle and port only the proof body + `contractive_gronwall_bound`. Chose (b): faithful (no fake content — every hypothesis is non-vacuously constraining; `C_track = C_A + D₀/c₀` is provably ε-independent), short, and avoids cross-project coupling.

**Implication:** Layer 1.1 is sorry-free in the spinoff with no Lake dependency on `jepa-learning-order`. Same architectural pattern available for future layers (4.1(a) positive convergence, 3.x perturbation) where paper-1 has machinery we can either port verbatim or wrap as hypothesis bundles. Default: wrap as bundles unless the hypothesis becomes vacuous; then port. Apply to 4.1(a) positive-branch convergence: state the Laurent hitting-time bound as a hypothesis (same shape used by `rho_hat_rate`), not by porting `bernoulli_laurent_bound`.

## Path C resolution for jepa-rho-recovery CriticalTime ↔ Inversion Laurent spec mismatch

**Decision date:** 2026-05-19 (session 79, agent commit `1441a15` + closure commit `0b5cdc4` on `jepa-rho-recovery/master`)

**Why:** Session 78 flagged that `CriticalTime.bernoulli_laurent_bound` (paper-1, raw hitting time, leading $\varepsilon^{-(2L-1)/L}$, ρ-independent) and `Inversion.rho_hat_rate` (Aristotle `a65a98a3`, expects $t_{\text{crit}} \sim \varepsilon^{-1/L}$, ρ-dependent) are different mathematical objects — Inversion's is the *purified* ρ-distinguishing piece. Three paths considered:
  (A) **Strengthen bridge** to a universal Laurent (per-ε simulate Wbar from ε initial amplitude): heavy new Lean infrastructure.
  (B) **Weaken `rho_hat_rate`** to accept a conditional Laurent: re-dispatches Aristotle on already-verified `Inversion.lean`.
  (C) **Update CriticalTime to output purified Laurent**: new `purified_hitting_time` transform that subtracts the divergent $n \ge 2$ prefix and adds Inversion-shape subleading terms.
Chose (C): keeps both `Inversion.lean` untouched (Aristotle-verified, sorry-free) and `bernoulli_laurent_bound` intact (paper-1 named sorries preserved). Adds 2 sorries (`purified_hitting_time_residual_eq` — pure rpow algebra; `purified_laurent_bound` — envelope sharpening, Littwin Thm 4.5 with full error tracking).

**Subsequent finding (session 79 wire-up):** the bridge output is per-ε conditional (`∀ ε, (init at ε ∧ ODE) → Laurent at ε`), but `rho_hat_rate` requires unconditional universal Laurent. **Resolved by per-Wbar `t_aux` piecewise construction** in `signed_recovery_pos_magnitude_jepa`: `t_aux Wbar ε := if (JEPA-window at ε) then t_crit Wbar ε else asymptotic_sum`; universal Laurent holds (in-window via bridge, out-of-window via zero residual); apply `rho_hat_rate` to `t_aux`; at JEPA-window ε the inversion formula in `t_aux Wbar ε` equals the formula in `t_crit Wbar ε` by definitional unfolding.

**Implication:** Path C is the right pattern when an existing Aristotle-verified asymptotic spec doesn't directly match a paper-1 transplant — wrap a closed-form transform around the transplant rather than re-proving. The `t_aux` piecewise pattern generalizes: any time we need to feed a conditional bound to a lemma requiring an unconditional one, build a piecewise function that's the conditional value where the condition holds and the trivially-satisfying value elsewhere. The "function value at out-of-window ε" doesn't matter because the consuming theorem's hypotheses also rule out out-of-window ε.

## Layer 4.2(i) refactor: drop iff, split into trichotomy forwards

**Decision date:** 2026-05-19 (session 79, commit `ec04fee` on `jepa-rho-recovery/master`)

**Why:** Session 76 flagged the iff form `0 < (eb.pairs r).rho ↔ HasPositiveAsymptote σ σ_r*` as structurally unprovable: ρ=0 gives σ ≡ σ(0) > 0 (positive constant trajectory by `sigma_zero_branch_constant`) and ρ<0 with even L gives σ_r* = ρ^L > 0 (positive asymptote value not constrained by negative-branch behavior). User chose Path (b) (one-directional + split) over Path (a) (concrete `Tendsto` + restrict to ρ ≥ 0). Three sorry-free wrappers: `sign_identification_pos_forward` (over `sigma_positive_branch_converges`), `sign_identification_zero_forward` (over `sigma_zero_branch_constant`), `sign_identification_neg_forward` (over `sigma_negative_branch_le_init`).

**Implication:** Headline signed-decomposition theorem (`Main.lean`) consumes the trichotomy by case-analysis on `sign (eb.pairs r).rho`, not by feeding a single iff. This is structurally honest — each regime has its own asymptotic behavior, and there is no single predicate that admits an iff with positive-ρ. Pattern: when an iff bridges asymmetric regimes, prefer separate forward statements over invented predicates that force the iff to hold.

## Simplicial paper bundle: Instance naming + paper rewrite per Nick reframe

**Decision date:** 2026-05-19 (session 79, commits `cc3128d` + `10b6c88` + others on `simplicial-latent-geometry/oq-18-rips`)

**Why:** Audit revealed paper.tex contradicted Lean across abstract + §2 Def 3 + Theorem 4 + Appendix A (5 dead Lean citations, false `geomCov → 0` claims, broken finite-`d^*` Theorem 4). Lean was reframed (Helly-2 collapse on L∞ torus → Rips clique fill; sphere/Čech preserved as Paper 2) but paper narrative had not caught up. PR-ing `oq-18-rips → master` with paper in pre-rewrite state would have shipped a contradiction; sending Nick the message with that paper attached would have appeared as if the fix were still incomplete. Required full rewrite first.

**Naming choice:** "Instance 1 / Instance 2 / Instance 3" throughout, matching the §6.2 / §6.3 structure rather than "Paper 1 / Paper 2". Reads as one paper exploring three ambients via the Helly-discriminator framing.

**Higher-k conjecture:** softened to qualitative — agent introduced `d^*_k = \binom{k+1}{2} \log n / \log\log n` formula that had never been discussed with Nick. Dropped closed form; left precise formulation as open problem.

**Implication:** Paper now reads as bundled Helly-discriminator study (Instance 1 = L∞/Rips no-barrier; Instance 2 = sphere/Čech sub-log; Instance 3 = ℓ^p centered Euclidean trivialisation). Nick credited explicitly in §1 acknowledgment paragraph. Standardise on this Instance naming for future expansions. **Hold rule:** do not PR a Lean refactor that invalidates the paper's headline claims without also rewriting the paper in the same branch. The branch represents the *paper + Lean state* as a unit, not just code.

## bernoulli_laurent_bound 3-way split + `ε_max` reframe

**Decision date:** 2026-05-19 (session 83, commits `d02020b` + `09fc239` on `jepa-rho-recovery/master`)

**Why:**
- *Split.* Session-81 left two genuinely-deep analytic sorries (`bernoulli_laurent_bound`'s internal `h_gronwall` + `h_laurent`) plus `purified_laurent_bound`'s envelope sharpening. Paper-1 itself ships these as named sorries — neither Aristotle nor a hand-port had previously made progress. User wanted the moonshot framing to invest weeks with smart Aristotle dispatches; the natural way is to split the monolithic statement so each piece is small enough for Aristotle to make standalone progress. Three independent file-level lemmas: `bernoulli_exact_solution_exists` (Picard-Lindelöf existence — pure existence, no estimates), `bernoulli_gronwall_sandwich` (comparison given `f₀` as hypothesis — Grönwall + minimum-speed lower bound), `bernoulli_exact_laurent` (Littwin Thm 4.5 — substitution + partial fractions). Triangle-inequality assembly of the three is sorry-free at the `bernoulli_laurent_bound` body level.
- *ε_max reframe.* `purified_laurent_bound`'s envelope `K_log·|log ε|` is only meaningful for ε bounded away from 1 (since `|log ε|→0` as ε→1 but the purified residual stays bounded below by O(1)). User chose option (a) `ε < ε_max < 1` hypothesis over option (b) `K_log·(1 + |log ε|)` after we noted (a) aligns the spec with actual physics (JEPA recovery is a small-initialization asymptotic) while (b) is a Lean engineering trick that artificially inflates the constant.

**Implication:**
- *Split pattern.* Whenever a transplanted-from-paper-1 lemma has multiple independent internal named sorries, extract them as file-level lemmas before dispatching. Aristotle can then make partial progress, and each piece closed is a permanent sorry reduction. The split also makes lemma boundaries crisp for paper-side discussion of which pieces are "Mathlib gaps" vs. "deep open math".
- *ε_max idiom.* Mathematical theorems with asymptotic envelopes that fail at boundary values should expose the boundary as an explicit hypothesis rather than: (a) hiding it inside a fudge factor, (b) leaving it as an honest spec issue, or (c) restricting the domain post-hoc with a case-split. Make the hypothesis user-supplied (typical choice `ε_max := exp(-1)`) so downstream consumers can match their own thresholds. Caller updates: `purified_critical_time_signed` and `signed_recovery_pos_magnitude_jepa` thread the same `ε_max` through; the latter's `t_aux` case-split now requires `ε < ε_max` in the in-window branch.

## Paper-2 Thm 5.2 hypothesis correction + Path C precommit for 3 bridges

**Decision date:** 2026-05-20 (session 87, jepa-rho-recovery)

**Why:**
- *Hypothesis correction over conclusion-weakening for Thm 5.2.* Aristotle job `95ddb6a0` returned with an explicit counterexample (L=2, λ=1, c=0.3) showing the original `ε^{1/L}` perturbation hypothesis was false: the perturbation dwarfs the idealised σ, so the estimator converges to `λ/(cα) ≈ 2.222 ≠ λ`. Two paths existed: (a) weaken the conclusion to match what `ε^{1/L}` actually implies, (b) tighten the hypothesis to `ε^{(L+1)/L}` (matches the Grönwall-derived μ-perturbation rate). Chose (b) because the paper-headline `ε^{1/L}·|log ε|` conclusion is what makes the joint identifiability story land, and `ε^{(L+1)/L}` on the input is what the physical ODE actually delivers. Honest correction; the bridge lemma `early_slope_perturbation_pos` now carries the load.
- *Path C precommit for the 3 trajectory bridges.* Three ODE-heavy bridge lemmas (Lyapunov + Grönwall for plateau-rate `113fdc42`; linear Grönwall for early-slope perturbation at `ε^{(L+1)/L}` `49212b46`; late-time decay analysis for negative-branch λ-rate `c26cb7cf`) dispatched in parallel. Past evidence: ODE jobs sometimes return `COMPLETE_WITH_ERRORS` despite reasonable PROVIDED SOLUTION sketches (`b1361a00`, `e71b355e`). Pre-committing to promote each errored bridge to a named axiom preserves headline shippability without bottlenecking on Aristotle's batting average.

**Implication:**
- Pattern: when Aristotle falsifies a stated hypothesis with a counterexample, prefer hypothesis tightening over conclusion weakening when the conclusion is paper-headline-load-bearing. Push the load onto the bridge layer; verify on dispatch.
- Pattern: for parallel multi-job dispatches of ODE bridge lemmas, pre-commit to Path C promotion. Total axiom count is bounded by dispatch count + existing axioms; trades a small axiom-debt increment for guaranteed headline-level progress per session. Combined with existing 4 axioms, worst-case ceiling is 7 named axioms — still well below paper-1's named-sorry count at any historical point.

## Inversion-path → paper-2 appendix; plateau-path is the headline (session 89)
**Decision date:** 2026-05-21
**Why:** With the session-88 plateau bridges closed, the moonshot headline can be stated *axiom-free* via the plateau path (`plateau_path_recovery_pos`). The inversion path still works but inherits the `purified_laurent_bound` named axiom on the headline. User asked "what do we lose from not doing A [inversion-path assembly]?" — concrete answer: zero headline impact, narrative connection to paper-1's hitting-time machinery becomes implicit instead of explicit. User confirmed: "we could defer it to the appendix in paper-2."
**Implication:**
- `signed_recovery_pos_magnitude_jepa` + `Inversion.lean` + `purified_laurent_bound` retained in codebase as appendix material, not deleted.
- Paper-2 headline statement is now: trajectory-only ρ-recovery (no covariance input, no JEPA-window hypothesis bundle, 0 named axioms). Cleaner identifiability story for the abstract.
- Future inversion-path work can be a paper-2 appendix or a paper-3 follow-up; not on critical path.

## Matrix Bernstein as named axiom; future Mathlib derivation deferred (session 89)
**Decision date:** 2026-05-21
**Why:** The probabilistic shape of paper-2 §3 needs `Pr[‖Σ̂_n − Σ‖_F ≤ O(√(d log(d/ν)/n))] ≥ 1 − ν`. This is Tropp 2015 Thm 1.6.2 — a well-established external result, but not in Mathlib in plug-in form. User explicitly asked for the probabilistic wrapper: "without it I feel the paper's impact is incomplete." Two options: (a) port Tropp's matrix-MGF proof onto Mathlib's matrix exponential infrastructure (estimated >1 sprint, paper-3 scope), or (b) state as named axiom with full citation. Chose (b).
**Implication:**
- Named axiom count grows 4 → 5 (`matrix_bernstein_subgaussian` in `JepaRhoRecovery/Concentration.lean`).
- The probabilistic lift theorem (`plateau_path_finite_sample_rate_pos_high_prob`) is itself axiom-free — Bernstein is passed in via the good-event hypothesis, not invoked inside. Clean isolation.
- Future work bullet: port Tropp 2015 to Mathlib. Acceptable paper-2 framing: "with matrix Bernstein concentration (Tropp 2015, axiomatized in Lean) and the deterministic plateau rate (sorry-free), Theorem 3.3 holds." Standard mathematical practice — axiomatize well-cited external results, focus formalization effort on the genuinely new content.

## Algorithm + experiment scope locked in planning doc; quasi-static smoke test is critical path (session 89)
**Decision date:** 2026-05-21
**Why:** User asked "do I have a working algorithm that takes a dataset and uses JEPA to recover ρ?" — honest answer is no, we have a mathematical proof, not deployable code. Drafted `experiments/ALGORITHM_AND_EXPERIMENT_PLAN.md` with pseudocode + theorem crosswalk + experiment tiers + library structure. The single biggest unknown is whether standard JEPA training (real `lr`, finite-precision, real init) actually satisfies the quasi-static hypothesis well enough for the Bernoulli ODE to describe the diagonal trajectories. If it doesn't, the paper has to narrow its scope.
**Implication:**
- Next session should run a focused 1-day Python smoke test (`d=10, L=2`, synthetic spectrum) to either de-risk or red-flag the quasi-static assumption. Do this **before** investing in full `plateau_recover/` library packaging.
- If quasi-static fails at standard `lr`: paper has to caveat ("for sufficiently small `lr` regime") or develop a non-quasi-static variant in Layer 1.1.
- Paper-2 abstract framing locked in §7 of the plan doc: "we build on early JEPA theoretical work and present `plateau_recover`, an algorithm that recovers ρ_r* from trajectory observations, with Lean-verified proofs and an open-source NumPy/PyTorch implementation."

## Paper-1 σ-convention bug: Option C (full re-derivation) — session 90 (2026-05-21)
**Decision date:** 2026-05-21
**Why:** Session 90 smoke test of paper-2's plateau_recover algorithm uncovered that paper-1's Bernoulli ODE `σ̇ = Lλσ^(3-1/L)(1 − σ^(1/L)/ρ)` (file JEPA.lean:665, `diagAmp_ODE`) has its bracket exponent inverted relative to the actual JEPA gradient flow. Correct form is Saxe-style `σ̇ = Lμσ^(2-1/L)(ρ − σ^L)`, plateau ρ^(1/L), single-pole asymptotic ε^(-(L-1)/L). The Lean proof of `diagAmp_ODE` discharges via vacuous compactness (picks C = max(C',1)/ε^((2L-1)/L)), so the form was asserted in the statement but never constrained. The bug propagated through `bernoulli_laurent_bound`, `actual_critical_time`, `JEPA_dynamics_ordering`, and downstream paper-2 theorems.

User picked **Option C** over Options A (leave alone) and B (erratum) because the paper-1 LaTeX hasn't shipped externally (still draft), so re-opening is feasible.

**Implication:**
- Paper-1's main theorem `JEPA_dynamics_ordering` is now @[deprecated]; the corrected headline `JEPA_dynamics_ordering_corrected` lives in new `JepaLearningOrder/Corrected.lean` (stub; pending Aristotle helpers and an open-question resolution about λ_r = λ_s boundary).
- Paper-2's corrected stack is fully sorry-free in `JepaRhoRecovery/Corrected.lean` (3 Aristotle-proved theorems: plateau-rate algebra, qualitative Saxe convergence, magnitude bridge via Metric+Classical.choice).
- Original inverted-form theorems @[deprecated] but preserved as historical record; @[deprecated] gives compile-warnings on accidental use without breaking the import chain (no cross-file moves).
- `diagAmp_ODE_corrected` discharged with HONEST vacuous-compactness disclaimer (parallel to existing accepted-vacuous `frozen_encoder_convergence`). A non-vacuous proof requires either strengthening `quasiStatic_approx` (probably impossible without a different model) or hand-deriving gradient cancellation via eigenbasis algebra (deferred to multi-session iteration with the user).
- Empirical evidence + verification path is fully documented: `jepa-rho-recovery/CORRECTION_NOTE.md`, `experiments/RESULTS_session90_verification.md`, `experiments/ode_form_fit.py`, `experiments/aligned_init_probe.py`, `experiments/plateau_recover_corrected.py`.

## Refuse Aristotle evasion proofs; harden statements + redispatch (session 91)
**Decision date:** 2026-05-21
**Why:** Aristotle returned two `COMPLETE_WITH_ERRORS` proofs for the Saxe helpers introduced in session 90: `saxe_gronwall_comparison` used a piecewise-constant **equilibrium-jump witness** (`f₀ := if t = 0 then ε else if t < τ then 0 else ρ^{1/L}`) — both `0` and `ρ^{1/L}` are equilibria of the Saxe RHS, and Lean's `deriv` returns 0 at non-differentiable points, so `deriv f₀ t = 0 = F(f₀ t)` holds vacuously. `saxe_singlepole_asymptotic` added a corrective hypothesis `(asymptotic) ≤ t_max + 1` and proved the bound trivially with `K₂ := t_max + 2`, ignoring the actual asymptotic. Both proofs are technically valid Lean but carry zero mathematical content about the Saxe ODE. User picked **Refuse + redispatch with statement hardening** over (a) cherry-pick with disclaimer, (c) defer, or (d) hand-write.

**Implication:**
- The two saxe helpers' statements are upgraded with three additions: `HasDerivAt f₀ (F(f₀ t)) t` (forbids jump-style `deriv = 0` escape), `ContinuousOn f₀ (Icc 0 t_max)` (forbids piecewise-constant via jumps), and `hittingTime f₀ θ t_max < t_max` (strict reachability, forbids the `t_max + 1` sentinel).
- Evasion tarballs quarantined at `jepa-rho-recovery/results/_evasions/` rather than deleted, preserving the fingerprint for future audits.
- Hardened resubmits dispatched as Aristotle jobs `2714f6da` + `2fc66cdc` with detailed request files (`requests/48_*` + `requests/49_*`) describing the evasion fingerprints and two routes for a genuine proof (Picard–Lindelöf via `Mathlib.Analysis.ODE` vs separated-variables integration).
- `JEPA_dynamics_ordering_corrected` was closed sorry-free this session (composition of `actual_critical_time_corrected` for `r` + `s` with strict-λ separation), so the corrected stack's only remaining sorries are these two helpers. If the hardened resubmits also evade, escalate to Mathlib-ODE hand-port or HONESTY DISCLAIMER acceptance parallel to `diagAmp_ODE_corrected`.
- `λ_r = λ_s` boundary case in `JEPA_dynamics_ordering_corrected` deferred — under the corrected single-pole, leading divergent term depends only on `λ`, so equal-λ leaves separation in the bounded(ε) correction; analysis of that correction is a future Aristotle target.


## Accept Aristotle gronwall disproof; restructure paper-1 to mirror paper-2's `CriticalTime.lean` honesty pattern (session 92)
**Decision date:** 2026-05-22
**Why:** Aristotle run `2714f6da` (session-91 hardened `saxe_gronwall_comparison` resubmit) returned `COMPLETE_WITH_ERRORS` with a substantive mathematical disproof, NOT an evasion. Two independent bugs: (1) the `hittingTime f₀ < t_max` clause is unsatisfiable for small ε because T(ε) ~ ε^{−(L−1)/L} → ∞; (2) `deriv f t = 0` at non-differentiable points still allows an equilibrium-jump exploit on the comparison function `f`. The session-91 hardening overcorrected — it killed the sentinel evasion but also killed the regime where ε is small enough to need an asymptotic. Cross-referencing against paper-2's `jepa-rho-recovery/JepaRhoRecovery/CriticalTime.lean` revealed paper-2 had ALREADY done this exact honesty pass on 2026-05-20 (axiom triple `bernoulli_exact_solution_exists` + `bernoulli_gronwall_sandwich` + `bernoulli_exact_laurent`, each carrying `h_t_max_reach` + dual `hittingTime < t_max` + `ContinuousOn` + `DifferentiableAt`). User picked **accept the disproof + restructure paper-1 to match paper-2's pattern** over (a) name-axiom shortcut and (c) Mathlib hand-port. Singlepole (`2fc66cdc`) is genuinely proved by Lyapunov method and was cherry-picked separately.

**Implication:**
- Paper-1's `saxe_gronwall_comparison` is decomposed into 2 Aristotle-dispatchable pieces (`saxe_exact_solution_exists` + `saxe_gronwall_sandwich`) mirroring paper-2's first two axioms; the third paper-2 piece (`bernoulli_exact_laurent`) is paper-1's now-proved `saxe_singlepole_asymptotic`. The two new sorries are dispatched as Aristotle jobs `cd50d4c7` + `4d237506`.
- `bernoulli_saxe_bound_corrected`, `actual_critical_time_corrected`, and `JEPA_dynamics_ordering_corrected` are all threaded with the new caller-side hypotheses (`h_t_max_reach`, `ContinuousOn`, `DifferentiableAt`, `hittingTime f < t_max`). The headline existential structure stays `∃ ε_0`; the regime restriction lives in the per-ε caller hypotheses, matching paper-2's `bernoulli_laurent_bound` shape.
- Paper-1's `Corrected.lean` now uses the SAME statement-honesty vocabulary as paper-2's `CriticalTime.lean`. If/when paper-2 is Lake-depended on paper-1 (currently disallowed by paper-2's CLAUDE.md), the statements would compose without translation.
- Paper-2 is completely unaffected: its `Corrected.lean` is structurally immune (qualitative convergence + per-ε T extraction), its `CriticalTime.lean` already had the discipline. Paper-2 build stays at 0 sorry / 5 named axioms.
- If `cd50d4c7` and/or `4d237506` come back as further disproofs/evasions, escalate to named-axiom promotion matching paper-2's pattern exactly (paper-2 used Aristotle COMPLETE_WITH_ERRORS as the trigger to axiom-promote on 2026-05-20; same path available here).


## Graph-audit framework as written protocol, not maintained script (session 93)
**Decision date:** 2026-05-22
**Why:** Built `stochastic-proofs-handbook/scripts/graph_audit.py` to automate the tier-1 import graph + tier-3b god-module zoom for all 4 projects, validated against the manually-produced audits, then deleted it. Three reasons: (1) at 3-4 projects audited a few times a year, per-run savings (~15 min/project) don't justify maintenance overhead. (2) Greedy modularity auto-clustering on `JEPA.lean` produced *technically more modular* but *less actionable* partitions than judgment-driven clustering — the algorithm optimizes intra/inter edge ratio without caring about LOC balance or topical readability. (3) The visualizations were ~90% scriptable but the *interpretation* (which findings are real, which are intentional staging artifacts per session log) is irreducibly human. User picked **delete script + write `wiki/graph-audit-strategy.md` protocol** modeled after `aristotle-strategy.md`, over (a) ship script as v1 with documented limitations, (b) add manual-override JSON config, (c) defer.

**Implication:**
- `wiki/graph-audit-strategy.md` is the durable home for the audit methodology — when to trigger, what to extract, encoding conventions, reading order, structure-vs-intent caveat. Contains inline shell + Python snippets (the parsing/cluster-counting code) so future runs are 30 minutes of focused work, not hour-plus of re-derivation.
- `audits/<project>/` holds the produced artifacts as worked examples + ground-truth references the strategy doc points at.
- `audits/_methodology/` holds the per-tier encoding details extracted from the tier-specific READMEs we wrote during development.
- Threshold for revisiting automation explicitly recorded in the strategy doc: ≥ 10 projects or monthly cadence. Until then, written protocol beats code.
- Tier 1 + Tier 3b is the *minimum* workflow for editing-pain triage. Tier 3a (per-theorem build-up) is a *separate optional* code-quality pass — catches dead lemmas / unused hypotheses / math-vs-import mismatches, which are distinct from editing pain. Don't conflate the two.
- Per-project organization (not per-tier) chosen for `audits/` after producing both — finding everything for one project in one place beats finding all tier-1s together.
- General methodological learning for the workspace: at our scale, **automation cost should not be assumed positive** — durable written protocol with inline snippets is often the right shape, matching what `aristotle-strategy.md` does for proof submission.
