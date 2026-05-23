#!/usr/bin/env python3
"""
Extract SimplicialDetection.lean's 132 declarations into a 15-file split tree.
Non-contiguous: clusters are interleaved in the source, so we extract by name.
"""
import re
import os
from collections import defaultdict

ROOT = "/Users/davidgoh/LocalFiles/lean-workspace/simplicial-latent-geometry"
SRC = "/tmp/SimplicialDetection_original.lean"
OUT_BASE = f"{ROOT}/SimplicialLatentGeometry/Detection"

with open(SRC) as f:
    lines = f.readlines()

# --- Step 1: find all decl heads ---
decl_re = re.compile(
    r"^(theorem|lemma|noncomputable\s+def|private\s+noncomputable\s+def|"
    r"private\s+lemma|private\s+theorem|private\s+def|"
    r"def|structure|class|abbrev|instance)\s+([A-Za-z_][A-Za-z_0-9'.]*)"
)
decl_starts = []  # list of (lineno_1indexed, name)
for i, line in enumerate(lines, 1):
    m = decl_re.match(line)
    if m:
        decl_starts.append((i, m.group(2)))

# --- Step 2: compute "effective start" for each decl
# (scan backwards to include preceding doc comments + attributes + blank lines) ---
def effective_start(idx):
    """idx: index into decl_starts. Returns effective_start lineno (1-indexed)."""
    decl_lineno = decl_starts[idx][0]
    prev_end = decl_starts[idx-1][0] if idx > 0 else 0  # 1-indexed; 0 means top of file
    i = decl_lineno - 1  # line above the decl, 1-indexed
    while i > prev_end:
        s = lines[i-1].rstrip()
        st = s.strip()
        if st == "":
            i -= 1; continue
        if st.startswith("@["):
            i -= 1; continue
        if st.startswith("--"):
            i -= 1; continue
        # `open X in` (one-shot open scoped to the next decl) — belongs to THIS decl
        if st.startswith("open ") and st.endswith(" in"):
            i -= 1; continue
        # `set_option ... in` (one-shot) — same logic
        if st.startswith("set_option ") and st.endswith(" in"):
            i -= 1; continue
        # Multi-line /- ... -/ doc block: line ends with -/
        if st.endswith("-/"):
            if st.startswith("/-"):
                i -= 1; continue
            j = i - 1
            while j > prev_end:
                inner = lines[j-1].strip()
                if inner.startswith("/-"):
                    i = j - 1
                    break
                j -= 1
            else:
                break
            continue
        if st.startswith("/-"):
            i -= 1; continue
        break
    return i + 1

eff_starts = [effective_start(i) for i in range(len(decl_starts))]

# --- Step 3: compute end of each decl (line before next decl's eff_start) ---
ranges_by_name = {}
for i, (lineno, name) in enumerate(decl_starts):
    es = eff_starts[i]
    end = eff_starts[i+1] - 1 if i + 1 < len(decl_starts) else len(lines)
    ranges_by_name[name] = (es, end)

