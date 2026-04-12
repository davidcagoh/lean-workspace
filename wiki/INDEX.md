# Wiki Index — lean-projects

## Files

| File | When to read |
|---|---|
| `INDEX.md` (this file) | Start of every session — check status block and next priorities |
| `session-log.md` | Start of every session — read the top (most recent) entry for project state |
| `decisions.md` | Before making architectural or proof-strategy choices |
| `open-questions.md` | When something seems ambiguous or undocumented; add new questions here |
| `lean4-reference.md` | Before writing any Lean — type conventions, Mathlib API, pitfalls, termination patterns |
| `aristotle-strategy.md` | Before submitting to Aristotle — sizing, statement quality, merging, domain patterns |

### Handbook
`stochastic-proofs-handbook/` is now scripts-only. Its `docs/`, `templates/`, and `archive/` directories have been deleted — all knowledge is in this wiki. The handbook README points here.

### Paper drafts
`papers/` directory has been removed (2026-04-12). Paper drafts now live inside each lean project's `my_theorems/` directory:
- `jepa-learning-order/my_theorems/JEPA_paper_draft.md` — canonical latest (v2, "Conditional" title, 767L)
- `stochastic-search-bounds/my_theorems/Manuscript_v6.md` — canonical latest
- Older drafts are in each project's `my_theorems/archive/`

## Status (2026-04-12)

| Project | Sorries | Status |
|---|---|---|
| `jepa-learning-order` | 2 (`bootstrap_consistency` + `frozen_encoder_convergence`) | Aristotle job `315fff00` queued for `frozen_encoder_convergence`. `bootstrap_consistency` is long-term open. |
| `stochastic-search-bounds` | **0** ✅ | All 4 AND-OR hypertree theorems proved. Renamed from `theorem-agents`. |
| `simplicial-latent-geometry` | 13 | matchRadius definition fixed. New sorries = asymptotic chain with PROVIDED SOLUTIONs. Aristotle submission pending (OQ-3). |
| `stochastic-proofs-handbook` | n/a | Scripts only |

## Next Priorities

1. **jepa:** Wait for Aristotle job `315fff00` (`frozen_encoder_convergence`) — then cherry-pick, resolve temporal re-indexing gap, wire into `JEPA_rho_ordering` (OQ-5)
2. **jepa:** Update paper abstract once `frozen_encoder_convergence` lands — then submit
3. **simplicial:** Decide Option A (fix `matchRadius` → full result) vs Option B (ship variance-bound result now) — see OQ-3
4. **simplicial:** Fix forward-ref for `volumeFill_div_le_one'` (move proof block earlier in file) — see OQ-6
5. **stochastic-search-bounds:** Update GitHub description to reflect meta-narrative
