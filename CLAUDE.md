# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This is the workspace root for all Lean 4 / Aristotle projects. Each subdirectory has its own CLAUDE.md with project-specific context; this file is intentionally minimal.

---

## Workspace Layout

```
lean-workspace/
├── wiki/                        # Workspace-wide state (read this first every session)
├── .lean-packages/              # Shared Mathlib/Lake cache (~7.7 GB) — do not delete
├── scripts/                     # Shared scripts
├── stochastic-proofs-handbook/  # Cross-project patterns, workflow, repo roles
├── jepa-learning-order/
├── simplicial-latent-geometry/
└── stochastic-search-bounds/
```

---

## Wiki structure — where things live

| What | Where |
|---|---|
| Sorry counts, arXiv readiness, Aristotle job IDs | `wiki/INDEX.md` — Status + Open Questions |
| Session history | `wiki/session-log.md` |
| Architectural decisions | `wiki/decisions.md` |
| Lean/Mathlib API reference | `wiki/lean4-reference.md` |
| Aristotle submission patterns AND ops protocol (CLI, API key, scripts) | `wiki/aristotle-strategy.md` — read **Operational protocol** before running any aristotle command |
| Shared script reference (submit/status/retrieve/watch) | `stochastic-proofs-handbook/scripts/README.md` |
| File maps, pitfalls, build commands | Each project's `CLAUDE.md` |

> **Rule:** project CLAUDE.md files contain architecture only — not status or roadmaps.
> `wiki/INDEX.md` is the single source of truth for project state.

---

## Session Start

Read `wiki/INDEX.md`, then the top entry of `wiki/session-log.md`.

## Session End

Run `/session-wrap` to update `wiki/session-log.md` and `wiki/INDEX.md`.
