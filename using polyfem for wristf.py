import polyfempy as pf
#import polyfempy.polyfempy_mesh as pf_mesh
import numpy as np

# Load the mesh file
mesh_path = "Squishy stuff.obj"

pf.load(mesh_path)


# Define the material properties of the structures in the wrist
youngs_modulus = 2.5e6  # Pa
poissons_ratio = 0.45
density = 1e3  # kg/m^3
print("1")
materials = [
    {"density": density, "youngs_modulus": youngs_modulus, "poissons_ratio": poissons_ratio},
    # Define additional materials for other structures in the wrist
    # ...
]

# Define the boundary conditions
displacement_boundary = {"dirichlet": {
    "boundary": mesh.boundaries_id["your_boundary_name"],
    "value": [0, 0, -0.1]  # Amount of displacement in the z-direction
}}
print("2")
# Define the problem settings
settings = {
    "problem": {
        "type": "elas",
        "youngs_modulus": youngs_modulus,
        "poissons_ratio": poissons_ratio,
        "density": density,
        "materials": materials
    },
    "solver": {
        "tolerance": 1e-9,
        "max_iterations": 10000,
        "type": "pardiso"
    },
    "boundary_conditions": displacement_boundary,
    "output": {
        "dir": "path/to/output/directory",
        "vtk_export": True,
        "vtk_compress": True
    }
}
print("3")
# Create and solve the problem
problem = pf.Problem()
problem.load_mesh(mesh)
problem.set_settings(settings)
problem.solve()

# Access the displacement, strain, and stress results
displacement = problem.displacements()
strain = problem.strain()
stress = problem.stress()
