"crete file with translations"
import sys
import copy
import numpy
import open3d as o3d

_DEBUG = True

FILE="tand.stl"

def show_objects(objlist, name=""):
    "Show the object list"
    o3d.visualization.draw_geometries(objlist, window_name=name, width=1000, height=1000, point_show_normal=False, mesh_show_wireframe=False)

def read_list(filename):
    "read list from file"
    arr = numpy.load(filename, allow_pickle=True)
    return arr

trans_list = read_list("data/translist.npy")
print("arr", trans_list)


#
meshlist = []

mymesh = o3d.io.read_triangle_mesh(FILE)
no=1
for trans in trans_list:
    mesh = copy.deepcopy(mymesh)
    print(trans)
    mesh.translate(trans[0])
    R = o3d.geometry.Geometry3D.get_rotation_matrix_from_axis_angle(trans[1])
    mesh.rotate(R)
    mesh.compute_triangle_normals()
    meshlist.append(mesh)
    no +=1

coord = o3d.geometry.TriangleMesh.create_coordinate_frame(size=10, origin=(0,0,0))
meshlist.append(coord)
#mymesh.compute_triangle_normals()
show_objects(meshlist)
