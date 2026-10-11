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
Carcass panel geometry for the printer cabinet.

Generates the structural vertical side panels, base plinth / toe-kick,
and full-height inset back panel.
"""

from typing import Dict, Tuple
import cadquery as cq

from params import (
    CABINET_WIDTH,
    CABINET_DEPTH,
    CABINET_HEIGHT,
    PLY_THICKNESS,
    BACK_THICKNESS,
    PLINTH_HEIGHT,
    PLINTH_SETBACK_FRONT,
    INSIDE_WIDTH,
    INSIDE_DEPTH,
    FRONT_FACE_Y,
    REAR_FACE_Y,
    Z_BOTTOM_PANEL_BOTTOM,
    Z_TOP_PANEL_BOTTOM,
    Z_LOWER_DIVIDER_BOTTOM,
    Z_PRINTER_SHELF_BOTTOM,
    Z_DRY_SHELF_BOTTOM,
)


def make_side_panel(side: str = "left") -> cq.Workplane:
    """
    Creates a single vertical side panel (3/4" Baltic birch).

    The panel spans the full cabinet depth and height, featuring a front
    toe-kick cutout at the bottom.
    """
    # Base rectangle in Y-Z plane
    # Global: Y depth, Z height, X thickness
    panel = cq.Workplane("XY").box(PLY_THICKNESS, CABINET_DEPTH, CABINET_HEIGHT)

    # Toe-kick cutout at bottom front (-Y, -Z relative to center)
    # Notch dimensions:
    #   Depth along Y: PLINTH_SETBACK_FRONT (from front edge FRONT_FACE_Y)
    #   Height along Z: PLINTH_HEIGHT (from floor Z = 0)
    notch_y = PLINTH_SETBACK_FRONT
    notch_z = PLINTH_HEIGHT
    notch_cutter = (
        cq.Workplane("XY")
        .box(PLY_THICKNESS * 2, notch_y, notch_z)
        .translate((
            0,
            FRONT_FACE_Y + notch_y / 2.0,
            notch_z / 2.0 - CABINET_HEIGHT / 2.0,
        ))
    )
    panel = panel.cut(notch_cutter)

    # Position in user space: bottom at Z = 0, depth centered at Y = 0
    # X positioned on left (-X) or right (+X)
    x_pos = (-CABINET_WIDTH / 2.0 + PLY_THICKNESS / 2.0) if side == "left" else (CABINET_WIDTH / 2.0 - PLY_THICKNESS / 2.0)
    panel = panel.translate((x_pos, 0, CABINET_HEIGHT / 2.0))

    return panel


def make_plinth_assembly() -> cq.Workplane:
    """
    Creates the recessed toe-kick plinth frame at the base of the cabinet.
    Consists of front toe-kick face rail, rear ground rail, and side stretchers.
    """
    plinth_parts = []

    # Front toe-kick face board (recessed by PLINTH_SETBACK_FRONT)
    front_rail_y = FRONT_FACE_Y + PLINTH_SETBACK_FRONT + PLY_THICKNESS / 2.0
    front_rail = (
        cq.Workplane("XY")
        .box(INSIDE_WIDTH, PLY_THICKNESS, PLINTH_HEIGHT)
        .translate((0, front_rail_y, PLINTH_HEIGHT / 2.0))
    )
    plinth_parts.append(front_rail.val())

    # Rear ground rail (flush with rear of interior)
    rear_rail_y = REAR_FACE_Y - BACK_THICKNESS - PLY_THICKNESS / 2.0
    rear_rail = (
        cq.Workplane("XY")
        .box(INSIDE_WIDTH, PLY_THICKNESS, PLINTH_HEIGHT)
        .translate((0, rear_rail_y, PLINTH_HEIGHT / 2.0))
    )
    plinth_parts.append(rear_rail.val())

    # Left and right plinth cross stretchers
    stretcher_len = (rear_rail_y - PLY_THICKNESS / 2.0) - (front_rail_y + PLY_THICKNESS / 2.0)
    stretcher_mid_y = (front_rail_y + rear_rail_y) / 2.0
    for x_offset in [-INSIDE_WIDTH / 2.0 + PLY_THICKNESS / 2.0, INSIDE_WIDTH / 2.0 - PLY_THICKNESS / 2.0]:
        stretcher = (
            cq.Workplane("XY")
            .box(PLY_THICKNESS, stretcher_len, PLINTH_HEIGHT)
            .translate((x_offset, stretcher_mid_y, PLINTH_HEIGHT / 2.0))
        )
        plinth_parts.append(stretcher.val())

    return cq.Workplane(cq.Compound.makeCompound(plinth_parts))


def make_back_panel() -> cq.Workplane:
    """
    Creates the structural 1/2" Baltic birch inset back panel.
    Spans from the top of the plinth to the top of the cabinet, locking
    the carcass completely square against racking forces.
    """
    back_h = CABINET_HEIGHT - PLINTH_HEIGHT
    back_z = PLINTH_HEIGHT + back_h / 2.0
    back_y = REAR_FACE_Y - BACK_THICKNESS / 2.0

    panel = (
        cq.Workplane("XY")
        .box(INSIDE_WIDTH, BACK_THICKNESS, back_h)
        .translate((0, back_y, back_z))
    )
    return panel
