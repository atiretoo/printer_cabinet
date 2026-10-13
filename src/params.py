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
DRAWER_PLY_THICKNESS = 0.50 * INCH_TO_MM # 12.70 mm (1/2" Baltic Birch for drawer box)
BACK_THICKNESS = 0.50 * INCH_TO_MM    # 12.70 mm (1/2" Baltic Birch back panel)
TRAY_LIP_THICKNESS = 0.50 * INCH_TO_MM# 12.70 mm (1/2" plywood for pull-out tray lips)
ACRYLIC_THICKNESS = 3.0               # 3.00 mm (1/8" clear acrylic door panes)

# Inside Usable Dimensions
INSIDE_WIDTH = CABINET_WIDTH - 2 * PLY_THICKNESS   # 571.50 mm (22.5")
INSIDE_DEPTH = CABINET_DEPTH - BACK_THICKNESS      # 596.90 mm (23.5")
FRONT_FACE_Y = -CABINET_DEPTH / 2.0                # -304.80 mm
REAR_FACE_Y = CABINET_DEPTH / 2.0                  # +304.80 mm
INSIDE_FRONT_Y = FRONT_FACE_Y                      # -304.80 mm
INSIDE_REAR_Y = REAR_FACE_Y - BACK_THICKNESS       # +292.10 mm

# Base / Plinth & Leveling Feet
VIBRATION_FEET_HEIGHT = 20.0                       # 20.00 mm heavy-duty rubber leveling feet
VIBRATION_FEET_DIAMETER = 60.0                     # 60.00 mm diameter elastomer base
PLINTH_WOOD_HEIGHT = 55.0                          # 55.00 mm wood plinth frame (houses bottom paver)
PLINTH_TOTAL_HEIGHT = VIBRATION_FEET_HEIGHT + PLINTH_WOOD_HEIGHT # 75.00 mm total base height
PLINTH_SETBACK_FRONT = 1.5 * INCH_TO_MM            # 38.10 mm
PLINTH_SETBACK_SIDES = 0.75 * INCH_TO_MM           # 19.05 mm

# Concrete / Granite Inertia Pavers (Dual Ballast: Bottom Base + Printer Platform)
PAVER_WIDTH = 450.0                                # 450.00 mm (~17.7" square paver)
PAVER_DEPTH = 450.0                                # 450.00 mm
PAVER_THICKNESS = 45.0                             # 45.00 mm (~1.77" thickness, ~22 kg each)
ISOLATION_PAD_THICKNESS = 12.0                     # 12.00 mm high-density closed-cell damping pad

# ==============================================================================
# 2. VERTICAL ELEVATIONS AND COMPARTMENT HEIGHTS (BOTTOM UP)
# ==============================================================================
# Floor: Z = 0
Z_FEET_BOTTOM = 0.0
Z_PLINTH_BOTTOM = VIBRATION_FEET_HEIGHT            # 20.00 mm
Z_PLINTH_TOP = PLINTH_TOTAL_HEIGHT                 # 75.00 mm

# Bottom Ballast Paver (Under bottom shelf, inside plinth)
Z_BOTTOM_PAVER_BOTTOM = Z_PLINTH_BOTTOM + 5.0      # 25.00 mm
Z_BOTTOM_PAVER_TOP = Z_BOTTOM_PAVER_BOTTOM + PAVER_THICKNESS # 70.00 mm

# Bottom Panel (above plinth / ballast compartment)
Z_BOTTOM_PANEL_BOTTOM = Z_PLINTH_TOP               # 75.00 mm
Z_BOTTOM_PANEL_TOP = Z_BOTTOM_PANEL_BOTTOM + PLY_THICKNESS  # 94.05 mm

# Zone 5: Paper Storage Bay (Reduced height)
PAPER_BAY_HEIGHT = 180.0                           # 180.00 mm (~7.09", holds 6 reams letter paper)

# Divider Shelf 1 (above paper storage / below scanner bay)
Z_LOWER_DIVIDER_BOTTOM = Z_BOTTOM_PANEL_TOP + PAPER_BAY_HEIGHT  # 274.05 mm
Z_LOWER_DIVIDER_TOP = Z_LOWER_DIVIDER_BOTTOM + PLY_THICKNESS    # 293.10 mm

# Zone 4: Inkjet / Scanner Pull-Out Bay
SCANNER_BAY_HEIGHT = 230.0                         # 230.00 mm (~9.06")

# Divider Shelf 2 (above scanner bay / below tool drawer)
Z_TOOL_DIVIDER_BOTTOM = Z_LOWER_DIVIDER_TOP + SCANNER_BAY_HEIGHT # 523.10 mm
Z_TOOL_DIVIDER_TOP = Z_TOOL_DIVIDER_BOTTOM + PLY_THICKNESS       # 542.15 mm

# Zone 3: Shallow Tool Drawer Bay
TOOL_DRAWER_BAY_HEIGHT = 90.0                      # 90.00 mm (~3.54")

# 3D Printer Solid Shelf (Double-Laminated 1.5" Baltic Birch for maximum mass/stiffness)
PRINTER_SHELF_THICKNESS = 2 * PLY_THICKNESS        # 38.10 mm (1.5" laminated shelf)
Z_PRINTER_SHELF_BOTTOM = Z_TOOL_DIVIDER_TOP + TOOL_DRAWER_BAY_HEIGHT # 632.15 mm
Z_PRINTER_SHELF_TOP = Z_PRINTER_SHELF_BOTTOM + PRINTER_SHELF_THICKNESS # 670.25 mm

