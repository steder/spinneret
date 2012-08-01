"""
This script clicks all the links on a page to generate some beta traffic
"""

import httplib
import urllib2

import mechanize
import yaml


def is_internal_url(url):
    if url.startswith("/"):
        return True
    return False



image_extensions = ('gif',
                    'jpg',
                    'png')
def is_image_url(url):
    for extension in image_extensions:
        if url.endswith(extension):
            return True
    return False



def urls_to_sitemap(urls):
    sitemap = {"": {}}
    for url in urls:
        segments = (segment for segment in url.split("/") if segment != '')
        root = sitemap[""]
        for segment in segments:
            if root.get(segment):
                root = root.get(segment)
            else:
                root[segment] = {}
                root = root[segment]
    return sitemap



def get_depth(url):
    depth = len([segment for segment in url.split("/") if segment])
    return depth



def main(root):
    bro = mechanize.Browser()
    bro.open(root)

    test_bro = mechanize.Browser()

    visited = {}
    ignored = {}

    def visit_links(url, links, max_depth=3):
        print "visiting links on: %s (nLinks=%s)"%(url, len(links))
        # for link in links:
        while links:
            link = links.pop(0)
            depth = get_depth(link.url)
            if (is_internal_url(link.url) and
                not is_image_url(link.url) and
                link.url not in visited and
                depth <= max_depth):
                visited[link.url] = link.absolute_url
                try:
                    print "Opening %s: ..."%(link.absolute_url,),
                    test_bro.open(link.absolute_url)
                    if depth < max_depth:
                        try:
                            links.extend(link for link in test_bro.links()
                                         if link.url not in visited and link.url not in ignored)
                        except mechanize.BrowserStateError:
                            print "ERROR"
                            print "\tError getting links for: %s"%(link.absolute_url,)
                except urllib2.HTTPError:
                    print "ERROR"
                    print "\tError opening: %s"%(link.absolute_url,)
                except httplib.BadStatusLine:
                    print "ERROR"
                    print "\tBad status error: %s"%(link.absolute_url,)
                else:
                    print "OK"
            else:
                ignored[link.url] = link.absolute_url

    visit_links(root, list(bro.links()))

    sitemap = urls_to_sitemap(visited.keys())
    with open("sitemap.yaml", "w") as f:
        yaml.dump(sitemap, f)
    with open("links.yaml", "w") as f2:
        yaml.dump(visited, f2)



if __name__=="__main__":
    main("http://beta.threadless.com/")
