# Open Questions

Add new questions at the top of the OPEN section. Move to RESOLVED when closed.

---

## OPEN

### OQ-9: simplicial — prove geomCov(p,d) = Θ(|log p|/d) to complete the BDER analogy

**Why this matters:** Without the decay rate, d*(n,p) ~ n^{3/2}|log p| is a heuristic (§4.4). We know geomCov→0 but not how fast. BDER proved both the phase transition AND the explicit threshold; we've only done the former. The paper should not be submitted until this is resolved.

**Mathematical content needed:**

The matched radius satisfies r(p,d) = p^{1/d}/2 = 1/2 · e^{(log p)/d}, so:
```
ε(d) := 1/2 - r(p,d) ≈ |log p| / (2d)   as d → ∞
```

Need to show geomCov(p,d) = Θ(ε(d)) = Θ(|log p|/d). This requires:

**Step 0 (prerequisite):** Read `SimplicialDetection.lean` around the current `fillingProb` definition (post-session-9 refactor). Understand exactly what the "torus fill indicator integral" computes — the precise integrand and measure. This is the foundation; don't proceed without it.

**Step 1 — Upper bound:** Show 1 - fillingProb(p,d) = O(|log p|/d).
- Argument: when r = 1/2 - ε, the fill fails only when three points are arranged so their r-balls don't share a point. The measure of such configurations shrinks at rate O(ε) = O(|log p|/d).
- Write a clear PROVIDED SOLUTION with the volume estimate; submit to Aristotle.

**Step 2 — Lower bound:** Show 1 - fillingProb(p,d) = Ω(|log p|/d).
- Harder: need a family of configurations where fill fails, with total measure Ω(ε).
- This is the genuine mathematical bottleneck. Identify an explicit bad region (e.g., points near opposite faces of the torus cube) and bound its measure from below.

**Step 3 — geomCov rate:** Translate the fillingProb rate into geomCov(p,d) = Θ(|log p|/d). The relationship is via the definition of geomCov as an expectation over Čech triples; the fill factor (F_t - q) = (F_t - fillingProb) dominates the decay.

**Step 4 — Threshold theorem:** With the rate, prove d*(n,p) = Θ(n^{3/2}|log p|) rigorously and replace §4.4's heuristic remark with a theorem.

**Step 5 — Paper update:** Upgrade §4.4 from heuristic to Theorem. The rest of the paper (intro, models, statistic, moments, detection theorem, Lean section) is fine as-is — do NOT scratch it.

**Caution:** Before doing any of the above, clarify the model. With the sup-norm Čech complex and Definition 2.3's fill criterion (balls of radius r, same as edge radius), a vertex x_i is always a common point of all three balls when all edges are present — meaning fillingProb = 1 always. If that's what the current Lean code computes, the model needs to be corrected first (standard Čech uses ball radius r/2, edge threshold 2r — or equivalently ball radius r, edge threshold r but fill balls of radius r/2). Resolve this before any Aristotle submission.

**Status:** OPEN — starting point for next session.

---

### OQ-8: simplicial — close `fillingProb_tendsto_one` via geometric bypass

**Context:** `substituted_tendsto` (the DCT pointwise convergence step) is likely false — see decisions.md. The correct fix is Task A in `wiki/substituted-tendsto-prompt.md`: prove `fillingProb_tendsto_one` directly using `fill_eventually_always'` (geometric: when matchRadius > 1/3, all triples fill → fillingProb = 1 eventually). This bypasses `substituted_tendsto` entirely.

**Blocking:** Need to connect the measure-theoretic integral definition of `fillingProb` with the geometric statement that fill is universal. Probably an Aristotle job targeting `fillingProb_tendsto_one` with the Task A provided solution.

**Status:** Prompt ready at `wiki/substituted-tendsto-prompt.md`. Not yet submitted to Aristotle.

---

### OQ-7: Publication strategy — finalize venue targets

**Decision needed:** Three-paper structure proposed:
1. JEPA standalone → ICLR theory / COLT / TMLR (submittable once abstract updated)
2. Simplicial standalone → AoAP / Bernoulli / TDA venue (blocked on matchRadius fix)
3. Methodology paper ("Aristotle-Assisted Formalization of ML Theory") → NeurIPS / ITP / CPP — uses all three as case studies; `stochastic-search-bounds` self-referential meta-narrative is the centrepiece

**Blocking:** Paper 2 needs matchRadius resolved (OQ-3). Paper 3 needs a rough outline and decision on whether to involve collaborators.

---

### OQ-6: simplicial — close `volumeFill_div_le_one'` forward-reference sorry (line 2296)

**Context:** Both downloaded jobs (`60e73ec0`, `b91c8747`) were already merged before this session. `disjoint_triangles_indepFun` (line 2586) and `volumeFill_div_volumeEmpty_le_one_ge2` (line 3454) are fully proved.

`volumeFill_div_le_one'` at line 2296 remains `sorry` due to a **forward reference**: it calls `volumeFill_div_volumeEmpty_le_one` which is defined at line 3479. Lean 4 rejects this — cannot call a name defined later in the file.

**Options:**
- (A) Move the `incBeta_*` + `volumeFill_div_volumeEmpty_le_one_ge2` block earlier in the file (before line 2296) — requires careful restructuring but is the clean fix
- (B) Duplicate the proof inline at line 2296

**Status:** Blocked on file restructuring. Not an Aristotle job.

---

### ~~OQ-5: jepa — `frozen_encoder_convergence` genuine proof + wiring~~ — RESOLVED 2026-04-19

**Resolution:** Aristotle job `f9906716` proved `frozen_encoder_convergence` genuinely (COMPLETE). 5 helper lemmas introduced. $C_A = K_0 + K_\text{qs}$ is $\varepsilon$-independent. Cherry-picked into `JEPA.lean` 2026-04-19; build passes (8028 jobs). Paper updated (Lemma 5.6 added; Appendix B table updated; Section 9 open problems reduced from 3 to 2).

**Remaining:** Wiring `hPhaseA` via `frozen_encoder_convergence` in `JEPA_rho_ordering` is a deferred mechanical step (low priority — paper is accurate as-is with `hPhaseA` as explicit hypothesis).

---

### ~~OQ-3: simplicial — matchRadius chain Aristotle job~~ — RESOLVED 2026-04-19

**Resolution:** Aristotle job `069b1a71-af74-41fe-9d94-15c92459c1e4` COMPLETE. `matchRadius_spec` (line 505) + `matchRadius_tendsto_half` (line 1277) cherry-picked into `SimplicialDetection.lean` 2026-04-19 (session 6). Both proofs use `Nat.cast_ne_zero.mpr (by omega)` — avoids the pre-existing `Nat.not_eq_zero_of_lt` build error. Downstream Aristotle job `cff9a2dd` now in flight.

---


### OQ-1: Paper submission venue for `jepa-learning-order`

**Context:** JEPA proof is near-complete (1 named sorry). Paper draft exists at `my_theorems/JEPA_paper_draft.md`. Strategic advice in `jepa-learning-order/CLAUDE.md` recommends submitting soon — "first machine-checked learning-dynamics result" claim has time value.

**Needed:** Decide on target venue (NeurIPS / ICLR / TMLR / COLT) and deadline. Update paper abstract to reflect current proof state before submission.

---

## RESOLVED

### ~~OQ-2: `stochastic-search-bounds` sorry count~~ — RESOLVED 2026-04-11
All 4 AND-OR hypertree theorems (Theorem1–4) fully proved. 0 sorries, builds clean.
