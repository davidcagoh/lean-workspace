# Decisions

Design choices already locked in. Read before changing anything architectural.

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
