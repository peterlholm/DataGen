"Utils for blender picture generation"
from pathlib import Path
import open3d as o3d

TEST_MODEL = Path(__file__).parent.parent / "models" / "small_r.stl"

_DEBUG = False

def show_objects(objlist, name=""):
    "Show the object list"
    o3d.visualization.draw_geometries(objlist, window_name=name, width=1000, height=1000, point_show_normal=False, mesh_show_wireframe=False)

def obj_size(obj : o3d.geometry.TriangleMesh):
    "calculate average size of mesh"
    max_size = obj.get_max_bound()
    min_size = obj.get_min_bound()
    s = 0
    for i in range(2):
        s += max_size[i] - min_size[i]
    s = s / 3
    return s


def pcl2pic(objects, outfile: Path = None, name=""):
    "Make a jpg file from pcl"
    ZOOM = 1
    CAM_POSITION = [0.0, -0.1, 0.1]
    LOOK_AT = (-0.004, -0.05, -0.01)
    UP = (0.0, 1.0, 0.0)

    coord = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.001,origin=(0,0,0))

    obj_center = objects[0].get_center()
    ob_size = obj_size(objects[0])
    vis = o3d.visualization.Visualizer()
    res = vis.create_window(visible = _DEBUG, window_name=name, width=1000, height=1000)
    if not res:
        print("create window result", res)
    for obj in objects:
        if not obj.has_triangle_normals():
            obj.compute_triangle_normals()
        vis.add_geometry(obj)
    vis.add_geometry(coord)
    ctr = vis.get_view_control()
    if ctr is None:
        print("pcl2jpg cant get view_control", vis)
    if _DEBUG:
        print('object center', obj_center, "object size", ob_size)
        print("cam position:", CAM_POSITION, "zoom", ZOOM)
    ctr.set_front(CAM_POSITION)
    #ctr.set_lookat(LOOK_AT)
    ctr.set_lookat(obj_center)
    ctr.set_up(UP)
    ctr.set_zoom(ZOOM)
    #ctr.set_front([2.0, 0.1, -3])

    #render
    opt = vis.get_render_option()
    opt.point_size = 3.0
    if _DEBUG:
        vis.run()
    if outfile:
        if _DEBUG:
            print(f"Witing to outfile {outfile}")
        vis.capture_screen_image(str(outfile), do_render=True)

if __name__ == "__main__":
    mymesh = o3d.io.read_triangle_mesh(str(TEST_MODEL))
    if not mymesh.has_triangle_normals():
        mymesh.compute_triangle_normals()
    #show_objects([mymesh])
    pcl2pic([mymesh],"ud.png","ud.png")
