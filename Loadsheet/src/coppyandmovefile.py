import shutil
import os
# Fetch the html file
import connectsqlserver
def coppyfilefromloadsheetfolder(src_dir,dest_dir,move_dir):   
    # path to source directory
    #src_dir = '/Volumes/MacintoshHD/foldertest1/'   
    # path to destination directory
    #dest_dir = '/Volumes/MacintoshHD/foldertest2/'
    #move_dir = '/Volumes/MacintoshHD/foldertest3/'
    
    # getting all the files in the source directory
    files = os.listdir(src_dir)
    for fname in files:
        # copying the files to the
        # destination directory
        shutil.copy2(os.path.join(src_dir,fname), dest_dir)
        shutil.move(os.path.join(src_dir,fname), move_dir)

while True:
    #readandimporttodb()
    coppyfilefromloadsheetfolder()
    time.sleep(600)