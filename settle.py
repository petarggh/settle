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
    return filetype.strip('.')


def renameImage(filePath, fileName):
    dateTime = "000000"
    exif = {}
    ext = getFileType(fileName)
    if(ext != "zip" and ext != "7z" and ext != "txt" and ext != "pdf"):
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
        newName = newName.replace(ext, getFileType(newName))
    else:
        newName = fileName
    return newName


def getYear(fileName):
    year = newName[0:4]
    return year


def doTheCopy(fullPath, newName):
    finalPath = outbox+'/'+getFileType(newName)+'/'+getYear(newName)+'/'
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
filesProcessed = 0
filesSkipped = 0

if len(sys.argv) == 3:
    inboxDirectory = sys.argv[1]
    outboxDirectory = sys.argv[2]

for subdir, dirs, files in os.walk(inbox):
    for file in files:
        fullPath = os.path.join(subdir, file)
        newName = ""
        newName = renameImage(fullPath, file)
        if(newName != ""):
            doTheCopy(fullPath, newName)
            filesProcessed += 1
        else:
            filesSkipped += 1

print("Files Processed: " + str(filesProcessed))
print("Files Skipped: " + str(filesSkipped))
