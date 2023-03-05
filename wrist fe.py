import os
import meshio
from sfepy.discrete.fem import Mesh, FEDomain, Field
from sfepy.discrete import (FieldVariable, Material, Integral,
                            Equation, Equations, Problem, Functions)
from sfepy.solvers.ls import ScipyDirect
from sfepy.base.base import Struct
from sfepy.discrete.functions import ConstantFunction
import numpy as np

#from sfepy.postprocess.viewer import Viewer

'''
os.chdir('./Yr4_ergonomics/')

stl1='combined.stl'

# Load the STL mesh file
stl_mesh = meshio.read(stl1)

# Write the VTK mesh to a file

meshio.write('combined.vtk', stl_mesh, file_format='vtk')
'''


# Read in the mesh from a VTK file
mesh = Mesh.from_file('combined.vtk')
cells = mesh.get_conn('2_3')


# Define the domain
domain = FEDomain('domain', mesh)

# Define the region
region = domain.create_region('Gamma1',
                              'vertices in (x < 0.1) & (z < 0.1)')

# Define the field
field = Field.from_args('fu', dtype=np.float64, shape=(3,), region=region, approx_order=1)

# Define the variables
variables = {
    'u': ('unknown field', field, 0),
    'v': ('test field', field, 1),
}

# Define the material
E = 1e6
nu = 0.3
D = (E / (1 - nu ** 2)) * np.array([[1, nu, 0], [nu, 1, 0], [0, 0, (1 - nu) / 2]])
material = Material('m', D=D)

# Define the functions
f = ConstantFunction(value=np.array([0, -1e3, 0]))
f.name = 'load'
bc_fun = Functions.bc('t', {'val': np.array([0, 0, 0]), 'region': 'Gamma1'})

# Define the equations
integral = Integral('i', order=2)
eq1 = Equation('balance_of_forces',
               integral(region, Dot(sigma(u), grad(v))) - integral(region, Dot(f, v)) == 0)
eq2 = Equation('boundary_condition',
               integral(region, Dot(u, v)) - integral(region, Dot(bc_fun(), v)) == 0)
eqs = Equations([eq1, eq2])

# Define the problem
pb = Problem('elasticity', equations=eqs, variables=variables, materials=[material])

# Define the solver
solver = ScipyDirect({})

# Solve the problem
state = pb.solve(solver=solver)

# Get the deformed mesh and output it to a VTK file
out = mesh.copy()
out.transform(state())
out.write('deformed_mesh.vtk')