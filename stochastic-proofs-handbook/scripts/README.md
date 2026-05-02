# Shared Scripts

This directory is the canonical shared script layer for the Lean workspace.

The repository-local `scripts/` folders remain the safest entry points when you are already inside a specific project repository. The workspace-level `scripts/` path is preserved as a compatibility entry point and resolves to this directory.

If you are working from a repository subfolder, prefer that repository's local `scripts/` folder unless you are intentionally updating the shared workflow.

## Scripts

### Proof submission (Aristotle)

| Script | Purpose |
|---|---|
| `submit.py` | Submit a Lean proof job to Aristotle. |
| `status.py` | Check job status. |
| `retrieve.py` | Pull completed proof and patch into the repo. |
| `watch.py` | Poll a running job. |
| `init.py` | Bootstrap a new project's Aristotle config. |
| `_common.py`, `_report.py`, `_template_manifest.json` | Shared helpers. |

### Paper writing (bibliography tooling)

These operate on a `.bib` file and are unrelated to proof generation. They expect `SEMANTIC_SCHOLAR_API_KEY` in the workspace-root `.env` (or environment).

| Script | Purpose |
|---|---|
| `verify_refs.py` | Check every `.bib` entry against Semantic Scholar. Classifies as VERIFIED / LIKELY / UNCERTAIN / NOT_FOUND and writes `verification_report.md` next to the `.bib`. Usage: `python verify_refs.py path/to/references.bib`. Deps: `bibtexparser httpx python-dotenv`. |
| `forward_cites.py` | For each entry in a `.bib`, fetch papers that cite it via Semantic Scholar, rank by recency + venue, and emit `forward_cites_report.md` + `forward_cites_edges.csv`. Used to surface recent forward citations worth integrating into related-work sections. |
