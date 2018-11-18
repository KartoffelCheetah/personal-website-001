#!.venv/bin/python3
"""Functions handling images."""

import subprocess
import os

# supported ImageMagic Formats?
def getDateTimeOriginal(filePath) :
    """If image has DateTimeOriginal then returns it as a string. If it's missing or there isn't EXIF at all then returns empty string."""
    return subprocess.check_output(['identify', '-format', '%[EXIF:DateTimeOriginal]', filePath], timeout=3).decode('utf8').strip()
def getDimensions(filePath) :
    """Returns dimensions of image in a tuple."""
    x,y = subprocess.check_output(['identify', '-format', '%[w]x%[h]', filePath], timeout=3).decode('utf8').strip().split('x')
    return int(x), int(y)
def createThumbnail(originPath, destinationPath, size='200x200') :
    """Creates a thumbnail image out of originPath in destinationPath of size (which defaults to maxWidth:200, maxHeight:200) and keeps ratio. The function creates directory if not exists already. Returns the subprocess's response."""
    print('Create thumbnail -> %s' % destinationPath)
    destDirPath = os.path.split(destinationPath)[0]
    if not os.path.exists(destDirPath) :
        os.makedirs(destDirPath)
    return subprocess.run(['convert', originPath, '-auto-orient', '-thumbnail', size, destinationPath], timeout=3)
def createRotatedImage(originPath, destinationPath) :
    """Creates a rotated image out of originPath in destinationPath. EXIF orientation will be adjusted with the rotation. The function creates directory if not exists already. Returns the subprocess's response."""
    print('Create rotatedImage -> %s' % destinationPath)
    destDirPath = os.path.split(destinationPath)[0]
    if not os.path.exists(destDirPath) :
        os.makedirs(destDirPath)
    return subprocess.run(['convert', originPath, '-auto-orient', destinationPath], timeout=3)
