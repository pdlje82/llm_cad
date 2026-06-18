"""01 - Basic parametric box.

Creates a rectangular box from length / width / height parameters and exports
it to STEP (default) and STL.

Run standalone:

    python examples/01_basic_box.py
    python examples/01_basic_box.py --length 80 --width 40 --height 25

All dimensions are in millimetres.
"""

from __future__ import annotations

import argparse

import cadquery as cq

# Allow running both as `python examples/01_basic_box.py` and as a module.
try:
    from _common import export
except ModuleNotFoundError:  # pragma: no cover
    from examples._common import export


def build_box(length: float, width: float, height: float) -> cq.Workplane:
    """Return a centred box of the given dimensions (mm)."""
    return cq.Workplane("XY").box(length, width, height)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a parametric box.")
    parser.add_argument("--length", type=float, default=60.0, help="X dimension (mm)")
    parser.add_argument("--width", type=float, default=40.0, help="Y dimension (mm)")
    parser.add_argument("--height", type=float, default=20.0, help="Z dimension (mm)")
    args = parser.parse_args()

    print(f"Building box {args.length} x {args.width} x {args.height} mm")
    box = build_box(args.length, args.width, args.height)

    export(box, "basic_box", step=True, stl=True)
    print("Done.")


if __name__ == "__main__":
    main()
