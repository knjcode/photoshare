#!/usr/local/bin/python
# -*- encoding: utf-8 -*-

import os
import glob
import datetime
import Cookie
import csv

pagetitle = os.path.basename(os.getcwd())
sc = Cookie.SimpleCookie(os.environ.get('HTTP_COOKIE',''))
expires = datetime.datetime.now() + datetime.timedelta(days=1)
c_name = sc.get('sort').value if sc.has_key('sort') else 'nocookie'

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
print "<script type=\"text/javascript\">"
print ""
print "</script>"
print "</head>"
print "<body>"
print "<div class=\"grid\">"

for row in reader:
    infile,unixdatetime,datetime,unixfiledate,filedate,orientation,width,height,tateyoko,iso,ape,exp = row
    print "<div class=\"section%s\">" % tateyoko
    print "<a href=\"%s\" rel=\"lightbox[group]\" title=\"%s %s %s\">" % (infile,iso,ape,exp)
    print "<img src=\"thumbnails/_thumb_%s\" width=\"%s\" height=\"%s\">" % (infile,width,height)
    print "<div class=\"title\">%s</div>" % infile
    print "</a></div>"

print """
<ul>
<li>get COOKIE value: {0}</li>
</ul>""".format(c_name)
print "</div>"
print "</body>"
print "</html>"
