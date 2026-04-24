# Open Questions

Add new questions at the top of the OPEN section. Move to RESOLVED when closed.

---

## OPEN

### OQ-11: stochastic-search-bounds — Aristotle Job `fc0719d6` (T4 sharp regime)

Submitted 2026-04-24 (session 22). Target: prove `sum_prod_erase_le_one_of_sum_le_one` and `sequential_le_parallel_sharp` in `AutomatedProofs/AOTree/Theorem4_Strong.lean`, replacing the uniform hypothesis `q(i) ≤ 1/2` with the sharp condition `∑ q(i) ≤ 1`. Proof strategy in spec: Maclaurin's inequality / iterated AM-GM gives `e_{n-1}(q) ≤ 1/n^{n-2} ≤ 1` for `n ≥ 2`.

- Request doc: `help_from_aristotle/05_fc0719d6_request.md`
- Retrieve when Aristotle emails: `python scripts/retrieve.py`
- On success: upgrade Proposition 4.15 in `paper.tex` to the sharp form; original `sequential_le_parallel` stays as special case.

---

### OQ-12: stochastic-search-bounds — T2 `hcorrect_better` weakening (design-before-submit)

Before submitting to Aristotle, pick a concrete weaker sufficient condition. Candidates:
1. **Locality:** require ordering only at OR nodes on actual proof paths.
2. **Greedy-wrt-value:** require `π'` greedy wrt per-subtree `V(T) = successProb(π', T, ·)`.
3. **Zero-on-incorrect:** require `π'(nid, i) = 0` for incorrect children (`hcorrect_better` becomes vacuous).

Option 2 is the cleanest research target; Option 1 is in the middle; Option 3 is easy but very restrictive. Action: pick one, formalise, scaffold, submit.

---

### ~~OQ-10: simplicial — `chebyshev_ratio_tendsto_zero` Lean signature weaker than proof needs~~ — RESOLVED 2026-04-24 (session 19)

Aristotle Job C `986efbdd` chose Option 1 verbatim: added `hNG : n·g → ∞` hypothesis to `chebyshev_ratio_tendsto_zero`, `paleyZygmund_cech_prob_tendsto_one`, and `detection_lower_bound`. Also introduced `derive_hNG` helper and tightened `phase_transition`'s `hbeyond` from `d/(n^{3/2}·G)^{1/α} → 0` to the (strictly stronger) `d/(n·G)^{1/α} → 0`. Session 19 cherry-picked all three jobs, dropped a spurious `hd` hypothesis from `paleyZygmund` + `detection_lower_bound`, and added `detection_lower_bound_fixed_d` — the exact Lean counterpart to the paper's fixed-`d` Theorem 4.2. Paper pointer at line 592 updated from `phase_transition` → `detection_lower_bound_fixed_d`.

---

### ~~OQ-9: simplicial — prove geomCov(p,d) = Θ(|log p|/d)~~ — RESOLVED 2026-04-20 (session 11)

The proposed decay rate was incorrect. Correct result: **sharp phase transition** at d*(p) = |log p|/log(3/2).
- For d ≥ d*(p): matchRadius > 1/3 → all triples fill on AddCircle(1) (1D Helly via complement measure) → fillingProb = 1 exactly → geometricCov = 0 exactly.
- For d < d*(p): geometricCov > 0, detection succeeds when SNR → ∞.
Proved in Lean as `geometricCov_eventually_zero` (session 11). §4.4 and full paper updated. Paper now submittable.

---

### ~~OQ-8: simplicial — close `fillingProb_tendsto_one`~~ — RESOLVED 2026-04-20 (session 9)

Aristotle jobs b1c3a2c5 + aa0cf669 proved `fillingProb_tendsto_one` via `fill_eventually_always'` + `tendsto_nhds_of_eventually_eq`. Cherry-picked into SimplicialDetection.lean. `substituted_tendsto` bypassed entirely.

---

### OQ-7: Publication strategy — JEPA and stochastic-search-bounds venue targets

Simplicial venue is now decided (RSA, session 12). Remaining open items:
1. **JEPA standalone** → ICLR theory / COLT / TMLR (submittable once abstract updated; 1 sorry remaining)
2. **Stochastic-search-bounds standalone** → venue TBD (0 sorries; LaTeX/bib pending)
3. **Methodology paper** ("Aristotle-Assisted Formalization of ML Theory") → NeurIPS / ITP / CPP — uses all three as case studies; `stochastic-search-bounds` self-referential meta-narrative is the centrepiece

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
