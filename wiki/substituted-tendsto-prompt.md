---
name: substituted-tendsto-prompt
description: Full LLM prompt to close substituted_tendsto / fillingProb_tendsto_one — includes all Lean definitions, mathematical analysis showing the DCT route is likely wrong, and three alternative proof strategies
type: project
---

# LLM Prompt: Close `substituted_tendsto` / `fillingProb_tendsto_one`

**Key finding:** `substituted_tendsto` as stated is likely **false**. For t > p, x_f = 1-(t/p)^{2/d} < 0, so volumeFill = 0 and the ratio is identically 0 — not → 1. The set {t ∈ (0,1) : t > p} has measure 1-p > 0, so the ∀ᵐ t claim fails. The DCT route via Euclidean volume-intersection integrals is the wrong path. Task A (prove `fillingProb_tendsto_one` directly from `fill_eventually_always'`) is the right strategy.

**To use:** submit as Aristotle job targeting `fillingProb_tendsto_one` with this as the PROVIDED SOLUTION block.

---

## Prompt text

You are working on a Lean 4 formalization of a mathematical paper about detecting
simplicial geometry. The primary remaining open item is the lemma `substituted_tendsto`.
This document gives full context.

---

### 1. Project setup

Lean toolchain: leanprover/lean4:v4.28.0, Mathlib v4.28.0.
Main file: SimplicialLatentGeometry/SimplicialDetection.lean (~3900 lines).

---

### 2. Key definitions (exact Lean)

```lean
noncomputable def euclidBallVol (d : ℕ) (r : ℝ) : ℝ :=
  Real.pi ^ ((d : ℝ) / 2) / Real.Gamma ((d : ℝ) / 2 + 1) * r ^ d

noncomputable def matchRadius (p : ℝ) (d : ℕ) : ℝ :=
  if d = 0 then 0 else p ^ ((1 : ℝ) / (d : ℝ)) / 2

-- Intersection volume of two (2r)-balls at centre-separation s.
-- Parameters: a = (d+1)/2, b = 1/2, x = 1-(s/(4r))²
noncomputable def volumeEmpty (d : ℕ) (r s : ℝ) : ℝ :=
  let x := 1 - (s / (2 * (2 * r))) ^ 2
  let a := ((d : ℝ) + 1) / 2
  let b := (1 : ℝ) / 2
  let incBeta := ∫ t in Set.Ioo 0 x, t ^ (a - 1) * (1 - t) ^ (b - 1)
  let betaFn := Real.Gamma a * Real.Gamma b / Real.Gamma (a + b)
  euclidBallVol d (2 * r) * incBeta / betaFn

-- Intersection volume of two r-balls at centre-separation s.
-- Parameters: a = (d+1)/2, b = 1/2, x = 1-(s/(2r))²
noncomputable def volumeFill (d : ℕ) (r s : ℝ) : ℝ :=
  let x := 1 - (s / (2 * r)) ^ 2
  let a := ((d : ℝ) + 1) / 2
  let b := (1 : ℝ) / 2
  let incBeta := ∫ t in Set.Ioo 0 x, t ^ (a - 1) * (1 - t) ^ (b - 1)
  let betaFn := Real.Gamma a * Real.Gamma b / Real.Gamma (a + b)
  euclidBallVol d r * incBeta / betaFn

noncomputable def fillingProb (p : ℝ) (d : ℕ) : ℝ :=
  let r := matchRadius p d
  ∫ s in Set.Ioo 0 1,
    volumeFill d r s / volumeEmpty d r s * (d : ℝ) * s ^ (d - 1)
```

---

### 3. The sorry

```lean
private lemma substituted_tendsto (p : ℝ) (hp0 : 0 < p) (hp1 : p < 1) :
    ∀ᵐ t ∂(MeasureTheory.volume.restrict (Set.Ioo (0:ℝ) 1)),
    Filter.Tendsto (fun d : ℕ =>
      volumeFill d (matchRadius p d) (t ^ ((1:ℝ)/(d:ℝ))) /
      volumeEmpty d (matchRadius p d) (t ^ ((1:ℝ)/(d:ℝ)))) Filter.atTop (nhds 1) := by
  sorry
```

