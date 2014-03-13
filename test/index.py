#!/usr/local/bin/python
# -*- encoding: utf-8 -*-

import os
import glob
import datetime
import Cookie
import csv

dir = os.path.basename(os.getcwd())
cookie = Cookie.SimpleCookie(os.environ.get('HTTP_COOKIE',''))
expires = datetime.datetime.now() + datetime.timedelta(days=7)
sort = cookie.get('sort').value if cookie.has_key('sort') else 'datetime'
selected = {"datetime":"", "datetime_reverse":"", "filedate":"", "filedate_reverse":""}
selected[sort] = " selected" 

try:
    if   sort == "datetime"         : reader = csv.reader(open("../thumbnails/"+dir+"/sort_datetime.csv"))
    elif sort == "datetime_reverse" : reader = csv.reader(open("../thumbnails/"+dir+"/sort_datetime_reverse.csv"))
    elif sort == "filedate"         : reader = csv.reader(open("../thumbnails/"+dir+"/sort_filedate.csv"))
    elif sort == "filedate_reverse" : reader = csv.reader(open("../thumbnails/"+dir+"/sort_filedate_reverse.csv"))
    else:
        print "CSV load error."
        exit()
except IOError:
    print "CSV load error."
    exit()

print "Content-type: text/html\n"
print "<!DOCTYPE html>"
print "<html>"
print "<head>"
print "<meta charset=\"utf-8\">"
print "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
print "<title>%s</title>" % dir
print "<link rel=\"stylesheet\" href=\"//photoshare.guit.net/css/grid.css\" />"
#print "<link rel=\"stylesheet\" href=\"//photoshare.guit.net/css/lightbox.css\" />"
print "<link rel=\"stylesheet\" href=\"//photoshare.guit.net/css/colorbox.css\" />"
print "<script src=\"//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js\"></script>"
print "<script src=\"//photoshare.guit.net/js/jquery.cookie.js\"></script>"
#print "<script src=\"//photoshare.guit.net/js/lightbox-2.6.min.js\"></script>"
print "<script src=\"//photoshare.guit.net/js/jQueryRotate.js\"></script>"
print "<script src=\"//photoshare.guit.net/js/jquery.colorbox-custom.js\"></script>"
print "<script src=\"//photoshare.guit.net/js/jquery.colorbox-ja.js\"></script>"
print "<script src=\"//photoshare.guit.net/js/myscript.js\"></script>"
print "</head>"
print "<body>"
print "<div align=\"right\">画像の並び順"
print "<select id=\"sort\" name=\"sort\">"
print "<option value=\"datetime\"%s>撮影日時昇順</option>" % selected["datetime"]
print "<option value=\"datetime_reverse\"%s>撮影日時降順</option>" % selected["datetime_reverse"]
print "<option value=\"filedate\"%s>ファイル更新日時昇順</option>" % selected["filedate"]
print "<option value=\"filedate_reverse\"%s>ファイル更新日時降順</option>" % selected["filedate_reverse"]
print "</select></div>"
print "<div class=\"grid\">"

for row in reader:
    infile,unixdatetime,datetime,unixfiledate,filedate,orientation,width,height,camera,lens,exp,fnumber,iso = row
    print "<div class=\"section\">"
    print "<a href=\"%s\" rel=\"group\" title=\"%s, %s, %s, F%s, ISO%s, %s\">" % (infile,camera,lens,exp,fnumber,iso,datetime)
    print "<img src=\"../thumbnails/%s/_thumb_%s\" width=\"%s\" height=\"%s\">" % (dir,infile,width,height)
    print "<div class=\"title\">%s</div>" % infile
    print "</a></div>"

print "</div>"
print "</body>"
print "</html>"
