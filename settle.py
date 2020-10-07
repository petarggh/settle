import os
import sys

directory = '.'

if len(sys.argv) > 1:
    directory = sys.argv[1]

for subdir, dirs, files in os.walk(directory):
    for file in files:
        print(os.path.join(subdir, file))
        # check file Type
        # if image
        #   read meta to determine create date
        #   if exists
        #       prefix filename with datetime string
        #       move to folder for that year
        #   if # NOT
        #       check other date fields
        #       if a good one
        #           use that
        #           move to the folder for that year
        #       else
        #           put in the mystery folder
        # if video
        #   read meta to determine create date
        #   if exists
        #       prefix filename with datetime string
        #       move to folder for that year
        #   if # NOT
        #       check other date fields
        #       if a good one
        #           use that
        #           move to the folder for that year
        #       else
        #           put in the mystery folder
        # if document
        #   Move to document folder
        # if software
        #   move to software folder
        # if disk image
        #   move to disk image folder
        # if archive
        #   move to archive folder
