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
Shallow tool drawer subsystem located directly under the 3D printer shelf
and above the pull-out scanner bay.

Engineered to house 3D printing maintenance tools, spare nozzles, scrapers,
calipers, lubricants, and modular Gridfinity organizing bins.
"""

from typing import List, Tuple
import cadquery as cq

from params import (
    INSIDE_WIDTH,
    TOOL_DRAWER_WIDTH,
    TOOL_DRAWER_DEPTH,
    TOOL_DRAWER_BOX_HEIGHT,
    TOOL_DRAWER_FRONT_HEIGHT,
    TOOL_DRAWER_WALL_THICKNESS,
    TOOL_DRAWER_BOTTOM_THICKNESS,
    SLIDE_THICKNESS,
    SLIDE_LENGTH,
    SLIDE_HEIGHT,
    Z_TOOL_DIVIDER_TOP,
    FRONT_FACE_Y,
    DOOR_CLEARANCE,
)


def make_tool_drawer(extension: float = 0.0) -> cq.Workplane:
    """
    Creates the shallow tool drawer box with butt joints, flush bottom,
    and 1/2" Baltic birch false front.

    :param extension: Distance in mm to extend forward along -Y (0 = stowed).
    """
    parts = []

    # Z elevation: rests 8 mm above divider shelf
    drawer_base_z = Z_TOOL_DIVIDER_TOP + 8.0 + TOOL_DRAWER_BOX_HEIGHT / 2.0
    stowed_front_y = FRONT_FACE_Y + 12.0
    drawer_center_y = stowed_front_y + TOOL_DRAWER_DEPTH / 2.0 - extension

    wall_h = TOOL_DRAWER_BOX_HEIGHT - TOOL_DRAWER_BOTTOM_THICKNESS
    z_wall_offset = drawer_base_z - TOOL_DRAWER_BOX_HEIGHT / 2.0 + TOOL_DRAWER_BOTTOM_THICKNESS + wall_h / 2.0

    # 1. Drawer Bottom (1/2" Baltic birch)
    bottom_z = drawer_base_z - TOOL_DRAWER_BOX_HEIGHT / 2.0 + TOOL_DRAWER_BOTTOM_THICKNESS / 2.0
    bottom = (
        cq.Workplane("XY")
        .box(TOOL_DRAWER_WIDTH, TOOL_DRAWER_DEPTH, TOOL_DRAWER_BOTTOM_THICKNESS)
        .translate((0, drawer_center_y, bottom_z))
    )
    parts.append(bottom.val())

    # 2. Side Walls (run full depth)
    for x_sign in [-1.0, 1.0]:
        x_pos = x_sign * (TOOL_DRAWER_WIDTH / 2.0 - TOOL_DRAWER_WALL_THICKNESS / 2.0)
        side = (
            cq.Workplane("XY")
            .box(TOOL_DRAWER_WALL_THICKNESS, TOOL_DRAWER_DEPTH, wall_h)
            .translate((x_pos, drawer_center_y, z_wall_offset))
        )
        parts.append(side.val())

    # 3. Front and Back Walls (fit between sides)
    fb_len = TOOL_DRAWER_WIDTH - 2 * TOOL_DRAWER_WALL_THICKNESS
    for y_sign in [-1.0, 1.0]:
        y_pos = drawer_center_y + y_sign * (TOOL_DRAWER_DEPTH / 2.0 - TOOL_DRAWER_WALL_THICKNESS / 2.0)
        fb = (
            cq.Workplane("XY")
            .box(fb_len, TOOL_DRAWER_WALL_THICKNESS, wall_h)
            .translate((0, y_pos, z_wall_offset))
        )
        parts.append(fb.val())

    # 4. False Front (1/2" Baltic birch covering the slide gap)
    front_w = INSIDE_WIDTH - 2 * DOOR_CLEARANCE
    front_y = stowed_front_y - extension - TOOL_DRAWER_WALL_THICKNESS / 2.0
    front_z = Z_TOOL_DIVIDER_TOP + 4.0 + TOOL_DRAWER_FRONT_HEIGHT / 2.0
    false_front = (
        cq.Workplane("XY")
        .box(front_w, TOOL_DRAWER_WALL_THICKNESS, TOOL_DRAWER_FRONT_HEIGHT)
        .translate((0, front_y, front_z))
    )
    # Bevel top front edge for grip pull
    false_front = false_front.edges("|X and >Z and <Y").chamfer(3.0)
    parts.append(false_front.val())

    return cq.Workplane(cq.Compound.makeCompound(parts))


def make_tool_drawer_slides(extension: float = 0.0) -> cq.Workplane:
    """
    Creates bounding models of the ball-bearing slides for the tool drawer.
    """
    parts = []
    slide_z = Z_TOOL_DIVIDER_TOP + 8.0 + SLIDE_HEIGHT / 2.0
    stowed_front_y = FRONT_FACE_Y + 12.0
    slide_y = stowed_front_y + SLIDE_LENGTH / 2.0

    for x_sign in [-1.0, 1.0]:
        cab_x = x_sign * (INSIDE_WIDTH / 2.0 - SLIDE_THICKNESS / 4.0)
        cab_rail = (
            cq.Workplane("XY")
            .box(SLIDE_THICKNESS / 2.0, SLIDE_LENGTH, SLIDE_HEIGHT)
            .translate((cab_x, slide_y, slide_z))
        )
        parts.append(cab_rail.val())

        tray_x = x_sign * (TOOL_DRAWER_WIDTH / 2.0 + SLIDE_THICKNESS / 4.0)
        tray_rail = (
            cq.Workplane("XY")
            .box(SLIDE_THICKNESS / 2.0, SLIDE_LENGTH, SLIDE_HEIGHT)
            .translate((tray_x, slide_y - extension, slide_z))
        )
        parts.append(tray_rail.val())

    return cq.Workplane(cq.Compound.makeCompound(parts))
