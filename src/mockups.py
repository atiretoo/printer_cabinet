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
Dimensional mockups of equipment and supplies for fit/clearance verification.

Includes:
  - Prusa Core One+ 3D Printer
  - Epson All-in-One Inkjet Scanner (with operable flatbed lid)
  - Paper reams and storage supplies
"""

import math
import cadquery as cq

from params import (
    PRUSA_CORE_ONE_WIDTH,
    PRUSA_CORE_ONE_DEPTH,
    PRUSA_CORE_ONE_HEIGHT,
    EPSON_SCANNER_WIDTH,
    EPSON_SCANNER_DEPTH,
    EPSON_SCANNER_HEIGHT_CLOSED,
    Z_PRINTER_SHELF_TOP,
    Z_LOWER_DIVIDER_TOP,
    TRAY_ELEVATION_ABOVE_DIVIDER,
    TRAY_THICKNESS,
    FRONT_FACE_Y,
    Z_BOTTOM_PANEL_TOP,
)


def make_prusa_core_one() -> cq.Workplane:
    """
    Creates a detailed dimensional mockup of the Prusa Core One+ 3D printer.
    """
    parts = []

    printer_z = Z_PRINTER_SHELF_TOP + PRUSA_CORE_ONE_HEIGHT / 2.0
    # Center along Y with equal front/rear margins
    printer_y = 0.0

    # Main chassis box
    chassis = (
        cq.Workplane("XY")
        .box(PRUSA_CORE_ONE_WIDTH, PRUSA_CORE_ONE_DEPTH, PRUSA_CORE_ONE_HEIGHT)
        .translate((0, printer_y, printer_z))
    )
    # Bevel / chamfer vertical corner columns
    chassis = chassis.edges("|Z").chamfer(10.0)
    parts.append(chassis.val())

    # Front glass door panel
    door_w = PRUSA_CORE_ONE_WIDTH - 40.0
    door_h = PRUSA_CORE_ONE_HEIGHT - 60.0
    door_y = printer_y - PRUSA_CORE_ONE_DEPTH / 2.0 - 2.0
    front_door = (
        cq.Workplane("XY")
        .box(door_w, 4.0, door_h)
        .translate((0, door_y, printer_z))
    )
    parts.append(front_door.val())

    # Top reverse Bowden guide fitting
    top_fitting_z = Z_PRINTER_SHELF_TOP + PRUSA_CORE_ONE_HEIGHT + 15.0
    top_fitting = (
        cq.Workplane("XY")
        .cylinder(30.0, 8.0)
        .translate((0, printer_y, top_fitting_z))
    )
    parts.append(top_fitting.val())

    return cq.Workplane(cq.Compound.makeCompound(parts))


def make_epson_scanner(extension: float = 0.0, lid_angle_deg: float = 0.0) -> cq.Workplane:
    """
    Creates a dimensional mockup of an Epson all-in-one inkjet scanner.

    :param extension: Pull-out tray forward travel distance in mm.
    :param lid_angle_deg: Flatbed scanner lid opening angle (0 = closed, 75-90 = open).
    """
    parts = []

    tray_top_z = Z_LOWER_DIVIDER_TOP + TRAY_ELEVATION_ABOVE_DIVIDER + TRAY_THICKNESS
    scanner_base_h = 135.0
    scanner_lid_h = 35.0
    stowed_front_y = FRONT_FACE_Y + 40.0
    scanner_y = stowed_front_y + EPSON_SCANNER_DEPTH / 2.0 - extension
    base_z = tray_top_z + scanner_base_h / 2.0

    # 1. Main printer / ink tank base
    base = (
        cq.Workplane("XY")
        .box(EPSON_SCANNER_WIDTH, EPSON_SCANNER_DEPTH, scanner_base_h)
        .translate((0, scanner_y, base_z))
    )
    base = base.edges("|Z").fillet(10.0)
    parts.append(base.val())

    # 2. Scanner Flatbed Lid
    hinge_y = scanner_y + EPSON_SCANNER_DEPTH / 2.0
    hinge_z = tray_top_z + scanner_base_h

    lid = (
        cq.Workplane("XY")
        .box(EPSON_SCANNER_WIDTH, EPSON_SCANNER_DEPTH, scanner_lid_h)
        .translate((0, -EPSON_SCANNER_DEPTH / 2.0, scanner_lid_h / 2.0))
    )

    if lid_angle_deg != 0.0:
        # Rotate about the hinge axis (parallel to X at rear top edge)
        # Positive rotation rotates upward
        lid = lid.rotate((0, 0, 0), (1, 0, 0), -lid_angle_deg)

    lid = lid.translate((0, hinge_y, hinge_z))
    parts.append(lid.val())

    return cq.Workplane(cq.Compound.makeCompound(parts))


def make_paper_storage() -> cq.Workplane:
    """
    Creates mockups of stored paper reams in the lower storage bay.
    """
    parts = []

    # Standard Letter Ream: 8.5" x 11" x 2" (216 mm x 279 mm x 50 mm)
    ream_w = 216.0
    ream_d = 279.0
    ream_h = 50.0

    z_start = Z_BOTTOM_PANEL_TOP + ream_h / 2.0

    # 2 stacks side-by-side, each 3 reams high
    for x_offset in [-130.0, 130.0]:
        for layer in range(3):
            ream = (
                cq.Workplane("XY")
                .box(ream_w, ream_d, ream_h - 2.0)
                .translate((x_offset, -20.0, z_start + layer * ream_h))
            )
            parts.append(ream.val())

    # Ledger / Tabloid Box (11" x 17" = 279 mm x 432 mm x 100 mm) at the rear
    tabloid = (
        cq.Workplane("XY")
        .box(432.0, 150.0, 140.0)
        .translate((0, 180.0, Z_BOTTOM_PANEL_TOP + 70.0))
    )
    parts.append(tabloid.val())

    return cq.Workplane(cq.Compound.makeCompound(parts))
