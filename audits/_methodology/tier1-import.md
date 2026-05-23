# Tier 1 — Import graphs

File-level view: nodes are `.lean` files; edges are `import` statements. Size ∝ LOC, border thickness ∝ fan-in, color by role.

## Reading order — start with SSB

SSB is the **reference shape**: depth 3, no god-module, clean sibling fan-out. Look at it first to internalize what "healthy" looks like, then compare the others against it.

| Project | File | One-line finding |
|---|---|---|
| stochastic-search-bounds | [`stochastic-search-bounds_import_tier1.svg`](stochastic-search-bounds_import_tier1.svg) | **Reference.** Single foundation file, four sibling theorems, two strong variants. No god-module. |
| jepa-rho-recovery | [`jepa-rho-recovery_import_tier1.svg`](jepa-rho-recovery_import_tier1.svg) | Intermediate shape — wide fan, no god-module, real foundation in `Basic.lean` (fan-in 13). |
| jepa-learning-order | [`jepa-learning-order_import_tier1.svg`](jepa-learning-order_import_tier1.svg) | **`JEPA.lean` (2002 LOC) is a god-module** holding 4 internal clusters; split candidate. |

## Encoding

| Channel | Meaning |
|---|---|
| Node size | ∝ LOC |
| Border thickness | ∝ fan-in (downstream invalidation cost) |
| Fill — red | God-module (single file holding multiple math clusters) |
| Fill — blue | Foundation (heavy fan-in, low LOC ideally) |
| Fill — yellow | Synthesis (assembles results from siblings) |
| Fill — gray | Helper (single-cluster extracted lemmas) |
| Dashed border | Orphan or stub (verify intent before acting) |
| Layout | `rankdir=BT`, foundations at top, terminals at bottom |
