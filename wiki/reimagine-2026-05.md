# Reimagine plan — paper-1 + paper-2 under Saxe ODE form

> **Status:** draft strategy, session 99, 2026-05-23.
> **Owner:** David Goh.
> **Scope:** jepa-learning-order (paper-1) and jepa-rho-recovery (paper-2).
> **Decision:** committed (user, session 99). Step 1 is the math-graph audit;
> later steps gated on audit findings.

---

## 1. Why we're doing this

Three observations from session 99:

1. **Paper-1's ODE form is empirically wrong.** Session 90 verified that JEPA gradient flow obeys the Saxe-style Bernoulli ODE
$$\dot\sigma \;=\; L\mu\sigma^{2-1/L}(\rho - \sigma^L)$$
with plateau $\sigma^\infty = \rho^{1/L}$, not paper-1's inverted form
$\dot\sigma \propto \sigma^{3-1/L}(1 - \sigma^{1/L}/\rho)$ with plateau $\rho^L$.

2. **Paper-1's `diagAmp_ODE` Lean proof is vacuous.** It discharges by `IsCompact.exists_bound_of_continuousOn` — picks any continuous bound on $[0, t_{\max}]$ and divides by $\eps^{(2L-1)/L}$, making the residual bound trivially true with no quantitative content. The wrong ODE form typechecks because nothing constrains it.

3. **Paper-1 is not frozen.** It hasn't been posted to arXiv; it's awaiting cs.LG endorsement. There is no extant version that needs to be defended. We can fix it.

The choice we've been making implicitly — treat paper-1 as fixed and apologize for it in paper-2 (Remark 1.2, Experiment 1 ODE-form pit, App. A inverted-form deprecation table) — is unnecessary baggage. The choice we should make: fix paper-1 in place, then write paper-2 in the corrected world without needing to acknowledge the prior wrong version. Both papers come out cleaner and the joint project is set up for the natural extensions (nonlinear JEPA, LeWM springboard, V-JEPA family).

---

## 2. What success looks like

