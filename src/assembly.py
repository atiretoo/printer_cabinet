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
Full cabinet assembly coordinating all structural, mechanical, and equipment elements.
"""

from typing import List, Tuple, Dict
import cadquery as cq

from carcass import make_side_panel, make_plinth_assembly, make_back_panel, make_isolation_feet
from shelves import (
    make_bottom_panel,
    make_lower_divider,
    make_printer_shelf,
    make_isolation_pad,
    make_paver_slab,
    make_dry_shelf,
    make_top_panel,
)
from pullout import make_tray_assembly, make_slides
from drybox import (
    make_sealed_door_frame,
    make_door_acrylic,
    make_door_gasket,
    make_spool_rack,
    make_filament_spools,
    make_desiccant_trays,
    make_ptfe_tubes,
)
from mockups import (
    make_prusa_core_one,
    make_epson_scanner,
    make_paper_storage,
)


def get_cabinet_components(
    extension: float = 0.0,
    scanner_lid_angle: float = 0.0,
    include_mockups: bool = True,
) -> Dict[str, cq.Workplane]:
    """
    Returns a dictionary of named CadQuery Workplane solids for the full assembly.
    """
    components = {}

    # Carcass and Structural Joinery
    components["isolation_feet"] = make_isolation_feet()
    components["side_left"] = make_side_panel("left")
    components["side_right"] = make_side_panel("right")
    components["plinth"] = make_plinth_assembly()
    components["back_panel"] = make_back_panel()

    # Shelves & Vibration Decoupling Platform
    components["bottom_panel"] = make_bottom_panel()
    components["lower_divider"] = make_lower_divider()
    components["printer_shelf"] = make_printer_shelf()
    components["isolation_pad"] = make_isolation_pad()
    components["paver_slab"] = make_paver_slab()
    components["dry_shelf"] = make_dry_shelf()
    components["top_panel"] = make_top_panel()

    # Pull-out Scanner Shelf
    components["pullout_tray"] = make_tray_assembly(extension=extension)
    components["slides"] = make_slides(extension=extension)

    # Dry Chamber
    components["door_frame"] = make_sealed_door_frame()
    components["door_acrylic"] = make_door_acrylic()
    components["door_gasket"] = make_door_gasket()
    components["spool_rack"] = make_spool_rack()
    components["filament_spools"] = make_filament_spools(count=5)
    components["desiccant_trays"] = make_desiccant_trays()
    components["ptfe_tubes"] = make_ptfe_tubes()

    # Optional Equipment Mockups
    if include_mockups:
        components["prusa_core_one"] = make_prusa_core_one()
        components["epson_scanner"] = make_epson_scanner(
            extension=extension, lid_angle_deg=scanner_lid_angle
        )
        components["paper_storage"] = make_paper_storage()

    return components


def build_full_compound(
    extension: float = 0.0,
    scanner_lid_angle: float = 0.0,
    include_mockups: bool = True,
) -> cq.Workplane:
    """
    Combines all components into a single unified compound Workplane.
    """
    comp_dict = get_cabinet_components(
        extension=extension,
        scanner_lid_angle=scanner_lid_angle,
        include_mockups=include_mockups,
    )
    solids = [wp.val() for wp in comp_dict.values()]
    return cq.Workplane(cq.Compound.makeCompound(solids))
