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
3D Printer Chamber Enclosure subsystem:
  - Full-height framed acrylic front door with ergonomic handle.
  - 120mm exhaust fan with 4" (100mm) duct collar adapter to vent emissions
    out to an external room window.
"""

from typing import List, Tuple
import cadquery as cq

from params import (
    INSIDE_WIDTH,
    PRINTER_BAY_HEIGHT,
    Z_PRINTER_SHELF_TOP,
    Z_DRY_SHELF_BOTTOM,
    FRONT_FACE_Y,
    REAR_FACE_Y,
    BACK_THICKNESS,
    PLY_THICKNESS,
    ACRYLIC_THICKNESS,
    DOOR_FRAME_WIDTH,
    DOOR_CLEARANCE,
    EXHAUST_FAN_SIZE,
    EXHAUST_FAN_DEPTH,
    EXHAUST_DUCT_DIA,
    EXHAUST_DUCT_LENGTH,
    EXHAUST_PORT_POS_X,
    EXHAUST_PORT_POS_Z,
)


def make_printer_door_frame(open_angle_deg: float = 0.0) -> cq.Workplane:
    """
    Creates the outer Baltic birch door frame for the 3D printer chamber.
    """
    door_w = INSIDE_WIDTH - 2 * DOOR_CLEARANCE
    door_h = PRINTER_BAY_HEIGHT - 2 * DOOR_CLEARANCE
    door_mid_z = (Z_PRINTER_SHELF_TOP + Z_DRY_SHELF_BOTTOM) / 2.0
    door_y = FRONT_FACE_Y - PLY_THICKNESS / 2.0

    frame = (
        cq.Workplane("XY")
        .box(door_w, PLY_THICKNESS, door_h)
        .translate((0, door_y, door_mid_z))
    )

    # Cut large center window opening
    window_w = door_w - 2 * DOOR_FRAME_WIDTH
    window_h = door_h - 2 * DOOR_FRAME_WIDTH
    window_cutter = (
        cq.Workplane("XY")
        .box(window_w, PLY_THICKNESS * 2, window_h)
        .translate((0, door_y, door_mid_z))
    )
    frame = frame.cut(window_cutter)

    if open_angle_deg != 0.0:
        # Rotate about left edge hinge axis
        hinge_x = -door_w / 2.0
        frame = frame.translate((-hinge_x, -door_y, -door_mid_z))
        frame = frame.rotate((0, 0, 0), (0, 0, 1), open_angle_deg)
        frame = frame.translate((hinge_x, door_y, door_mid_z))

    return frame


def make_printer_door_acrylic(open_angle_deg: float = 0.0) -> cq.Workplane:
    """
    Creates the 1/8" (3mm) clear acrylic window pane for the printer chamber door.
    """
    door_w = INSIDE_WIDTH - 2 * DOOR_CLEARANCE
    door_h = PRINTER_BAY_HEIGHT - 2 * DOOR_CLEARANCE
    door_mid_z = (Z_PRINTER_SHELF_TOP + Z_DRY_SHELF_BOTTOM) / 2.0
    door_y = FRONT_FACE_Y - PLY_THICKNESS / 2.0

    pane_w = door_w - 2 * (DOOR_FRAME_WIDTH - 12.0)
    pane_h = door_h - 2 * (DOOR_FRAME_WIDTH - 12.0)

    pane = (
        cq.Workplane("XY")
        .box(pane_w, ACRYLIC_THICKNESS, pane_h)
        .translate((0, door_y, door_mid_z))
    )

    if open_angle_deg != 0.0:
        hinge_x = -door_w / 2.0
        pane = pane.translate((-hinge_x, -door_y, -door_mid_z))
        pane = pane.rotate((0, 0, 0), (0, 0, 1), open_angle_deg)
        pane = pane.translate((hinge_x, door_y, door_mid_z))

    return pane


def make_printer_door_handle(open_angle_deg: float = 0.0) -> cq.Workplane:
    """
    Creates a modern vertical pull handle on the right stile of the door.
    """
    door_w = INSIDE_WIDTH - 2 * DOOR_CLEARANCE
    door_mid_z = (Z_PRINTER_SHELF_TOP + Z_DRY_SHELF_BOTTOM) / 2.0
    door_y = FRONT_FACE_Y - PLY_THICKNESS / 2.0

    handle_x = door_w / 2.0 - 25.0
    handle_y = door_y - 20.0

    # 150mm vertical pull bar
    bar = (
        cq.Workplane("XY")
        .box(16.0, 16.0, 160.0)
        .translate((handle_x, handle_y, door_mid_z))
    )

    # Standoffs connecting to door face
    standoff1 = (
        cq.Workplane("XY")
        .box(16.0, 20.0, 16.0)
        .translate((handle_x, handle_y + 10.0, door_mid_z + 60.0))
    )
    standoff2 = (
        cq.Workplane("XY")
        .box(16.0, 20.0, 16.0)
        .translate((handle_x, handle_y + 10.0, door_mid_z - 60.0))
    )

    handle = cq.Workplane(cq.Compound.makeCompound([bar.val(), standoff1.val(), standoff2.val()]))

    if open_angle_deg != 0.0:
        hinge_x = -door_w / 2.0
        handle = handle.translate((-hinge_x, -door_y, -door_mid_z))
        handle = handle.rotate((0, 0, 0), (0, 0, 1), open_angle_deg)
        handle = handle.translate((hinge_x, door_y, door_mid_z))

    return handle


def make_exhaust_fan_assembly() -> cq.Workplane:
    """
    Creates the 120mm exhaust fan and 4" round duct collar flange adapter
    mounted on the upper rear panel to vent emissions to an external window.
    """
    parts = []
    fan_inner_y = REAR_FACE_Y - BACK_THICKNESS - EXHAUST_FAN_DEPTH / 2.0

    # 1. 120mm x 120mm Fan Housing
    fan_box = (
        cq.Workplane("XY")
        .box(EXHAUST_FAN_SIZE, EXHAUST_FAN_DEPTH, EXHAUST_FAN_SIZE)
        .translate((EXHAUST_PORT_POS_X, fan_inner_y, EXHAUST_PORT_POS_Z))
    )
    # Fan rotor bore
    fan_bore = (
        cq.Workplane("ZX")
        .workplane(offset=fan_inner_y - EXHAUST_FAN_DEPTH)
        .center(EXHAUST_PORT_POS_Z, EXHAUST_PORT_POS_X)  # local (z, x)
        .circle(115.0 / 2.0)
        .extrude(EXHAUST_FAN_DEPTH * 2)
    )
    fan_box = fan_box.cut(fan_bore)
    parts.append(fan_box.val())

    # 2. 4" (100mm) Round Duct Collar Flange (protruding outside rear of cabinet)
    collar_y = REAR_FACE_Y + EXHAUST_DUCT_LENGTH / 2.0
    collar = (
        cq.Workplane("ZX")
        .workplane(offset=REAR_FACE_Y)
        .center(EXHAUST_PORT_POS_Z, EXHAUST_PORT_POS_X)  # local (z, x)
        .circle(EXHAUST_DUCT_DIA / 2.0)
        .circle((EXHAUST_DUCT_DIA - 4.0) / 2.0)
        .extrude(EXHAUST_DUCT_LENGTH)
    )
    parts.append(collar.val())

    return cq.Workplane(cq.Compound.makeCompound(parts))