**Role in the proof:** `substituted_tendsto` is the pointwise convergence hypothesis in a
dominated convergence argument inside `fillingProb_tendsto_one`:

```lean
lemma fillingProb_tendsto_one (p : ℝ) (hp0 : 0 < p) (hp1 : p < 1) :
    Filter.Tendsto (fun d : ℕ => fillingProb p d) Filter.atTop (nhds 1) := by
  have h_dominated : Filter.Tendsto (fun d => ∫ t in Set.Ioo (0:ℝ) 1,
      volumeFill d (matchRadius p d) (t ^ ((1:ℝ)/(d:ℝ))) /
      volumeEmpty d (matchRadius p d) (t ^ ((1:ℝ)/(d:ℝ)))) Filter.atTop (nhds (∫ _ in Set.Ioo (0:ℝ) 1, 1)) := by
    apply_rules [ MeasureTheory.tendsto_integral_filter_of_dominated_convergence ];
    any_goals exact fun _ => 2;
    · exact Filter.Eventually.of_forall fun n => substituted_aesm p n;
    · exact substituted_bound p hp0 hp1;   -- ‖ratio‖ ≤ 2 uniformly (proved)
    · norm_num +zetaDelta at *;
    · exact substituted_tendsto p hp0 hp1; -- ← THIS IS THE SORRY
  ...
```

`fillingProb_tendsto_one` is needed by `geometricCov_tendsto_zero` (proved),
which is needed by `phase_transition` (the main theorem).

---

### 4. What is already proved

The following are proved (0 sorries) and available:

```lean
lemma matchRadius_tendsto_half (p : ℝ) (hp0 : 0 < p) (hp1 : p < 1) :
    Filter.Tendsto (fun d : ℕ => matchRadius p d) Filter.atTop (nhds (1/2))

lemma matchRadius_spec (p : ℝ) (hp0 : 0 < p) (hp1 : p < 1) (d : ℕ) (hd : 1 ≤ d) :
    (2 * matchRadius p d) ^ d = p

lemma volumeFill_div_volumeEmpty_le_one (d : ℕ) (r s : ℝ)
    (hr : 0 < r) (hs : 0 < s) (hs1 : s < 1) :
    volumeFill d r s / volumeEmpty d r s ≤ 1

private lemma substituted_bound (p : ℝ) (hp0 : 0 < p) (hp1 : p < 1) :
    ∀ᶠ d : ℕ in Filter.atTop, ∀ᵐ t ∂(MeasureTheory.volume.restrict (Set.Ioo (0:ℝ) 1)),
    ‖volumeFill d (matchRadius p d) (t ^ ((1:ℝ)/(d:ℝ))) /
      volumeEmpty d (matchRadius p d) (t ^ ((1:ℝ)/(d:ℝ)))‖ ≤ 2

-- Geometric lemmas (Aristotle, April 2026):
private lemma addCircle_three_balls_intersect' (r : ℝ) (hr : r > 1/3)
    (a₁ a₂ a₃ : AddCircle (1 : ℝ)) :
    ∃ z : AddCircle (1 : ℝ), dist a₁ z ≤ r ∧ dist a₂ z ≤ r ∧ dist a₃ z ≤ r

private lemma matchRadius_eventually_gt_third' (p : ℝ) (hp0 : 0 < p) (hp1 : p < 1) :
    ∀ᶠ d in Filter.atTop, matchRadius p d > 1/3

private lemma fill_eventually_always' (p : ℝ) (hp0 : 0 < p) (hp1 : p < 1) :
    ∀ᶠ d in Filter.atTop, ∀ pts : Fin 3 → Torus d,
      ∃ z : Torus d, dist (pts 0) z ≤ matchRadius p d ∧
                      dist (pts 1) z ≤ matchRadius p d ∧
                      dist (pts 2) z ≤ matchRadius p d
```

---

### 5. Mathematical analysis

**Setting:** For fixed p ∈ (0,1) and t ∈ (0,1), the claim is that as d → ∞:

```
volumeFill d (p^{1/d}/2) (t^{1/d}) / volumeEmpty d (p^{1/d}/2) (t^{1/d}) → 1
```

