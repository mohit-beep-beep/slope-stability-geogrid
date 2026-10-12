"""
Geogrid-Reinforced Slope Stability AI Research
Baseline 01: unreinforced, homogeneous slope in OPTUM GX.

This script adapts the OPTUM GX documentation example supplied by the user.
It intentionally starts with an unreinforced homogeneous soil model. Geogrids
and parameter sweeps will be added only after this baseline has been checked.

Important:
- Run with the Python environment supplied/configured for your OPTUM GX version.
- Soil parameters below are illustrative starting values, not site-specific design data.
- Confirm the unit convention used by your OPTUM GX installation and supervisor.
- This script has not been executed here because OPTUM GX is not available in this environment.
"""

import os
from OptumGX import *

# ---------------------------------------------------------------------
# 1. Application and project
# ---------------------------------------------------------------------
gx = GX()
project_name = "Geogrid Slope AI - Baseline 01"
prj = gx.create_project(project_name)

# Start with a clean current model, following the documentation example.
prj.get_current_model().delete()

# ---------------------------------------------------------------------
# 2. Geometry: 2D plane-strain homogeneous slope
# ---------------------------------------------------------------------
model = prj.create_model("Homogeneous unreinforced slope", model_type="plane_strain")
stage = model.create_stage("Baseline factor of safety")

# Coordinates follow the supplied OPTUM GX example.
# Crest: y = 0; toe: (16, -7); base: y = -9.
model.add_polygon(
    points=[
        [0, 0],
        [8, 0],
        [16, -7],
        [21, -7],
        [21, -9],
        [0, -9],
    ]
)

# ---------------------------------------------------------------------
# 3. Soil material: one homogeneous Mohr-Coulomb domain
# ---------------------------------------------------------------------
# Illustrative parameters adapted from the documentation example.
# Confirm the units expected by your installed OPTUM GX version.
soil = prj.MohrCoulomb(
    name="Baseline soil - illustrative",
    color=rgb(119, 67, 56),
    E=25,
    nu=0.30,
    c=10,
    phi=20,
    gamma_dry=20,
    gamma_sat=20,
)

# Select the single soil face and assign the material.
soil_face = model.select(p0=[1, -1], types="face")
model.set_solid(shapes=soil_face, material=soil)

# ---------------------------------------------------------------------
# 4. Boundary conditions
# ---------------------------------------------------------------------
model.set_standard_fixities()

# ---------------------------------------------------------------------
# 5. Factor-of-safety analysis
# ---------------------------------------------------------------------
stage.set_analysis_properties(
    analysis_type="factor_of_safety",
    element_type="mixed",
    no_of_elements=1000,
    mesh_adaptivity="yes",
    adaptivity_iterations=3,
)

# ---------------------------------------------------------------------
# 6. Run and report the result
# ---------------------------------------------------------------------
print("Running baseline slope-stability analysis in OPTUM GX...")
prj.run_analysis()

fos = stage.output.global_results.factor_of_safety
print(f"Baseline factor of safety: {fos:.3f}")

# Zoom to fit the model in the OPTUM GX view.
model.zoom_all()

# ---------------------------------------------------------------------
# 7. Save the project and a small text result
# ---------------------------------------------------------------------
# Save into the current working directory. Change to False if you prefer
# to save manually from OPTUM GX.
save_project = True

if save_project:
    output_dir = os.getcwd()
    safe_project_name = "Geogrid_Slope_AI_Baseline_01.gxx"
    project_path = os.path.join(output_dir, safe_project_name)
    gx.save_project(file_path=project_path)
    print(f"OPTUM GX project save requested: {project_path}")

    result_path = os.path.join(output_dir, "baseline_result.txt")
    with open(result_path, "w", encoding="utf-8") as result_file:
        result_file.write("Project: Geogrid Slope AI - Baseline 01\n")
        result_file.write("Model: homogeneous unreinforced 2D plane-strain slope\n")
        result_file.write(f"Factor of safety: {fos:.6f}\n")
    print(f"Result record written to: {result_path}")
