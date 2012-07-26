"""
This script clicks all the links on a page to generate some beta traffic
"""

import urllib2

import mechanize
import yaml


def is_internal_url(url):
    if url.startswith("/"):
        return True
    return False



def urls_to_sitemap(urls):
    sitemap = {"": {}}
    for url in urls:
        segments = (segment for segment in url.split("/") if segment != '')
        root = sitemap[""]
        for segment in segments:
            if root.get(segment):
                print "root:", root, segment
                root = root.get(segment)
            else:
                print "adding new segment to root"
                root[segment] = {}
                root = root[segment]
    return sitemap



def main(root, debug=False):
    bro = mechanize.Browser()
    bro.open(root)

    test_bro = mechanize.Browser()

    visited = {}

    def visit_links(url, links, level=0, max_level=5):
        print "visiting links on: %s (level=%s)"%(url, level)
        for link in links:
            print "inspecting link:", link.url
            if is_internal_url(link.url) and link.url not in visited:
                visited[link.url] = link.absolute_url
                print "Opening: %s"%(link.absolute_url)
                try:
                    test_bro.open(link.absolute_url)
                    if level < max_level:
                        visit_links(link.absolute_url,
                                    test_bro.links(),
                                    level=level+1)
                except urllib2.HTTPError:
                    print "Error opening: %s"%(link.absolute_url)

    visit_links(root, bro.links())

    sitemap = urls_to_sitemap(visited.keys())
    print sitemap
    with open("sitemap.yaml", "w") as f:
        print yaml.dump(sitemap, f)



if __name__=="__main__":
    main("http://beta.threadless.com/")
