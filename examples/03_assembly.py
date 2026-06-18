"""03 - Minimal two-part assembly: a bolt through a plate.

Demonstrates CadQuery's Assembly API by positioning two independently built
solids (a plate with a clearance hole, and a simple bolt) into one assembly,
then exporting the whole assembly to STEP.

Run standalone:

    python examples/03_assembly.py

All dimensions are in millimetres.
"""

from __future__ import annotations

import cadquery as cq

try:
    from _common import export
except ModuleNotFoundError:  # pragma: no cover
    from examples._common import export

# --- Parameters (mm) -------------------------------------------------------
PLATE_L = 60.0
PLATE_W = 40.0
PLATE_T = 8.0
HOLE_DIA = 8.5        # clearance for an M8 bolt

BOLT_DIA = 8.0
SHANK_LEN = 20.0
HEAD_DIA = 13.0
HEAD_T = 6.0


def build_plate() -> cq.Workplane:
    """Flat plate centred on the origin with a central through-hole."""
    return (
        cq.Workplane("XY")
        .box(PLATE_L, PLATE_W, PLATE_T)
        .faces(">Z")
        .workplane()
        .hole(HOLE_DIA)
    )


def build_bolt() -> cq.Workplane:
    """Simple bolt: cylindrical shank with a hex head, built along +Z.

    The shank base sits at z=0 and extends upward; the head sits below z=0.
    """
    shank = cq.Workplane("XY").circle(BOLT_DIA / 2).extrude(SHANK_LEN)
    head = (
        cq.Workplane("XY")
        .polygon(6, HEAD_DIA)
        .extrude(-HEAD_T)
    )
    return shank.union(head)


def build_assembly() -> cq.Assembly:
    """Position the bolt so its shank passes through the plate hole."""
    plate = build_plate()
    bolt = build_bolt()

    asm = cq.Assembly(name="bolt_through_plate")
    asm.add(plate, name="plate", color=cq.Color("gray"))
    # Drop the bolt so its head rests on the top face of the plate and the
    # shank protrudes downward through the hole.
    asm.add(
        bolt,
        name="bolt",
        loc=cq.Location(cq.Vector(0, 0, PLATE_T / 2)),
        color=cq.Color("steelblue"),
    )
    return asm


def main() -> None:
    print("Building bolt-through-plate assembly")
    asm = build_assembly()
    export(asm, "assembly", step=True)
    print("Done.")


if __name__ == "__main__":
    main()
