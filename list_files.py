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
ch = 0
sl = 0
fr = 0
# the function to find the max slices and frames
def find_max(folder):
    global ch
    global sl
    global fr 
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

find_max(r02c02_tiffs)
print("Channel: ", ch)
print("Slice: ", sl)
print("Frame: ", fr)



