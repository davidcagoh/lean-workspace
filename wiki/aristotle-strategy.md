# Aristotle Strategy

Everything learned about getting good results from Aristotle. Merges the submission strategy from `Lean 4 Proofs.md` and the workflow lessons earned from JEPA proof rounds.

---

## Submission Sizing

- **≤ 5 sorries per job** — jobs with more than 5 rarely close all of them. Split by logical cluster.
- **≤ 5 sorries in one file: usually fine as one job.** More than 5, or sorries across multiple files: split by lemma cluster.
- **Split measure-theoretic sorries** — custom measure types (pushforwards, product measures) are hardest. Decompose into: (1) norm/measurability sub-lemma, (2) independence/covariance argument, (3) assembly. Submit each separately.

## Statement Quality

- **A disproof means the statement is wrong** — Aristotle found a counterexample; the hypotheses are under-constrained. Re-examine the hypotheses before resubmitting. (Example: `diagonal_ODE` was disproved because `sigma_r` was a free function — fix was binding it to the gradient flow via `hsigma_def` and `hflow`.)
- **Correct the statement first** — a sorry with a wrong statement will never be proved.
- **If Aristotle flags a wrong quantity or direction, fix the Lean statement** before resubmitting.
- **Variance vs. E[f²]** — for Chebyshev arguments, always bound `MeasureTheory.variance f μ`, not `∫ x, f x ^ 2 ∂μ`. Variance is strictly smaller (by `E[f]²`) and is what Chebyshev actually requires.

## Crafting PROVIDED SOLUTION Blocks

- Place the `PROVIDED SOLUTION` inside the `/-- ... -/` docstring, not in a `-- comment` inside the `by` block. Aristotle reads the header docstring; it ignores tactic-block comments.
- The richer the steps, the better the output. ODE/integral arguments especially benefit from detailed step-by-step hints.
- Template:
  ```lean
  /-- **Lemma N.M (Name).** Statement in plain English.

      PROVIDED SOLUTION
      Step 1: First proof step from the paper.
      Step 2: Key substitution or identity used.
      Step 3: Conclusion. -/
  lemma my_lemma ... : ... := by
    sorry
  ```

## Effective Prompts

| Goal | Prompt |
|---|---|
| Fill all sorries | `"Fill in all the sorries in this project"` |
| Single file | `"Fill in the sorries in <Module>/<File>.lean"` |
| Targeted | `"Fill in <LemmaA> and <LemmaB>. Each has a detailed PROVIDED SOLUTION."` |
| Golf proofs | `"Golf all the proofs: minimize tactic count and simplify where possible"` |
| Repair | `"Fix all compilation errors and linter warnings"` |

## Merging Results

- **Never wholesale replace local files** — Aristotle jobs are independent snapshots. A later job may re-sorry lemmas proved by an earlier job.
- Always read `ARISTOTLE_SUMMARY_<id>.md` first. Diff the returned `.lean` files against local versions — Aristotle may add hypotheses.
- Cherry-pick only the proved lemma bodies into the local file.
- **`OUT_OF_BUDGET` means partial results are available** — download them anyway with `retrieve.py` and see what was proved before resubmitting the remainder.
- **Aristotle may add new hypotheses** — incorporate them (e.g. `h_denom_order`, `h_cont`, `hDelta_nz`) before the next submission.

## Domain-Specific Patterns

**Helper file pattern** — when a theorem needs classical results not in Mathlib (Grönwall, Rayleigh quotient bounds), create a separate `Lemmas.lean` or `<Name>Helpers.lean` with sorry'd lemmas and their own PROVIDED SOLUTION blocks. This lets Aristotle tackle each gap separately. Import order in the entry file matters — list files in dependency order.

**Dimension case-splits for volume lemmas** — when a lemma about `volumeFill`/`volumeEmpty` fails for all `d`, split into `_d0`, `_d1`, `_ge2` sub-lemmas. The `d=0` and `d=1` cases are degenerate (Gamma function values) and close with `norm_num`/`simp`; `d≥2` is the real content.

