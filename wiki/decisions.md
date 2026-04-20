# Decisions

Design choices already locked in. Read before changing anything architectural.

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
