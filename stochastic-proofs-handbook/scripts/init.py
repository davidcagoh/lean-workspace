#!/usr/bin/env python3
"""Scaffold a new Lean proof project as a subdirectory of this workspace.

Usage (run from the workspace root, lean-projects/):
    python scripts/init.py MyTheoremName

Creates:
    my-theorem-name/
    ├── .env                  (template — add ARISTOTLE_API_KEY)
    ├── .gitignore
    ├── lakefile.toml
    ├── lean-toolchain
    ├── lake-manifest.json    (copied from a sibling project)
    ├── MyTheoremName.lean    (entry point)
    └── MyTheoremName/
        └── Basic.lean

Gitignored dirs are created but not committed:
    my_theorems/  results/  reports/  help_from_aristotle/

After running this, cd into the project and add your API key:
    echo "ARISTOTLE_API_KEY=arstl_..." >> my-theorem-name/.env
"""

import pathlib
import re
import shutil
import sys


def to_kebab(name: str) -> str:
    """CamelCase -> kebab-case (e.g. MyTheoremName -> my-theorem-name)."""
    s = re.sub(r'([A-Z])', r'-\1', name).lstrip('-').lower()
    return s


def find_manifest() -> pathlib.Path | None:
    """Return a lake-manifest.json to copy — bundled template first, then a sibling project."""
    bundled = pathlib.Path(__file__).parent / "_template_manifest.json"
    if bundled.exists():
        return bundled
    workspace = pathlib.Path(".")
    for sibling in sorted(workspace.iterdir()):
        if not sibling.is_dir() or sibling.name.startswith('.') or sibling.name == 'scripts':
            continue
        manifest = sibling / "lake-manifest.json"
        if manifest.exists():
            return manifest
    return None


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    lib_name = sys.argv[1]
    if not re.match(r'^[A-Z][A-Za-z0-9]*$', lib_name):
        print(f"Error: ProjectName must be CamelCase starting with a capital letter (got: {lib_name!r})")
        sys.exit(1)

    dir_name = to_kebab(lib_name)
    project_dir = pathlib.Path(dir_name)

    if project_dir.exists():
        print(f"Error: {project_dir} already exists.")
        sys.exit(1)

    print(f"Scaffolding {lib_name} → {project_dir}/")

    # ── Directory structure ───────────────────────────────────────────────────
    (project_dir / lib_name).mkdir(parents=True)
    for d in ("my_theorems", "results", "reports", "help_from_aristotle"):
        (project_dir / d).mkdir()

    # ── .env template ─────────────────────────────────────────────────────────
    (project_dir / ".env").write_text("ARISTOTLE_API_KEY=arstl_...\n")

    # ── .gitignore ────────────────────────────────────────────────────────────
    (project_dir / ".gitignore").write_text(
        "/.lake\n"
        ".env\n"
        "aristotle-docs.md\n"
        "memory/\n"
        "proofs-from-literature/\n"
        ".DS_Store\n"
        "**/.DS_Store\n"
        ".claude/settings.local.json\n"
        "results/\n"
        "my_theorems/\n"
        "reports/\n"
        "help_from_aristotle/\n"
    )

    # ── lean-toolchain ────────────────────────────────────────────────────────
    (project_dir / "lean-toolchain").write_text("leanprover/lean4:v4.28.0\n")

    # ── lakefile.toml ─────────────────────────────────────────────────────────
    (project_dir / "lakefile.toml").write_text(
        f'name = "{dir_name}"\n'
        f'version = "0.1.0"\n'
        f'keywords = ["math"]\n'
        f'defaultTargets = ["{lib_name}"]\n'
        f'packagesDir = "../.lean-packages"\n'
        f'\n'
        f'[leanOptions]\n'
        f'pp.unicode.fun = true # pretty-prints `fun a ↦ b`\n'
        f'relaxedAutoImplicit = false\n'
        f'weak.linter.mathlibStandardSet = true\n'
        f'maxSynthPendingDepth = 3\n'
        f'\n'
        f'[[require]]\n'
        f'name = "mathlib"\n'
        f'scope = "leanprover-community"\n'
        f'rev = "v4.28.0"\n'
        f'git = "https://github.com/leanprover-community/mathlib4.git"\n'
        f'\n'
        f'[[lean_lib]]\n'
        f'name = "{lib_name}"\n'
    )

    # ── lake-manifest.json (copy from sibling) ────────────────────────────────
    manifest_src = find_manifest()
    if manifest_src:
        shutil.copy(manifest_src, project_dir / "lake-manifest.json")
        print(f"  Copied lake-manifest.json from {manifest_src.parent.name}/")
    else:
        print("  (no sibling manifest found — run `lake build` to generate lake-manifest.json)")

    # ── Entry point .lean ─────────────────────────────────────────────────────
    (project_dir / f"{lib_name}.lean").write_text(
        f"import {lib_name}.Basic\n"
        f"-- import {lib_name}.<TheoremName>  -- add theorem files here in dependency order\n"
    )

    # ── Basic.lean placeholder ────────────────────────────────────────────────
    (project_dir / lib_name / "Basic.lean").write_text(
        f"import Mathlib\n"
        f"\n"
        f"/-! # {lib_name}\n"
        f"\n"
        f"Add definitions and theorems here.\n"
        f"-/\n"
    )

    print(f"\nDone. Next steps:")
    print(f"  1. cd {project_dir}")
    print(f"  2. echo 'ARISTOTLE_API_KEY=arstl_...' > .env")
    print(f"  3. Place your paper in my_theorems/")
    print(f"  4. Use /new-theorem to scaffold the Lean skeleton and submit")


main()
