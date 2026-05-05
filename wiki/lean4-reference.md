# Lean 4 Reference

Consolidated knowledge for writing, debugging, and formalizing Lean 4 proofs with Mathlib. Merges content from `Lean 4 Mathlib Patterns.md`, `Lean 4 Proofs.md`, and the pitfalls/API sections of the workspace CLAUDE.md.

**Environment:** Lean `v4.28.0` / Mathlib `v4.28.0` (commit `8f9d9cff6bd728b17a24e163c9402775d9e6a365`)

---

## Core Workflow

1. **Scratchpad first** — for complex proofs, create a minimal `test.lean` to check exact goal contexts, auto-named variables, and lemma signatures before editing the real file.
2. **Check signatures** — `#check @lemma_name` shows the full type with implicit arguments.
3. **Build incrementally** — `lake build Module.Name` after each meaningful change.
4. **Isolate errors** — if a file has multiple errors, `sorry` out later lemmas to fix the first one first.
5. **Avoid double builds** — use `tee` so output is captured once and can be re-examined without re-running. Standard pattern:
   ```bash
   lake build SimplicialLatentGeometry.SimplicialDetection 2>&1 \
     | tee /tmp/lean_build.log \
     | grep -E "^error:|Build completed"
   # Re-examine without rebuilding:
   tail -20 /tmp/lean_build.log
   grep -E "^error:" /tmp/lean_build.log
   ```
6. **Fast module check** — when editing only `TorusIntegrals.lean`, build that module first (~60 s) before the full 5-min `SimplicialDetection` build:
   ```bash
   lake build SimplicialLatentGeometry.TorusIntegrals
   ```
   Only run the full `SimplicialDetection` build before committing.

---

## Type Conventions

| Mathematical object | Lean type |
|---|---|
| d×d real matrix | `Matrix (Fin d) (Fin d) ℝ` |
| Positive definite matrix | `Matrix.PosDef M` |
| Matrix inverse | `M⁻¹` (via `Matrix.nonsing_inv`) |
| Matrix trace | `Matrix.trace M` |
| Matrix transpose | `Mᵀ` (requires `open scoped Matrix`) |
| Matrix-vector product | `M.mulVec v` |
| Dot product | `dotProduct u v` (top-level — NOT `Matrix.dotProduct`) |
| Real square root | `Real.sqrt x` |
| Real power (non-integer exponent) | `Real.rpow x r` |
| Norm | `‖M‖` (operator norm via `NNNorm`) |
| Inner product | `inner u v` (from `InnerProductSpace`) |
| Finite sum | `∑ i : Fin n, f i` |
| ODE derivative | `deriv f t` (for `f : ℝ → X`) |
| Set interval | `Set.Icc a b`, `Set.Ioo a b` |

---

## Termination for Recursive Functions on Nested Inductives

Lean's default termination checker fails on nested inductives (e.g. a tree with a `List` of children) because it can't automatically see that a list element is structurally smaller than the parent.

**Pattern: explicit membership**

```lean
-- BAD: implicit membership — termination tactic can't access the proof
def hasProperty : Tree → Prop
  | orNode cs => ∃ c ∈ cs, hasProperty c

-- GOOD: explicit membership
def hasProperty : Tree → Prop
  | orNode cs => ∃ (c : Tree) (hc : c ∈ cs), hasProperty c
termination_by t => sizeOf t
decreasing_by
  simp_wf
  rename_i hc
  have h := List.sizeOf_lt_of_mem hc
  omega
```

**Pattern: index-based recursion**

```lean
def successProb : Tree → ℕ → NNReal
  | orNode cs, nid =>
      ∑ i : Fin cs.length, successProb (cs.get i) (nid + 1)
termination_by t => sizeOf t
decreasing_by
  all_goals simp_wf
  all_goals (have h := List.sizeOf_lt_of_mem (by assumption); omega)
```

Use `List.getElem_mem` to produce the membership proof when needed:
```lean
have h := List.sizeOf_lt_of_mem (List.getElem_mem (by assumption))
```

---

## Common NNReal Lemmas

`NNReal` subtraction and division are truncated at 0 — different from `Real`.

