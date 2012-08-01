"""
Builds a really simple sitemap from a list of urls.

Assuming you've got a sitemap.yaml this will convert it
to an xml file::

    python sitemap_to_xml.py

Pretty print the xml with::

    xmllint --format sitemap.xml

"""
from xml.etree import ElementTree as etree

from spinneret import traffic

urls = traffic.sitemap_to_urls("sitemap.yaml")



"""
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.sitemaps.org/schemas/sitemap-image/1.1"
        xmlns:video="http://www.sitemaps.org/schemas/sitemap-video/1.1">
  <url>
    <loc>http://www.example.com/foo.html</loc>
    <image:image>
       <image:loc>http://example.com/image.jpg</image:loc>
    </image:image>
    <video:video>
      <video:content_loc>http://www.example.com/video123.flv</video:content_loc>
      <video:player_loc allow_embed="yes" autoplay="ap=1">http://www.example.com/videoplayer.swf?video=123</video:player_loc>
      <video:thumbnail_loc>http://www.example.com/thumbs/123.jpg</video:thumbnail_loc>
      <video:title>Grilling steaks for summer</video:title>
      <video:description>Get perfectly done steaks every time</video:description>
    </video:video>
  </url>
</urlset>
"""

BASE = "http://beta.threadless.com"

builder = etree.TreeBuilder()
builder.start("urlset", {"xmlns":"http://www.sitemaps.org/schemas/sitemap/0.9"})
for url in urls:
    builder.start("url", {})
    builder.start("loc", {})
    builder.data(BASE + url)
    builder.end("loc")
    builder.end("url")

builder.end("urlset")
root = builder.close()


with open("sitemap.xml", "w") as sitemap_file:
    tree = etree.ElementTree(root)
    tree.write(sitemap_file,
               encoding='utf-8',
               xml_declaration=True,
               method="xml")