Write r_d = p^{1/d}/2 → 1/2 and s_d = t^{1/d} → 1. Then:

  - x_f = 1 - (s_d / (2·r_d))² = 1 - (t/p)^{2/d} → 0 as d → ∞ (for t ≠ p)
  - x_e = 1 - (s_d / (4·r_d))² = 1 - (t/p)^{2/d}/4 → 3/4 as d → ∞

**Key concern:** Since x_f → 0, the numerator integral I_f = ∫₀^{x_f} τ^{a-1}(1-τ)^{-1/2} dτ
shrinks as the upper limit → 0, while I_e → I_{3/4}(a,1/2) stays bounded away from 0.
Combined with the factor (euclidBallVol d r / euclidBallVol d (2r)) = (1/2)^d,
the ratio appears to tend to 0, not 1, for fixed t < p.

For t > p: (t/p)^{2/d} > 1 so x_f < 0 and I_f = 0, making the ratio exactly 0.

**This suggests `substituted_tendsto` may be false as stated.** The `volumeFill`/`volumeEmpty`
definitions use Euclidean ball intersection formulas, but the torus is equipped with the
sup-norm metric. The geometric incompleteness means the Euclidean volume integrals do not
correctly model the torus fill probability, so the DCT route via these integrals is the wrong
approach.

---

### 6. Alternative strategy: prove `fillingProb_tendsto_one` directly

The geometric fact `fill_eventually_always'` establishes that for large enough d, every triple
of points on the torus has intersecting balls. **If** the integral formula for `fillingProb`
correctly captures the conditional fill probability, this implies `fillingProb p d = 1`
eventually, and thus `fillingProb_tendsto_one` follows without using `substituted_tendsto`.

---

### 7. Your task

Please attempt ONE of the following, in order of preference:

**Task A (preferred):** Prove `fillingProb_tendsto_one` directly using `fill_eventually_always'`,
bypassing `substituted_tendsto`. Show that eventually `fillingProb p d = 1` (because fill
is universal), so the sequence is eventually the constant 1, hence converges to 1.

```lean
lemma fillingProb_tendsto_one (p : ℝ) (hp0 : 0 < p) (hp1 : p < 1) :
    Filter.Tendsto (fun d : ℕ => fillingProb p d) Filter.atTop (nhds 1) := by
  -- Strategy: show fillingProb p d = 1 for all sufficiently large d,
  -- then conclude the limit is 1.
  -- For d large (matchRadius > 1/3), fill_eventually_always' gives that every
  -- triple of points fills, so the conditional fill probability = 1.
  sorry
```

The challenge: connecting `fill_eventually_always'` (a geometric statement about point
configurations on Torus d) with the integral formula
`fillingProb p d = ∫₀¹ [volumeFill d r s / volumeEmpty d r s] · d · s^{d-1} ds`.
This requires showing that when fill is universal (every triple of points fills), the
integral formula gives 1 — i.e., volumeFill d r s = volumeEmpty d r s for all s in the
support of d·s^{d-1} on (0,1), when r = matchRadius p d > 1/3.

For the sup-norm torus: when r > 1/3, the ball of radius r centered at any point covers more
than 1/3 of each coordinate circle, so three such balls always have common intersection.
In that case the fill constraint is vacuous and volumeFill = volumeEmpty, giving ratio = 1.

**Task B (fallback):** If Task A is not feasible, provide a complete Lean 4 proof of
`substituted_tendsto` by establishing the asymptotic claim directly. Key tools:
- Asymptotics of the regularized incomplete beta function I_x(a, 1/2) as a → ∞ and x → 0
  simultaneously with x·a → log(p/t) = const
- Stirling-type identity B(a, 1/2) ~ √(π/a) for large a
- MeasureTheory.tendsto_integral_filter_of_dominated_convergence (already set up)

**Task C (last resort):** Prove a weaker result sufficient for `fillingProb_tendsto_one`:
show that for any ε > 0, fillingProb p d > 1 - ε for all sufficiently large d.

The target lemma that must be closed is:

```lean
lemma fillingProb_tendsto_one (p : ℝ) (hp0 : 0 < p) (hp1 : p < 1) :
    Filter.Tendsto (fun d : ℕ => fillingProb p d) Filter.atTop (nhds 1)
```

All other proved lemmas in the file are available. Do not introduce new axioms.
