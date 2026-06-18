"""Shared helpers for the example scripts.

Keeps the export logic in one place so every example obeys the project rules:
STEP by default, no silent fallbacks (failures raise), and the output directory
is read from ``settings.yml``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import cadquery as cq
import yaml

# Repo root is the parent of the examples/ directory this file lives in.
REPO_ROOT = Path(__file__).resolve().parents[1]
SETTINGS_PATH = REPO_ROOT / "settings.yml"


def load_settings(section: str | None = None) -> dict[str, Any]:
    """Load settings.yml, optionally returning a named section."""
    if not SETTINGS_PATH.exists():
        raise RuntimeError(f"Missing settings file: {SETTINGS_PATH}")

    with SETTINGS_PATH.open("r", encoding="utf-8") as stream:
        settings = yaml.safe_load(stream)

    if not isinstance(settings, dict):
        raise RuntimeError(f"Settings file must contain a mapping: {SETTINGS_PATH}")

    if section is None:
        return settings

    try:
        selected = settings[section]
    except KeyError as exc:
        raise RuntimeError(
            f"Missing settings section '{section}' in {SETTINGS_PATH}"
        ) from exc

    if not isinstance(selected, dict):
        raise RuntimeError(
            f"Settings section '{section}' must contain a mapping"
        )
    return selected


def output_path(filename: str) -> Path:
    """Return an absolute path inside output/, creating the directory."""
    settings = load_settings()
    try:
        output_dir = Path(settings["output_dir"])
    except KeyError as exc:
        raise RuntimeError(f"Missing 'output_dir' in {SETTINGS_PATH}") from exc

    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / filename


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
