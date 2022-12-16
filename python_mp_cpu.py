import os
import re
import sys
import cv2
import fnmatch
import numpy as np
from datetime import datetime
from threading import Thread
# @File(label='Destination directory', style="directory") save_path
# @File(label='Source directory', style="directory") tgt_path
tgt_path = input("Enter source directory: ")
save_path = input("Enter destination directory: ")

# debug the paths
print(tgt_path)
print(save_path)

folders = []

autoSort = False
# autosort
if autoSort:
    for filename in os.listdir(tgt_path):
        if os.path.splitext(filename)[1] == ".tiff":
            if filename[0:6].upper() not in folders:
                try:
                    os.mkdir(os.path.join(tgt_path,filename[0:6].upper()))
                except:
                    pass
            os.rename(os.path.join(tgt_path, filename), os.path.join(tgt_path, filename[0:6].upper(), filename))
            folders.append(filename[0:6].upper())
else:
    for (dirpath, dirnames, filenames) in os.walk(tgt_path):
        folders.extend(dirnames)
        break
print(folders)

# function to find the maximums of channel, slice, frame
def find_max(folderName):
    # Warning: before using the script, please make sure the filenames are in the correct format!!!

    fileOfDirectory = os.listdir(os.path.join(tgt_path, folderName))
    print("The path", os.path.join(tgt_path, folderName))
    patternPrefix = folderName.lower()+"*"

    folder = []

    # append everything into the list
    for filename in fileOfDirectory:
        if fnmatch.fnmatch(filename, patternPrefix):
            folder.append(filename)
    ch = 0
    sl = 0
    fr = 0
    
    for filename in folder:
        if(int(filename[15:16])>int(ch)):
            ch = filename[15:16]
        if(filename[18:20].isnumeric()):
            if(int(filename[18:20])>int(fr)):
                fr = filename[18:20]
        else:
            if(int(filename[18])>int(fr)):
                fr = filename[18]
        if(int(filename[10:12])>int(sl)):
            sl = filename[10:12]

    return (ch, sl, fr)
# function to perform Z-projection and hyperstack conversion using OpenCV and CUDA
def process_folder(filename):
    # Find the maximums
    ch, sl, fr = find_max(filename)
    
    print("channel: "+str(ch))
    print("slice: "+str(sl))
    print("frame: "+str(fr))
    
    # open the target folder
    image_list = []
    hyperstack_r = None
    hyperstack = np.zeros((int(ch), int(sl), int(fr)))
    fileOfDirectory = os.listdir(os.path.join(tgt_path, filename))
    patternPrefix = filename.lower()+"*"
    iter1 = 0
    image_chunk = []
    for filename2 in fileOfDirectory:
        if fnmatch.fnmatch(filename2, patternPrefix):
            image = cv2.imread(os.path.join(tgt_path, filename, filename2), cv2.IMREAD_ANYCOLOR | cv2.IMREAD_ANYDEPTH)
            image_chunk.append(image)
            iter1+=1
        if(iter1==5):
            stack = np.stack(image_chunk)
            hyperstack = cv2.merge(stack)
            print("stacking finished")
            image_chunk = []
            iter1=0
    # perform Z-projection using OpenCV and CUDA
    z_projection = cv2.cuda.createGpuMat()
    cv2.cuda.mean(hyperstack, z_projection, None, cv2.CV_REDUCE_MAX)

    # save Z-projection and hyperstack as TIFF images
    cv2.imwrite(os.path.join(save_path, "Z-Proj", filename+"_MAX.tiff"), z_projection)
    cv2.imwrite(os.path.join(save_path, "hyperstack", filename+"_hyperstack.tiff"), hyperstack)

threads = []
'''
for f in folders:
    Thread(target=process_folder, args=(f,)).start()
    threads.append(Thread(target=process_folder, args=(f,)))

for t in threads:
    t.join()
'''

process_folder(folders[0])

