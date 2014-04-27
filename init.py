#!/usr/local/bin/python
# -*- encoding: utf-8 -*-

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

input_dir = ""
try:
    if os.environ.has_key("PATH_INFO"):
        if os.environ['PATH_INFO'] != "":
            path_info = os.environ["PATH_INFO"].split("/")
            input_dir = path_info[1:2]
            # add a trailing slash.
            input_dir = os.path.join(input_dir[0],"")
except:
    input_dir = ""

cwd = os.getcwd()
dirlist = glob.glob(cwd+"/*")
dirlist.sort()
dirlist.reverse()

try:
    # using join to get target-directory with a trailing slash.
    if input_dir == "" :
        input_dir = os.path.join(sys.argv[1],"")
    if not os.path.isdir(input_dir):
        print "target directory is not exists or not directory.\n"
        raise Exception()
except:
    #print "Initpics make thumbnails and gather properties of pictures in target directory."
    #print "usage : python pripics.py <target directory>"

    print "Content-type: text/html"
    print
    print "<html>"
    print "<head>"
    print "<meta charset=\"utf-8\">"
    print "<title>dynatree test</title>"
    print "<script src=\"//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js\"></script>"
    print "<script src=\"//photoshare.guit.net/js/jquery-ui.custom.js\"></script>"
    print "<script src=\"//photoshare.guit.net/js/jquery.dynatree.js\"></script>"
    print "<link rel=\"stylesheet\" href=\"//photoshare.guit.net/css/dynatree/ui.dynatree.css\" />"
    print "<script type=\"text/javascript\">"
    print """
$(function(){
  $(document).ready( function() {
    $("input:button").click(function(){
      alert('hello world!');
    });
  });
  $("#tree").dynatree({
    checkbox: true,
    selectMode: 1,
    onSelect: function(select, node) {
      // Get a list of all selected nodes, and convert to a key array:
      var selKeys = $.map(node.tree.getSelectedNodes(), function(node){
        return node.data.key;
      });
      $("#echoSelection3").text(selKeys.join(", "));

      // Get a list of all selected TOP nodes
      var selRootNodes = node.tree.getSelectedNodes(true);
      // ... and convert to a key array:
      var selRootKeys = $.map(selRootNodes, function(node){
        return node.data.key;
      });
      $("#echoSelectionRootKeys3").text(selRootKeys.join(", "));
      $("#echoSelectionRoots3").text(selRootNodes.join(", "));
    },
    onDblClick: function(node, event) {
      node.toggleSelect();
    },
    onKeydown: function(node, event) {
      if( event.which == 32 ) {
        node.toggleSelect();
        return false;
      }
    }
  });
  $(document).ready( function() {
    $("input:button").click(function(){
      alert('hello world!');
    });
  });
});
"""
    print "</script>"
    print "</head>"
    print "<body>"
    print "<div>処理対象ディレクトリを選択</div>"
    print "<div id=\"tree\"><ul id=\"treeData\">"
    root = os.path.basename(cwd)
    print "<li id=\"%s\" class=\"folder expanded\" data='\"hideCheckbox\" : true' title=\"%s\">/%s" % (root,root,root)
    print "<ul>"

    for dir in dirlist:
        if os.path.isdir(dir):
            file = os.path.basename(dir)
            print "<li id=\"%s\" class=\"folder\" title=\"%s\">%s" % (file,file,file)

    print "</ul></li></ul></div>"
    print "<div>Selected keys: <span id=\"echoSelection3\">-</span></div>"
    print "<div>Selected root keys: <span id=\"echoSelectionRootKeys3\">-</span></div>"
    print "<div>Selected root nodes: <span id=\"echoSelectionRoots3\">-</span></div>"
    print "<input type=\"button\" value=\"submit\" />"
    print "</body>"
    print "</html>"

    sys.exit()

print "Content-type: text/html\n"
print "<!DOCTYPE html>"
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
        if   orientation == "Rotated 90 CW"  : image = image.rotate(90)
        elif orientation == "Rotated 90 CCW" : image = image.rotate(270)
        elif orientation == "Rotated 180"    : image = image.rotate(180)
        elif orientation == "Mirrored horizontal" : image = image.transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == "Mirrored vertical"   : image = image.transpose(Image.FLIP_TOP_BOTTOM)
        elif orientation == "Mirrored horizontal then rotated 90 CCW" : image = image.rotate(90).transpose(Image.FLIP_TOP_BOTTOM)
        elif orientation == "Mirrored horizontal then rotated 90 CW"  : image = image.rotate(270).transpose(Image.FLIP_TOP_BOTTOM)

        # make thumbnail
        hpercent = (ImageHeight/float(image.size[1]))
        wsize = int((float(image.size[0])*float(hpercent)))
        image = image.resize((wsize,ImageHeight), Image.ANTIALIAS)

        # save filtered image
        image.save(dir+"_thumb_"+os.path.basename(infile),quality=ImageQuality,optimize=True,progressive=True)
    else:
        print i+1,": a thumbnail exists."
        image = Image.open(dir+"_thumb_"+os.path.basename(infile))

    width, height = image.size


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
