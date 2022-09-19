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

    fileOfDirectory = os.listdir(tgt_path+folderName)
    print("The path", tgt_path+folderName)
    patternPrefix = folderName.lower()+"*"

    folder = []

    # append everything into the list
    for filename in fileOfDirectory:
        if fnmatch.fnmatch(filename, patternPrefix):
            folder.append(filename)
    print("files: ", folder)
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
    return (ch, sl, fr)

# run the macro folder by folder
for filename in folders:
    
    # Find the maximums
    ch, sl, fr = find_max(filename)
    
    print("channel: "+str(ch))
    print("slice: "+str(sl))
    print("frame: "+str(fr))
    
    # open the target folder
    try:
        imp = plugin.FolderOpener.open(tgt_path+"/"+filename, "")
    except:
        pass
    try:
        # Execute the macro of Z projection, and changing to hyperstack
        IJ.run(imp, "Stack to Hyperstack...", "order=xytcz channels="+str(ch)+" slices="+str(sl)+" frames="+str(fr)+" display=Color")
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
    except:
        pass