#!/usr/local/bin/python
# -*- encoding: utf-8 -*-

import os
import glob
import csv

pagetitle = os.path.basename(os.getcwd())

try:
    reader = csv.reader(open("sort_datetime.csv"))
except IOError:
    print "CSV load error."
    exit()

print "Content-type: text/html\n"
print "<!DOCTYPE html>"
print "<html>"
print "<head>"
print "<meta http-equiv=\"content-type\" content=\"text/html; charset=utf-8\">"
print "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
print "<link href=\"http://photo.guit.net/css/grid.css\" rel=\"stylesheet\" />"
print "<link href=\"http://photo.guit.net/css/lightbox.css\" rel=\"stylesheet\" />"
print "<script src=\"http://photo.guit.net/js/jquery-1.10.2.min.js\"></script>"
print "<script src=\"http://photo.guit.net/js/lightbox-2.6.min.js\"></script>"
print "<title>%s</title>" % pagetitle
print "</head>"
print "<body>"
print "<div class=\"grid\">"

for row in reader:
    infile,unixdatetime,datetime,unixfiledate,filedate,orientation,width,height,tateyoko = row
    print "<div class=\"section%s\">" % tateyoko
    print "<a href=\"%s\" rel=\"lightbox[group]\">" % infile
    print "<img src=\"thumbnails/_thumb_%s\" width=\"%s\" height=\"%s\">" % (infile,width,height)
    print "<div class=\"title\">%s</div>" % infile
    print "</a></div>"

print "</div>"
print "</body>"
print "</html>"
