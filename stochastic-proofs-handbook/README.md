# Stochastic Proofs Handbook

This repository is the canonical home for the **shared scripts** used across all Lean 4 projects in the workspace. Knowledge and conventions have moved to `lean-projects/wiki/`.

## Scripts

| Script | Purpose |
|---|---|
| `scripts/status.py` | Project dashboard — sorry count + Aristotle job statuses |
| `scripts/submit.py` | Package and submit a project to Aristotle |
| `scripts/retrieve.py` | Download and annotate completed Aristotle results |
| `scripts/watch.py` | Adaptive background poller for in-flight jobs |
| `scripts/init.py` | Scaffold a new Lean project (run from workspace root) |

Run from inside a project directory:

```bash
python scripts/status.py       # via project-local copy
python ../scripts/status.py    # via workspace-root compatibility path
```

## Knowledge base

Cross-project knowledge (Lean 4 patterns, Aristotle strategy, decisions, open questions) lives at:

```
lean-projects/wiki/
├── INDEX.md               # Status + next priorities — read at session start
├── session-log.md         # Running session log
├── decisions.md           # Locked-in architectural choices
├── open-questions.md      # Blocking/ambiguous questions
├── lean4-reference.md     # Lean 4 / Mathlib patterns and pitfalls
└── aristotle-strategy.md  # Submission strategy and workflow lessons
```
