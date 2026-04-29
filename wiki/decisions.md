# Decisions

Design choices already locked in. Read before changing anything architectural.

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
