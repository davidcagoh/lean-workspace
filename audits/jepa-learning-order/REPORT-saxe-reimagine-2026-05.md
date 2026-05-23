# Phase 0 audit — Saxe reimagine of jepa-learning-order

> **Session:** 99, 2026-05-23.
> **Scope:** map ODE-form dependencies in paper-1's Lean tree; identify what
> needs new math vs. template transfer vs. is already done.
> **Strategy doc:** `wiki/reimagine-2026-05.md` (this is Phase 0's output).

---

## Headline

**The Saxe-form math is already in the tree.** `JepaLearningOrder/Corrected.lean`
(881 LOC, session 90 + later iterations) contains Saxe-form analogues of every
inverted-form lemma in the critical chain, sorry-free, with one named axiom
(`saxe_exact_solution_exists` — Picard-Lindelöf for the Saxe ODE, the natural
analogue of the inverted-form `bernoulli_exact_solution_exists`).

The "Phase 1 math closure" risk that the strategy doc concentrated on is
**not a risk** — the closure exists. The Saxe-form Bernoulli asymptotic was
derived as `saxe_singlepole_asymptotic` (note: single-pole, not 2L-1 Laurent
terms — Saxe form has a different asymptotic structure, which matters).

The reimagine is therefore *structural cleanup + prose rewrite*, not a
research project.

---

## What's in paper-1's tree

### Inverted-form (deprecated)
- `JEPA/DiagAmpODE.lean`
  - `diagAmp_ODE` `@[deprecated]` — vacuous proof via `IsCompact`
  - `bernoulli_laurent_bound` `@[deprecated]` — inverted-form Laurent
  - `actual_critical_time` `@[deprecated]` — uses inverted form
- `JEPA/Bernoulli.lean`
  - `critical_time_formula`, `critical_time_ordering`, `bernoulli_partial_fractions`, `jepa_bernoulli_solution`, `jepa_critical_time_diag` — all under inverted form
  - `jepa_bernoulli_solution_WRONG` — explicitly marked wrong (kept for record)
- `MainTheorem.lean`
  - `JEPA_rho_ordering'`, `JEPA_dynamics_ordering`, `laurent_separation_dominates` — all built on the inverted critical-time chain
- `LaurentHelpers.lean`
  - `projCov_mul_rho_strict_lt`, `projCov_mul_rho_pow_le`, `rpow_two_L_minus_two_split` etc. — Laurent-specific arithmetic helpers

### Saxe-form (live, sorry-free)
- `Corrected.lean`
  - `preconditioner_self`, `gradient_dot_eq` — Saxe preconditioner identities
  - `diagAmp_ODE_corrected` — Saxe ODE with quantitatively-constraining residual
  - `axiom saxe_exact_solution_exists` — Saxe Picard-Lindelöf existence
  - `saxe_gronwall_sandwich`, `saxe_gronwall_comparison` — Saxe-form ODE comparison
  - `saxe_singlepole_asymptotic` — **single-pole** asymptotic (not 2L-1 Laurent terms)
  - `bernoulli_saxe_bound_corrected` — Saxe-form hitting-time bound
  - `actual_critical_time_corrected` — JEPA-side wrapper
  - `JEPA_dynamics_ordering_corrected` — Saxe-form ordering headline

### ODE-form-independent (survive untouched)
- `JEPA/Core.lean` — JEPA data, eigenbasis, gradient definitions
- `JEPA/QuasiStatic.lean` — quasi-static decoder (`quasiStatic_approx` is the
  lemma with vacuous compactness discharge; statement is form-independent, but
  proof needs upgrading separately — see Finding 2 below)
- `JEPA/EncoderHelpers.lean` — Frobenius helpers, contraction infrastructure
- `JEPA/OffDiagFinal.lean` — off-diagonal coupling control
  - `offDiag_ODE`, `offDiag_bound`, `JEPA_rho_ordering` — controls $c_{rs}(t)$
    via depth-$L$ Grönwall; ODE-form-independent
- `BootstrapLemmas.lean` — auxiliary continuity + bootstrap consistency
- `Lemmas.lean` — Grönwall theory, contractive bounds
- `OffDiagHelpers.lean`, `PDLowerHelpers.lean` — purely arithmetic
- `SaxeAsymptoticHelpers.lean` — already Saxe-named, hitting-time machinery

---

## Per-theorem dependency tag

| Theorem | File | Saxe-dependent? | Status |
|---|---|---|---|
| `gradient_projection` | `QuasiStatic` | no | unchanged |
| `quasiStatic_approx` | `QuasiStatic` | partially (statement) | proof is vacuous; not Saxe-specific, but needs upgrading |
| `diagAmp_ODE` | `DiagAmpODE` | yes | deprecated; replaced by `Corrected.diagAmp_ODE_corrected` |
| `bernoulli_laurent_bound` | `DiagAmpODE` | yes | deprecated; replaced by `Corrected.bernoulli_saxe_bound_corrected` |
| `actual_critical_time` | `DiagAmpODE` | yes | deprecated; replaced by `Corrected.actual_critical_time_corrected` |
| `critical_time_formula` | `Bernoulli` | yes | needs Saxe analogue (or removal — only relevant for the Littwin closed form) |
| `critical_time_ordering` | `Bernoulli` | yes | needs Saxe analogue |
| `bernoulli_partial_fractions` | `Bernoulli` | yes (inverted-form specific) | can be removed — the partial-fractions trick is inverted-form-only |
| `jepa_bernoulli_solution` | `Bernoulli` | yes | needs Saxe analogue (Saxe has explicit single-pole closed form) |
| `jepa_critical_time_diag` | `Bernoulli` | yes | needs Saxe analogue |
| `jepa_bernoulli_solution_WRONG` | `Bernoulli` | — | already marked wrong; delete |
| `offDiag_ODE` | `OffDiagFinal` | no | unchanged |
| `offDiag_bound` | `OffDiagFinal` | no | unchanged |
| `JEPA_rho_ordering` | `OffDiagFinal` | no | unchanged (off-diagonal-only) |
| `JEPA_rho_ordering'` | `MainTheorem` | yes (composes Saxe and off-diag) | re-wire to use `Corrected.JEPA_dynamics_ordering_corrected` |
| `JEPA_dynamics_ordering` | `MainTheorem` | yes | replaced by `Corrected.JEPA_dynamics_ordering_corrected` |
| `laurent_separation_dominates` | `MainTheorem` | yes (inverted Laurent) | replaced; Saxe has single-pole, not Laurent, so this is structurally different |
| Encoder helpers (all) | `EncoderHelpers` | no | unchanged |
| Bootstrap helpers (all) | `BootstrapLemmas` | no | unchanged |
| Lemmas (all) | `Lemmas`, `Gronwall*` | no | unchanged |

**Headcount.**
- ODE-form-independent: 8 lemmas + all of EncoderHelpers/BootstrapLemmas/Lemmas (~30 lemmas)
- Already replaced (Corrected.lean): 4 main theorems
- Needs explicit Saxe-form analogue (not just replacement): ~5 lemmas in `Bernoulli.lean`
- Should be deleted entirely: 1 (`jepa_bernoulli_solution_WRONG`)
- Should be deprecated then deleted in next pass: 5 (the inverted-form versions in DiagAmpODE/Bernoulli)

---

## Findings

### Finding 1 — Math closure is done, not pending

Strategy doc §3.1 listed the Saxe-form Bernoulli Laurent as the critical math
risk. It is not a risk: `Corrected.saxe_singlepole_asymptotic` (lines 582–688)
gives the closed-form asymptotic. The structure is **single-pole**, not 2L-1
Laurent terms — this is the right answer mathematically (the Saxe ODE has
a different equilibrium structure than the inverted form, so the asymptotic
expansion type is different too), and it's already in the tree.

Phase 1 of the strategy doc is **already complete**.

### Finding 2 — `quasiStatic_approx` has a separate vacuous-proof issue

`JEPA/QuasiStatic.lean::quasiStatic_approx` discharges via `IsCompact.exists_bound_of_continuousOn` (the same vacuous pattern as `diagAmp_ODE` had).
This is not ODE-form-dependent — the quasi-static decoder analysis is the same under either ODE form — but the **proof is non-quantitative** for the same reason. The strategy doc's Phase 2 should add `quasiStatic_approx` upgrade to the work list.

This upgrade is the natural one we discussed in paper-2 (§3 Theorem 3.1's
`C_qs` should depend only on the population covariances, not $\eps$). Doing
the upgrade in paper-1 directly is cleaner.

### Finding 3 — `JEPA_rho_ordering` (off-diagonal-only) survives untouched

The Phase 0 hypothesis ("off-diagonal Grönwall transfers cleanly") is
confirmed: `OffDiagFinal::JEPA_rho_ordering` controls $c_{rs}(t)$ uniformly
at $O(\eps^{1/L})$ via the depth-$L$ Grönwall argument, with no reference to
the diagonal ODE form. This is one of the genuinely ODE-form-independent
contributions of paper-1 and carries through verbatim.

### Finding 4 — Five `Bernoulli.lean` lemmas need Saxe analogues but are small

`critical_time_formula`, `critical_time_ordering`, `jepa_bernoulli_solution`,
`jepa_critical_time_diag` are each ~30–60 LOC and depend on the inverted-form
closed-form Bernoulli solution. Their Saxe analogues fall directly out of
`Corrected.saxe_singlepole_asymptotic`. Estimated effort: 1–2 sessions of
template-transfer hand-port; no Aristotle needed.

`bernoulli_partial_fractions` is genuinely inverted-form-specific (it's the
partial-fraction decomposition of `1/(ψ^{2L}(1-ψ))`). Its Saxe analogue is
not the same calculation — Saxe's asymptotic is single-pole, derivable
differently. So this lemma should be deleted, not transferred.

### Finding 5 — Paper-2's CriticalTime.lean axioms are now provably redundant

Paper-2's four `CriticalTime.lean` axioms (`bernoulli_exact_solution_exists`,
`bernoulli_gronwall_sandwich`, `bernoulli_exact_laurent`,
`purified_laurent_bound`) all describe the inverted-form Bernoulli ODE.
With paper-1's Corrected.lean machinery in place under Saxe form:
- The first three are obsoleted by paper-1's Saxe-form analogues
  (`Corrected.saxe_exact_solution_exists`, `saxe_gronwall_sandwich`,
  `saxe_singlepole_asymptotic`)
