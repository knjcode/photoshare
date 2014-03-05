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

    # convert thumbnail
    if not os.path.isfile(dir+"_thumb_"+os.path.basename(infile)):
        print i+1,": making a thumbnail."
        # read image
        image = Image.open(infile)
        hpercent = (ImageHeight/float(image.size[1]))
        print "hpercent is %s" % hpercent
        wsize = int((float(image.size[0])*float(hpercent)))
        print "wsize is %s" % wsize
        image = image.resize((wsize,ImageHeight), Image.ANTIALIAS)
#        image.thumbnail((thumbnail_size,thumbnail_size), Image.ANTIALIAS)

        # save filtered image
        image.save(dir+"_thumb_"+os.path.basename(infile),quality=ImageQuality,optimize=True,progressive=True)
    else:
        print i+1,": a thumbnail exists."
        image = Image.open(dir+"_thumb_"+os.path.basename(infile))


    width, height = image.size
    print "width, height = %s, %s" % (width,height)


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
        orientation = exif['Image Orientation']
    except KeyError:
        orientation = "Orientation Undefined"

    if width>height:
        tateyoko = "yoko"
    else:
        tateyoko = "tate"

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

    csvdata.append((os.path.basename(infile),unixdatetime,datetime,unixfiledate,filedate,orientation,width,height,tateyoko,camera,lens,exp,fnumber,iso))

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
