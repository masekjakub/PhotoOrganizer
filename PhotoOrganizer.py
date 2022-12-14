import os
import exifread
from pathlib import Path
import shutil
import re


class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


IMGTYPES = ('.img', '.jpg', '.JPG', '.jpeg', '.JPEG', '.GIF','.gif',
            '.png', '.PNG', '.raw', '.RAW', '.jfif', '.mp4', '.avi', '.CR4')

dateRegex = "\\\[0-9]{4}-[0-1][0-9]$"
movedCount = 0
notMovedCount = 0
invalidCount = 0


def getDate(file):
    with open(file, 'rb') as fh:
        tags = exifread.process_file(fh, stop_tag="EXIF DateTimeDigitized")
        dateTaken = tags["EXIF DateTimeDigitized"]
        dateTimeArr = str(dateTaken).split(" ")
        return dateTimeArr[0]


def moveToDir(fileName, fileFullPath, newDirName):
    global movedCount
    global notMovedCount
    os.makedirs(newDirName, exist_ok=True)

    # if image is already in folder
    if os.path.exists(f"{startDir}\{newDirName}\{fileName}"):
        os.remove(fileFullPath)
        return
    try:
        shutil.move(fileFullPath, newDirName)
        movedCount = movedCount+1
    except:
        notMovedCount = notMovedCount+1


###### MAIN #######
print()
print("This utility takes all images in entered path (including sub-directories) and organize them by date to folders.")
print(bcolors.WARNING + "Warning! Changes in folders can't be reverted!"+bcolors.ENDC)
startDir = input("Enter path:")

while not os.path.exists(startDir):
    startDir = input("Enter path:")
os.chdir(startDir)

# walk through all directories and find files
for root, dirs, files in os.walk(startDir, topdown=True):
    if re.search(dateRegex, root) or root.endswith("Unknown date"):
        continue
    for file in files:
        name, ext = os.path.splitext(file)
        if any(ext in file for ext in IMGTYPES):
            fileFullPath = os.path.join(root, file)
            try:
                dateTaken = getDate(fileFullPath)
            except:
                moveToDir(file, fileFullPath, "Unknown date")
                invalidCount = invalidCount+1
                continue

            year, month, day = dateTaken.split(":")
            newDirName = f"{year}\{year}-{month}"
            moveToDir(file, fileFullPath, newDirName)

print()
print(bcolors.OKGREEN + f"Moved files: {movedCount}"+bcolors.ENDC)
print(f"Files with unknown date: {invalidCount}"+bcolors.ENDC)
print(bcolors.FAIL + f"Errors: {notMovedCount}"+bcolors.ENDC)
print()
