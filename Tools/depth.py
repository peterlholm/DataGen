"Test depth"
from pathlib import Path
from PIL import Image
import numpy as np

FIL= Path("data/depth.npy")
IMG = Path('data/obj.png')
OUT = Path('data/depth.png')

def show_png(fil):
    "show std png file"
    print("--------PNG-----------")
    img = Image.open(fil)
    img.show()
    print(img.getpixel((0,0)))
    np_arr = np.array(img)

    print("PNG number dimensions", np_arr.ndim)
    print("shape", np_arr.shape)
    print("size", np_arr.size)
    print("datatype", np_arr.dtype)

    for i in range(5):
        print(np_arr[0,i])
    print("jj")
    for i in range(5):
        print(np_arr[i,0])

def show_np(file):
    print("-----------NP-----------")
    np_arr = np.load(FIL)
    print("NP number dimensions", np_arr.ndim)
    print("shape", np_arr.shape)
    print("size", np_arr.size)
    print("datatype", np_arr.dtype)

    for i in range(10):
        print(np_arr[i])

def convert_arr(input, dimx=160, dimy=160):
    res = np.reshape(input, (dimx, dimy, 4))
    #res = np.reshape(input, (dimx, dimy, 4), order="C")
    print(res[0,0])
    print(res[0,1])
    return res

def depth_arr(img):
    res = img[1]
    print(res)


show_png(IMG)
show_np(FIL)

np_arr = np.load(FIL)

img = convert_arr(np_arr)

print("-------------- img ")
print( img[0,0])
print( img[0,1])
print( img[1,0])

print ("ksdkskdskdsdsdksdkksdk")
dep = img[:,:,3]
print(dep)
print("max",dep.max())
print("min",dep.min())
dep1 = (dep - 0.014)*10000.0
print("max",dep1.max())
print("min",dep1.min())

dep2 = dep1 * (255.0 / dep1.max())
print("max",dep2.max())
print("min",dep2.min())

print(dep2)
im = Image.fromarray(dep2)
img = im.convert(mode='L')

print("jdjdfjdfjdfjdf")
#img.show()
#print(im)
img.save(OUT)




dfdfdf


print("------------reshape")
res = np.reshape(np_arr, (-1,160, 4), order="C")

print("number dimensions", res.ndim)
print("shape", res.shape)
print("size", res.size)
print("datatype", res.dtype)

print(res[0,0])
print(res[0,1])
print("finis")
#print(np_arr)

#np.save('np_arr.npy', np_arr)
