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
High-resolution off-screen technical rendering for the printer cabinet.

Uses CadQuery VTK polydata generation and vtkFeatureEdges to produce
clean architectural illustrations with distinct material palettes,
wood tones, transparent acrylic, and feature seam outlines.
"""

import os
import sys
from typing import List, Tuple, Dict, Optional
import cadquery as cq
import vtk

# Add src to path if executed standalone
sys.path.insert(0, os.path.dirname(__file__))

from assembly import get_cabinet_components
from params import (
    CABINET_WIDTH,
    CABINET_DEPTH,
    CABINET_HEIGHT,
)

# ==============================================================================
# Color Palette (Woodworking & Hardware Technical CAD)
# ==============================================================================
COLOR_BALTIC_BIRCH = (0.88, 0.80, 0.65)     # Warm Baltic birch plywood face
COLOR_PLY_EDGES    = (0.75, 0.63, 0.48)     # Slightly darker ply edge tone
COLOR_PLINTH       = (0.82, 0.74, 0.58)     # Sub-base lumber
COLOR_SLIDES       = (0.55, 0.58, 0.62)     # Zinc-plated steel drawer slides
COLOR_ACRYLIC      = (0.70, 0.85, 0.95)     # Translucent clear acrylic pane
COLOR_GASKET       = (0.20, 0.20, 0.22)     # Charcoal silicone bulb gasket
COLOR_PRUSA_BODY   = (0.18, 0.18, 0.20)     # Anthracite printer frame
COLOR_PRUSA_DOOR   = (0.45, 0.45, 0.50)     # Smoked transparent front door
COLOR_SCANNER      = (0.92, 0.92, 0.94)     # Clean office matte white/gray
COLOR_SCANNER_LID  = (0.25, 0.25, 0.27)     # Dark gray scanner platen lid
COLOR_PAPER        = (0.98, 0.98, 0.98)     # Bright white paper reams
COLOR_CARDBOARD    = (0.72, 0.58, 0.40)     # Kraft paper packaging
COLOR_PTFE         = (0.95, 0.95, 0.98)     # Translucent PTFE tubing
COLOR_DESICCANT    = (0.40, 0.60, 0.80)     # Silica gel indicator tray
COLOR_EDGE_LINE    = (0.12, 0.10, 0.08)     # Crisp dark seam outline

# Vibration Damping Palette
COLOR_PAVER        = (0.74, 0.73, 0.71)     # Dense concrete / granite inertia paver
COLOR_FOAM         = (0.28, 0.38, 0.48)     # High-density closed-cell damping pad
COLOR_FEET         = (0.18, 0.18, 0.20)     # Heavy-duty elastomeric machine feet

SPOOL_COLORS = [
    (0.95, 0.45, 0.10),  # Prusa Orange
    (0.15, 0.55, 0.85),  # Galaxy Blue
    (0.30, 0.75, 0.35),  # Forest Green
    (0.65, 0.35, 0.75),  # Deep Purple
    (0.90, 0.20, 0.25),  # Lipstick Red
]


def assign_component_colors(comp_dict: Dict[str, cq.Workplane]) -> List[Tuple[cq.Workplane, Tuple[float, float, float], float]]:
    """
    Pairs each named assembly solid with an RGB color and opacity.
    """
    items = []
    for name, wp in comp_dict.items():
        opacity = 1.0
        if "side_" in name or "panel" in name or "divider" in name or "shelf" in name or "door_frame" in name or "tray" in name:
            col = COLOR_BALTIC_BIRCH
        elif name == "plinth":
            col = COLOR_PLINTH
        elif name == "isolation_feet":
            col = COLOR_FEET
        elif name == "isolation_pad":
            col = COLOR_FOAM
        elif name == "paver_slab":
            col = COLOR_PAVER
        elif name == "slides":
            col = COLOR_SLIDES
        elif name == "door_acrylic":
            col = COLOR_ACRYLIC
            opacity = 0.55
        elif name == "door_gasket":
            col = COLOR_GASKET
        elif name == "spool_rack":
            col = COLOR_BALTIC_BIRCH
        elif name == "filament_spools":
            col = SPOOL_COLORS[0]
        elif name == "desiccant_trays":
            col = COLOR_DESICCANT
        elif name == "ptfe_tubes":
            col = COLOR_PTFE
        elif name == "prusa_core_one":
            col = COLOR_PRUSA_BODY
        elif name == "epson_scanner":
            col = COLOR_SCANNER
        elif name == "paper_storage":
            col = COLOR_PAPER
        else:
            col = COLOR_BALTIC_BIRCH

        items.append((wp, col, opacity))
    return items


def shape_to_polydata(shape: cq.Shape, tolerance: float = 0.5) -> vtk.vtkPolyData:
    """
    Converts a CadQuery Shape or Compound to vtkPolyData using native OpenCASCADE tessellation.
    Avoids VTK 9.5+ pipeline connection regressions in CadQuery's toVtkPolyData().
    """
    pts, triangles = shape.tessellate(tolerance)
    poly = vtk.vtkPolyData()

    vtk_pts = vtk.vtkPoints()
    vtk_pts.SetNumberOfPoints(len(pts))
    for i, p in enumerate(pts):
        vtk_pts.SetPoint(i, p.x, p.y, p.z)
    poly.SetPoints(vtk_pts)

    cells = vtk.vtkCellArray()
    for t in triangles:
        tri = vtk.vtkTriangle()
        tri.GetPointIds().SetId(0, t[0])
        tri.GetPointIds().SetId(1, t[1])
        tri.GetPointIds().SetId(2, t[2])
        cells.InsertNextCell(tri)
    poly.SetPolys(cells)

    # Compute smooth normals
    normals = vtk.vtkPolyDataNormals()
    normals.SetInputData(poly)
    normals.SetComputePointNormals(True)
    normals.SetComputeCellNormals(True)
    normals.SetFeatureAngle(45.0)
    normals.Update()
    return normals.GetOutput()


def render_scene(
    items: List[Tuple[cq.Workplane, Tuple[float, float, float], float]],
    output_path: str,
    camera_pos: Tuple[float, float, float] = (2400.0, -2800.0, 2100.0),
    focal_point: Tuple[float, float, float] = (0.0, 0.0, 914.4),
    view_up: Tuple[float, float, float] = (0.0, 0.0, 1.0),
    parallel_projection: bool = False,
    parallel_scale: float = 950.0,
    resolution: Tuple[int, int] = (1280, 960),
    feature_angle: float = 25.0,
    edge_width: float = 1.4,
    bg_color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
) -> None:
    """
    Renders CadQuery objects using off-screen VTK rendering with crisp feature edges.
    """
    ren = vtk.vtkRenderer()
    ren.SetBackground(*bg_color)

    for wp, color, opacity in items:
        poly = shape_to_polydata(wp.val())

        # Surface
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(poly)
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(*color)
        actor.GetProperty().SetOpacity(opacity)
        actor.GetProperty().SetAmbient(0.35)
        actor.GetProperty().SetDiffuse(0.65)
        actor.GetProperty().SetSpecular(0.08)
        ren.AddActor(actor)

        # Feature Edges (omits internal triangle seams, renders geometry edges)
        edges = vtk.vtkFeatureEdges()
        edges.SetInputData(poly)
        edges.BoundaryEdgesOn()
        edges.FeatureEdgesOn()
        edges.SetFeatureAngle(feature_angle)
        edges.ManifoldEdgesOff()
        edges.NonManifoldEdgesOff()

        edge_mapper = vtk.vtkPolyDataMapper()
        edge_mapper.SetInputConnection(edges.GetOutputPort())
        edge_mapper.SetResolveCoincidentTopologyToPolygonOffset()

        edge_actor = vtk.vtkActor()
        edge_actor.SetMapper(edge_mapper)
        edge_actor.GetProperty().SetColor(*COLOR_EDGE_LINE)
        edge_actor.GetProperty().SetLineWidth(edge_width)
        ren.AddActor(edge_actor)

    rw = vtk.vtkRenderWindow()
    rw.SetOffScreenRendering(1)
    rw.AddRenderer(ren)
    rw.SetSize(*resolution)

    cam = ren.GetActiveCamera()
    cam.SetPosition(*camera_pos)
    cam.SetFocalPoint(*focal_point)
    cam.SetViewUp(*view_up)
    if parallel_projection:
        cam.ParallelProjectionOn()
        cam.SetParallelScale(parallel_scale)

    ren.ResetCameraClippingRange()
    rw.Render()

    w2if = vtk.vtkWindowToImageFilter()
    w2if.SetInput(rw)
    w2if.Update()

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    writer = vtk.vtkPNGWriter()
    writer.SetFileName(output_path)
    writer.SetInputConnection(w2if.GetOutputPort())
    writer.Write()
    print(f"Generated render: {output_path}")


def render_all_views(output_dir: Optional[str] = None) -> None:
    """
    Renders four standard architectural views:
      1. Perspective Isometric (Overall Stowed)
      2. Front Orthographic Elevation
      3. Right Orthographic Elevation
      4. Perspective Isometric (Scanner Tray Extended & Open)
    """
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "exports")

    # 1. Stowed assembly
    comp_stowed = get_cabinet_components(extension=0.0, scanner_lid_angle=0.0, include_mockups=True)
    items_stowed = assign_component_colors(comp_stowed)

    print("Rendering Isometric View...")
    render_scene(
        items_stowed,
        output_path=os.path.join(output_dir, "cabinet_isometric.png"),
        camera_pos=(2300.0, -2600.0, 2000.0),
        focal_point=(0.0, 0.0, 914.4),
        resolution=(1280, 960),
    )

    print("Rendering Front Elevation...")
    render_scene(
        items_stowed,
        output_path=os.path.join(output_dir, "cabinet_front_elevation.png"),
        camera_pos=(0.0, -3200.0, 914.4),
        focal_point=(0.0, 0.0, 914.4),
        parallel_projection=True,
        parallel_scale=960.0,
        resolution=(1024, 1280),
    )

    print("Rendering Right Elevation...")
    render_scene(
        items_stowed,
        output_path=os.path.join(output_dir, "cabinet_right_elevation.png"),
        camera_pos=(3200.0, 0.0, 914.4),
        focal_point=(0.0, 0.0, 914.4),
        parallel_projection=True,
        parallel_scale=960.0,
        resolution=(1024, 1280),
    )

    # 2. Scanner Extended & Lid Open View
    comp_extended = get_cabinet_components(extension=420.0, scanner_lid_angle=75.0, include_mockups=True)
    items_extended = assign_component_colors(comp_extended)

    print("Rendering Scanner Extended View...")
    render_scene(
        items_extended,
        output_path=os.path.join(output_dir, "cabinet_scanner_extended.png"),
        camera_pos=(2300.0, -2600.0, 1600.0),
        focal_point=(0.0, -100.0, 800.0),
        resolution=(1280, 960),
    )


if __name__ == "__main__":
    render_all_views()
