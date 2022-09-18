import os, fnmatch, re, sys
from ij import IJ, plugin, gc

tgt_path = "Images/"
folders = []

gc.enable()

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
        folders.extend(filenames)
        break
# find the maximums of channel, slice, frame
ch = 0
sl = 0
fr = 0
def find_max(folderName):
    # Warning: before using the script, please make sure the filenames are in the correct format!!!

    fileOfDirectory = folderName
    # first pattern to filter all the tiffs with the prefix
    patternPrefix = sys.argv[-1].lower()+"*"
    folder = []

    # append everything into the list
    for filename in fileOfDirectory:
        if fnmatch.fnmatch(filename, patternPrefix):
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
    # open the target folder
    imp = plugin.FolderOpener(tgt_path+filename,"")
    # The macro from CCLin
    IJ.run(imp, "Stack to Hyperstack...", "order=xyctz channels="+str(ch)+" slices="+str(sl)+" frames="+str(fr)+" display=Color")
    IJ.run(imp, "Z Project...", "projection=[Max Intensity] all")
    IJ.run(imp, "Make Composite", "")
    # Garbage Collection
    IJ.run(imp, "Collect Garbage", "")

