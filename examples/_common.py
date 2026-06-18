"""Shared helpers for the example scripts.

Keeps the export logic in one place so every example obeys the project rules:
STEP by default, no silent fallbacks (failures raise), and output always lands
in the repo-level ``output/`` directory regardless of the current working
directory.
"""

from __future__ import annotations

from pathlib import Path

import cadquery as cq

# Repo root is the parent of the examples/ directory this file lives in.
REPO_ROOT = Path("D:/CAD/llm_cad")
OUTPUT_DIR = REPO_ROOT / "output"


def output_path(filename: str) -> Path:
    """Return an absolute path inside output/, creating the directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUTPUT_DIR / filename


def export(obj, basename: str, *, step: bool = True, stl: bool = False,
           iges: bool = False) -> list[Path]:
    """Export a CadQuery object to the requested formats.

    STEP is exported by default. Any failure raises explicitly — there are no
    silent fallbacks (see CLAUDE.md). Returns the list of files written.

    ``obj`` may be a Workplane, a Shape/Compound, or an Assembly.
    """
    written: list[Path] = []

    def _do(fmt_name: str, suffix: str, exporttype: str | None) -> None:
        target = output_path(f"{basename}{suffix}")
        try:
            if exporttype is None:
                # Assembly.export infers format from the file extension.
                obj.export(str(target))
            else:
                cq.exporters.export(obj, str(target), exportType=exporttype)
        except Exception as exc:  # noqa: BLE001 - re-raise explicitly, no fallback
            raise RuntimeError(
                f"{fmt_name} export failed for {target}: {exc}"
            ) from exc
        if not target.exists() or target.stat().st_size == 0:
            raise RuntimeError(
                f"{fmt_name} export produced no usable file at {target}"
            )
        written.append(target)
        print(f"  wrote {target}  ({target.stat().st_size} bytes)")

    is_assembly = isinstance(obj, cq.Assembly)

    if step:
        _do("STEP", ".step", None if is_assembly else "STEP")
    if iges:
        if is_assembly:
            raise RuntimeError("IGES export is not supported for assemblies")
        _do("IGES", ".igs", "IGES")
    if stl:
        if is_assembly:
            raise RuntimeError("STL export is not supported for assemblies")
        _do("STL", ".stl", "STL")

    if not written:
        raise RuntimeError("export() called with no formats enabled")
    return written
