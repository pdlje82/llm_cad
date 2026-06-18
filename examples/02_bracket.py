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

try:
    from _common import export, load_settings
    from geometry import LBracket
except ModuleNotFoundError:  # pragma: no cover
    from examples._common import export, load_settings
    from examples.geometry import LBracket


def main() -> None:
    settings = load_settings("bracket")
    model = LBracket.from_settings(settings)

    print("Building L-shaped mounting bracket")
    bracket = model.build()
    export(bracket, "bracket", step=True)
    print("Done.")


if __name__ == "__main__":
    main()
