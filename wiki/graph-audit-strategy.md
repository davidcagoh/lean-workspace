# Graph Audit Strategy

Everything learned about diagnosing file-partition health in our Lean projects. The audit's purpose is **reducing editing pain** on large `.lean` files; secondary uses (catching dead code, unused hypotheses) are a separate optional pass.

Worked examples live in [`wiki/audits/`](audits/). When in doubt, look at the SSB renders — that project's tier 1 graph is the reference shape we aim for.

---

## Operational protocol (READ FIRST)

> If you're about to audit a project — use this section. The procedure is run-by-hand with small shell snippets; we don't maintain a dedicated script (we tried; the value didn't justify the maintenance cost at our scale).

**When to audit:**
- **Tier 1 (import graph)**: any time editing pain comes up, or any time you've added ≥ 3 files / ~1000 LOC to a project. ~5 minutes of work.
- **Tier 3b (god-module zoom)**: any time tier 1 flags a file ≥ 800 LOC. ~30 minutes of work.
- **Tier 3a (per-theorem build-up)**: before paper submission, or as a code-quality review. ~1 hour per theorem.

**The minimal workflow (editing-pain triage):**

```
tier 1  →  (god-module detected?)  →  tier 3b  →  split file  →  re-run tier 1
```

Tier 3a is an *optional* separate pass — it catches different things (dead lemmas, unused hypotheses) than what affects editing pain.

---

## Tier 1 — import graph

**Goal:** file-level structural view. One node per `.lean` file; edges are intra-project imports. Surfaces god-modules, depth, fan-in concentration, orphans.

**Procedure (from project root, e.g. `jepa-learning-order/`):**

```bash
# 1. List source files + LOC (excluding build/results)
find . -name "*.lean" \
  -not -path "*/.lake/*" -not -path "*/lake-packages/*" \
  -not -path "*/results/*" -not -path "*/.aristotle-results/*" \
  -not -path "*/.claude/*" -not -path "*/.lean-packages/*" \
  -exec wc -l {} + | sort -rn

# 2. Extract intra-project imports (drops Mathlib)
for f in JepaLearningOrder.lean JepaLearningOrder/*.lean; do
  echo "=== $f ==="
  grep "^import " "$f" 2>/dev/null | grep -v "^import Mathlib"
done

# 3. Fan-in per file: how many other files import each one
# (do this by reading the output of step 2 — manual tally is fast for ≤ 20 files)
```

Compose by hand into a DOT file using the [encoding](#tier-1-encoding) and render:

```bash
dot -Tsvg foo.dot -o foo.svg
dot -Tpng -Gdpi=140 foo.dot -o foo.png
```

Stash under `wiki/audits/<project>/<project>_import_tier1.{dot,svg,png}`.

### Tier 1 encoding

| Channel | Meaning |
|---|---|
| Node size | ∝ LOC |
| Border thickness | ∝ fan-in (downstream invalidation cost) |
| Fill — red `#f4cccc` | God-module (LOC ≥ 800) |
| Fill — blue `#cfe2f3` | Foundation (fan-in ≥ 5) |
| Fill — yellow `#fff2cc` | Synthesis (headline file pulling many siblings) |
| Fill — gray `#efefef` | Helper (single-cluster extracted lemmas) |
| Dashed border | Orphan or stub (verify intent before acting) |
| Layout | `rankdir=BT`, foundations at top, terminals at bottom, exclude umbrella file |

The legend block we use is at the bottom of each [`tier1` DOT file](audits/stochastic-search-bounds/stochastic-search-bounds_import_tier1.dot) — copy-paste as a template.

### Tier 1 reading order

1. **Are any nodes red?** That's a god-module. Tier 3b time.
2. **Are border thicknesses concentrated on one or two nodes?** Those are your fan-in hubs. Editing them invalidates the world — keep them small and stable.
3. **Any dashed nodes?** Check the session log before acting — orphans are often intentional (staged future work, deprecation siblings).
4. **What's the depth?** Long chains (≥ 5 levels) cascade rebuilds. SSB has depth 3 (target), JEPA-LO has depth 5.

---

## Tier 3b — god-module zoom

**Goal:** when a single file is too large, find the natural sub-clusters within it to inform splitting.

**Procedure** (uses Python regex for the mechanical parsing — copy-paste):

```python
# Run from project root. Adjust the path to the god-module file.
import re
from collections import defaultdict

path = "JepaLearningOrder/JEPA.lean"  # ← change me
with open(path) as f:
    lines = f.readlines()

decl_re = re.compile(
    r"^(theorem|lemma|noncomputable\s+def|private\s+lemma|private\s+theorem|private\s+def|"
    r"def|structure|class|abbrev|instance)\s+([A-Za-z_][A-Za-z_0-9'.]*)"
)
decls = []
for i, line in enumerate(lines, 1):
    m = decl_re.match(line)
    if m:
        decls.append((i, m.group(1), m.group(2)))

ranges = []
for idx, (lineno, kind, name) in enumerate(decls):
    end = decls[idx + 1][0] - 1 if idx + 1 < len(decls) else len(lines)
    ranges.append((name, lineno, end))

ordered_names = sorted([r[0] for r in ranges], key=len, reverse=True)
edges = []
for name, lo, hi in ranges:
    # IMPORTANT: include the keyword line — Lean signatures like `(dat : JEPAData d)`
    # often live on the same line as the declaration keyword.
    body = "\n".join(lines[lo - 1:hi])
    for target in ordered_names:
        if target == name:
            continue
        if re.search(r"\b" + re.escape(target) + r"\b", body):
            edges.append((name, target))

# Print the table — line ranges, fan-in, fan-out
out_deg = defaultdict(int); in_deg = defaultdict(int)
for s, t in edges:
    out_deg[s] += 1; in_deg[t] += 1
for name, lo, hi in ranges:
    print(f"{name:45s} {lo:>5}-{hi:<5} uses={out_deg[name]:>3} used_by={in_deg[name]:>3}")
print(f"\nTotal: {len(ranges)} decls, {len(edges)} intra-file edges")
```

Then **assign clusters by hand**. Look for:
- **Topical name patterns** (e.g. `bernoulli_*`, `frozen_*`, `actual_critical_time_*`).
- **Line-range contiguity** (declarations that live near each other often belong together).
- **High-in-degree foundation nodes** (these define the universal vocabulary — usually their own "Core" cluster).
- **Densely-connected subgraphs** (count edges between candidate clusters; ≥ 8 edges between two candidates means **merge them**).

> **Lesson learned (the hard way):** automated community detection (greedy modularity) is *worse* than judgment-driven clustering at our scale. The algorithm optimizes intra/inter edge ratio without caring about cluster size, topical readability, or split-target LOC. Use the data to inform your judgment; don't outsource the judgment.

Once clusters are assigned, build the [cluster-summary DOT](audits/jepa-learning-order/jepa_cluster_summary.dot) by hand. Edge weights are cross-cluster edge counts (one number per cluster pair) — compute with:

```python
# Continuing from the snippet above
clusters = {  # ← your manual assignment
    "Core": ["matFrobNorm", "JEPAData", ...],
    "QuasiStatic": [...],
    # ...
}
name2c = {n: c for c, names in clusters.items() for n in names}
inter = defaultdict(int); intra = 0
for s, t in edges:
    cs, ct = name2c[s], name2c[t]
    if cs == ct: intra += 1
    else: inter[(cs, ct)] += 1
print(f"Intra: {intra}, Inter: {sum(inter.values())}")
for (cs, ct), n in sorted(inter.items(), key=lambda x: -x[1]):
    print(f"  {cs} -> {ct}: {n}")
```

### Tier 3b encoding (cluster summary)

| Channel | Meaning |
|---|---|
| Node size | ∝ LOC of the proposed split file |
| Node thick border | Foundation cluster (most pointed-into) or headline-bearing cluster |
| Edge thickness | ∝ # cross-cluster math edges |
| Edge — blue `#7ba6c9` | Pointing into foundation (expected) |
| Edge — dark gray | Non-foundation coupling (the "real" signal) |
| Edge — dashed | Single-edge link (probably proof-incidental, not structural) |

### Tier 3b reading order

1. **Identify the foundation cluster** — should hold defs + heavy fan-in, ideally < 200 LOC.
2. **Look at edge thicknesses between non-foundation clusters.** Any pair with ≥ 8 edges between them should probably **stay in one file** — splitting them creates avoidable import noise.
3. **Check cluster sizes against the 400-LOC target.** Clusters ≥ 500 LOC might need further splitting (rare but possible).
4. **Read the headline-bearing cluster (the one with the main theorem) last.** It often stays larger than ideal because the proof itself is long — that's not a god-module problem, that's a proof-length problem, and splitting can't fix it.

---

## Caveat — structure ≠ intent

The audit surfaces structural *facts* (god-modules, orphans, fan-in hotspots). Whether to *act* on them depends on intent:

- **Staged future work** (e.g. `Concentration.lean` in rho-recovery — orphan by design, holds an axiom for paper-3).
- **Deprecation policy** (e.g. `Corrected.lean` in both JEPA projects — over the 800-LOC threshold but intentional: corrected siblings live alongside `@[deprecated]` originals to avoid breaking import chains).
- **Archived wrong variants** (e.g. `jepa_bernoulli_solution_WRONG` — kept as a teaching artifact, not to be acted on).

**Always read `wiki/session-log.md` before acting on a tier-1 or tier-3b finding.** A red node may be a deliberate choice the structural view can't see.

---

## Worked examples

| Project | Tier 1 | Tier 3a | Tier 3b | Action |
|---|---|---|---|---|
| [stochastic-search-bounds](audits/stochastic-search-bounds/) | ✓ Reference shape | ✓ All 4 theorems | n/a (no god-modules) | None needed at file level; tier 3a found 4 dead lemmas + unused hyp + 4 unjustified imports for paper-submission cleanup |
| [jepa-rho-recovery](audits/jepa-rho-recovery/) | ✓ Intermediate | not run | n/a (largest 798 LOC just under threshold) | None at file level |
| [jepa-learning-order](audits/jepa-learning-order/) | ⚠ `JEPA.lean` 2002 LOC | not run | ✓ 8-cluster manual partition | **Split `JEPA.lean`** into 6 files per the recommendation; merge FrobeniusHelpers + EncoderConvergence (11-edge bond) |

---

## What we tried that didn't work

- **Lemma-level math graph for the whole project (tier 3 v1).** Drawn as one big diagram with per-file clusters: too many nodes (47+ in JEPA-LO), no readable signal beyond what tier 1 already showed at file level. Tier 3a (per-theorem) and tier 3b (per-god-module) are the right granularities.
- **Automated tier 3b clustering** via NetworkX `greedy_modularity_communities`: technically more modular than hand-clustering, but produces unbalanced clusters (one giant 19-decl bucket + several singletons) that aren't actionable for splitting. The 30 minutes of human judgment beats an hour of script debugging at our scale.
- **A maintained `graph_audit.py` script.** Built, validated against all 3 projects, then deleted — the script saved ~15 min/project but added maintenance overhead and produced worse tier-3b clustering than judgment. Replaced by this strategy doc + inline snippets.

If our scale changes (≥ 10 projects, monthly audit cadence), revisit. For 3-4 projects audited a few times a year, written protocol beats code.
