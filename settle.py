import os
import sys
import shutil
import errno
from PIL import Image
from PIL.ExifTags import TAGS


def getFileType(filename):
    filetype = os.path.splitext(filename)[1].lower()
    if(filetype == ".jpeg"):
        filetype = ".jpg"
    print(filetype)
    return filetype


def renameJpg(filePath, fileName):
    dateTime = "000000"
    exif = {}
    ext = os.path.splitext(fileName)[1]
    try:
        image = Image.open(filePath)
        image.verify()
        for (key, value) in image._getexif().items():
            exif[TAGS.get(key)] = value
        if(exif.get("DateTime")):
            dateTime = str(exif.get("DateTime")).replace(":", "")
        elif(exif.get("DateTimeOriginal")):
            dateTime = str(exif.get("DateTimeOriginal")).replace(":", "")
        elif(exif.get("DateTimeDigitized")):
            dateTime = str(exif.get("DateTimeDigitized")).replace(":", "")
        elif(exif.get("29")):
            dateTime = str(exif.get("29")).replace(":", "")
    except Exception:
        dateTime = "000000"
    dateTime = str(dateTime).replace(" ", "-", 1)
    newName = dateTime + "__" + fileName
    newName = str(newName).replace(" ", "_")
    if ext != "jpg":
        newName = newName.replace(ext, getFileType(newName))
    return newName


def getYear(fileName):
    year = newName[0:4]
    return year


def doTheCopy(fileType, fullPath, newName):
    finalPath = outbox+'/'+fileType+'/'+getYear(newName)+'/'
    try:
        shutil.copy(fullPath, finalPath+newName)
    except IOError as e:
        if e.errno != errno.ENOENT:
            raise
        # try creating parent directories
        os.makedirs(os.path.dirname(finalPath))
        shutil.copy(fullPath, finalPath+newName)


inbox = '../TestInbox'
outbox = '../TestOutbox'


if len(sys.argv) == 3:
    inboxDirectory = sys.argv[1]
    outboxDirectory = sys.argv[2]

for subdir, dirs, files in os.walk(inbox):
    for file in files:
        fullPath = os.path.join(subdir, file)
        type = getFileType(file)
        newName = "noName"
        if(type == ".jpg"):
            newName = renameJpg(fullPath, file)
        elif(type == ".gif"):
            print("GIF")
        elif(type == ".bmp"):
            print("BMP")
        elif(type == ".png"):
            print("PING")
        elif(type == ".tif"):
            print("WTIF")
        else:
            print("I DON'T KNOW")
        # newPath = outbox + '/' + type.strip('.') + '/' + newName
        if(newName != "noName"):
            doTheCopy(type.strip('.'), fullPath, newName)
