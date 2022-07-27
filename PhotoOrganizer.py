import os
import exifread
from pathlib import Path
import shutil
import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

IMGTYPES=('.img','.jpg','.JPG','.jpeg','JPEG','.png','.PNG','.raw','.jfif')

def getDate(file):
    with open(file, 'rb') as fh:
        tags = exifread.process_file(fh, stop_tag="EXIF DateTimeDigitized")
        dateTaken = tags["EXIF DateTimeDigitized"]
        dateTimeArr = str(dateTaken).split(" ")
        return dateTimeArr[0]

def moveToDir(file, dirName):
    Path(newDirName).mkdir(exist_ok=True)
    try:
        shutil.move(file, dirName)
        movedCount = movedCount+1
    except:
        notMovedCount = notMovedCount+1

print("This utility takes all images in entered path (including sub-directories) and organize them by date to folders.")       
rootPath = input("Enter path:")
while not os.path.exists(rootPath):
    rootPath = input("Enter path:")

movedCount=0
notMovedCount=0
startDir = os.getcwd()
#walk through all directories and find files
for root, dirs, files in os.walk(startDir,topdown=True):
    if re.search("\\\[0-9][0-9][0-9][0-9]-[0-1][0-9]$", root):
        continue
    for file in files:
        name, ext = os.path.splitext(file)
        if any (ext in file for ext in IMGTYPES):
            pathOfFile = os.path.join(root, file)
            try:
                dateTaken = getDate(pathOfFile)
            except:
                moveToDir(pathOfFile, "Unknown date")
                continue

            year, month, day = dateTaken.split(":")
            newDirName = f"{year}-{month}"
            moveToDir(pathOfFile, newDirName)

print(bcolors.OKGREEN+ f" Moved files:{movedCount}"+bcolors.ENDC)
print(bcolors.FAIL+ f" Files with invalid metadata:{notMovedCount}"+bcolors.ENDC)
input("Press enter to close")