**3-sub-lemma pattern for variance bounds over custom measures** — when `MeasureTheory.variance f μ ≤ C` fails monolithically, decompose into:
1. `f_sq_le_one`: `f(s)^2 ≤ 1` via `Finset.abs_prod` + `sq_le_one_iff_abs_le_one`
2. `cov_independent_zero`: covariance = 0 for independent pairs via `integral_mul_eq_integral_mul_integral`
3. `cov_dependent_le`: covariance bound for dependent pairs by factoring the shared variable

Submit sub-lemmas as one job; assembly as a separate follow-up.

**`∀ᶠ` for eventually-true bounds** — when a bound only holds for large `k`, state it as `Filter.Eventually` rather than `∀ k`. This avoids a `k < N` edge case Aristotle cannot close without extra hypotheses.

**Derive positivity at call sites** — if a lemma needs `hg : 0 < g` and the caller has `hSNR : n^{3/2} * g → ∞`, derive `hg` via `pos_of_mul_pos_left` inside a `filter_upwards` block rather than adding it to the outer `∀ k` quantifier.

## Workflow Lessons (Earned from JEPA Rounds)

- **Vacuous proofs are a trap** — Aristotle proved `frozen_encoder_convergence` with a witness `C_A = (‖V(τ_A)‖+1)/ε^{2(L-1)/L}`, making C_A depend on ε and the trajectory. Physically meaningless. If the existential allows a trivial witness, tighten the conclusion to force a genuine proof.
- **Don't re-run already-proved lemmas** — once a lemma is genuine, never let Aristotle's snapshot overwrite it. Cherry-pick; never replace.
- **`bootstrap_consistency` convention (JEPA)** — ODE continuation for a joint gradient-flow system requires Picard-Lindelöf infrastructure not in Mathlib. Keep it as an explicit named `sorry` (CompCert convention). Name it in the paper as the single explicit open assumption.

---

## Setup

**Install once** (Python 3.10+ required):
```bash
pip install aristotlelib pathspec python-dotenv
# or: uv pip install aristotlelib pathspec python-dotenv
```

**`.env` in each project root** (gitignored — never commit):
```
ARISTOTLE_API_KEY=arstl_...
```

---

## Python API

```python
from aristotlelib import Project, ProjectStatus, AristotleAPIError

# Submit
project = await Project.create(prompt="Fill in the sorries", tar_file_path="./project.tar.gz")
project = await Project.create_from_directory(prompt="Fill in the sorries", project_dir=".")

# Monitor
await project.refresh()
print(project.status, project.percent_complete)

# Download when complete
path = await project.get_solution(destination="results/output.tar.gz")
# Or wait and download in one call:
path = await project.wait_for_completion(destination="results/output.tar.gz")

# List / retrieve existing
project = await Project.from_id("abc-123-def")
projects, next_key = await Project.list_projects(status=ProjectStatus.COMPLETE, limit=10)

# Cancel
await project.cancel()
```

**`ProjectStatus` enum:** `QUEUED` → `IN_PROGRESS` → `COMPLETE` | `COMPLETE_WITH_ERRORS` | `OUT_OF_BUDGET` | `FAILED` | `CANCELED`

Terminal statuses (no further changes): `COMPLETE`, `COMPLETE_WITH_ERRORS`, `OUT_OF_BUDGET`, `FAILED`, `CANCELED`

## CLI

```bash
aristotle submit "Fill in the sorries" --project-dir . --wait --destination output.tar.gz
aristotle list --status COMPLETE IN_PROGRESS --limit 20
aristotle result <project-id> --wait --destination output.tar.gz
aristotle cancel <project-id>
```

---

## Result File Structure

```
{project_id}_aristotle/
├── ARISTOTLE_SUMMARY_{project_id}.md   # read this first — what changed, what compiled
├── README.md
├── lake-manifest.json
├── lakefile.toml
├── lean-toolchain
└── RequestProject/
    └── {TheoremName}.lean              # proven files (sorries filled)
```

Always read `ARISTOTLE_SUMMARY_*.md` first. Diff returned `.lean` files against local versions — Aristotle may add hypotheses.
