import os, fnmatch, re, sys
from ij import IJ, plugin
# import gc


# @File(label='Destination directory', style="directory") save_path
# @File(label='Source directory', style="directory") tgt_path
tgt_path = IJ.getDirectory("Source directory")
save_path = IJ.getDirectory("Destination directory")

# debug the paths
print(tgt_path)
print(save_path)

folders = []

# gc.enable()

autoSort = False
# autosort
if autoSort:
    for filename in os.listdir(tgt_path):
        if os.path.splitext(filename)[1] == ".tiff":
            if filename[0:6].upper() not in folders:
                try:
                    os.mkdir(filename[0:6].upper())
                except:
                    pass
            os.rename(filename, filename[0:6].upper()+"/"+filename)
            folders.append(filename[0:6].upper())
else:
    for (dirpath, dirnames, filenames) in os.walk(tgt_path):
        folders.extend(dirnames)
        break
print(folders)
# find the maximums of channel, slice, frame
ch = 0
sl = 0
fr = 0
def find_max(folderName):
    # Warning: before using the script, please make sure the filenames are in the correct format!!!

    fileOfDirectory = os.listdir(folderName)
    print(folderName)
    folder = []

    # append everything into the list
    for filename in fileOfDirectory:
        folder.append(filename)

    global ch
    global sl
    global fr
    
    for filename in folder:
        if(int(filename[15:16])>int(ch)):
            ch = filename[15:16]
        if(filename[18:20].isnumeric()):
            if(int(filename[18:20])>int(sl)):
                sl = filename[18:20]
        else:
            if(int(filename[18:19])>int(sl)):
                sl = filename[18:19]

        if(int(filename[10:11])>int(fr)):
            fr = filename[10:11]
# run the macro folder by folder
for filename in folders:
    # Find the maximums
    find_max(tgt_path+"/"+filename)
    # open the target folder
    imp = plugin.FolderOpener.open(tgt_path+"/"+filename, "")
    # Execute the macro of Z projection, and changing to hyperstack
    IJ.run(imp, "Stack to Hyperstack...", "order=xyctz channels="+str(ch)+" slices="+str(sl)+" frames="+str(fr)+" display=Color")
    if os.path.exists(save_path+"/hyperstack"):
        os.mkdir(save_path+"/hyperstack")
    IJ.saveAs(imp, "Tiff", save_path+"/hyperstack/"+filename+"_hyperstack.tiff")
    # Z Projection
    if os.path.exists(save_path+"/Z-Proj"):
        os.mkdir(save_path+"/Z-Proj")
    IJ.saveAs(imp, "Tiff", save_path+"/Z-Proj/"+filename+"_MAX.tiff")
    IJ.run(imp, "Z Project...", "projection=[Max Intensity] all")
    IJ.run(imp, "Make Composite", "")
    # Close everything
    IJ.run("Close All", "")
    # Garbage Collection
    IJ.run(imp, "Collect Garbage", "")
