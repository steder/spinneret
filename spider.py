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

    def visit_links(url, links, visitor_depth=1, max_depth=6):
        print "visiting links on %s (depth: %s/%s)"%(url, visitor_depth, max_depth)
        for link in links:
            depth = get_depth(link.url)
            if "product" in link.url:
                print "\tproduct link.url:", link.url
                print "\tinternal:", is_internal_url(link.url)
                print "\timage:", not is_image_url(link.url)
                print "\tvisited:", link.url not in visited
                print "\tvisitor_depth <= max_depth:", visitor_depth <= max_depth
                print "\tdepth <= max_depth:", depth <= max_depth
            if (is_internal_url(link.url) and
                not is_image_url(link.url) and
                link.url not in visited and
                visitor_depth <= max_depth and
                depth <= max_depth):
                visited[link.url] = link.absolute_url
                try:
                    test_bro.open(link.absolute_url)
                    if depth < max_depth:
                        try:
                            visit_links(link.absolute_url,
                                        test_bro.links(),
                                        visitor_depth=depth + 1)
                        except mechanize.BrowserStateError:
                            print "Error getting links for: %s"%(link.absolute_url,)
                except urllib2.HTTPError:
                    print "Error opening: %s"%(link.absolute_url,)

    visit_links(root, bro.links())

    sitemap = urls_to_sitemap(visited.keys())
    with open("sitemap.yaml", "w") as f:
        yaml.dump(sitemap, f)
    with open("links.yaml", "w") as f2:
        yaml.dump(visited, f2)



if __name__=="__main__":
    main("http://beta.threadless.com/")
