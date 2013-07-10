import argparse

from spinneret import spider
from spinneret import traffic


base = "http://localhost"
sitemap = 'sitemap.yaml'
inflight = 10
processes = 1


parser = argparse.ArgumentParser(description='crawl or generate traffic')
subparsers = parser.add_subparsers()


parser_spider = subparsers.add_parser('spider', help="crawl the specified webpage")
parser_spider.set_defaults(func=spider.main)
parser_spider.add_argument('-b', '--base_url',
                    metavar='BASE', type=str, default=base,
                    help='the URL to crawl')
parser_spider.add_argument('-s', '--sitemap_path',
                    metavar='SITEMAP', type=str, default=sitemap,
                    help='the path to store the sitemap yaml document')
parser_spider.add_argument('-d', '--debug',
                    action='store_true',
                    help='turn on debugging')


parser_traffic = subparsers.add_parser('traffic', help="generate traffic")
parser_traffic.set_defaults(func=traffic.main)
parser_traffic.add_argument('-b', '--base_url',
                    metavar='BASE', type=str, default=base,
                    help='request pages from this URL')
parser_traffic.add_argument('-s', '--sitemap_path',
                    metavar='SITEMAP', type=str, default=sitemap,
                    help='the sitemap.yaml to use to generate traffic')
parser_traffic.add_argument('-i', '--inflight',
                    metavar='N', type=int, default=inflight,
                    help='the number of requests to have in flight at any time')
parser_traffic.add_argument('-p', '--processes',
                    metavar='P', type=int, default=processes,
                    help='the number of processes; each process has N requests in flight')
parser_traffic.add_argument('-t', '--ttl',
                    metavar='SECONDS', type=int, default=0,
                    help='generate load and stop after SECONDS seconds')
parser_traffic.add_argument('-d', '--debug',
                    action='store_true',
                    help='turn on debugging')
