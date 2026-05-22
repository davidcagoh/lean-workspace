# Audit methodology

How each tier is constructed, what it encodes, and how to read it.

| Tier | Doc | When to run |
|---|---|---|
| 1 — import graph | [`tier1-import.md`](tier1-import.md) | Every project, every audit cycle |
| 3a — math build-up | [`tier3a-build-up.md`](tier3a-build-up.md) | Before paper submission, or when reviewing for code quality |
| 3b — god-module zoom | [`tier3b-god-module-zoom.md`](tier3b-god-module-zoom.md) | When tier 1 flags a file as a god-module (LOC > 800) |

## Minimal workflow for editing-pain triage

```
tier 1  →  (god-module?)  →  tier 3b  →  split  →  re-run tier 1
```

Tier 3a is an optional separate pass for code-quality findings (dead lemmas, unused hypotheses), not editing-pain.
