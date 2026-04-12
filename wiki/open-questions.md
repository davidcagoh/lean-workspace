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

### OQ-5: jepa — `frozen_encoder_convergence` genuine proof + wiring

**Active Aristotle job:** `f9906716-3fc4-4962-8bc9-3182bc98e62e` — QUEUED (2026-04-12)

**Attempt history:**
- `1afe6f24` — vacuous (∃ C_A; picked trajectory-dependent witness)
- `315fff00` — vacuous again (COMPLETE_WITH_ERRORS, do not cherry-pick)
- `f9906716` — **existential eliminated** — Aristotle must now produce a genuine exponential decay proof or fail

**Current lemma signature (JEPA.lean lines 886–916):**
- Explicit constants: `K₀ K_qs c₀ : ℝ` (not existential)
- `hV_init : matFrobNorm (V 0) ≤ K₀ * ε^{1/L}`
- `hK_qs : matFrobNorm (quasiStaticDecoder dat W₀) ≤ K_qs * ε^{1/L}`
- `hτ_A_def : τ_A = (2(L-1)/L)/c₀ · ε^{-2/L} · log(1/ε)`
- **Conclusion:** `matFrobNorm (V τ_A - quasiStaticDecoder dat W₀) ≤ (K₀ + K_qs) * ε^{2(L-1)/L}`

**When `f9906716` lands:**
1. Check ARISTOTLE_SUMMARY — if not vacuous, cherry-pick
2. Wire into `JEPA_rho_ordering`: caller supplies `C_A := K₀ + K_qs` (positivity from `hK₀`, `hK_qs_pos`)
3. Temporal re-indexing gap: `V(τ_A)` → `V(0)` for Phase B start — structural, needs `hτ_A_link` or time-shift

---

### OQ-3: simplicial — submit Aristotle job for matchRadius asymptotic chain

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
