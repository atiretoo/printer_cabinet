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
Horizontal structural shelves, reinforced 3D printer shelf, and vibration
decoupling platform (elastomer damping mat + concrete/granite inertia paver).
"""

from typing import List, Tuple
import cadquery as cq

from params import (
    INSIDE_WIDTH,
    INSIDE_DEPTH,
    FRONT_FACE_Y,
    INSIDE_REAR_Y,
    PLY_THICKNESS,
    PRINTER_SHELF_THICKNESS,
    Z_BOTTOM_PANEL_BOTTOM,
    Z_LOWER_DIVIDER_BOTTOM,
    Z_PRINTER_SHELF_BOTTOM,
    Z_DRY_SHELF_BOTTOM,
    Z_TOP_PANEL_BOTTOM,
    PTFE_FITTING_HOLE_DIA,
    PTFE_PORT_OFFSETS_X,
    PTFE_PORT_OFFSET_Y,
    PAVER_WIDTH,
    PAVER_DEPTH,
    PAVER_THICKNESS,
    ISOLATION_PAD_THICKNESS,
    Z_PAD_BOTTOM,
    Z_PAVER_BOTTOM,
)

SHELF_MID_Y = (FRONT_FACE_Y + INSIDE_REAR_Y) / 2.0


def make_standard_shelf(z_bottom: float, thickness: float = PLY_THICKNESS) -> cq.Workplane:
    """
    Creates a standard horizontal Baltic birch shelf at elevation z_bottom.
    """
    shelf = (
        cq.Workplane("XY")
        .box(INSIDE_WIDTH, INSIDE_DEPTH, thickness)
        .translate((0, SHELF_MID_Y, z_bottom + thickness / 2.0))
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
    Creates the reinforced permanent shelf for the 3D printer.

    Constructed from double-laminated 1.5" (38.1 mm) Baltic birch plywood,
    augmented by a front stiffening apron rib. This mass and section modulus
    drastically reduces deflection and drum-skin resonance under the moving printer.
    """
    base_shelf = make_standard_shelf(Z_PRINTER_SHELF_BOTTOM, thickness=PRINTER_SHELF_THICKNESS)

    # Front stiffener apron rib under the shelf
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


def make_isolation_pad() -> cq.Workplane:
    """
    Creates the high-density closed-cell EVA foam / Sorbothane decoupling mat
    resting directly on top of the printer shelf.
    """
    pad_z = Z_PAD_BOTTOM + ISOLATION_PAD_THICKNESS / 2.0
    pad = (
        cq.Workplane("XY")
        .box(PAVER_WIDTH, PAVER_DEPTH, ISOLATION_PAD_THICKNESS)
        .translate((0, 0, pad_z))
    )
    return pad


def make_paver_slab() -> cq.Workplane:
    """
    Creates the dense concrete or granite inertia ballast paver (~22 kg).
    Sits on top of the isolation mat and acts as the immediate platform for the printer.
    """
    paver_z = Z_PAVER_BOTTOM + PAVER_THICKNESS / 2.0
    paver = (
        cq.Workplane("XY")
        .box(PAVER_WIDTH, PAVER_DEPTH, PAVER_THICKNESS)
        .translate((0, 0, paver_z))
    )
    paver = paver.edges().chamfer(3.0)
    return paver


def make_dry_shelf() -> cq.Workplane:
    """
    Creates the permanent shelf separating the 3D printer bay from the dry chamber.
    Includes pass-through holes for PTFE bulkhead fittings.
    """
    shelf = make_standard_shelf(Z_DRY_SHELF_BOTTOM)

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
