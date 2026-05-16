# lean-workspace

A workflow for using **Aristotle** (Harmonic's automated theorem prover) on **original mathematical research**, not as a benchmark or as an autoformalizer for known theorems.

> Three independent projects — linear-JEPA dynamics, simplicial latent geometry, stochastic search bounds — each consisting of a paper draft plus a Lean 4 formalization. Sorries are submitted to Aristotle as scoped jobs. Returned proofs are audited before being merged. The same workflow has driven all three projects toward submission. One of them (stochastic-search-bounds) currently has zero sorries in its Lean formalization.

This repo is the **workflow itself**: shared scripts, the running session-by-session wiki, and the cross-project handbook. The proof code lives in three sibling repositories:

| Project | Repo | Status |
|---|---|---|
| Linear-JEPA $\rho^*$-ordering dynamics | [`jepa-learning-order`](https://github.com/davidcagoh/jepa-learning-order) | 12pp paper draft; 2 named sorries (Picard-Lindelöf / Littwin 2024 Thm 4.5), both standard ODE/Laurent facts treated as named axioms under the CompCert convention |
| Simplicial latent geometry detection | [`simplicial-latent-geometry`](https://github.com/davidcagoh/simplicial-latent-geometry) | 16pp paper draft; main theorems sorry-free |
| Stochastic search bounds for guided search | [`stochastic-search-bounds`](https://github.com/davidcagoh/stochastic-search-bounds) | 0 sorries; 18pp paper compiles clean |

A methodology paper describing the workflow itself is in preparation.

---

## Why this exists

Aristotle and similar AI theorem provers are usually evaluated on miniF2F, ProofNet, or single-shot formalizations of textbook results. That's a useful benchmark but a poor model of how this kind of tool actually plugs into research mathematics, where:

- Statements evolve as understanding does. A sorry's statement is often wrong on the first pass; the AI proving it would be a bug.
- Sorries cluster in load-bearing places (measure-theoretic moves, ODE comparisons, perturbation arguments) where mathematicians normally hand-wave or cite Mathlib.
- Returned proofs need to be audited. Modern provers can produce technically-valid Lean that satisfies a wrong statement, evades the intended argument, or relies on hidden assumptions. Without an audit step, you accumulate junk.
- Workflow state matters as much as proof state. Sessions are long, jobs run for hours, paper drafts and Lean code drift apart without explicit synchronization.

This workspace is the answer I converged on after ~50 sessions of doing this for real, on results I wanted to publish.

---

## The workflow, in one paragraph

Write the mathematical statement as Lean. Leave the hard step as a `sorry`. Decompose the sorry into named sub-lemmas (≤ 5 sorries per Aristotle job is the sweet spot; more rarely closes). Submit the job with a structured prompt — context, target lemma, hypotheses, known available facts, and a fingerprint of the intended strategy. While it runs, work on the paper draft so the informal argument and the formal one converge. When the job returns, **audit before cherry-picking**: check that hypotheses are actually consumed, witnesses aren't ε-dependent where they shouldn't be, no `decide`/`native_decide`/`admit`, and that the proof matches the intended argument rather than a triangle-inequality shortcut that makes the statement trivially true. If the audit fails, the sorry usually means the statement is wrong, not the proof — fix the statement and resubmit. Commit only audited results. Update the wiki. Repeat.

The wiki and handbook in this repo are the artifact of doing this many times.

---

## Repo layout

```
lean-workspace/
├── wiki/                              # Cross-project knowledge — patterns that took sessions to learn
│   ├── aristotle-strategy.md          # Submission sizing, statement quality, evasion patterns to audit for
│   ├── lean4-reference.md             # Lean 4 / Mathlib patterns and pitfalls learned the hard way
│   ├── decisions.md                   # Locked-in architectural choices with rationale
│   └── open-questions.md              # Open tactical questions
├── stochastic-proofs-handbook/        # Cross-project workflow assets
│   ├── README.md
│   └── scripts/                       # Shared CLI tooling
│       ├── submit.py                  # Package and submit a Lean job to Aristotle
│       ├── status.py                  # Sorry inventory + in-flight job status
│       ├── retrieve.py                # Download + auto-annotate completed jobs
│       ├── watch.py                   # Poll running jobs
│       ├── init.py                    # Scaffold a new project
│       ├── verify_refs.py             # Audit a .bib file against Semantic Scholar (VERIFIED / LIKELY / NOT_FOUND)
│       └── forward_cites.py           # Find recent forward citations of your bib entries
├── CLAUDE.md                          # Instructions for Claude Code agents working in this repo
└── .gitignore                         # Excludes the three proof projects (they're independent repos)
```

The three proof projects (`jepa-learning-order`, `simplicial-latent-geometry`, `stochastic-search-bounds`) are intentionally `.gitignore`d here — they live as siblings in the parent directory and have their own independent repositories. This workspace is the *spine*: shared tooling and accumulated knowledge.

---

## What the wiki actually contains

The wiki holds patterns and pitfalls that took many sessions to discover, in a form that should be useful to other Aristotle / Lean 4 users:

- **`wiki/aristotle-strategy.md`** — what to do when Aristotle returns a disproof (usually the statement is wrong, not the proof), how to size and cluster sorries, named evasion patterns to audit for (`hWbar never used`, `ε-dependent K`, `decide / native_decide / admit`, exponent rewrites that make a statement trivially false, etc.).
- **`wiki/lean4-reference.md`** — Lean 4 / Mathlib pitfalls accumulated across many sessions: doc-comment + `open ... in` incompatibility, `MeasureTheory.variance` vs `∫ f^2`, three-level file organization for fast subset builds, when `Finset.single_le_sum` is the right move.
- **`wiki/decisions.md`** — architectural choices made and why: paper-writing scripts live under the handbook, three-level file hierarchy, RSA-via-Wiley submission order, etc.
- **`wiki/open-questions.md`** — open tactical questions across the three projects.

Per-session running state (status, sorry counts, in-flight job IDs, next priorities) is kept in `wiki/INDEX.md` and `wiki/session-log.md`, which are not tracked in this repository.

---

## What the three projects show

A methodology paper has to answer: *how do we know your workflow actually works?* Three concrete data points:

1. `stochastic-search-bounds` has zero sorries. The 18-page paper has every load-bearing claim formalized in Lean.
2. `simplicial-latent-geometry`'s main theorems are sorry-free. The geometric-covariance arguments (Tracks A, B, C) are closed, including a `TorusIntegrals.lean` covering measure-theoretic moves at the edge of what Mathlib currently supports.
3. `jepa-learning-order` has two named sorries (`h_gronwall` and `h_laurent`) — standard ODE/Laurent facts that informal learning-theory papers leave implicit. Both are documented as named axioms in the paper appendix.

The audit step on returned proofs is non-trivial in practice. As one example, a returned proof of `actual_critical_time` (JEPA Job H) silently rewrote an exponent from `-(L-2)/L` to `-(2L-1)/L` so that triangle inequality would close it without using the `hWbar` hypothesis. The wiki session-36 entry documents the catch. The audit checklist in `wiki/aristotle-strategy.md` is what makes that catch routine rather than lucky.

---

## Using the scripts

From a project subdirectory (e.g. `jepa-learning-order/`):

```bash
# Submit a Lean file with named sorries to Aristotle
python ../stochastic-proofs-handbook/scripts/submit.py my_theorems/Paper.md "Fill in the sorries"

# Check status of all in-flight jobs and the current sorry inventory
python ../stochastic-proofs-handbook/scripts/status.py

# Retrieve a completed job (downloads tarball, annotates results in-place)
python ../stochastic-proofs-handbook/scripts/retrieve.py [project-id]

# Audit references in a paper
python ../stochastic-proofs-handbook/scripts/verify_refs.py path/to/references.bib

# Find recent forward citations of your references — surface relevant new work
python ../stochastic-proofs-handbook/scripts/forward_cites.py path/to/references.bib
```

The scripts walk up from `cwd` to find the workspace-root `.env`. You'll need `ARISTOTLE_API_KEY` for proof submission and `SEMANTIC_SCHOLAR_API_KEY` for the bibliography tooling.

---

## Status and roadmap

| | State (2026-05-16) |
|---|---|
| Three proof projects | All paper-ready; SSB compiles clean with 0 sorries |
| arXiv | Simplicial + SSB pending Cook math.* endorsement (email sent); JEPA cs.LG endorsement pipeline being reset (Papyan ask did not land) |
| Methodology paper | In preparation. Target venue under discussion — likely ITP or a NeurIPS/ICLR workshop |
| Workshop tracks | CICM 2026 presentation-only (June 15 deadline) is the next viable venue while endorsements clear |

This repository is being made public **now**, ahead of the arXiv submissions, so that the workflow itself has a public timestamp independent of the endorsement queue.

---

## Contact

David Goh — MScAC Applied Mathematics, University of Toronto.

- Email: davidcagoh@gmail.com
- Site: https://davidcagoh.github.io/

If you're an Aristotle user, a Lean proof engineer, or a mathematician thinking about putting an AI prover in your workflow and want to compare notes, please write.

---

## License

MIT — see [`LICENSE`](LICENSE). The proof code in each sibling repository carries its own license.
