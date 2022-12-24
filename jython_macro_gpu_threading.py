import os
from ij import IJ, macro
from ij.plugin import FolderOpener, HyperStackConverter, ZProjector

# @File(label='Destination directory', style="directory") save_path
# @File(label='Source directory', style="directory") tgt_path
tgt_path = IJ.getDirectory("Source directory")
save_path = IJ.getDirectory("Destination directory")

def process_folder(folder_name):
    # Find the maximums
    ch, sl, fr = 0, 0, 0
    for file in os.listdir(os.path.join(tgt_path, folder_name)):
        if file.startswith(folder_name.lower()):
            ch = max(ch, int(file[15:16]))
            if file[18:20].isnumeric():
                fr = max(fr, int(file[18:20]))
            else:
                fr = max(fr, int(file[18]))
            sl = max(sl, int(file[10:12]))
    
    # Open the target folder
    imp = FolderOpener.open(os.path.join(tgt_path,folder_name), "virtual")
    
    # Execute the macro of Z projection, and changing to hyperstack
    # args_hyperstack = "order=xytcz channels={} slices={} frames={} display=Color".format(ch, sl, fr)
    # IJ.run(imp, "Stack to Hyperstack...", args_hyperstack)
    hsc = HyperStackConverter()
    imp2 = hsc.toHyperStack(imp, ch, sl, fr, "xytcz", "color")
    # hsc.shuffle(imp, hsc.TCZ)
    
    # zproj = ZProjector(imp2)
    # zproj.setMethod(ZProjector.MAX_METHOD)
    # zproj.doProjection()
    # imp3 = zproj.getProjection()
    # imp3.show()
    if not os.path.exists(os.path.join(save_path, "hyperstack")):
        try:
            os.mkdir(os.path.join(save_path, "hyperstack"))
        except:
            pass
    if not os.path.exists(os.path.join(save_path, "hyperstack", folder_name+"_hyperstack.tiff")):
    	IJ.saveAs(imp2, "TIFF", os.path.join(save_path, "hyperstack", folder_name + "_hyperstack.tiff"))
    IJ.run(imp2, "Maximum-Z-Projection frame by frame on multiple GPUs (experimental)", "")
    # Save the maximum intensity projection if the image title includes "MAX"
    # IJ.run(imp2, "Z Project...", "projection=[Max Intensity] all")
    if not os.path.exists(os.path.join(save_path, "Z-Proj")):
        try:
            os.mkdir(os.path.join(save_path, "Z-Proj"))
        except:
            pass
    IJ.selectWindow("MaximumZProjectionFrameProcessor_"+folder_name)
    if not os.path.exists(os.path.join(save_path, "Z-Proj", folder_name+"_MAX.tiff")):
        IJ.saveAs(  "TIFF", os.path.join(save_path, "Z-Proj", folder_name + "_MAX.tiff"))
    print(imp2.getTitle())
    imp.close()
    imp2.close()
    # imp3.close()
    
    

# Run the macro on each folder in parallel using multithreading
from threading import Thread
threads = []
for folder in os.listdir(tgt_path):
    thread = Thread(target=process_folder, args=(folder,))
    thread.start()
    threads.append(thread)

# Wait for all threads to finish
for thread in threads:
    thread.join()

IJ.showMessage("Processing complete.")
