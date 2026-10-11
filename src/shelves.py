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
Horizontal structural shelves and dividers for the printer cabinet.

Generates the bottom panel, lower divider shelf (above paper storage),
reinforced solid 3D printer shelf, filament dry chamber shelf with
PTFE feed pass-through holes, and top ceiling panel.
"""

from typing import List
import cadquery as cq

from params import (
    INSIDE_WIDTH,
    INSIDE_DEPTH,
    FRONT_FACE_Y,
    INSIDE_REAR_Y,
    PLY_THICKNESS,
    Z_BOTTOM_PANEL_BOTTOM,
    Z_LOWER_DIVIDER_BOTTOM,
    Z_PRINTER_SHELF_BOTTOM,
    Z_DRY_SHELF_BOTTOM,
    Z_TOP_PANEL_BOTTOM,
    PTFE_FITTING_HOLE_DIA,
    PTFE_PORT_OFFSETS_X,
    PTFE_PORT_OFFSET_Y,
)

# Standard shelf center along Y (flush with front, abuts rear back panel)
SHELF_MID_Y = (FRONT_FACE_Y + INSIDE_REAR_Y) / 2.0


def make_standard_shelf(z_bottom: float) -> cq.Workplane:
    """
    Creates a standard horizontal 3/4" Baltic birch shelf at elevation z_bottom.
    """
    shelf = (
        cq.Workplane("XY")
        .box(INSIDE_WIDTH, INSIDE_DEPTH, PLY_THICKNESS)
        .translate((0, SHELF_MID_Y, z_bottom + PLY_THICKNESS / 2.0))
    )
    return shelf


def make_bottom_panel() -> cq.Workplane:
    """Creates the structural bottom panel above the plinth."""
    return make_standard_shelf(Z_BOTTOM_PANEL_BOTTOM)


def make_lower_divider() -> cq.Workplane:
    """Creates the divider shelf between paper storage and the pull-out scanner bay."""
    return make_standard_shelf(Z_LOWER_DIVIDER_BOTTOM)


def make_printer_shelf() -> cq.Workplane:
    """
    Creates the solid, reinforced permanent shelf for the 3D printer.

    Includes a 1.5" (38.1 mm) under-shelf hardwood/birch stiffening apron
    along the front edge to eliminate deflection under the 22.5 kg printer
    and dynamic acceleration vibrations.
    """
    base_shelf = make_standard_shelf(Z_PRINTER_SHELF_BOTTOM)

    # Front stiffener apron
    stiffener_h = 38.1  # 1.5"
    stiffener_y = FRONT_FACE_Y + PLY_THICKNESS / 2.0
    stiffener_z = Z_PRINTER_SHELF_BOTTOM - stiffener_h / 2.0

    stiffener = (
        cq.Workplane("XY")
        .box(INSIDE_WIDTH, PLY_THICKNESS, stiffener_h)
        .translate((0, stiffener_y, stiffener_z))
    )

    comp = cq.Compound.makeCompound([base_shelf.val(), stiffener.val()])
    return cq.Workplane(comp)


def make_dry_shelf() -> cq.Workplane:
    """
    Creates the permanent shelf separating the 3D printer bay from the dry chamber.

    Features two counterbored pass-through openings for PC4-M10 pneumatic fittings,
    allowing PTFE reverse Bowden tubes to feed filament directly into the printer.
    """
    shelf = make_standard_shelf(Z_DRY_SHELF_BOTTOM)

    # Cut pass-through holes for PTFE fittings
    cutters = []
    for x_offset in PTFE_PORT_OFFSETS_X:
        cutter = (
            cq.Workplane("XY")
            .cylinder(PLY_THICKNESS * 2, PTFE_FITTING_HOLE_DIA / 2.0)
            .translate((x_offset, PTFE_PORT_OFFSET_Y, Z_DRY_SHELF_BOTTOM + PLY_THICKNESS / 2.0))
        )
        shelf = shelf.cut(cutter)

    return shelf


def make_top_panel() -> cq.Workplane:
    """Creates the structural top panel / ceiling of the cabinet."""
    return make_standard_shelf(Z_TOP_PANEL_BOTTOM)
