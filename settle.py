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


def doTheCopy(sourcePath, finalPath, newName):
    global dupeFiles, outbox, dupeBox
    # finalPath = outbox+'/'+getFileType(newName)+'/'+getYear(newName)+'/'
    if(os.path.exists(outbox+finalPath+newName)):
        if(filecmp.cmp(sourcePath, outbox+finalPath+newName)):
            newName = 'dupe_' + newName
            finalPath = dupeBox+'/'+finalPath+'/'
            dupeFiles += 1
    try:
        shutil.copy2(sourcePath, outbox+finalPath+newName)
    except IOError as e:
        if e.errno != errno.ENOENT:
            raise
        # try creating parent directories
        os.makedirs(os.path.dirname(outbox+finalPath))
        shutil.copy2(sourcePath, outbox+finalPath+newName)


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
            finalPath = getFileType(newName)+'/'+getYear(newName)+'/'
            doTheCopy(sourcePath, finalPath, newName)
            filesProcessed += 1
        else:
            filesSkipped += 1

print("Files Processed: " + str(filesProcessed))
print("Files Skipped: " + str(filesSkipped))
print("Duplicate Files: " + str(dupeFiles))
