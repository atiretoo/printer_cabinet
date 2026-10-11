# Copyright (C) 2026 Andrew Tyre
#
# This file is part of printer_cabinet.
#
# printer_cabinet is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# printer_cabinet is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with printer_cabinet.  If not, see <https://www.gnu.org/licenses/>.

"""
Filament Dry Chamber subsystem for the printer cabinet.

Includes:
  - Airtight gasketed door with clear acrylic viewing window and compression latches.
  - Dual-roller spool rack holding up to 6 standard 1kg filament reels.
  - Removable slotted desiccant trays for silica gel beads.
  - PTFE tube guide pass-throughs feeding directly into the 3D printer chamber.
"""

from typing import List, Tuple
import cadquery as cq

from params import (
    INSIDE_WIDTH,
    DRY_BAY_HEIGHT,
    Z_DRY_SHELF_TOP,
    Z_TOP_PANEL_BOTTOM,
    FRONT_FACE_Y,
    PLY_THICKNESS,
    ACRYLIC_THICKNESS,
    DOOR_FRAME_WIDTH,
    DOOR_CLEARANCE,
    SPOOL_DIAMETER,
    SPOOL_WIDTH,
    ROLLER_DOWEL_DIAMETER,
    ROLLER_SPACING,
    ROLLER_ELEVATION,
    DESICCANT_TRAY_WIDTH,
    DESICCANT_TRAY_DEPTH,
    DESICCANT_TRAY_HEIGHT,
    PTFE_TUBE_OD,
    PTFE_PORT_OFFSETS_X,
    PTFE_PORT_OFFSET_Y,
    Z_DRY_SHELF_BOTTOM,
)


def make_sealed_door_frame() -> cq.Workplane:
    """
    Creates the outer Baltic birch door frame for the dry chamber.
    """
    door_w = INSIDE_WIDTH - 2 * DOOR_CLEARANCE
    door_h = DRY_BAY_HEIGHT - 2 * DOOR_CLEARANCE
    door_mid_z = (Z_DRY_SHELF_TOP + Z_TOP_PANEL_BOTTOM) / 2.0
    door_y = FRONT_FACE_Y - PLY_THICKNESS / 2.0  # overlay / flush front

    # Outer solid box
    frame = (
        cq.Workplane("XY")
        .box(door_w, PLY_THICKNESS, door_h)
        .translate((0, door_y, door_mid_z))
    )

    # Cut center window opening
    window_w = door_w - 2 * DOOR_FRAME_WIDTH
    window_h = door_h - 2 * DOOR_FRAME_WIDTH
    window_cutter = (
        cq.Workplane("XY")
        .box(window_w, PLY_THICKNESS * 2, window_h)
        .translate((0, door_y, door_mid_z))
    )
    frame = frame.cut(window_cutter)

    return frame


def make_door_acrylic() -> cq.Workplane:
    """
    Creates the 1/8" (3mm) clear acrylic / polycarbonate window pane.
    """
    door_w = INSIDE_WIDTH - 2 * DOOR_CLEARANCE
    door_h = DRY_BAY_HEIGHT - 2 * DOOR_CLEARANCE
    door_mid_z = (Z_DRY_SHELF_TOP + Z_TOP_PANEL_BOTTOM) / 2.0
    door_y = FRONT_FACE_Y - PLY_THICKNESS / 2.0

    pane_w = door_w - 2 * (DOOR_FRAME_WIDTH - 12.0)  # captured in rabbet
    pane_h = door_h - 2 * (DOOR_FRAME_WIDTH - 12.0)

    pane = (
        cq.Workplane("XY")
        .box(pane_w, ACRYLIC_THICKNESS, pane_h)
        .translate((0, door_y, door_mid_z))
    )
    return pane


def make_door_gasket() -> cq.Workplane:
    """
    Creates the silicone bulb perimeter gasket representing the airtight seal.
    """
    door_w = INSIDE_WIDTH - 2 * DOOR_CLEARANCE
    door_h = DRY_BAY_HEIGHT - 2 * DOOR_CLEARANCE
    door_mid_z = (Z_DRY_SHELF_TOP + Z_TOP_PANEL_BOTTOM) / 2.0
    gasket_y = FRONT_FACE_Y - 1.5  # between door and carcass face

    # Outer perimeter
    gasket = (
        cq.Workplane("XY")
        .box(door_w - 10.0, 3.0, door_h - 10.0)
        .translate((0, gasket_y, door_mid_z))
    )
    # Inner opening
    inner_cutter = (
        cq.Workplane("XY")
        .box(door_w - 30.0, 10.0, door_h - 30.0)
        .translate((0, gasket_y, door_mid_z))
    )
    gasket = gasket.cut(inner_cutter)
    return gasket


