"""04 - Planar face STEP export.

Creates a zero-thickness rectangular planar face and exports it to STEP.

Run standalone:

    python examples/04_plane.py

All dimensions are in millimetres.
"""

from __future__ import annotations

# Allow running both as `python examples/04_plane.py` and as a module.
try:
    from _common import export, load_settings
    from geometry import PlaneFace
except ModuleNotFoundError:  # pragma: no cover
    from examples._common import export, load_settings
    from examples.geometry import PlaneFace


def main() -> None:
    settings = load_settings("plane")
    model = PlaneFace.from_settings(settings)

    print(f"Building plane {model.length} x {model.width} mm at Z={model.z} mm")
    plane = model.build()
    export(plane, "plane", step=True)
    print("Done.")


if __name__ == "__main__":
    main()
