"""01 - Basic parametric box.

Creates a rectangular box from length / width / height parameters and exports
it to STEP (default) and STL.

Run standalone:

    python examples/01_basic_box.py

All dimensions are in millimetres.
"""

from __future__ import annotations

# Allow running both as `python examples/01_basic_box.py` and as a module.
try:
    from _common import export, load_settings
    from geometry import BasicBox
except ModuleNotFoundError:  # pragma: no cover
    from examples._common import export, load_settings
    from examples.geometry import BasicBox


def main() -> None:
    settings = load_settings("basic_box")
    model = BasicBox.from_settings(settings)

    print(f"Building box {model.length} x {model.width} x {model.height} mm")
    box = model.build()
    export(box, "basic_box", step=True, stl=True)
    print("Done.")


if __name__ == "__main__":
    main()
