"crete file with translations"
from pathlib import Path
# import argparse
import copy
import math
import numpy
import open3d as o3d

_DEBUG = True

FILE="small_r.stl"
ROTATION_NUMBER = 5
MIDT = int(ROTATION_NUMBER / 2)
ROTATION_STEP = 20   #degrees

#
# list format
#
#   [[location_x, location_y, location_z], [rotation_x, rotation_y, rotation_z]]
#

START_DIST = 0.015

def show_objects(objlist, name=""):
    "Show the object list"
    o3d.visualization.draw_geometries(objlist, window_name=name, width=1000, height=1000, point_show_normal=False, mesh_show_wireframe=False)

def generate_distances(mylist):
    "moving object away"
    ROTATION_NUMBER = 10
    step = 0.001    # mm
    for i in range(ROTATION_NUMBER):
        dist = START_DIST + i * step
        mylist.append(([0, 0, -dist], [0,0,0]))

def generate_rotations_x(mylist):
    "rotating about x"
    for r in range(ROTATION_NUMBER):
        print(r)
        v = (r - MIDT) * ROTATION_STEP/180*math.pi
        matrix = [[0, 0, -START_DIST],[v,0,0]]
        mylist.append(matrix)

def generate_rotations_y(mylist):
    "rotating about y"
    ROTATION_NUMBER = ROTATION_NUMBER

    for r in range(ROTATION_NUMBER):
        v = (r - MIDT) * ROTATION_STEP/180*math.pi
        matrix = [[0, 0, -START_DIST],[0,v,0]]
        mylist.append(matrix)

def generate_rotations_z(mylist):
    "rotating about z"
    ROTATION_NUMBER = ROTATION_NUMBER
    MIDT = int(ROTATION_NUMBER / 2)
    for r in range(ROTATION_NUMBER):
        v = (r - MIDT) * ROTATION_STEP/180*math.pi
        matrix = [[0, 0, -START_DIST],[0,0,v]]
        mylist.append(matrix)

def generate_rotations_ttrans(mylist):
    "rotate about z"
    ROTATION_NUMBER = 6
    MIDT = int(ROTATION_NUMBER / 2)
    step = 15    # degres
    for r in range(ROTATION_NUMBER):
        v = (r - MIDT) * step/180*math.pi
        co = math.cos(v)
        si = math.sin(v)
        matrix = [[co, -si, 0, 0],[si,co,0,0],[0, 0, 1, 0],[0,0,0,1]]
        mylist.append(matrix)

def save_list(translist, filename : Path):
    "save list in numpy file"
    numpy.save(filename, translist, allow_pickle=True)

trans_list = []

#generate_distances(trans_list)
generate_rotations_x(trans_list)
# generate_rotations_y(trans_list)
# generate_rotations_z(trans_list)

save_list(trans_list, "data/translist")

#print(trans_list)

if _DEBUG:
    meshlist = []
    mymesh = o3d.io.read_triangle_mesh(FILE)
    NO=1
    for trans in trans_list:
        mesh = copy.deepcopy(mymesh)
        mesh.translate(trans[0])
        R = o3d.geometry.Geometry3D.get_rotation_matrix_from_axis_angle(trans[1])
        mesh.rotate(R)
        mesh.compute_triangle_normals()
        FILENAME = "data/pic"+str(NO)+".stl"
        o3d.io.write_triangle_mesh(FILENAME, mesh)
        meshlist.append(mesh)
        NO +=1

    coord = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.010, origin=(0,0,0))
    meshlist.append(coord)
    show_objects(meshlist)
