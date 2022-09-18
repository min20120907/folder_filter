import os, fnmatch, re, sys

# Warning: before using the script, please make sure the filenames are in the correct format!!!

fileOfDirectory = os.listdir(sys.argv[-1])
# first pattern to filter all the tiffs with the prefix "r02c02"
patternPrefix = sys.argv[-1].lower()+"*"
r02c02_tiffs = []
# append everything into the list
for filename in fileOfDirectory:
    if fnmatch.fnmatch(filename, patternPrefix):
            r02c02_tiffs.append(filename)
# print(r02c02_tiffs)

# the function to find the max slive and frame
def find_max(folder):
    ch = 0
    sl = 0
    fr = 0 
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
    print("Channel: ", ch)
    print("Slice: ", sl)
    print("Frame: ", fr)

find_max(r02c02_tiffs)



