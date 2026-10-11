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
CAD Export utility for the printer cabinet project.

Exports:
  - STEP files for woodworking CAD modeling and full assembly verification.
  - STL files for 3D printable accessories (desiccant trays, roller brackets).
"""

import os
import sys
import cadquery as cq

sys.path.insert(0, os.path.dirname(__file__))

from assembly import build_full_compound, get_cabinet_components
from drybox import make_desiccant_trays, make_spool_rack


def export_cad_files(output_dir: str = None) -> None:
    """
    Exports STEP assembly and individual 3D-printable component STLs.
    """
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")
    os.makedirs(output_dir, exist_ok=True)

    print("Exporting Full Cabinet Assembly STEP file...")
    assy_compound = build_full_compound(extension=0.0, scanner_lid_angle=0.0, include_mockups=False)
    step_path = os.path.join(output_dir, "printer_cabinet_carcass.step")
    cq.exporters.export(assy_compound, step_path)
    print(f"Exported: {step_path}")

    print("Exporting Full Assembly with Mockups STEP file...")
    full_step_path = os.path.join(output_dir, "printer_cabinet_full_assembly.step")
    full_compound = build_full_compound(extension=350.0, scanner_lid_angle=70.0, include_mockups=True)
    cq.exporters.export(full_compound, full_step_path)
    print(f"Exported: {full_step_path}")

    # 3D Printable accessories: Desiccant trays
    print("Exporting Desiccant Tray STL...")
    tray = make_desiccant_trays()
    tray_stl_path = os.path.join(output_dir, "desiccant_tray.stl")
    cq.exporters.export(tray, tray_stl_path)
    print(f"Exported: {tray_stl_path}")


if __name__ == "__main__":
    export_cad_files()
