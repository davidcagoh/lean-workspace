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

## Session Start

Read `wiki/INDEX.md`, then the top entry of `wiki/session-log.md`.

## Session End

Run `/session-wrap` to update `wiki/session-log.md` and `wiki/INDEX.md`.

---

## Project-Specific Context

Everything else — Lean 4 conventions, Aristotle API usage, proof strategy, pitfalls, scripts — lives in each project's own `CLAUDE.md` and `wiki/` files.
