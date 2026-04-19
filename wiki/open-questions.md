# Open Questions

Add new questions at the top of the OPEN section. Move to RESOLVED when closed.

---

## OPEN

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

### OQ-3: simplicial — matchRadius chain Aristotle job

**Status: Aristotle job `069b1a71-af74-41fe-9d94-15c92459c1e4` SUBMITTED 2026-04-19**

OQ-6 (forward-ref) was already resolved in an earlier session (a primed copy was used). Job submitted 2026-04-19 targeting `matchRadius_tendsto_half` and downstream. `matchRadius_spec` is already proved. When job completes, run `python scripts/retrieve.py` and cherry-pick `matchRadius_tendsto_half` body.

*(original notes below)*

**Status: definition fixed (2026-04-12), Aristotle submission pending**

`matchRadius` definition corrected to `p^(1/d)/2` (sup-norm torus). New sorry chain ready:
- `matchRadius_spec` (line 505): `(2 * matchRadius p d)^d = p` — may need Aristotle
- `matchRadius_tendsto_half` (line 1275): `matchRadius p d → 1/2` as d→∞ — sorry + PROVIDED SOLUTION ✅
- Downstream asymptotic lemmas (lines ~1312, ~1526, ~1650): re-sorry'd with PROVIDED SOLUTION ✅
- Forward-ref sorry at line 2296: status unclear — check before next session

**Next step (first thing next session):**
```bash
cd simplicial-latent-geometry
python scripts/submit.py my_theorems/strategy2.md "Prove the matchRadius asymptotic chain: (1) matchRadius_spec: (2·matchRadius p d)^d = p for d≥1 using the sup-norm torus formula r=p^(1/d)/2; (2) matchRadius_tendsto_half: matchRadius p d → 1/2 as d→∞ using Real.rpow tendsto; (3) downstream lemmas using fillingProb → 1 and geometricCov → 0." --dry-run
```
Then submit for real.

---


### OQ-1: Paper submission venue for `jepa-learning-order`

**Context:** JEPA proof is near-complete (1 named sorry). Paper draft exists at `my_theorems/JEPA_paper_draft.md`. Strategic advice in `jepa-learning-order/CLAUDE.md` recommends submitting soon — "first machine-checked learning-dynamics result" claim has time value.

**Needed:** Decide on target venue (NeurIPS / ICLR / TMLR / COLT) and deadline. Update paper abstract to reflect current proof state before submission.

---

## RESOLVED

### ~~OQ-2: `stochastic-search-bounds` sorry count~~ — RESOLVED 2026-04-11
All 4 AND-OR hypertree theorems (Theorem1–4) fully proved. 0 sorries, builds clean.
