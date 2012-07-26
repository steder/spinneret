"""
This script clicks all the links on a page to generate some beta traffic
"""

import urllib2

import mechanize



bro = mechanize.Browser()
bro.open("http://godzilla.threadless.com/")

test_bro = mechanize.Browser()

for link in bro.links():
    for segment in ("/make", "/pick", "/play"):
        if link.url.startswith(segment):
            print "Opening: %s"%(link.absolute_url)
            try:
                test_bro.open(link.absolute_url)
            except urllib2.HTTPError:
                print "Error opening: %s"%(link.absolute_url)
