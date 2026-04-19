# Decisions

Design choices already locked in. Read before changing anything architectural.

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

## `bootstrap_consistency` as named regularity assumption (jepa-learning-order)

**Decision:** `bootstrap_consistency` stays as an explicit named `sorry` in `JEPA.lean`. No attempt to close it via Aristotle.

**Why:** Requires Picard-Lindelöf ODE continuation for a joint gradient-flow system — infrastructure not in Mathlib. This is the CompCert convention; every ODE learning-dynamics paper assumes joint solution existence.

**Consequence:** The paper §5.3 should name it as the single explicit open assumption. Do not chase it in Lean.

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
