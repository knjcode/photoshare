#!/usr/local/bin/python

import os
import sys
import glob
import time
import datetime
import csv
import exifread
import Image
import ConfigParser
from operator import itemgetter
from fractions import Fraction

# load config
Config_file = "config.ini"
conf = ConfigParser.SafeConfigParser()
conf.read(Config_file)
ImageHeight = int(conf.get('options','ImageHeight'))
Generated = conf.get('options','Generated')
ImageQuality = int(conf.get('options','ImageQuality'))

try:
    # using join to get target-directory with a trailing slash.
    input_dir = os.path.join(sys.argv[1],"")
    if not os.path.isdir(input_dir):
        print "target directory is not exists or not directory.\n"
        raise Exception()
except:
    print "Initpics make thumbnails and gather properties of pictures in target directory."
    print "usage : python pripics.py <target directory>"
    sys.exit()
print "target directory is %s" % input_dir

# make name of thumbnails directory
dir = os.path.join(Generated,input_dir)

# make thumbnails directory
if not os.path.isdir(dir):
    try:
        os.makedirs(dir)
    except:
        print "Can't make thumbnails direcotry."
        sys.exit()
print "thumbnails directory is %s" % dir


print "Making thumbnails and gathering properties of pictures."
csvdata = []

# read file name
for i, infile in enumerate(glob.glob(input_dir+'*.jpg')):

    # getmtime
    unixfiledate = os.path.getmtime(infile)
    filedate = time.strftime('%Y:%m:%d %X',time.localtime(unixfiledate))

    # file open
    fp = open(infile)
    exif = exifread.process_file(fp)

    # get EXIF datetime
    try:
        datetime = exif['EXIF DateTimeOriginal']
    except KeyError:
        datetime = filedate

    unixdatetime = time.mktime(time.strptime(str(datetime),'%Y:%m:%d %X'))

    # get EXIF Image Orientation
    try:
        orientation = str(exif['Image Orientation'])
    except KeyError:
        orientation = "Orientation Undefined"

    #get Image Model
    try:
        camera = exif['Image Model']
    except KeyError:
        camera = "unknown"

    #get EXIF LensModel
    try:
        lens = exif['EXIF LensModel']
    except KeyError:
        lens = "unknown"

    #get EXIF ExposureTime
    try:
        exp = exif['EXIF ExposureTime']
    except KeyError:
        exp = "unknown"

    #get EXIF FNumber
    try:
        fnumber = float(Fraction(str(exif['EXIF FNumber'])))
    except KeyError:
        fnumber = "unknown"

    #get EXIF ISOSpeedRatings
    try:
        iso = exif['EXIF ISOSpeedRatings']
    except KeyError:
        iso = "unknown"

    fp.close()

    # convert thumbnail
    if not os.path.isfile(dir+"_thumb_"+os.path.basename(infile)):
        print i+1,": making a thumbnail."
        # read image
        image = Image.open(infile)

        # rotate image
        print orientation
        if   orientation == "Rotated 90 CW"  : image = image.rotate(90)
        elif orientation == "Rotated 90 CCW" : image = image.rotate(270)
        elif orientation == "Rotated 180"    : image = image.rotate(180)
        elif orientation == "Mirrored horizontal" : image = image.transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == "Mirrored vertical"   : image = image.transpose(Image.FLIP_TOP_BOTTOM)
        elif orientation == "Mirrored horizontal then rotated 90 CCW" : image = image.transpose(Image.FLIP_TOP_BOTTOM).rotate(90)
        elif orientation == "Mirrored horizontal then rotated 90 CW"  : image = image.transpose(Image.FLIP_TOP_BOTTOM).rotate(270)

        # make thumbnail
        hpercent = (ImageHeight/float(image.size[1]))
        print "hpercent is %s" % hpercent
        wsize = int((float(image.size[0])*float(hpercent)))
        print "wsize is %s" % wsize
        image = image.resize((wsize,ImageHeight), Image.ANTIALIAS)

        # save filtered image
        image.save(dir+"_thumb_"+os.path.basename(infile),quality=ImageQuality,optimize=True,progressive=True)
    else:
        print i+1,": a thumbnail exists."
        image = Image.open(dir+"_thumb_"+os.path.basename(infile))


    width, height = image.size
    print "width, height = %s, %s" % (width,height)


    # add Image Information to csvdata
    csvdata.append((os.path.basename(infile),unixdatetime,datetime,unixfiledate,filedate,orientation,width,height,camera,lens,exp,fnumber,iso))

csvdata = sorted(csvdata, key=itemgetter(1))
writer = csv.writer(open(dir+"sort_datetime.csv","wb"))
for row in csvdata: writer.writerow(row)

csvdata = sorted(csvdata, key=itemgetter(1),reverse=True)
writer = csv.writer(open(dir+"sort_datetime_reverse.csv","wb"))
for row in csvdata: writer.writerow(row)

csvdata = sorted(csvdata, key=itemgetter(3))
writer = csv.writer(open(dir+"sort_filedate.csv","wb"))
for row in csvdata: writer.writerow(row)

csvdata = sorted(csvdata, key=itemgetter(3),reverse=True)
writer = csv.writer(open(dir+"sort_filedate_reverse.csv","wb"))
for row in csvdata: writer.writerow(row)
