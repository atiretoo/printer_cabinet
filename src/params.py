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
Parametric configuration and global constants for the printer cabinet CAD model.

Coordinate System Standard:
  - +X = Right, -X = Left (Width = 24.0" / 609.6 mm, centered at X = 0)
  - +Y = Rear,  -Y = Front (Depth = 24.0" / 609.6 mm, centered at Y = 0)
  - +Z = Up,    -Z = Down  (Height = 72.0" / 1828.8 mm, Floor at Z = 0)
"""

# ==============================================================================
# 1. OVERALL ENCLOSURE DIMENSIONS
# ==============================================================================
INCH_TO_MM = 25.4

CABINET_WIDTH = 24.0 * INCH_TO_MM     # 609.6 mm (~2 ft)
CABINET_DEPTH = 24.0 * INCH_TO_MM     # 609.6 mm (~2 ft)
CABINET_HEIGHT = 72.0 * INCH_TO_MM    # 1828.8 mm (~6 ft)

# Sheet Goods Thicknesses
PLY_THICKNESS = 0.75 * INCH_TO_MM     # 19.05 mm (3/4" Baltic Birch plywood)
BACK_THICKNESS = 0.50 * INCH_TO_MM    # 12.70 mm (1/2" Baltic Birch back panel)
TRAY_LIP_THICKNESS = 0.50 * INCH_TO_MM# 12.70 mm (1/2" plywood for pull-out tray lips)
ACRYLIC_THICKNESS = 3.0               # 3.00 mm (1/8" clear acrylic door pane)

# Inside Usable Dimensions
INSIDE_WIDTH = CABINET_WIDTH - 2 * PLY_THICKNESS   # 571.50 mm (22.5")
INSIDE_DEPTH = CABINET_DEPTH - BACK_THICKNESS      # 596.90 mm (23.5")
FRONT_FACE_Y = -CABINET_DEPTH / 2.0                # -304.80 mm
REAR_FACE_Y = CABINET_DEPTH / 2.0                  # +304.80 mm
INSIDE_FRONT_Y = FRONT_FACE_Y                      # -304.80 mm
INSIDE_REAR_Y = REAR_FACE_Y - BACK_THICKNESS       # +292.10 mm

# Base / Plinth (Toe-kick) and Vibration Isolation Feet
VIBRATION_FEET_HEIGHT = 20.0                       # 20.00 mm heavy-duty rubber leveling feet
VIBRATION_FEET_DIAMETER = 60.0                     # 60.00 mm diameter elastomer base
PLINTH_WOOD_HEIGHT = 50.0                          # 50.00 mm wood plinth frame
PLINTH_TOTAL_HEIGHT = VIBRATION_FEET_HEIGHT + PLINTH_WOOD_HEIGHT # 70.00 mm total base height
PLINTH_SETBACK_FRONT = 1.5 * INCH_TO_MM            # 38.10 mm
PLINTH_SETBACK_SIDES = 0.75 * INCH_TO_MM           # 19.05 mm

# ==============================================================================
# 2. VERTICAL ELEVATIONS AND COMPARTMENT HEIGHTS (BOTTOM UP)
# ==============================================================================
# Floor: Z = 0
Z_FEET_BOTTOM = 0.0
Z_PLINTH_BOTTOM = VIBRATION_FEET_HEIGHT            # 20.00 mm
Z_PLINTH_TOP = PLINTH_TOTAL_HEIGHT                 # 70.00 mm

# Bottom Panel
Z_BOTTOM_PANEL_BOTTOM = Z_PLINTH_TOP               # 70.00 mm
Z_BOTTOM_PANEL_TOP = Z_BOTTOM_PANEL_BOTTOM + PLY_THICKNESS  # 89.05 mm

# Zone 4: Paper Storage Bay (Lowest - serves as 30+ kg low-CG acoustic ballast)
PAPER_BAY_HEIGHT = 330.0                           # 330.00 mm (~13.00")

# Divider Shelf (above paper storage / below scanner)
Z_LOWER_DIVIDER_BOTTOM = Z_BOTTOM_PANEL_TOP + PAPER_BAY_HEIGHT  # 419.05 mm
Z_LOWER_DIVIDER_TOP = Z_LOWER_DIVIDER_BOTTOM + PLY_THICKNESS    # 438.10 mm

# Zone 3: Inkjet / Scanner Pull-Out Bay
SCANNER_BAY_HEIGHT = 270.0                         # 270.00 mm (~10.63")

# 3D Printer Solid Shelf (Double-Laminated 1.5" Baltic Birch for mass & stiffness)
PRINTER_SHELF_THICKNESS = 2 * PLY_THICKNESS        # 38.10 mm (1.5" laminated shelf)
Z_PRINTER_SHELF_BOTTOM = Z_LOWER_DIVIDER_TOP + SCANNER_BAY_HEIGHT # 708.10 mm
Z_PRINTER_SHELF_TOP = Z_PRINTER_SHELF_BOTTOM + PRINTER_SHELF_THICKNESS # 746.20 mm

# Vibration Decoupling Platform (Under 3D Printer)
ISOLATION_PAD_THICKNESS = 12.0                     # 12.00 mm high-density closed-cell EVA / Sorbothane
PAVER_WIDTH = 450.0                                # 450.00 mm (~17.7" concrete / granite paver)
PAVER_DEPTH = 450.0                                # 450.00 mm
PAVER_THICKNESS = 45.0                             # 45.00 mm (~1.77" thickness, ~22 kg inertia ballast)

Z_PAD_BOTTOM = Z_PRINTER_SHELF_TOP                 # 746.20 mm
Z_PAD_TOP = Z_PAD_BOTTOM + ISOLATION_PAD_THICKNESS # 758.20 mm
Z_PAVER_BOTTOM = Z_PAD_TOP                         # 758.20 mm
Z_PAVER_TOP = Z_PAVER_BOTTOM + PAVER_THICKNESS     # 803.20 mm

# Zone 2: 3D Printer Chamber (Prusa Core One+)
# Clearance above printer shelf to underside of dry shelf
PRINTER_BAY_HEIGHT = 693.80                        # 693.80 mm (~27.31")
# Clearance above printer top (Z_PAVER_TOP + 555mm = 1358.2mm) to dry shelf (1440mm) = ~82mm

# Zone 1 Floor: Filament Dry Chamber Shelf (with PTFE pass-through)
Z_DRY_SHELF_BOTTOM = Z_PRINTER_SHELF_TOP + PRINTER_BAY_HEIGHT     # 1440.00 mm
Z_DRY_SHELF_TOP = Z_DRY_SHELF_BOTTOM + PLY_THICKNESS             # 1459.05 mm

# Top Panel
Z_TOP_PANEL_TOP = CABINET_HEIGHT                   # 1828.80 mm (72.0")
Z_TOP_PANEL_BOTTOM = Z_TOP_PANEL_TOP - PLY_THICKNESS # 1809.75 mm

# Zone 1: Filament Dry Chamber Clear Height
DRY_BAY_HEIGHT = Z_TOP_PANEL_BOTTOM - Z_DRY_SHELF_TOP # 350.70 mm (~13.81")

# ==============================================================================
# 3. PULL-OUT SCANNER TRAY & HARDWARE
# ==============================================================================
SLIDE_THICKNESS = 0.50 * INCH_TO_MM                # 12.70 mm (standard slide clearance)
SLIDE_LENGTH = 22.0 * INCH_TO_MM                   # 558.80 mm
SLIDE_HEIGHT = 45.0                                # 45.00 mm

TRAY_WIDTH = INSIDE_WIDTH - 2 * SLIDE_THICKNESS    # 546.10 mm (21.5")
TRAY_DEPTH = 550.0                                 # 550.00 mm
TRAY_THICKNESS = PLY_THICKNESS                     # 19.05 mm
TRAY_LIP_HEIGHT = 32.0                             # 32.00 mm
TRAY_ELEVATION_ABOVE_DIVIDER = 15.0                # 15.00 mm clearance off divider shelf

# ==============================================================================
# 4. FILAMENT DRY CHAMBER & SEALED DOOR
# ==============================================================================
DOOR_FRAME_WIDTH = 50.0                            # 50.00 mm border
DOOR_GASKET_THICKNESS = 3.0                        # 3.00 mm compressed silicone bulb seal
DOOR_CLEARANCE = 2.0                               # 2.00 mm perimeter reveal

# Spool Rack & Desiccant Trays
SPOOL_DIAMETER = 200.0                             # Standard 1kg reel diameter
SPOOL_WIDTH = 65.0                                 # Standard 1kg reel width
ROLLER_DOWEL_DIAMETER = 25.4                       # 1" wooden dowel or aluminum rod
ROLLER_SPACING = 110.0                             # Center-to-center distance between rollers
ROLLER_ELEVATION = 45.0                            # Height above dry shelf

DESICCANT_TRAY_WIDTH = 250.0                       # 250.00 mm
DESICCANT_TRAY_DEPTH = 160.0                       # 160.00 mm
DESICCANT_TRAY_HEIGHT = 28.0                       # 28.00 mm

PTFE_TUBE_OD = 4.0                                 # 4.00 mm
PTFE_FITTING_HOLE_DIA = 10.0                       # 10.00 mm (M10 / PC4-M10 pass-through thread)
PTFE_PORT_OFFSETS_X = [-60.0, 60.0]                # Dual feed ports
PTFE_PORT_OFFSET_Y = 0.0                           # Centered over printer top inlet

# ==============================================================================
# 5. HARDWARE & EQUIPMENT BOUNDING SPECIFICATIONS
# ==============================================================================
# Prusa Core One+
PRUSA_CORE_ONE_WIDTH = 415.0                       # 415 mm (16.3")
PRUSA_CORE_ONE_DEPTH = 444.0                       # 444 mm (17.5")
PRUSA_CORE_ONE_HEIGHT = 555.0                      # 555 mm (21.8")
PRUSA_CORE_ONE_WEIGHT_KG = 22.5

# Epson Inkjet / Scanner (e.g., EcoTank ET-2800 series)
EPSON_SCANNER_WIDTH = 375.0                        # 375 mm (14.8")
EPSON_SCANNER_DEPTH = 347.0                        # 347 mm (13.7")
EPSON_SCANNER_HEIGHT_CLOSED = 179.0                # 179 mm (7.0")
EPSON_SCANNER_HEIGHT_OPEN = 380.0                  # 380 mm (15.0" lid open)
