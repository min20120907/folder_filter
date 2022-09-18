import os

tgt_path = "."

folders = []

for filename in os.listdir(tgt_path):
    if os.path.splitext(filename)[1] == ".tiff":
        if filename[0:6].upper() not in folders:
            try:
                os.mkdir(filename[0:6].upper())
            except:
                pass
        os.rename(filename, filename[0:6].upper()+"/"+filename)

        folders.append(filename[0:6].upper())