- The fourth (`purified_laurent_bound`) supports paper-2's "fast variant"
  critical-time estimator, which the reimagine removes from the paper

After the reimagine, paper-2's live axiom inventory drops from 5 to 1
(`matrix_bernstein_subgaussian` on the finite-sample chain), as the strategy
doc predicted.

### Finding 6 — Naming convention: drop `_corrected` suffix

Once the deprecated inverted-form lemmas are deleted, the `_corrected`
suffix is meaningless. Cleanup pass: rename
- `diagAmp_ODE_corrected` → `diagAmp_ODE`
- `bernoulli_saxe_bound_corrected` → `bernoulli_saxe_bound`
- `actual_critical_time_corrected` → `actual_critical_time`
- `JEPA_dynamics_ordering_corrected` → `JEPA_dynamics_ordering`

This requires deleting the deprecated versions first, then renaming. ~30 min
mechanical work.

---

## Revised plan (replaces strategy doc §4)

The strategy doc's 5-phase plan compresses substantially. The new plan:

### Phase 1′ (formerly Phases 0–1): Done

Phase 0 (this audit) + Phase 1 (math closure) both complete.

### Phase 2′ — Paper-1 Lean cleanup (1–2 sessions)

A. Delete `JEPA/Bernoulli.lean::jepa_bernoulli_solution_WRONG` and the
   inverted-form `bernoulli_partial_fractions`.
