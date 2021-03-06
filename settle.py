import os
import sys
import shutil
import errno
import filecmp
import curses
from PIL import Image
from PIL.ExifTags import TAGS


def slowCompare(sourcePath, fileName, outbox):
    for subdir, dirs, files in os.walk(outbox):
        for file in files:
            try:
                if(filecmp.cmp(sourcePath, outbox+newPath+file)):
                    return True
            except IOError as e:
                if e.errno != errno.ENOENT:
                    raise
    return False


def getFileType(filename):
    filetype = os.path.splitext(filename)[1].lower()
    if(filetype == ".jpeg"):
        filetype = ".jpg"
    elif(filetype == ""):
        filetype = ".unknown"
    return filetype.strip('.')


def getYear(fileName):
    year = newName[0:4]
    return year


def doTheCopy(outbox, sourcePath, newPath, newName):
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


def renameFile(sourcePath, fileName):
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


inbox = ''
outbox = ''
width, height = os.get_terminal_size()
filesProcessed = 0
filesSkipped = 0
dupeFiles = 0

if len(sys.argv) == 3:
    inbox = sys.argv[1]
    outbox = sys.argv[2]

outbox = outbox + '/'
dupeBox = outbox + '/0dupes/'
introText = "Settling files from " + inbox + " to " + outbox
print(introText)
screen = curses.initscr()
screen.addstr(0, 0, "This string gets printed at position (0, 0)")
screen.addstr(3, 1, "Try Russian text: Привет")  # Python 3 required for unicode
screen.addstr(4, 4, "X")
screen.addch(5, 5, "Y")
screen.refresh()
for subdir, dirs, files in os.walk(inbox):
    for file in files:
        print("Current file " + file, end="\r")  # +
        sourcePath = os.path.join(subdir, file)
        newName = ""
        newName = renameFile(sourcePath, file)
        if(newName != ""):
            newPath = getFileType(newName)+'/'+getYear(newName)+'/'
            if (slowCompare(sourcePath, file, outbox)):
                dupeFiles += 1
                doTheCopy(dupeBox, sourcePath, newPath, newName)
            else:
                doTheCopy(outbox, sourcePath, newPath, newName)
                filesProcessed += 1
        else:
            filesSkipped += 1

print("\n")
print("Files Processed: " + str(filesProcessed))
print("Files Skipped: " + str(filesSkipped))
print("Duplicate Files: " + str(dupeFiles))
curses.endwin()
