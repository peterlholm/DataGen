"crete file with translations"

# import sys
# from pathlib import Path
# import argparse
import open3d as o3d

_DEBUG = True

FILE="tand.stl"

def show_objects(objlist, name=""):
    "Show the object list"
    o3d.visualization.draw_geometries(objlist, window_name=name, width=1000, height=1000, point_show_normal=False, mesh_show_wireframe=False)

mymesh = o3d.io.read_triangle_mesh(FILE)

center = mymesh.get_center()
print("Center", mymesh.get_center())


mymesh.translate((-center[0], -center[1], -center[2]))
print("Center", mymesh.get_center())
mymax = mymesh.get_max_bound()
print("Max", mymax)
mymesh.translate((0, -mymax[1], 0))
mymesh.scale(0.001,[0,0,0])
mymesh.compute_triangle_normals()

o3d.io.write_triangle_mesh('copy.ply', mymesh)
o3d.io.write_triangle_mesh('copy.stl', mymesh)
coord = o3d.geometry.TriangleMesh.create_coordinate_frame(size=10, origin=(0,0,0))
show_objects([mymesh, coord])
