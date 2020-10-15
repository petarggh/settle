import os
import sys
import shutil
import errno
import filecmp
from PIL import Image
from PIL.ExifTags import TAGS


def getFileType(filename):
    filetype = os.path.splitext(filename)[1].lower()
    if(filetype == ".jpeg"):
        filetype = ".jpg"
    return filetype.strip('.')


def renameImage(sourcePath, fileName):
    dateTime = "000000"
    exif = {}
    ext = getFileType(fileName)
    if(ext != "zip" and ext != "7z" and ext != "txt" and ext != "pdf"):
        try:
            image = Image.open(sourcePath)
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


def dupeCheck(sourcePath, newPath, newName):
    if(os.path.exists(newPath+newName)):
        if(filecmp.cmp(sourcePath, newPath+newName)):
            newName = 'dupe_' + newName
            newName = dupeCheck(sourcePath, newPath, newName)
    return newName


def doTheCopy(sourcePath, newPath, newName):
    global dupeFiles, outbox, dupeBox
    tmpName = dupeCheck(sourcePath, outbox+newPath, newName)
    if tmpName != newName:
        dupeFiles += 1
        try:
            shutil.copy2(sourcePath, outbox+'dupes/'+newPath+tmpName)
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise
            # try creating parent directories
            os.makedirs(os.path.dirname(outbox+'dupes/'+newPath))
            # try copy again
            shutil.copy2(sourcePath, outbox+'dupes/'+newPath+newName)
    else:
        try:
            shutil.copy2(sourcePath, outbox+newPath+newName)
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise
            # try creating parent directories
            os.makedirs(os.path.dirname(outbox+newPath))
            # try copy again
            shutil.copy2(sourcePath, outbox+newPath+newName)
    return True


inbox = '../TestInbox'
outbox = '../TestOutbox'
dupeBox = outbox + '/dupes'
filesProcessed = 0
filesSkipped = 0
dupeFiles = 0

if len(sys.argv) == 3:
    inbox = sys.argv[1]
    outbox = sys.argv[2]
    dupeBox = sys.argv[3]

outbox = outbox + '/'
for subdir, dirs, files in os.walk(inbox):
    for file in files:
        sourcePath = os.path.join(subdir, file)
        newName = ""
        newName = renameImage(sourcePath, file)
        if(newName != ""):
            newPath = getFileType(newName)+'/'+getYear(newName)+'/'
            doTheCopy(sourcePath, newPath, newName)
            filesProcessed += 1
        else:
            filesSkipped += 1

print("Files Processed: " + str(filesProcessed))
print("Files Skipped: " + str(filesSkipped))
print("Duplicate Files: " + str(dupeFiles))
