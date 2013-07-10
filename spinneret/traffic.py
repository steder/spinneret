"""
This script takes a sitemap file generated by `spider.py` and
spins up a number of workers (threads/processes/greenlets) to
hit those URLs.

A few additional features would be helpful here like:
 - remembering stats about the URLs requested
   + min, max, and avg response times
   + min, max, and avg response sizes
 - failure rates for URLs
 - response code counts (e.g.: 95 2xx, 4 4xx, and 1 5xx)

This script runs forever (or until it's killed) checking
these URLs and periodically outputing stats.

"""
from multiprocessing import Process
import logging
import signal
import timeit

import gevent
from gevent import pool
from gevent import monkey
import requests
import yaml


monkey.patch_socket()
requests_log = logging.getLogger("requests")


def sitemap_to_urls(sitemap_path):
    with open(sitemap_path, "r") as sitemap_file:
        sitemap = yaml.load(sitemap_file.read())

    urls = []

    def append_paths(parent_path, d, urls):
        for key in d:
            url_path = parent_path + (key,)
            url = "/".join(url_path)
            urls.append(url)
            append_paths(url_path, d[key], urls)
    append_paths((), sitemap, urls)

    return urls



def takeN(size, iterable):
    batch = []
    for n, i in enumerate(iterable):
        batch.append(i)
        if n % size == 0:
            yield batch
            batch = []
        yield batch


base = ""


def get_url(url):
    absolute_url = base + url
    logging.debug("getting: %s ... ", absolute_url)
    start = timeit.default_timer()
    try:
        resp = requests.get(absolute_url, timeout=30.0)
    except requests.exceptions.Timeout:
        stop = timeit.default_timer()
        elapsed = stop - start
        logging.debug("%s: Timed out (%s)", absolute_url, elapsed)
    except requests.exceptions.SSLError:
        stop = timeit.default_timer()
        elapsed = stop - start
        logging.debug("%s: SSL Error (%s)", absolute_url, elapsed)
    except requests.exceptions.ConnectionError:
        stop = timeit.default_timer()
        elapsed = stop - start
        logging.debug("%s: Connection Error (%s)", absolute_url, elapsed)
    else:
        stop = timeit.default_timer()
        elapsed = stop - start
        logging.debug("%s: %s (%s) (%4f)", absolute_url, resp.status_code, resp.reason, elapsed)


def run(inflight, urls):
    gevent.reinit()
    p = pool.Pool(inflight)
    while True:
        p.map(get_url, urls)
        p.join()


def main(arguments):
    global base

    base = arguments.base_url
    sitemap_path = arguments.sitemap_path
    inflight = arguments.inflight
    processes = arguments.processes
    debug = arguments.debug
    ttl = arguments.ttl

    if ttl > 0:
        signal.alarm(ttl)

    if debug:
        logging.basicConfig(level=logging.DEBUG,
                            format="%(asctime)s - %(levelname)s - %(message)s")
    else:
        requests_log.setLevel(logging.WARNING)
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s")

    logging.info("spinneret generating traffic - URL=%s N=%s P=%s",
                 base, inflight, processes)

    urls = sitemap_to_urls(sitemap_path)

    if processes == 1:
        run(inflight, urls)
    else:
        process_list = [Process(target=run, args=(inflight, urls)) for x in xrange(processes)]
        for proc in process_list:
            proc.start()
