"""02 - L-shaped mounting bracket.

An L-bracket built from two flanges joined at a right angle:

  - base (horizontal) flange with two mounting holes
  - vertical flange with one mounting hole
  - a fillet on the inner corner where the two flanges meet

Exports to STEP.

Run standalone:

    python examples/02_bracket.py

All dimensions are in millimetres.
"""

from __future__ import annotations

import cadquery as cq

try:
    from _common import export
except ModuleNotFoundError:  # pragma: no cover
    from examples._common import export

# --- Parameters (mm) -------------------------------------------------------
LENGTH = 80.0        # extent of both flanges along the shared (Y) axis
BASE_DEPTH = 60.0     # how far the base flange reaches in X
WALL_HEIGHT = 50.0    # how tall the vertical flange is in Z
THICKNESS = 6.0       # material thickness of both flanges
HOLE_DIA = 6.5        # mounting hole diameter (M6 clearance)
INNER_FILLET = 5.0    # fillet radius on the inner corner


def build_bracket() -> cq.Workplane:
    """Build the L-shaped bracket as a single solid.

    Geometry (all in the first octant of X/Z, centred in Y):
      - base flange:  x in [0, BASE_DEPTH],  z in [0, THICKNESS]
      - wall flange:  x in [0, THICKNESS],   z in [0, WALL_HEIGHT]
    The two share the corner column x in [0, THICKNESS], z in [0, THICKNESS],
    so their union is a clean L. Holes are drilled per-flange before the union
    (simpler, robust face selection), then the inner concave corner is filleted.
    """
    # Base flange with its two mounting holes, drilled down through the top.
    base = cq.Workplane("XY").box(
        BASE_DEPTH, LENGTH, THICKNESS, centered=(False, True, False)
    )
    base = (
        base.faces(">Z")
        .workplane(origin=(0, 0, 0))
        .pushPoints([(BASE_DEPTH * 0.65, LENGTH * 0.28),
                     (BASE_DEPTH * 0.65, -LENGTH * 0.28)])
        .hole(HOLE_DIA)
    )

    # Wall flange with its single mounting hole, drilled through in X.
    wall = cq.Workplane("XY").box(
        THICKNESS, LENGTH, WALL_HEIGHT, centered=(False, True, False)
    )
    wall = (
        wall.faces("<X")
        .workplane(origin=(0, 0, 0))
        # Local axes on the -X face: x->-Y(world), y->+Z(world). Place the hole
        # high on the wall, clear of the base and the corner fillet.
        .pushPoints([(0, WALL_HEIGHT * 0.70)])
        .hole(HOLE_DIA)
    )

    bracket = base.union(wall)

    # Fillet the inner concave corner: the edge running along Y at the junction
    # of the base top (z == THICKNESS) and the wall inner face (x == THICKNESS).
    bracket = (
        bracket.edges("|Y")
        .edges(cq.NearestToPointSelector((THICKNESS, 0.0, THICKNESS)))
        .fillet(INNER_FILLET)
    )

    return bracket


def main() -> None:
    print("Building L-shaped mounting bracket")
    bracket = build_bracket()
    export(bracket, "bracket", step=True)
    print("Done.")


if __name__ == "__main__":
    main()
