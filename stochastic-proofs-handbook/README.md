# Stochastic Proofs Handbook

Canonical home for the **shared scripts** used across all Lean 4 projects in the workspace. Knowledge and conventions live in `lean-workspace/wiki/`.

## Scripts

Run from inside a project directory (e.g. `jepa-learning-order/`):

| Script | Command | Purpose |
|---|---|---|
| `status.py` | `python ../stochastic-proofs-handbook/scripts/status.py` | Sorry count + Aristotle job statuses |
| `submit.py` | `python ../stochastic-proofs-handbook/scripts/submit.py my_theorems/Paper.md "..."` | Package and submit to Aristotle |
| `retrieve.py` | `python ../stochastic-proofs-handbook/scripts/retrieve.py [project-id]` | Download tarball + annotate results |
| `watch.py` | `python ../stochastic-proofs-handbook/scripts/watch.py` | Poll in-flight jobs |
| `init.py` | `python scripts/init.py` | Scaffold a new project (run from workspace root) |

API key is loaded by walking up from cwd — the workspace-root `.env` is sufficient.

## Knowledge base

```
lean-workspace/wiki/
├── INDEX.md               # Status + next priorities — read at session start
├── session-log.md         # Running session log
├── decisions.md           # Locked-in architectural choices
├── lean4-reference.md     # Lean 4 / Mathlib patterns and pitfalls
└── aristotle-strategy.md  # Submission strategy and workflow lessons
```
