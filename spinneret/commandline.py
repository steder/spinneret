import argparse

from spinneret import spider
from spinneret import traffic


base = "http://localhost"
sitemap = 'sitemap.yaml'
inflight = 10
processes = 1


parser = argparse.ArgumentParser(description='crawl or generate traffic')
parser.add_argument('-b', '--base_url',
                    metavar='BASE', type=str, default=base,
                    help='')
parser.add_argument('-s', '--sitemap_path',
                    metavar='SITEMAP', type=str, default=sitemap,
                    help='')
parser.add_argument('-i', '--inflight',
                    metavar='N', type=int, default=inflight,
                    help='')
parser.add_argument('-p', '--processes',
                    metavar='P', type=int, default=processes,
                    help='')
parser.add_argument('-d', '--debug',
                    action='store_true',
                    help='')

subparsers = parser.add_subparsers()

parser_spider = subparsers.add_parser('spider')
parser_spider.set_defaults(func=spider.main)

parser_traffic = subparsers.add_parser('traffic')
parser_traffic.set_defaults(func=traffic.main)