**Paper-1 (jepa-learning-order):**
- ODE form is Saxe-style throughout, in prose and Lean
- `diagAmp_ODE` Lean statement is quantitatively constraining (not vacuous)
- Critical-time / hitting-time analysis is re-derived under Saxe form, threshold redefined to be a near-plateau condition (since `p·ρ^L` isn't reachable for `p < 1` under Saxe)
- Ordering theorem (the headline) survives, ideally with the same proof template; may need weaker statement if Saxe-form Laurent doesn't admit closed form
- Simultaneous-diagonalisability removal (the structural contribution) is unchanged

**Paper-2 (jepa-rho-recovery):**
- States and proves the signed-decomposition headline directly in Saxe form, no apologetic remarks
- Drops `Remark 1.2` (ODE-form correction), Experiment 1's pit-vs-paper-1 framing, Remark 3.2 (vacuous quasi-static comparison), App. A's inverted-form deprecation table
- `Corrected.lean` is absorbed into the main Lean modules (no parallel "corrected" namespace)
- Cites paper-1 cleanly as the ordering result + simultaneous-diagonalisability removal

**Cross-project infrastructure:**
- Both Lean projects use a shared CriticalTime/Bernoulli module pattern, or paper-2 Lake-depends on paper-1 (re-decision point)
- 4 inverted-form axioms in paper-2's `CriticalTime.lean` are deleted, not deprecated
- Live axiom inventory across both projects: 1 (matrix Bernstein, Tropp 2015) on the finite-sample chain; 0 on the structural-identifiability chain

**Set up for what comes next:**
- Paper-3 candidates: nonlinear JEPA (LeWM-style, Maes et al. 2026), V-JEPA representational structure, density-of-states for continuous spectra
- The Saxe-form analysis is the natural baseline for any non-linear-as-perturbation argument; the inverted-form was a dead end for that purpose

---

## 3. Dependency map

The reimagine touches three layers. Each has dependencies that gate the others.

### 3.1 Math layer

The critical math risk is whether the Saxe-form Bernoulli ODE admits a clean hitting-time Laurent expansion.

**ODE-form-independent results** (probably survive without re-derivation):
- Simultaneous-diagonalisability removal (paper-1's contribution beyond Littwin)
- Off-diagonal coupling control via depth-$L$ Grönwall
- Quasi-static decoder existence and uniqueness (statement; the rate may change)
- Ordering claim at the qualitative level: trajectories cross thresholds in $\rho^*$ order

**ODE-form-dependent results** (need re-derivation):
- The diagonal scalar ODE itself (different form)
- Hitting-time analysis: paper-1 hits threshold `p·ρ^L`; under Saxe this is unreachable. Natural replacement: hitting time to `(1-δ)·ρ^{1/L}` near-plateau.
- Bernoulli-Laurent expansion: paper-1 uses Littwin 2024 Thm 4.5's partial-fraction integration of `1/(ψ^{2L}(1-ψ))`. Under Saxe form the integrand changes; may or may not admit a clean closed form.
- Ordering at the *quantitative* (hitting-time-Laurent) level: depends on the Saxe-form Laurent being derivable

**Critical math question:** does
$$\int_\eps^{(1-\delta)\rho^{1/L}} \frac{d\sigma}{\sigma^{2-1/L}(\rho - \sigma^L)}$$
admit a closed-form expansion as $\eps \to 0$? Substitution $\psi := \sigma^L/\rho$ gives
$$\frac{1}{L\rho^{1-1/L}}\int_{\eps^L/\rho}^{1-\delta} \frac{\psi^{(1/L)-1}\,d\psi}{\psi^{2-1/L}(1-\psi)}$$
which is a Lauricella-type hypergeometric integral. *Plausibly* clean (Littwin's case is the special $1/L \to 0$ degeneration); *plausibly* harder. This is the math-risk piece we want to dispatch to Aristotle early so the rest of the plan is contingent on it.

### 3.2 Lean layer

Topological order of Lean refactor (deepest dependency first):

1. **`jepa-learning-order/JEPA/Core.lean`**: change the ODE statement in `diagAmp_ODE` to Saxe form; make the residual bound quantitatively constraining (the current `IsCompact` discharge fails on the new statement).
2. **`jepa-learning-order/JEPA/Bernoulli.lean`**: re-derive Bernoulli ODE machinery under Saxe form. If the Saxe Laurent closes (§3.1 risk), this is direct port; if not, fall back to monotone scalar sandwich without the closed-form leading order.
3. **`jepa-learning-order/JEPA/DiagAmpODE.lean`**: thread the new ODE form through.
4. **`jepa-learning-order` headline (`MainTheorem.lean`)**: prove ordering under Saxe-form critical times. The ordering character should survive but may need re-stating.
5. **`jepa-rho-recovery`**: delete `Corrected.lean`. Absorb its content into `SignedRecovery.lean` / `PlateauEstimator.lean` / `Main.lean` as the canonical (no-suffix) versions. Delete the 4 inverted-form axioms from `CriticalTime.lean` once paper-1 provides Saxe-form replacements. Re-export from paper-1 instead of re-deriving locally (decision point: Lake-depend on paper-1, or copy the corrected Bernoulli machinery into paper-2's tree?).

### 3.3 Prose layer

- **Paper-1**: re-write §6 (hitting-time analysis) under Saxe form. Update Theorem 6.1's statement if the Laurent doesn't close. Other sections largely unchanged.
- **Paper-2**: drop Remark 1.2, restructure Experiment 1 (validation of the Saxe form against simulation is still useful, but framed as "we verified our ODE assumption" not "we corrected paper-1"), drop Remark 3.2, drop App. A's inverted-form deprecation block.
- **Both papers**: ensure citation flow is clean (paper-2 cites paper-1 as the simultaneous-diagonalisability removal + the ordering result, nothing about inverted form).

---

## 4. Phased plan

Five phases, gated.

### Phase 0 — Math-graph audit (1 session, blocking)

Run a tier-3a per-theorem audit on `jepa-learning-order`. For each theorem in paper-1:
- Tag ODE-form-dependent vs. ODE-form-independent
- Identify the proof-step dependency graph among the ODE-form-dependent theorems
- Output a partition: which theorems can be re-derived mechanically under Saxe form (template transfer) vs. which need new math

Output artifact: `audits/jepa-learning-order/REPORT-saxe-reimagine-2026-05.md`.

**Go/no-go gate:** if the audit shows > 50% of paper-1's apparatus needs genuinely new math (not template transfer), shrink scope to Option 2 (paper-2-only cleanup, fix paper-1 later). Else proceed to Phase 1.

### Phase 1 — Math closure (2–4 sessions, math-risk concentrated)

Dispatch Aristotle on the Saxe-form Bernoulli Laurent. Two attempts:
1. First attempt: ask for the Laurent expansion via the $\psi := \sigma^L/\rho$ substitution
2. Second attempt (if first fails or returns vacuous): ask for a monotone scalar sandwich version that gives the leading-order hitting time without a full Laurent series

**Go/no-go gate:** if neither closes after honest review, accept the weaker form (ordering claim becomes asymptotic-rate rather than hitting-time-Laurent) and proceed. If either closes, the rest is mechanical.

### Phase 2 — Paper-1 Lean refactor (3–5 sessions)

Re-derive `diagAmp_ODE` (quantitatively), `bernoulli_laurent_bound`, `actual_critical_time`, and the ordering headline under Saxe form. Each lemma either:
- Closed via Aristotle job carrying the Phase 1 result
- Closed via template-transfer hand-port (the proof structure is identical, only the exponents change)
- Tagged as a Lean sorry that calls into the Phase 1 closed-form lemma

The 3 paper-1 named axioms in `CriticalTime.lean` (paper-2's `bernoulli_exact_solution_exists`, `bernoulli_gronwall_sandwich`, `bernoulli_exact_laurent`) get replaced by Saxe-form analogues, in place. `purified_laurent_bound` (paper-2-specific) gets the same treatment.

### Phase 3 — Paper-2 Lean cleanup (1–2 sessions)

Delete `Corrected.lean`. Move its three theorems into their natural homes:
- `rho_hat_plateau_rate_corrected` → `PlateauEstimator.rho_hat_plateau_rate` (the existing inverted-form version gets deleted)
- `sigma_positive_branch_converges_corrected` → `SignedODE.sigma_positive_branch_converges`
- `signed_recovery_pos_magnitude_plateau_corrected` → `SignedRecovery.signed_recovery_pos_magnitude_plateau`

Delete the 4 inverted-form axioms from paper-2's `CriticalTime.lean` (they were dead weight even under the deprecation framing).

Reconcile naming: decide whether paper-2 Lake-depends on paper-1 (cleaner DAG, paper-2 imports `JepaLearningOrder.JEPA.Bernoulli`) or re-derives the Bernoulli machinery locally (independence, but duplication).

### Phase 4 — Paper-1 prose rewrite (2–3 sessions)

Rewrite paper-1's §6 (hitting-time analysis) under Saxe form. State Theorem 6.1's hitting-time Laurent in the new form (or as a rate bound if Phase 1 fell back to weaker). Update §5 (diagonal ODE) to match. §§1–4 mostly survive — they cover the gradient-flow setup, balanced init, eigenbasis structure, all ODE-form-independent.

### Phase 5 — Paper-2 prose rewrite (1–2 sessions)

Rewrite paper-2 §1.1 abstract, §10 experiments, Remark 1.2 → removed, Experiment 1 → reframed as Saxe-form simulation validation only, Remark 3.2 → removed, App. A → axiom inventory has only Tropp 2015 left. Body sections (§§2–9) survive with minor edits.

---

## 5. Risks and contingencies

**R1 — Saxe-form Laurent doesn't close in finite Aristotle attempts.**
*Mitigation:* fall back to monotone scalar sandwich + asymptotic rate. Paper-1's headline becomes "trajectories cross thresholds in $\rho^*$ order at rate $\eps^{-1/L}$" rather than the Laurent-precise version. Still publishable.

**R2 — Saxe-form critical-time threshold is harder to define cleanly.**
*Mitigation:* near-plateau threshold `(1-δ)·ρ^{1/L}` with `δ`-dependent rate. Less clean but works.

**R3 — Off-diagonal Grönwall machinery doesn't transfer cleanly to Saxe form.**
*Mitigation:* unlikely — the off-diagonal control is on coupling coefficients, not the diagonal dynamics. Audit-Phase-0 confirms.

**R4 — Paper-2 Lake-dep on paper-1 creates circular history.**
*Mitigation:* if paper-1 hasn't shipped to arXiv yet, paper-2 referencing its Lean is fine (private repo). If it has, paper-2 cites the paper, depends on the Lean. Decision deferred to Phase 3.

**R5 — Scope creep into nonlinear JEPA.**
*Mitigation:* the nonlinear extension is paper-3+. This reimagine is purely about getting the linear case right. Explicitly out of scope for this plan.

---

## 6. Autonomous execution protocol

After Phase 0 (math audit) completes, the remaining work is largely mechanical execution against the audit findings. The plan can run with limited check-ins:

**Per-phase decision points:**
- End of Phase 0: human approval to proceed (go/no-go gate)
- End of Phase 1: human approval to proceed (math-risk resolved)
- After Phase 2: human spot-check on the corrected Lean
- After Phase 5: human approval before pushing or rebuilding the arXiv submission

**Between decision points, the autonomous loop runs:**
- Each session: pick the next concrete task from the phase's checklist
- Dispatch Aristotle jobs as identified
- Update `wiki/session-log.md` at end of each session
- Update `wiki/INDEX.md` with phase progress
- Flag any unexpected math obstacle as a new risk in this doc and pause for human input

**This document is the source of truth.** If the plan changes, edit this doc first, then act. If session-log diverges from this plan, the plan wins until explicitly amended.

---

## 7. First action

Phase 0: math-graph audit on `jepa-learning-order`. Will produce `audits/jepa-learning-order/REPORT-saxe-reimagine-2026-05.md` answering:

1. For each theorem in paper-1, is it ODE-form-dependent or independent?
2. For each ODE-form-dependent theorem, can it be re-derived by template transfer (same proof structure, new exponents) or does it need genuinely new math?
3. What is the minimum set of new lemmas we need Aristotle to close?
4. Is the Saxe-form hitting-time Laurent reachable, plausible, or hard?

The audit's output gates the rest of the plan.

---

## 8. Open questions to revisit

- **Single paper or two?** With paper-1 corrected, the case for merging is stronger (no defensive remarks needed). The case against (paper-1 has time-stamped novelty for the simultaneous-diagonalisability removal; paper-2 carries the algorithm + empirics) still mostly holds. Revisit after Phase 4.
- **Nonlinear extension framing.** The LeWM/Maes 2026 architecture is the obvious target. Does it admit a Saxe-style linearisation around some operating point that lets us apply this paper-2's machinery? Out of scope here; revisit as paper-3 planning.
- **Real-data demonstration.** Mentioned as follow-on in paper-2 §11. Worth scoping during Phase 5: is there a public dataset where we can run `PlateauRecover` against a JEPA training run and report recovered $\hat\rho$ against a downstream-task ordering?
