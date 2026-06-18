"""03 - Minimal two-part assembly: a bolt through a plate.

Demonstrates CadQuery's Assembly API by positioning two independently built
solids (a plate with a clearance hole, and a simple bolt) into one assembly,
then exporting the whole assembly to STEP.

Run standalone:

    python examples/03_assembly.py

All dimensions are in millimetres.
"""

from __future__ import annotations

try:
    from _common import export, load_settings
    from geometry import BoltThroughPlateAssembly
except ModuleNotFoundError:  # pragma: no cover
    from examples._common import export, load_settings
    from examples.geometry import BoltThroughPlateAssembly


def main() -> None:
    settings = load_settings("assembly")
    model = BoltThroughPlateAssembly.from_settings(settings)

    print("Building bolt-through-plate assembly")
    asm = model.build()
    export(asm, "assembly", step=True)
    print("Done.")


if __name__ == "__main__":
    main()
