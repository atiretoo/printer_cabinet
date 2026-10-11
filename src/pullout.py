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
Pull-out shelf subsystem for the Epson inkjet scanner.

Features a 3/4" Baltic birch tray with rear and side retention lips,
paired with heavy-duty full-extension ball-bearing slides.
"""

from typing import Tuple, List
import cadquery as cq

from params import (
    INSIDE_WIDTH,
    TRAY_WIDTH,
    TRAY_DEPTH,
    TRAY_THICKNESS,
    TRAY_LIP_THICKNESS,
    TRAY_LIP_HEIGHT,
    TRAY_ELEVATION_ABOVE_DIVIDER,
    SLIDE_THICKNESS,
    SLIDE_LENGTH,
    SLIDE_HEIGHT,
    Z_LOWER_DIVIDER_TOP,
    FRONT_FACE_Y,
    INSIDE_REAR_Y,
)


def make_tray_assembly(extension: float = 0.0) -> cq.Workplane:
    """
    Creates the pull-out wooden tray with retaining lips.

    :param extension: Distance in mm to extend forward along -Y (0 = stowed).
    """
    parts = []

    tray_base_z = Z_LOWER_DIVIDER_TOP + TRAY_ELEVATION_ABOVE_DIVIDER + TRAY_THICKNESS / 2.0
    # Stowed tray front sits 10mm back from carcass front face
    stowed_front_y = FRONT_FACE_Y + 10.0
    tray_center_y = stowed_front_y + TRAY_DEPTH / 2.0 - extension

    # 1. Main Tray Bottom Board (3/4" Baltic Birch)
    base_board = (
        cq.Workplane("XY")
        .box(TRAY_WIDTH, TRAY_DEPTH, TRAY_THICKNESS)
        .translate((0, tray_center_y, tray_base_z))
    )
    parts.append(base_board.val())

    # 2. Rear Retention Lip (keeps equipment from sliding off the back)
    rear_lip_y = (tray_center_y + TRAY_DEPTH / 2.0) - TRAY_LIP_THICKNESS / 2.0
    rear_lip_z = tray_base_z + TRAY_THICKNESS / 2.0 + TRAY_LIP_HEIGHT / 2.0
    rear_lip = (
        cq.Workplane("XY")
        .box(TRAY_WIDTH, TRAY_LIP_THICKNESS, TRAY_LIP_HEIGHT)
        .translate((0, rear_lip_y, rear_lip_z))
    )
    parts.append(rear_lip.val())

    # 3. Left and Right Low-Profile Side Lips
    side_lip_len = TRAY_DEPTH - TRAY_LIP_THICKNESS
    side_lip_y = tray_center_y - TRAY_LIP_THICKNESS / 2.0
    side_lip_z = rear_lip_z
    for x_sign in [-1.0, 1.0]:
        x_pos = x_sign * (TRAY_WIDTH / 2.0 - TRAY_LIP_THICKNESS / 2.0)
        side_lip = (
            cq.Workplane("XY")
            .box(TRAY_LIP_THICKNESS, side_lip_len, TRAY_LIP_HEIGHT)
            .translate((x_pos, side_lip_y, side_lip_z))
        )
        parts.append(side_lip.val())

    return cq.Workplane(cq.Compound.makeCompound(parts))


def make_slides(extension: float = 0.0) -> cq.Workplane:
    """
    Creates bounding models of the pair of full-extension ball-bearing slides.
    """
    parts = []
    slide_z = Z_LOWER_DIVIDER_TOP + TRAY_ELEVATION_ABOVE_DIVIDER + SLIDE_HEIGHT / 2.0
    stowed_front_y = FRONT_FACE_Y + 10.0
    slide_y = stowed_front_y + SLIDE_LENGTH / 2.0

    for x_sign in [-1.0, 1.0]:
        # Cabinet member (fixed to cabinet side panel)
        cab_x = x_sign * (INSIDE_WIDTH / 2.0 - SLIDE_THICKNESS / 4.0)
        cab_rail = (
            cq.Workplane("XY")
            .box(SLIDE_THICKNESS / 2.0, SLIDE_LENGTH, SLIDE_HEIGHT)
            .translate((cab_x, slide_y, slide_z))
        )
        parts.append(cab_rail.val())

        # Drawer member (attached to tray, extends with tray)
        tray_x = x_sign * (TRAY_WIDTH / 2.0 + SLIDE_THICKNESS / 4.0)
        tray_rail = (
            cq.Workplane("XY")
            .box(SLIDE_THICKNESS / 2.0, SLIDE_LENGTH, SLIDE_HEIGHT)
            .translate((tray_x, slide_y - extension, slide_z))
        )
        parts.append(tray_rail.val())

    return cq.Workplane(cq.Compound.makeCompound(parts))