def make_spool_rack() -> cq.Workplane:
    """
    Creates the spool support cradle and two longitudinal roller dowels.
    """
    parts = []
    rack_mid_y = 40.0  # biased slightly to rear to leave room for desiccant trays in front
    roller_z = Z_DRY_SHELF_TOP + ROLLER_ELEVATION
    dowel_len = INSIDE_WIDTH - 2 * PLY_THICKNESS

    # 1. Left and Right End Support Brackets (3/4" Baltic birch)
    bracket_w = PLY_THICKNESS
    bracket_d = ROLLER_SPACING + 70.0
    bracket_h = ROLLER_ELEVATION + 35.0
    bracket_z = Z_DRY_SHELF_TOP + bracket_h / 2.0

    for x_sign in [-1.0, 1.0]:
        bx = x_sign * (INSIDE_WIDTH / 2.0 - PLY_THICKNESS / 2.0)
        bracket = (
            cq.Workplane("XY")
            .box(bracket_w, bracket_d, bracket_h)
            .translate((bx, rack_mid_y, bracket_z))
        )
        parts.append(bracket.val())

    # 2. Front and Rear Roller Dowels (25.4mm / 1" dowels)
    for y_sign in [-1.0, 1.0]:
        ry = rack_mid_y + y_sign * (ROLLER_SPACING / 2.0)
        # Cylinder aligned along X: create on YZ and extrude X
        roller = (
            cq.Workplane("YZ")
            .circle(ROLLER_DOWEL_DIAMETER / 2.0)
            .extrude(dowel_len)
            .translate((-dowel_len / 2.0, ry, roller_z))
        )
        parts.append(roller.val())

    return cq.Workplane(cq.Compound.makeCompound(parts))


def make_filament_spools(count: int = 5) -> cq.Workplane:
    """
    Creates mockups of standard 1kg filament reels resting on the rollers.
    """
    parts = []
    rack_mid_y = 40.0
    spool_r = SPOOL_DIAMETER / 2.0
    # Tangent elevation on the two rollers:
    # h = sqrt(R_total^2 - (spacing/2)^2) where R_total = R_spool + R_roller
    r_total = spool_r + (ROLLER_DOWEL_DIAMETER / 2.0)
    dy = ROLLER_SPACING / 2.0
    dz = (r_total**2 - dy**2)**0.5
    spool_center_z = Z_DRY_SHELF_TOP + ROLLER_ELEVATION + dz

    # Distribute spools across the width
    spacing_x = 90.0
    start_x = -((count - 1) * spacing_x) / 2.0

    for i in range(count):
        sx = start_x + i * spacing_x

        # Spool body: cylinder along X
        # Flanges (2x outer disks)
        flange_t = 4.0
        flange1 = (
            cq.Workplane("YZ")
            .circle(spool_r)
            .extrude(flange_t)
            .translate((sx - SPOOL_WIDTH / 2.0, rack_mid_y, spool_center_z))
        )
        flange2 = (
            cq.Workplane("YZ")
            .circle(spool_r)
            .extrude(flange_t)
            .translate((sx + SPOOL_WIDTH / 2.0 - flange_t, rack_mid_y, spool_center_z))
        )
        # Center core/barrel
        core = (
            cq.Workplane("YZ")
            .circle(50.0)
            .extrude(SPOOL_WIDTH - 2 * flange_t)
            .translate((sx - SPOOL_WIDTH / 2.0 + flange_t, rack_mid_y, spool_center_z))
        )
        # Center arbor hole
        hole = (
            cq.Workplane("YZ")
            .circle(26.0)
            .extrude(SPOOL_WIDTH * 2)
            .translate((sx - SPOOL_WIDTH, rack_mid_y, spool_center_z))
        )

        spool = cq.Workplane(cq.Compound.makeCompound([flange1.val(), flange2.val(), core.val()])).cut(hole)
        parts.append(spool.val())

    return cq.Workplane(cq.Compound.makeCompound(parts))


def make_desiccant_trays() -> cq.Workplane:
    """
    Creates two removable desiccant bead trays sitting in front of the spool rack.
    """
    parts = []
    tray_y = -170.0  # forward section of dry chamber
    tray_z = Z_DRY_SHELF_TOP + DESICCANT_TRAY_HEIGHT / 2.0

    for x_sign in [-1.0, 1.0]:
        tx = x_sign * (DESICCANT_TRAY_WIDTH / 2.0 + 10.0)
        # Outer tray box
        box = (
            cq.Workplane("XY")
            .box(DESICCANT_TRAY_WIDTH, DESICCANT_TRAY_DEPTH, DESICCANT_TRAY_HEIGHT)
            .translate((tx, tray_y, tray_z))
        )
        # Inner cavity for silica gel beads
        cavity = (
            cq.Workplane("XY")
            .box(DESICCANT_TRAY_WIDTH - 8.0, DESICCANT_TRAY_DEPTH - 8.0, DESICCANT_TRAY_HEIGHT - 4.0)
            .translate((tx, tray_y, tray_z + 2.0))
        )
        tray = box.cut(cavity)
        parts.append(tray.val())

    return cq.Workplane(cq.Compound.makeCompound(parts))


def make_ptfe_tubes() -> cq.Workplane:
    """
    Creates the PTFE guide tubes passing through the dry shelf floor
    down toward the 3D printer inlet.
    """
    parts = []
    tube_top_z = Z_DRY_SHELF_TOP + 80.0
    tube_bottom_z = Z_DRY_SHELF_BOTTOM - 80.0
    tube_len = tube_top_z - tube_bottom_z
    tube_mid_z = (tube_top_z + tube_bottom_z) / 2.0

    for x_pos in PTFE_PORT_OFFSETS_X:
        tube = (
            cq.Workplane("XY")
            .cylinder(tube_len, PTFE_TUBE_OD / 2.0)
            .translate((x_pos, PTFE_PORT_OFFSET_Y, tube_mid_z))
        )
        parts.append(tube.val())

    return cq.Workplane(cq.Compound.makeCompound(parts))
