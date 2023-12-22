"turn up to z axis"
import math
# import sys
# from pathlib import Path
# import argparse
import open3d as o3d

_DEBUG = True

FILE="small.stl"

def show_objects(objlist, name=""):
    "Show the object list"
    o3d.visualization.draw_geometries(objlist, window_name=name, width=1000, height=1000, point_show_normal=False, mesh_show_wireframe=False)

mymesh = o3d.io.read_triangle_mesh(FILE)
rot_matrix = o3d.geometry.Geometry3D.get_rotation_matrix_from_axis_angle([math.pi/2,0,0])
mymesh.rotate(rot_matrix, [0,0,0])
mymesh.compute_triangle_normals()
o3d.io.write_triangle_mesh("small_r.stl", mymesh)

coord = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.010, origin=(0,0,0))

show_objects([mymesh, coord])


# mymesh.translate((-center[0], -center[1], -center[2]))
# print("Center", mymesh.get_center())