# --- Step 4: cluster map (with the IntegralsAndMoments merge applied) ---
clusters = {
    "Core/Types": [
        "Torus", "CechSample", "CechSample.hasEdge", "CechSample.hasFill",
        "euclidBallVol", "matchRadius",
        "volumeEmpty", "volumeFill", "fillingProb",
        "matchRadius_spec", "matchRadius_lt_half", "matchRadius_pos'",
        "torus_dist_le_half",
        "fillingProb_nonneg", "fillingProb_nonneg'", "fillingProb_le_one", "fillingProb_le_one'",
        "expectedFillVol", "expectedEmptyVol",
        # Forward-ref workaround helper used by fillingProb_*' (Core/Types) and
        # downstream Chebyshev/PaleyZygmund — promoted into Core/Types since it
        # is the natural foundation home.
        "torus_pi_measure_real_univ'",
    ],
    "Core/MeasureScaffold": [
        "cechFilledCount", "cechMeasure", "cechSignedCount", "signedFilledCount",
        "cechObservation",
        "cechMeasure_isProbabilityMeasure",
        "measurableSet_cechSample_hasFill", "cechObservation_measurable",
        "cechFilledCount_integrable", "cechDoublySignedCount",
        "cechEquiv", "cech_integral_eq",
        "doublySignedTriangle_sq_le_one",
        "doublySignedFilledCount_cechObservation",
        "cechPushforward_isProbabilityMeasure",
        "moments_twoParam_mean",
    ],
    "Core/BetaIncomplete": [
        "incBeta_nonneg", "incBeta_mono",
        "incBeta_nonneg'", "incBeta_mono'",
        "volumeFill_div_volumeEmpty_le_one_ge2", "volumeFill_div_volumeEmpty_le_one_d0",
        "volumeFill_div_volumeEmpty_le_one", "beta_density_integral_le_one",
        "volumeFill_div_volumeEmpty_le_one_ge2'", "volumeFill_div_volumeEmpty_le_one'",
        "volumeFill_div_le_one'", "beta_density_integral_le_one'",
        "beta_density_integral",
    ],
    "DeepRegime/IntegralsAndMoments": [
        # Merged: DeepIntegrals + DeepCentered (16-edge bond)
        "wedge_implies_fill", "gamma_pow_eq", "mu_e_pow_eq",
        "fillingProb_eq_low_r",
        "edge_integral", "wedge_integral", "p_sq_mu_eq",
        "edge_integral_02", "edge_integral_12",
        "wedge_integral_1center", "wedge_integral_2center",
        "mu_e_pow_eq_02", "mu_e_pow_eq_12",
        "centered_edge_moment", "integrand_fill_rewrite", "centered_edge_moment_fill",
    ],
    "DeepRegime/GeometricCov": [
        "geometricCov", "geometricCov_eq_deep", "geometricCov_eq_deep_OLD",
        "geometricCov_decay_rate_le", "doubleFill_joint_prob",
        "cechDoublySigned_triangle_integral", "cechDoublySigned_summand_integrable",
        "moments_cech_signed",
    ],
    "MidRegime/Scaffold": [
        "matchRadius_tendsto_half", "fillingProb_eq_mid_r",
        "matchRadius_eventually_mid", "gammaMid_matchRadius_pow_tendsto_pcubed",
        "fillingProb_tendsto_pcubed", "edgeProduct_integral_bounded'",
    ],
    "MidRegime/FreeIntegrals": [
        "edgeSet01", "wedgeSet01",
        "volume_edgeSet01", "edgeSet01_measurable", "edgeSet01_torus_eq",
        "edge_integral_free", "edge_integral_02_free", "edge_integral_12_free",
        "volume_wedgeSet01", "wedgeSet01_measurable", "wedgeSet01_torus_eq",
        "wedge_integral_free", "wedge_integral_1center_free", "wedge_integral_2center_free",
        "centered_edge_moment_fill_free", "centered_edge_moment_free",
    ],
    "MidRegime/GeomCovFree": [
        "geometricCov_eq",
        "geometricCov_sub_closedForm_tendsto_zero", "geometricCov_tendsto_pcubed_compcubed",
    ],
    "Independence/TriangleIndicators": [
        "triangleIndicator'",  # the def itself
        "triangleIndicator'_measurable", "triangleIndicator'_translate",
        "triangleIndicator'_congr",
        "integral_over_nu_eq'", "single_triangle_integral_eq_g'",
        "triangleIndicator'_factor_coord_diffs",
        "triangleIndicator'_bound'",
    ],
    "Independence/VertexIndep": [
        "shear_measurePreserving_vertex", "indepFun_proj_pairs_vertex",
        "indepFun_comp_measurePreserving_vertex", "indepFun_coord_diffs_vertex",
        "extract_vertices_of_card_inter_one",
        "vertex_sharing_indepFun'",
    ],
    "Independence/EdgeSharing": [
        "edge_sharing_integral_eq'", "edge_sharing_integral_factoring'",
        "doublySignedTriangle_cov_vertex_sharing_zero",
        "doublySignedTriangle_cov_edge_sharing_le_sq",
        "disjoint_triangles_indepFun",
        "doublySignedTriangle_cov_disjoint_eq_gsq",
    ],
    "PhaseTransition/SecondMoment": [
        "cech_second_moment_structured", "cech_mean_eq", "cech_second_moment_bound",
        "doublySignedFilledCount_memLp",
    ],
    "PhaseTransition/PaleyZygmund": [
        "cech_complement_set_inclusion", "cech_complement_prob_bound",
        "paleyZygmund_cech_prob_tendsto_one",
    ],
    "PhaseTransition/Chebyshev": [
        "chebyshev_single_bound", "choose3_g_sq_tendsto_atTop",
        "chebyshev_2PC_prob_tendsto_zero",
    ],
    "PhaseTransition/Headline": [
        "detection_lower_bound", "detection_lower_bound_fixed_d",
        "derive_hSNR", "derive_hNG", "phase_transition",
    ],
}

# Validate
all_assigned = [n for ns in clusters.values() for n in ns]
unassigned = set(ranges_by_name.keys()) - set(all_assigned)
dupes = [n for n in all_assigned if all_assigned.count(n) > 1]
assert not unassigned, f"Unassigned: {sorted(unassigned)}"
assert not dupes, f"Duplicates: {sorted(set(dupes))}"