# Upper Vibration Decoupling Platform (Under 3D Printer)
Z_PAD_BOTTOM = Z_PRINTER_SHELF_TOP                 # 670.25 mm
Z_PAD_TOP = Z_PAD_BOTTOM + ISOLATION_PAD_THICKNESS # 682.25 mm
Z_PAVER_BOTTOM = Z_PAD_TOP                         # 682.25 mm
Z_PAVER_TOP = Z_PAVER_BOTTOM + PAVER_THICKNESS     # 727.25 mm

# Zone 2: 3D Printer Chamber (Prusa Core One+ with Door & Exhaust Fan)
PRINTER_BAY_HEIGHT = 730.0                         # 730.00 mm (~28.74")
# Top of printer is Z_PAVER_TOP + 555mm = 1282.25mm.
# Underside of dry shelf is 670.25 + 730 = 1400.25mm.
# Vertical clearance above printer = 1400.25 - 1282.25 = 118.0 mm (~4.65") for reverse Bowden tube.

# Zone 1 Floor: Filament Dry Chamber Shelf (with PTFE pass-through)
Z_DRY_SHELF_BOTTOM = Z_PRINTER_SHELF_TOP + PRINTER_BAY_HEIGHT     # 1400.25 mm
Z_DRY_SHELF_TOP = Z_DRY_SHELF_BOTTOM + PLY_THICKNESS             # 1419.30 mm

# Top Panel
Z_TOP_PANEL_TOP = CABINET_HEIGHT                   # 1828.80 mm (72.0")
Z_TOP_PANEL_BOTTOM = Z_TOP_PANEL_TOP - PLY_THICKNESS # 1809.75 mm

# Zone 1: Filament Dry Chamber Clear Height
DRY_BAY_HEIGHT = Z_TOP_PANEL_BOTTOM - Z_DRY_SHELF_TOP # 390.45 mm (~15.37")

# ==============================================================================
# 3. SHALLOW TOOL DRAWER & SCANNER PULL-OUT HARDWARE
# ==============================================================================
SLIDE_THICKNESS = 0.50 * INCH_TO_MM                # 12.70 mm (standard slide clearance)
SLIDE_LENGTH = 22.0 * INCH_TO_MM                   # 558.80 mm
SLIDE_HEIGHT = 45.0                                # 45.00 mm

# Shallow Tool Drawer
TOOL_DRAWER_WIDTH = INSIDE_WIDTH - 2 * SLIDE_THICKNESS  # 546.10 mm (21.5")
TOOL_DRAWER_DEPTH = 550.0                          # 550.00 mm
TOOL_DRAWER_BOX_HEIGHT = 65.0                      # 65.00 mm (fits 8U Gridfinity)
TOOL_DRAWER_FRONT_HEIGHT = 84.0                    # 84.00 mm false front
TOOL_DRAWER_WALL_THICKNESS = DRAWER_PLY_THICKNESS  # 12.70 mm
TOOL_DRAWER_BOTTOM_THICKNESS = DRAWER_PLY_THICKNESS# 12.70 mm

# Scanner Pull-Out Tray
TRAY_WIDTH = INSIDE_WIDTH - 2 * SLIDE_THICKNESS    # 546.10 mm (21.5")
TRAY_DEPTH = 550.0                                 # 550.00 mm
TRAY_THICKNESS = PLY_THICKNESS                     # 19.05 mm
TRAY_LIP_HEIGHT = 32.0                             # 32.00 mm
TRAY_ELEVATION_ABOVE_DIVIDER = 12.0                # 12.00 mm clearance off divider shelf

# ==============================================================================
# 4. ENCLOSURE DOORS & EXHAUST SYSTEM
# ==============================================================================
DOOR_FRAME_WIDTH = 50.0                            # 50.00 mm border
DOOR_GASKET_THICKNESS = 3.0                        # 3.00 mm compressed silicone seal
DOOR_CLEARANCE = 2.0                               # 2.00 mm perimeter reveal

# Exhaust Fan & Duct Flange (Venting out upper rear of printer bay to external window)
EXHAUST_FAN_SIZE = 120.0                           # 120.00 mm standard enclosure fan
EXHAUST_FAN_DEPTH = 25.0                           # 25.00 mm
EXHAUST_DUCT_DIA = 100.0                           # 100.00 mm (4" standard duct collar)
EXHAUST_DUCT_LENGTH = 40.0                         # 40.00 mm
EXHAUST_PORT_POS_X = 140.0                         # Offset to right of rear panel
EXHAUST_PORT_POS_Z = Z_DRY_SHELF_BOTTOM - 100.0    # Near top of printer chamber

# Acoustic Wall Tether Bracket (Upper rear)
WALL_TETHER_WIDTH = 75.0                           # 75.00 mm heavy-duty steel angle
WALL_TETHER_HEIGHT = 60.0                          # 60.00 mm
WALL_TETHER_DEPTH = 50.0                           # 50.00 mm
WALL_TETHER_GROMMET_DIA = 25.0                     # 25.00 mm neoprene isolation grommet

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
PTFE_FITTING_HOLE_DIA = 10.0                       # 10.00 mm (M10 / PC4-M10 pass-through)
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
