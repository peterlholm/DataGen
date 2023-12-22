import sys, os
from pathlib import Path
from shutil import copy, rmtree
import bpy
from math import pi
from time import sleep

tand="Tooth_H003046.res"

def set_object_position(nr):
    positions = [(0,0,0),(20,0,0),(-20,0,0),(0,20,0),(0,-20,0),(0,0,20),(0,0,-20)]
    obj = bpy.data.collections['Objects'].objects['tand']
    rot = positions[nr]
    obj_rot = (rot[0]/180*pi,rot[1]/180*pi,rot[2]/180*pi)
    obj.rotation_euler = obj_rot

def set_plane_pos(nr):
    positions = [ -0.01,-0.015,-0.020,-0.03]
    obj = bpy.data.collections['Objects'].objects['1cm_2400']
    #rot = positions[nr]
    dist = -0.03 + nr * 0.002
    obj.location = (0,0, dist)

def render(outfile):
    "render the current scene to file" 
    #print("Now scanning to", outfile)
    print("Outfile: ", outfile)
    bpy.context.scene.render.filepath = str(outfile)
    #print(bpy.context.scene.render.filepath)
    # Render still image, automatically write to output path
    bpy.ops.render.render(write_still=True)

def render_object(obj, path):
    copy(obj, path)
    #load_object(obj)
    for pos in range(3):
        set_object_position(pos)
        outfile = path / f"file{pos}.png"
        #print(outfile)
        render(outfile)

def render_plane(path):
    #copy(obj, path)
    #load_object(obj)
    for pos in range(12):
        set_plane_pos(pos)
        outfile = "//" + str(path / f"file{pos}.png")
        #print(outfile)
        render(outfile)
        
def get_object_list(path):
    #imagePath = Path(sys.argv[-1])
    imagePath = Path(path)
    #print("ImagePath", imagePath)
    obj_list = []
    if not imagePath.is_dir():
        print(f"Imagepath is not folder {imagePath}")
    else:
        for o in imagePath.glob('*.stl'):
            #print(o)
            obj_list.append(o)
        
    #print("Objlist", obj_list)
    return obj_list
    

def run_planes():
    outfolder = Path("output")
    print("Outputfolder:", outfolder)
    rmtree(outfolder, ignore_errors=True)
    outfolder.mkdir()
    foldernr = 1

    folder = outfolder / str(foldernr)
    print(folder)
    folder.rmdir
    folder.mkdir(exist_ok=True)
    #copy(obj, folder)
    render_plane(folder)

def run_tooth():
    outfolder = Path("output")
    print("Outputfolder:", outfolder)
    rmtree(outfolder, ignore_errors=True)
    #outfolder.mkdir()

    folder = "//output/" 
    #print(folder)
    for pos in range(7):
        set_object_position(pos)
        outfile = folder + f"file{pos}.png"
        print(outfile)
        render(outfile)


def run_folder(path):
    obj_list = get_object_list(folder)
    run_list(obj_list)
    
def get_folder_param():
    # Run as: blender -b <filename> -P <this_script> -- <image_folder_path>
    print("Starting render script")
    folderPath = Path(sys.argv[-1])
    print("folderPath", folderPath)
    if not folderPath.is_dir():
        print(f"folder: {folderPath} does not exist")
        return None
    return folderPath

#run_list(get_object_list('objects'))

#print("Running rendering script")
#folder = get_folder_param()
#run_folder(folder)

#run_planes()

print("Outfolder: ", bpy.context.scene.render.filepath)

run_tooth()