B. Delete the `@[deprecated]` inverted-form lemmas:
   `diagAmp_ODE`, `bernoulli_laurent_bound`, `actual_critical_time`.
C. Port the 4 still-needed `Bernoulli.lean` lemmas to Saxe form
   (`critical_time_formula`, `critical_time_ordering`,
   `jepa_bernoulli_solution`, `jepa_critical_time_diag`) — template transfer
   from `Corrected.saxe_singlepole_asymptotic`.
D. Move `Corrected.lean`'s contents into their natural homes:
   - `diagAmp_ODE_corrected`, `saxe_exact_solution_exists`,
     `saxe_gronwall_sandwich`, `saxe_gronwall_comparison`,
     `saxe_singlepole_asymptotic`, `bernoulli_saxe_bound_corrected`,
     `actual_critical_time_corrected` → `JEPA/DiagAmpODE.lean` (or split into
     `JEPA/Saxe.lean` if the file grows)
   - `JEPA_dynamics_ordering_corrected` → `MainTheorem.lean`
E. Rename `_corrected` suffix away across the tree.
F. Upgrade `quasiStatic_approx` to a quantitatively-constraining statement
   (paper-2 §3 Theorem 3.1's framing).
G. Delete `Corrected.lean` entirely.

Build target: 8044 → ~8030 (slight decrease as deprecated decls drop).

### Phase 3′ — Paper-2 Lean cleanup (1 session)

A. Delete paper-2's `Corrected.lean`. Move its three corrected theorems into
   their natural homes (`PlateauEstimator.lean`, `SignedODE.lean`,
   `SignedRecovery.lean`) replacing the inverted-form deprecated versions.
B. Delete the 4 inverted-form axioms from paper-2's `CriticalTime.lean`.
   Possibly delete `CriticalTime.lean` entirely if nothing else lives there.
C. Decide: Lake-depend on paper-1, or keep paper-2's Saxe machinery
   independent? (Original CLAUDE.md invariant says no Lake dep; revisit.)
D. Rename `_corrected` suffix away.
E. Update `Main.signed_decomposition` to cite the clean (no-suffix) targets.

### Phase 4′ — Paper-1 prose rewrite (2–3 sessions)

A. Rewrite paper-1 §6 (hitting-time analysis) under Saxe form, citing
   `saxe_singlepole_asymptotic` rather than the Laurent expansion.
B. Update the abstract: drop "Bernoulli-Laurent" language, replace with
   "single-pole asymptotic" or equivalent.
C. Update §5 (diagonal ODE) statement to Saxe form.
D. Other sections (§§1–4, §7) survive with minor edits.

### Phase 5′ — Paper-2 prose rewrite (1 session)

A. Drop Remark 1.2 (ODE-form correction apology).
B. Rewrite Experiment 1 (ODE-form preference) as "we ran a sanity check
   against simulation; the Saxe form predicts $\dot\sigma$ correctly across
   the spectrum" — without the paper-1-vs-Saxe pit.
C. Drop Remark 3.2 (vacuous quasi-static comparison) — paper-1 no longer has
   the issue.
D. App. A: axiom inventory has only `matrix_bernstein_subgaussian` left, no
   "deprecated" framing needed.
E. Update citation flow: paper-2 cites paper-1 as the ordering result and
   the simultaneous-diagonalisability removal, nothing about ODE-form.

---

## Estimated total effort

- Phase 1′: done
- Phase 2′: 1–2 sessions
- Phase 3′: 1 session
- Phase 4′: 2–3 sessions
- Phase 5′: 1 session

**Total: 5–7 sessions, no Aristotle work needed.**

Down from the strategy doc's 8–12 estimate, because the Phase 1 math closure
is already done.

---

## Go decision

**GO.** The audit found that the math-risk piece is already resolved; the
remaining work is structural and editorial, well within scope. Proceeding to
Phase 2′ in this session.
