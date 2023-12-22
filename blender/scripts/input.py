"module for startting input"
from pathlib import Path
from shutil import copy2
import open3d as o3d
from utils import pcl2pic


INFOLDER = Path(__file__).parent.parent / "input"
OUTFOLDER =  Path(__file__).parent.parent / "output"

# input folder hold stl files with different names
# the stlfiles must be normalized to top at y=0 and size about 1 cm eg 0.01

def get_model_list(folder):
    "get a list of models from folder"
    modellist = []
    modelfolder = folder / "models"
    for file in modelfolder.glob("*.stl"):
        modellist.append(file)
    return modellist

def make_model_picture(file):
    "create a png picture of stl file"
    mymesh = o3d.io.read_triangle_mesh(str(file))
    pcl2pic([mymesh], file.with_suffix(".png"))

def prepare_output(inmodel, translist):
    "copy original to folders"
    outfolder = OUTFOLDER / inmodel.stem
    outfolder.mkdir(exist_ok=True)
    copy2(inmodel, outfolder / inmodel.name)
    copy2(inmodel.with_suffix(".png"), outfolder / (inmodel.stem + '.png'))
    copy2(translist, outfolder)
    return outfolder

if __name__ == "__main__":
    models = get_model_list(INFOLDER)
    print("Models", models)
    for model in models:
        make_model_picture(model)
        prepare_output(model, INFOLDER / 'translist.npy')
