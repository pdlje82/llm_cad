"""Reusable CadQuery geometry models for the example scripts."""

from __future__ import annotations

from dataclasses import dataclass

import cadquery as cq


@dataclass(frozen=True)
class BasicBox:
    """Centred rectangular box."""

    length: float
    width: float
    height: float

    @classmethod
    def from_settings(cls, settings: dict[str, float]) -> "BasicBox":
        return cls(
            length=settings["length"],
            width=settings["width"],
            height=settings["height"],
        )

    def build(self) -> cq.Workplane:
        return cq.Workplane("XY").box(self.length, self.width, self.height)


@dataclass(frozen=True)
class LBracket:
    """L-shaped mounting bracket with three clearance holes."""

    length: float
    base_depth: float
    wall_height: float
    thickness: float
    hole_dia: float
    inner_fillet: float

    @classmethod
    def from_settings(cls, settings: dict[str, float]) -> "LBracket":
        return cls(
            length=settings["length"],
            base_depth=settings["base_depth"],
            wall_height=settings["wall_height"],
            thickness=settings["thickness"],
            hole_dia=settings["hole_dia"],
            inner_fillet=settings["inner_fillet"],
        )

    def build(self) -> cq.Workplane:
        # Base flange with its two mounting holes, drilled down through the top.
        base = cq.Workplane("XY").box(
            self.base_depth,
            self.length,
            self.thickness,
            centered=(False, True, False),
        )
        base = (
            base.faces(">Z")
            .workplane(origin=(0, 0, 0))
            .pushPoints(
                [
                    (self.base_depth * 0.65, self.length * 0.28),
                    (self.base_depth * 0.65, -self.length * 0.28),
                ]
            )
            .hole(self.hole_dia)
        )

        # Wall flange with its single mounting hole, drilled through in X.
        wall = cq.Workplane("XY").box(
            self.thickness,
            self.length,
            self.wall_height,
            centered=(False, True, False),
        )
        wall = (
            wall.faces("<X")
            .workplane(origin=(0, 0, 0))
            .pushPoints([(0, self.wall_height * 0.70)])
            .hole(self.hole_dia)
        )

        bracket = base.union(wall)
        return (
            bracket.edges("|Y")
            .edges(cq.NearestToPointSelector((self.thickness, 0.0, self.thickness)))
            .fillet(self.inner_fillet)
        )


@dataclass(frozen=True)
class BoltThroughPlateAssembly:
    """Two-part assembly with a bolt passing through a plate."""

    plate_l: float
    plate_w: float
    plate_t: float
    hole_dia: float
    bolt_dia: float
    shank_len: float
    head_dia: float
    head_t: float

    @classmethod
    def from_settings(
        cls, settings: dict[str, float]
    ) -> "BoltThroughPlateAssembly":
        return cls(
            plate_l=settings["plate_l"],
            plate_w=settings["plate_w"],
            plate_t=settings["plate_t"],
            hole_dia=settings["hole_dia"],
            bolt_dia=settings["bolt_dia"],
            shank_len=settings["shank_len"],
            head_dia=settings["head_dia"],
            head_t=settings["head_t"],
        )

    def build_plate(self) -> cq.Workplane:
        return (
            cq.Workplane("XY")
            .box(self.plate_l, self.plate_w, self.plate_t)
            .faces(">Z")
            .workplane()
            .hole(self.hole_dia)
        )

    def build_bolt(self) -> cq.Workplane:
        shank = cq.Workplane("XY").circle(self.bolt_dia / 2).extrude(self.shank_len)
        head = cq.Workplane("XY").polygon(6, self.head_dia).extrude(-self.head_t)
        return shank.union(head)

    def build(self) -> cq.Assembly:
        asm = cq.Assembly(name="bolt_through_plate")
        asm.add(self.build_plate(), name="plate", color=cq.Color("gray"))
        asm.add(
            self.build_bolt(),
            name="bolt",
            loc=cq.Location(cq.Vector(0, 0, self.plate_t / 2)),
            color=cq.Color("steelblue"),
        )
        return asm


@dataclass(frozen=True)
class PlaneFace:
    """Zero-thickness rectangular planar face."""

    length: float
    width: float
    z: float

    @classmethod
    def from_settings(cls, settings: dict[str, float]) -> "PlaneFace":
        return cls(
            length=settings["length"],
            width=settings["width"],
            z=settings["z"],
        )

    def build(self) -> cq.Workplane:
        face = cq.Face.makePlane(
            self.length,
            self.width,
            basePnt=cq.Vector(-self.length / 2.0, -self.width / 2.0, self.z),
            dir=cq.Vector(0, 0, 1),
        )
        return cq.Workplane("XY").add(face)