| Goal | Lemma |
|---|---|
| `a - b ≤ a` (e.g. `1 - ε ≤ 1`) | `tsub_le_self` |
| `0 < a - b` from `b < a` | `tsub_pos_of_lt` |
| `a - b < a` | `tsub_lt_self one_pos hε` |
| `b⁻¹ ≤ a⁻¹` from `a ≤ b` | `inv_anti₀ hpos hle` |
| `(a⁻¹)^n = (a^n)⁻¹` | `inv_pow` |
| `1 < a/b` iff `b < a` | `one_lt_div₀ hb_pos` |
| `a^n ≤ a^m` when `a ≤ 1, m ≤ n` | `pow_le_pow_of_le_one` |
| `a * b ≤ a * c` from `b ≤ c, 0 ≤ a` | `mul_le_mul_of_nonneg_left` — use `zero_le_one` for `0 ≤ 1`, NOT `le_rfl` |
| `r^n → ∞` when `1 < r` | `tendsto_pow_atTop_atTop_of_one_lt` |
| `g → ∞` from `f ≤ g` and `f → ∞` | `Filter.tendsto_atTop_mono` (fully qualified — `Filter.Tendsto.atTop_mono` does not exist) |

**`Filter.tendsto_atTop_mono` gotcha:** avoid `apply Filter.tendsto_atTop_mono _ htend` — it leaves a goal that immediately errors. Use:
```lean
exact Filter.tendsto_atTop_mono (fun n => ...) htend
```

---

## Eventually-True Bounds (`∀ᶠ`)

When a bound only holds for large `k` (e.g. once some `g_k > 0`), state it as `∀ᶠ k in Filter.atTop` rather than `∀ k`. This avoids an edge-case sorry for small `k`:

```lean
-- BAD: need to handle k < N separately, which Aristotle can't close
have h : ∀ k, bound k := ...

-- GOOD: eventually-true, closeable with filter_upwards
have h : ∀ᶠ k in Filter.atTop, bound k := by
  filter_upwards [hg_pos] with k hg_k
  exact bound_lemma ... hg_k
```

---

## Verified Mathlib API Patterns (v4.28.0)

```lean
-- Open scoped notations:
open scoped Matrix          -- enables Mᵀ for Matrix.transpose

-- FTC (interval integral, upper limit):
intervalIntegral.integral_hasDerivAt_right
  (hf : IntervalIntegrable f volume a b)
  (hmeas : StronglyMeasurableAtFilter f (nhds b) volume)
  (hb : ContinuousAt f b) : HasDerivAt (fun u => ∫ x in a..u, f x) (f b) b

-- StronglyMeasurableAtFilter from ContinuousOn:
ContinuousOn.stronglyMeasurableAtFilter (hs : IsOpen s) (hf : ContinuousOn f s) :
  ∀ x ∈ s, StronglyMeasurableAtFilter f (nhds x) volume
-- Usage:
ContinuousOn.stronglyMeasurableAtFilter isOpen_Ioo (hf.mono Set.Ioo_subset_Icc_self) s hs

-- Continuity of integral primitive:
intervalIntegral.continuousOn_primitive_interval' (h_int : IntervalIntegrable f μ b₁ b₂)
  (ha : a ∈ [[b₁, b₂]]) : ContinuousOn (fun b => ∫ x in a..b, f x) [[b₁, b₂]]

-- Antitone from nonpositive derivative:
antitoneOn_of_deriv_nonpos (hD : Convex ℝ D) (hf : ContinuousOn f D)
  (hf' : DifferentiableOn ℝ f (interior D))
  (hf'_nonpos : ∀ x ∈ interior D, deriv f x ≤ 0) : AntitoneOn f D

-- HasDerivAt for exp composition:
hB_da.neg.exp : HasDerivAt (fun x => Real.exp (-B x)) (Real.exp (-B s) * (-β s)) s
-- (.exp is Real exp, not Complex)

-- ContinuousOn.exp for real functions — use .rexp, not .exp:
hB_cont.neg.rexp : ContinuousOn (fun x => Real.exp (-B x)) S

-- Division/exp identities:
Real.exp_neg : Real.exp (-x) = (Real.exp x)⁻¹
div_inv_eq_mul : a / b⁻¹ = a * b
le_div_iff₀ (hc : 0 < c) : a ≤ b / c ↔ a * c ≤ b
div_le_div_of_nonneg_right (hab : a ≤ b) (hc : 0 ≤ c) : a / c ≤ b / c

-- Interval integral of 1 (top-level namespace, not intervalIntegral):
integral_one : ∫ _ in a..b, (1 : ℝ) = b - a
-- Connect Ioo set integrals via:
-- MeasureTheory.integral_Ioc_eq_integral_Ioo → intervalIntegral.integral_of_le
```

