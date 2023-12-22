"Run the specified model"
from pathlib import Path
from time import perf_counter
from shutil import copy2
import numpy as np
import bpy

STANDARD_DIST = 0.01
INFOLDER = bpy.path.abspath("//input")
OUTFOLDER = bpy.path.abspath("//output")

TRANSFORMATION_FILE = "translist.npy"

_DEBUG = False

def import_object(filename : Path):
    "Import a stl file as object"
    filepath =  bpy.path.abspath(str(filename))
    bpy.ops.import_mesh.stl(filepath=filepath)
    ob_new = bpy.context.selected_objects[0]
    if _DEBUG:
        print(f"Importing {filepath} as {ob_new.name}")
    return ob_new

def move_to_std_position(obj):
    "move object to position"
    obj.location.z  -= STANDARD_DIST

def read_transformation_list(filename):
    "read list from file"
    arr = np.load(filename, allow_pickle=True)
    if _DEBUG:
        print("Reading Transformationlist")
    return arr

def pos_obj(obj, trans):
    "position object to trans"
    #print("position object from", obj.location, obj.rotation_euler)
    obj.location = trans[0]
    obj.rotation_euler = trans[1]
    #print("position object from", obj.location, obj.rotation_euler)

def render(outfile):
    "render the current scene to file" 
    #print("Now scanning to", outfile)
    if _DEBUG:
        print("Render to: ", outfile)
    bpy.context.scene.render.filepath = str(outfile)
    #print(bpy.context.scene.render.filepath)
    # Render still image, automatically write to output path
    bpy.ops.render.render(write_still=True)

def save_depth_map(filename):
    "generate npy file as depthmath"
    # get viewer pixels
    pixels = bpy.data.images['Viewer Node'].pixels
    print("Saving depthmap pixels", len(pixels)) # size is always width * height * 4 (rgba)
    # copy buffer to numpy array for faster manipulation
    arr = np.array(pixels[:])
    #print(arr)
    np.save(filename, arr, allow_pickle=True)

def render_list(obj, trans_list, outpath : Path):
    "render current object throug list positions"
    if _DEBUG:
        print("Render list to", outpath)
    i = 1
    fname = Path(outpath).stem
    for pos in trans_list:
        if _DEBUG:
            print(f"Rendering {i} Position: {pos[0]},{pos[1]}")
        pos_obj(obj, pos)
        path = outpath / (fname + "_" + str(i) )
        picture_path = str(path) + ".jpg"
        #print(picture_path)
        render(picture_path)
        save_depth_map(str(path) + ".npy")
        i += 1

def run_model(model, translist, outfolder):
    "Run the serie of positions for the given model and place result in folder"
    start_time = perf_counter()
    print(f"Running model: {model} to folder: {outfolder}")
    obj = import_object(model)
    move_to_std_position(obj)
    trans_list = read_transformation_list(translist)
    render_list(obj, trans_list, outfolder)
    bpy.data.objects.remove(obj, do_unlink=True)
    print("Model-time", start_time-perf_counter)

def get_input_models(infolder):
    "get the models and translist for generation"
    model_list = (infolder / 'models').glob("*.stl")
    trans_list = infolder / 'translist.npy'
    if (len(model_list) > 0) and translist.exists(): 
        for model in model_list:
            print(model)
            m_folder = Path(OUTFOLDER) / model.stem
            print(m_folder)
            m_folder.mkdir(exist_ok=True)
            copy2(model, m_folder / model.name)
            copy2(model.with_suffix(".png"), m_folder)
            copy2(trans_list, m_folder)
            run_model(model, trans_list, m_folder)
    else:
        print("missing modelfiles or translist")

#get_input_models(Path(INFOLDER))

MODEL = "cylinder.stl"
TRANSLIST = Path(INFOLDER) / "translist.npy"
Outfolder = Path(OUTFOLDER) / "cyl"
Model = Path(INFOLDER) / 'models' / MODEL
name = Path(Model).stem
print(Model)
print(TRANSLIST)
print(Outfolder)
run_model(Model, TRANSLIST, Outfolder)

print("----FINISH-----")
