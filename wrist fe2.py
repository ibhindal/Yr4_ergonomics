import numpy as np
from sfepy import data_dir
from sfepy.base.base import Struct
from sfepy.discrete import (FieldVariable, Material, Integral, Function,
                            Equation, Equations, Problem)
from sfepy.discrete.fem import Mesh, FEDomain, Field
from sfepy.discrete.fem.meshio import UserMeshIO
from sfepy.mesh.mesh_generators import gen_block_mesh
from sfepy.mechanics.matcoefs import stiffness_from_lame


# Define the Lamé constants for the bone and the soft tissue
lam_bone = 1.0
mu_bone = 1.0
lam_tissue = 2.0
mu_tissue = 2.0

# Define the stiffness matrices for the bone and the soft tissue
D_bone = stiffness_from_lame(dim=2, lam=lam_bone, mu=mu_bone)
D_tissue = stiffness_from_lame(dim=2, lam=lam_tissue, mu=mu_tissue)

# Define the materials for the bone and the soft tissue
bone_mat = Material('bone_mat', D=D_bone)
tissue_mat = Material('tissue_mat', D=D_tissue)

# Define the mesh and the domain
filename_mesh = 'combined.vtk'
mesh = Mesh.from_file(filename_mesh)
domain = FEDomain('domain', mesh)


# Define the region
region = domain.create_region('Omega', 'all')

# Define the field
field = Field.from_args('fu', np.float64, 'vector', region, approx_order=1)


# Define the field and the field variable

u = FieldVariable('u', 'unknown', field)

# Define the regions
region_bone = domain.create_region('Omega_bone', 'cells of group 1')
region_bone.material = bone_mat

region_tissue = domain.create_region('Omega_tissue', 'cells of group 2')
region_tissue.material = tissue_mat

region_load = domain.create_region('Gamma_load',
                                    'vertices of surface',
                                    'facet')

# Define the Dirichlet boundary condition
u_dirichlet = EssentialBC('u_dirichlet', region=region_bone, dofs='all',
                          val=np.zeros(3))

# Define the Neumann boundary condition
f = Function('load', lambda ts, coors, **kwargs: np.array([0, -1e3, 0]))
integral = Integral('i', order=2)
eq = Equation('balance', Integral('i', order=2, region=region_load),
              -integral.eval_on_facet('ev_surface_ltr', u, f=f,
                                      region=region_load))

# Define the equations
eqs = Equations([eq])

# Define the problem
problem = Problem('elasticity', equations=eqs)
problem.set_bcs(ebcs=Conditions([u_dirichlet]))
problem.set_solver_options(max_iterations=100)

# Solve the problem
state = problem.solve()

# Export the deformed mesh
out = mesh.transform(state)
filename = 'wrist_deformed.vtk'
out.write(filename)
