# CLAUDE.md — llm_cad project constraints

This file defines hard constraints for all geometry-generating code in this
repository. Treat them as non-negotiable unless the user explicitly overrides
them in a request.

## Environment

- All work is scoped to the conda environment `env_llm_cad` (Python 3.11).
- Never install packages globally. Use `conda` (conda-forge) or `pip` *inside*
  the activated environment only.
- `cadquery` is installed via **conda-forge**, never via pip.
- `build123d` is installed via **pip** (it is the secondary/experimental API).

## Geometry & export rules (enforce always)

1. **STEP is the default export format.** Every geometry script must produce a
   `.step` file in `output/`. IGES and STL are optional extras.
2. **No silent fallbacks.** If an export (or any geometry operation) fails, the
   script must raise an explicit exception. Never swallow errors, never write a
   placeholder file, never "best-effort" continue.
3. **Standalone runnable.** Every script under `examples/` must run directly,
   e.g. `python examples/01_basic_box.py`, with no extra setup beyond the
   activated environment.
4. **Output location.** All generated files land in `output/` (gitignored).
   Scripts resolve this path relative to the repo root so they work from any
   CWD.

## API preference

- **CadQuery is the primary API.** Use it for all production examples.
- **build123d is secondary/experimental.** Only use it when a script is
  explicitly exploring build123d features.

## Format notes

- STEP / IGES are B-rep (exact boundary representation) — preferred for CAD
  interchange and for opening in Autodesk Inventor.
- STL is a triangulated mesh — lossy, for visualization / 3D printing only.
