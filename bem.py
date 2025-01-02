#various installations: vtk, capytaine, pygmsh

#just a check 
msg = "Hello world"
print(msg)

#this line checks for installation, will print the version of capytaine installed 
import capytaine as cpt; print(cpt.__version__)
import vtk; print(vtk.__version__)
import pygmsh
from numpy import inf


#set and declare constants 
#info is estimate for AOA's off santa barbara
DENSITY = 1025.0 #kg/m^3
PERIOD_AVG = 8.41449 #in seconds 
OMEGA = 2*3.1415/PERIOD_AVG  #angular wave frequency in radians 
DEPTH = 90 #depth in meters
GRAVITY = 9.81


#get information on what Capytaine is doing
cpt.set_logging('INFO') #DEBUG gets more info, WARNING prints only warnings 

#import mesh
#to create your own mesh
#this is a test of pygmsh

#to import existing mesh file
#for common accepted fl types in .extension/name, .stl/stl; .gdf/gdf, .msh/msh
#note for some reason from rhino, gdfs work when marked as wamit, not gdf 
myMesh = cpt.load_mesh('meshes\\testsix.gdf', file_format = 'wamit')
#make body
#currently, set to have all 6 DOFs, but maybe we just want heave & yaw? or maybe heave, yaw, surge, pitch
#for DoFs (surge, sway, heave, roll, pitch, yaw), x y z? trans/rot
myMesh.show() #shows mesh
#note because it is a floatin body, mesh MUST intersect the surface AND go in the negative zed direction. you actually want the surface to be at 0
body = cpt.FloatingBody(mesh = myMesh, dofs = cpt.rigid_body_dofs(rotation_center = (0, 0, -0.3335)), center_of_mass = (0, 0, -0.3335), mass = 50)
#CANT HAVE MESH DISPLAY WINDOW OPEN - must close to run 
#3333mm OD, 1333mm ID, 667mm height

#hydrostatic computations 
hydrostatics = body.compute_hydrostatics(rho = DENSITY)
print(hydrostatics["disp_volume"]) #volume 
print(hydrostatics["hydrostatic_stiffness"])


#radiation problem (for heave DoF)
radiation_problem = cpt.RadiationProblem(body = body , radiating_dof = "Heave", omega = OMEGA, water_depth = 90, g = GRAVITY, rho = DENSITY)
print(radiation_problem.period)  #good to double check 

#diffraction problem (currently angle does not matter because device is symmetrical)
diffraction_problem = cpt.DiffractionProblem(body=body, wave_direction=0, omega=OMEGA)


#solve
solver = cpt.BEMSolver()
radiation_result = solver.solve(radiation_problem)
diffraction_result = solver.solve(diffraction_problem)







