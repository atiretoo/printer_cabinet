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
Carcass panel geometry, bottom ballast compartment, machine feet, and wall tether.
"""

from typing import Dict, Tuple, List
import cadquery as cq

from params import (
    CABINET_WIDTH,
    CABINET_DEPTH,
    CABINET_HEIGHT,
    PLY_THICKNESS,
    BACK_THICKNESS,
    PLINTH_TOTAL_HEIGHT,
    PLINTH_WOOD_HEIGHT,
    PLINTH_SETBACK_FRONT,
    INSIDE_WIDTH,
    FRONT_FACE_Y,
    REAR_FACE_Y,
    VIBRATION_FEET_HEIGHT,
    VIBRATION_FEET_DIAMETER,
    Z_PLINTH_BOTTOM,
    Z_BOTTOM_PAVER_BOTTOM,
    PAVER_WIDTH,
    PAVER_DEPTH,
    PAVER_THICKNESS,
    EXHAUST_DUCT_DIA,
    EXHAUST_PORT_POS_X,
    EXHAUST_PORT_POS_Z,
    WALL_TETHER_WIDTH,
    WALL_TETHER_HEIGHT,
    WALL_TETHER_DEPTH,
    WALL_TETHER_GROMMET_DIA,
)


def make_side_panel(side: str = "left") -> cq.Workplane:
    """
    Creates a single vertical side panel (3/4" Baltic birch).
    """
    panel = cq.Workplane("XY").box(PLY_THICKNESS, CABINET_DEPTH, CABINET_HEIGHT)

    # Toe-kick cutout at bottom front (-Y, -Z relative to center)
    notch_y = PLINTH_SETBACK_FRONT
    notch_z = PLINTH_TOTAL_HEIGHT
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
    x_pos = (-CABINET_WIDTH / 2.0 + PLY_THICKNESS / 2.0) if side == "left" else (CABINET_WIDTH / 2.0 - PLY_THICKNESS / 2.0)
    panel = panel.translate((x_pos, 0, CABINET_HEIGHT / 2.0))

    return panel


def make_plinth_assembly() -> cq.Workplane:
    """
    Creates the recessed toe-kick plinth frame at the base of the cabinet,
    housing the bottom inertia ballast paver.
    """
    plinth_parts = []
    plinth_mid_z = Z_PLINTH_BOTTOM + PLINTH_WOOD_HEIGHT / 2.0

    # Front toe-kick face board
    front_rail_y = FRONT_FACE_Y + PLINTH_SETBACK_FRONT + PLY_THICKNESS / 2.0
    front_rail = (
        cq.Workplane("XY")
        .box(INSIDE_WIDTH, PLY_THICKNESS, PLINTH_WOOD_HEIGHT)
        .translate((0, front_rail_y, plinth_mid_z))
    )
    plinth_parts.append(front_rail.val())

    # Rear ground rail
    rear_rail_y = REAR_FACE_Y - BACK_THICKNESS - PLY_THICKNESS / 2.0
    rear_rail = (
        cq.Workplane("XY")
        .box(INSIDE_WIDTH, PLY_THICKNESS, PLINTH_WOOD_HEIGHT)
        .translate((0, rear_rail_y, plinth_mid_z))
    )
    plinth_parts.append(rear_rail.val())

    # Left and right plinth cross stretchers
    stretcher_len = (rear_rail_y - PLY_THICKNESS / 2.0) - (front_rail_y + PLY_THICKNESS / 2.0)
    stretcher_mid_y = (front_rail_y + rear_rail_y) / 2.0
    for x_offset in [-INSIDE_WIDTH / 2.0 + PLY_THICKNESS / 2.0, INSIDE_WIDTH / 2.0 - PLY_THICKNESS / 2.0]:
        stretcher = (
            cq.Workplane("XY")
            .box(PLY_THICKNESS, stretcher_len, PLINTH_WOOD_HEIGHT)
            .translate((x_offset, stretcher_mid_y, plinth_mid_z))
        )
        plinth_parts.append(stretcher.val())

    return cq.Workplane(cq.Compound.makeCompound(plinth_parts))


def make_bottom_ballast_paver() -> cq.Workplane:
    """
    Creates the secondary concrete or granite inertia ballast paver (~22 kg)
    seated directly in the base plinth beneath the paper storage bay.
    Permanently anchors the base of the cabinet directly at floor level.
    """
    paver_mid_z = Z_BOTTOM_PAVER_BOTTOM + PAVER_THICKNESS / 2.0
    paver = (
        cq.Workplane("XY")
        .box(PAVER_WIDTH, PAVER_DEPTH, PAVER_THICKNESS)
        .translate((0, 0, paver_mid_z))
    )
    paver = paver.edges().chamfer(3.0)
    return paver


def make_isolation_feet() -> cq.Workplane:
    """
    Creates 4 heavy-duty industrial elastomer vibration-damping machine feet
    under the plinth base to decouple the entire cabinet from the floor.
    """
    feet_parts = []
    foot_mid_z = VIBRATION_FEET_HEIGHT / 2.0

    front_y = FRONT_FACE_Y + PLINTH_SETBACK_FRONT + 35.0
    rear_y = REAR_FACE_Y - BACK_THICKNESS - 35.0
    x_offset = INSIDE_WIDTH / 2.0 - 45.0

    for x_pos in [-x_offset, x_offset]:
        for y_pos in [front_y, rear_y]:
            foot = (
                cq.Workplane("XY")
                .cylinder(VIBRATION_FEET_HEIGHT, VIBRATION_FEET_DIAMETER / 2.0)
                .translate((x_pos, y_pos, foot_mid_z))
            )
            feet_parts.append(foot.val())

    return cq.Workplane(cq.Compound.makeCompound(feet_parts))


def make_wall_tether() -> cq.Workplane:
    """
    Creates an acoustic-decoupling wall tether bracket mounted at the upper rear.
    Consists of a heavy steel angle with a central vibration-damping neoprene grommet
    to secure against tall-cabinet sway without transmitting motor sound to the studs.
    """
    parts = []
    tether_z = CABINET_HEIGHT - WALL_TETHER_HEIGHT / 2.0
    tether_y = REAR_FACE_Y + WALL_TETHER_DEPTH / 2.0 - 3.0  # abuts wall

    # Steel angle bracket (3mm thick)
    bracket = (
        cq.Workplane("XY")
        .box(WALL_TETHER_WIDTH, WALL_TETHER_DEPTH, WALL_TETHER_HEIGHT)
        .translate((0, tether_y, tether_z))
    )
    # Inner cutout to form L-shape
    bracket_cut = (
        cq.Workplane("XY")
        .box(WALL_TETHER_WIDTH + 10.0, WALL_TETHER_DEPTH - 4.0, WALL_TETHER_HEIGHT - 4.0)
        .translate((0, tether_y - 2.0, tether_z + 2.0))
    )
    bracket = bracket.cut(bracket_cut)
    parts.append(bracket.val())

    # Neoprene rubber isolation bushing / grommet in wall-flange
    grommet = (
        cq.Workplane("YZ")
        .cylinder(12.0, WALL_TETHER_GROMMET_DIA / 2.0)
        .translate((0, REAR_FACE_Y + WALL_TETHER_DEPTH - 6.0, tether_z))
    )
    parts.append(grommet.val())

    return cq.Workplane(cq.Compound.makeCompound(parts))


def make_back_panel() -> cq.Workplane:
    """
    Creates the structural 1/2" Baltic birch inset back panel.
    Features a 4" (100 mm) round cutout for the 3D printer chamber exhaust duct.
    """
    back_h = CABINET_HEIGHT - PLINTH_TOTAL_HEIGHT
    back_z = PLINTH_TOTAL_HEIGHT + back_h / 2.0
    back_y = REAR_FACE_Y - BACK_THICKNESS / 2.0

    panel = (
        cq.Workplane("XY")
        .box(INSIDE_WIDTH, BACK_THICKNESS, back_h)
        .translate((0, back_y, back_z))
    )

    # Exhaust duct cutout: use cyclic ZX plane (# local (z, x), normal is +Y)
    duct_cutter = (
        cq.Workplane("ZX")
        .workplane(offset=back_y - BACK_THICKNESS)
        .center(EXHAUST_PORT_POS_Z, EXHAUST_PORT_POS_X)  # local (z, x)
        .circle(EXHAUST_DUCT_DIA / 2.0)
        .extrude(BACK_THICKNESS * 2)
    )
    panel = panel.cut(duct_cutter)

    return panel