# --- Step 5: import map per file ---
# Each file imports the original 5 imports + sibling sub-modules it needs.
# Compute sub-module deps from edges (cross-cluster usage).
def strip_comments(text):
    """Remove -- line comments and /- ... -/ block comments (including /-- ... -/)."""
    # Block comments (greedy DOTALL match for /- ... -/, including nested levels naively)
    out = []
    i = 0
    n = len(text)
    depth = 0
    while i < n:
        if depth == 0 and text[i:i+2] == "/-":
            depth = 1; i += 2; continue
        if depth > 0:
            if text[i:i+2] == "/-":
                depth += 1; i += 2; continue
            if text[i:i+2] == "-/":
                depth -= 1; i += 2; continue
            i += 1; continue
        if text[i:i+2] == "--":
            # line comment to EOL
            j = text.find("\n", i)
            if j == -1:
                i = n
            else:
                out.append("\n"); i = j + 1
            continue
        out.append(text[i]); i += 1
    return "".join(out)

ordered_names = sorted(ranges_by_name.keys(), key=len, reverse=True)
edges = []
def name_re(n):
    # Boundary BEFORE: not preceded by word char or apostrophe.
    # Boundary AFTER: not followed by word char or apostrophe (covers `foo'` ending).
    return r"(?<![A-Za-z0-9_'])" + re.escape(n) + r"(?![A-Za-z0-9_'])"
for name, (lo, hi) in ranges_by_name.items():
    body = strip_comments("".join(lines[lo - 1:hi]))
    for target in ordered_names:
        if target == name: continue
        if re.search(name_re(target), body):
            edges.append((name, target))

name2c = {n: c for c, names in clusters.items() for n in names}
cluster_deps = defaultdict(set)  # cluster -> set of clusters it depends on
for s, t in edges:
    cs, ct = name2c[s], name2c[t]
    if cs != ct:
        cluster_deps[cs].add(ct)

# Convert cluster name "Core/Types" to module name "SimplicialLatentGeometry.Detection.Core.Types"
def cluster_to_module(c):
    return "SimplicialLatentGeometry.Detection." + c.replace("/", ".")

# --- Step 6: write each file ---
base_imports = """import Mathlib
import SimplicialLatentGeometry.Core.Statistic
import SimplicialLatentGeometry.Core.Detection
import SimplicialLatentGeometry.DisjointTriangles
import SimplicialLatentGeometry.TorusIntegrals"""

base_options = """set_option linter.style.longLine false
set_option linter.style.whitespace false"""

namespace_open = """open MeasureTheory ENNReal Finset Real Set"""

os.makedirs(OUT_BASE, exist_ok=True)

cluster_loc = {}
for cname, names in clusters.items():
    out_path = f"{OUT_BASE}/{cname}.lean"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Compose imports
    sibling_imports = sorted(cluster_to_module(d) for d in cluster_deps[cname])
    imports = base_imports
    if sibling_imports:
        imports += "\n" + "\n".join(f"import {m}" for m in sibling_imports)

    # Sort decls by original source line order
    decls_in_cluster = sorted(names, key=lambda n: ranges_by_name[n][0])

    # Extract bodies
    body_chunks = []
    for name in decls_in_cluster:
        lo, hi = ranges_by_name[name]
        chunk = "".join(lines[lo - 1:hi])
        # Drop `private` modifier so cross-file references resolve.
        # (These decls were originally private as file-internal helpers; with the
        #  split they need package-level visibility.)
        chunk = re.sub(r"^(\s*)private\s+", r"\1", chunk, flags=re.MULTILINE)
        if not chunk.endswith("\n"):
            chunk += "\n"
        body_chunks.append(chunk)

    header_doc = f"""/-!
# `SimplicialLatentGeometry.Detection.{cname.replace('/', '.')}`

Extracted from `SimplicialDetection.lean` during the session-96 god-module split
(see `audits/simplicial-latent-geometry/README.md` and
`audits/REPORT-2026-05-23-simplicial-split.md`).
-/"""

    out = "\n\n".join([imports, base_options, header_doc, namespace_open, *body_chunks])
    if not out.endswith("\n"):
        out += "\n"

    with open(out_path, "w") as f:
        f.write(out)

    cluster_loc[cname] = out.count("\n") + 1
    print(f"Wrote {out_path}: {cluster_loc[cname]} LOC ({len(decls_in_cluster)} decls)")

print(f"\nTotal LOC written: {sum(cluster_loc.values())}")
print(f"Original SimplicialDetection.lean: {len(lines)} LOC")