---

## Common Pitfalls (confirmed v4.28.0)

**ℕ truncation in exponents** — never write `2 * (L - k) / L` where `L k : ℕ`. Integer division truncates. Cast to `ℝ` first:
```lean
-- WRONG (e.g. L=3, k=0 → 4/3 truncates to 1):
sigma ^ (2 * (L - k) / L)
-- RIGHT:
Real.rpow sigma (2 * ((L : ℝ) - (k : ℝ)) / (L : ℝ))
```

**`Matrix.mulVec_mulVec` argument order** — first explicit arg is `v` (the vector), not `M`. Use bare rewrite:
```lean
-- WRONG (passes matrix as v):
rw [← Matrix.mulVec_mulVec Wbar]
-- RIGHT:
rw [← Matrix.mulVec_mulVec]
```

**Renamed lemmas in v4.28.0:**
- `pow_le_pow_left` → `pow_le_pow_left₀`
- `div_lt_div_iff` → `div_lt_div_iff₀`

**`λ` (U+03BB) in identifiers** — `λ` is a Lean 4 keyword. Identifiers like `hλr` cause parse errors. Use `hLr`, `hlam`, etc.

**`let` bindings in return types** — a `let x := expr` in a lemma's return type creates a local def visible in the goal but `x` is NOT in scope during `exact`. Inline the full expression:
```lean
-- WRONG: "Unknown identifier 't_crit_leading'"
exact ⟨0, t_crit_leading, by simp, by simp⟩
-- RIGHT:
exact ⟨0, (L : ℝ) / (projectedCovariance dat eb r * ...), by simp, by simp⟩
```

**`set_option maxHeartbeats N in` placement** — must appear before the docstring, not between the docstring and the declaration.

**Doc comments near `-/`** — avoid backticks or operators (e.g. `<`, `≤`) immediately before the closing `-/`. Lean's parser can misread them as code:
```lean
-- RISKY: `lemma_name` -/  or  a ≤ b -/
-- SAFE: simplify the comment, or switch to -- line comments
```

**`apply ... ?_` leaving "No goals to be solved"** — use `exact` with a lambda instead:
```lean
-- WRONG: apply Filter.tendsto_atTop_mono _ htend
-- RIGHT: exact Filter.tendsto_atTop_mono (fun n => ...) htend
```

**Adding hypotheses after Aristotle** — if Aristotle's proof requires a positivity condition (e.g. `hg : 0 < g`) not in the original signature, add it and update all call sites. Derive at call sites from stronger hypotheses (`n^{3/2} * g → ∞` implies eventually `g > 0` via `pos_of_mul_pos_left`).

**`"Imports are out of date"` in VS Code** — LSP cache stale after adding an import. Not a code error. Fix: `lake build` or "Restart File" in editor.

**`corollary` keyword** — does not exist in Lean 4. Use `theorem`.

**Doc comment + `open ... in` incompatibility** — a `/-- doc -/` doc comment must be immediately followed by a declaration keyword (`lemma`, `theorem`, `def`, `instance`). Placing `open Foo in` between a doc comment and the declaration causes a parse error: `unexpected token 'open'; expected 'lemma'`. Two fixes:
- **(a) Change `/--` to `/-`** (block comment, not doc comment) — simpler:
  ```lean
  /- description -/
  open Foo in
  lemma bar ...
  ```
- **(b) Place `open ... in` before the doc comment** — keeps doc comment on the declaration:
  ```lean
  open Foo in
  /-- doc -/
  lemma bar ...
  ```

---

## Environment

**Toolchain:** `leanprover/lean4:v4.28.0`
**Mathlib:** `v4.28.0` / commit `8f9d9cff6bd728b17a24e163c9402775d9e6a365`

All projects in this workspace are pinned to match Aristotle's fixed environment — proofs returned by Aristotle compile locally without porting.

**Standard Lean options (used across all projects):**
```lean
set_option pp.unicode.fun true          -- pretty-prints lambdas as fun a ↦ b
set_option relaxedAutoImplicit false    -- all variables must be explicitly declared
set_option weak.linter.mathlibStandardSet true  -- Mathlib standard linter active
set_option maxSynthPendingDepth 3
```

If a proof returned by Aristotle fails to compile locally, the issue is a hallucinated lemma name or syntax error in Aristotle's output — not a version mismatch.
