#!/usr/local/bin/python
# -*- encoding: utf-8 -*-

import os
import glob
import datetime
import Cookie
import csv

pagetitle = os.path.basename(os.getcwd())
#sc = Cookie.SimpleCookie(os.environ.get('HTTP_COOKIE',''))
#expires = datetime.datetime.now() + datetime.timedelta(days=1)
#c_name = sc.get('sort').value if sc.has_key('sort') else 'nocookie'

try:
    reader = csv.reader(open("sort_datetime.csv"))
except IOError:
    print "CSV load error."
    exit()

print "Content-type: text/html\n"
print "<!DOCTYPE html>"
print "<html>"
print "<head>"
print "<meta charset=\"utf-8\">"
print "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
print "<title>%s</title>" % pagetitle
print "<link rel=\"stylesheet\" href=\"//photo.guit.net/css/grid.css\" />"
print "<link rel=\"stylesheet\" href=\"//photo.guit.net/css/lightbox.css\" />"
print "<script src=\"//ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js\"></script>"
print "<script src=\"//photo.guit.net/js/jquery.cookie.js\"></script>"
print "<script src=\"//photo.guit.net/js/lightbox-2.6.min.js\"></script>"
print "<script src=\"//photo.guit.net/js/myscript.js\"></script>"
print "</head>"
print "<body>"
print "<p>set cookie</p>"
print "<select id=\"sort\" name=\"sort\">"
print "<option value=\"datetime\">撮影日時昇順</option>"
print "<option value=\"datetime_reverse\">撮影日時降順</option>"
print "<option value=\"filedate\">ファイル更新日時昇順</option>"
print "<option value=\"filedate_reverse\">ファイル更新日時降順</option>"
print "</select>"
print "<div class=\"grid\">"

for row in reader:
    infile,unixdatetime,datetime,unixfiledate,filedate,orientation,width,height,tateyoko,camera,lens,exp,fnumber,iso = row
    print "<div class=\"section%s\">" % tateyoko
    print "<a href=\"%s\" rel=\"lightbox[group]\" title=\"%s, %s, %s, F%s, ISO%s, %s\">" % (infile,camera,lens,exp,fnumber,iso,datetime)
    print "<img src=\"thumbnails/_thumb_%s\" width=\"%s\" height=\"%s\">" % (infile,width,height)
    print "<div class=\"title\">%s</div>" % infile
    print "</a></div>"

#print """
#<ul>
#<li>get COOKIE value: {0}</li>
#</ul>""".format(c_name)

print "</div>"
print "</body>"
print "</html>"
