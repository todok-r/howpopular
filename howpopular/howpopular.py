#!/usr/bin/env python

######################################################
#
# howpopular - command line popularity checker
# written by todok_r
# inspired by Benjamin Gleitzman (gleitz@mit.edu)
#
######################################################

import argparse
import glob
import os
import random
import re
import requests
import requests_cache
import sys
from . import __version__

from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError
from requests.exceptions import SSLError

# Handle imports for Python 2 and 3
if sys.version < '3':
    import codecs
    from urllib import quote as url_quote
    from urllib import getproxies

    # Handling Unicode: http://stackoverflow.com/a/6633040/305414
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    from urllib.request import getproxies
    from urllib.parse import quote as url_quote

    def u(x):
        return x


if os.getenv('HOWPOPULAR_DISABLE_SSL'):  # Set http instead of https
    SCHEME = 'http://'
    VERIFY_SSL_CERTIFICATE = False
else:
    SCHEME = 'https://'
    VERIFY_SSL_CERTIFICATE = True

USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) '
                'Chrome/19.0.1084.46 Safari/536.5'),
               ('Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46'
                'Safari/536.5'), )
SEARCH_URLS = {
    'google': SCHEME + 'www.google.com/search?q={0}'
}
XDG_CACHE_DIR = os.environ.get('XDG_CACHE_HOME',
                               os.path.join(os.path.expanduser('~'), '.cache'))
CACHE_DIR = os.path.join(XDG_CACHE_DIR, 'howpopular')
CACHE_FILE = os.path.join(CACHE_DIR, 'cache{0}'.format(
    sys.version_info[0] if sys.version_info[0] == 3 else ''))

if os.getenv('HOWPOPULAR_DISABLE_CACHE'):
    howpopular_session = requests.session()
else:
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    howpopular_session = requests_cache.CachedSession(CACHE_FILE)


def get_proxies():
    proxies = getproxies()
    filtered_proxies = {}
    for key, value in proxies.items():
        if key.startswith('http'):
            if not value.startswith('http'):
                filtered_proxies[key] = 'http://%s' % value
            else:
                filtered_proxies[key] = value
    return filtered_proxies


def _get_result(url):
    try:
        return howpopular_session.get(url, headers={'User-Agent': random.choice(USER_AGENTS)},
                                  proxies=get_proxies(),
                                  verify=VERIFY_SSL_CERTIFICATE).text
    except requests.exceptions.SSLError as e:
        print('[ERROR] Encountered an SSL Error. Try using HTTP instead of '
              'HTTPS by setting the environment variable "HOWPOPULAR_DISABLE_SSL".\n')
        raise e


def _get_search_url(search_engine):
        return SEARCH_URLS.get(search_engine, SEARCH_URLS['google'])


def _clear_cache():
    for cache in glob.iglob('{0}*'.format(CACHE_FILE)):
        os.remove(cache)


def _get_result_status(query):
    search_engine = os.getenv('HOWPOPULAR_SEARCH_ENGINE', 'google')
    search_url = _get_search_url(search_engine)

    result = _get_result(search_url.format(url_quote(query)))
    html = pq(result)
    ret = html('#resultStats').text()

    return ret


def _make_text_popularity_histgram(popularities):
    histgrams = []
    most_hits = max(hits for _, hits in popularities)
    query_width = max(len(query) for query, _ in popularities)
    hits_width = len(str(most_hits))
    for name, hits in popularities:
        histgrams.append('{0:{query_width}} {1:{hits_width}} hits: {2}'.
                   format(name, hits, '*'*(hits*100//most_hits), query_width=query_width,
                          hits_width=hits_width))
    return histgrams


def _make_text_popularity(popularities):
    texts = []
    width = max(len(query) for query, _ in popularities)
    for query, hits in popularities:
        texts.append('{0:{width}} {1} hits'.format(query, hits, width=width))

    return texts


def _get_popularity(args):
    popularities = []
    for query in args['query']:
        status = _get_result_status(query)
        m = re.search(r'([,0-9]+)', status)
        hits = 0
        if m:
            hits = int(m.group(1).replace(',', ''))

        popularities.append((query, hits))

    return popularities


def howpopular(args):
    texts = []
    try:
        popularities = _get_popularity(args) or 'Sorry, couldn\'t find any help with that topic\n'
    except (ConnectionError, SSLError):
        return 'Failed to establish network connection\n'

    if args['histgram']:
        texts = _make_text_popularity_histgram(popularities)
    else:
        texts = _make_text_popularity(popularities)

    return '\n'.join(texts)


def get_parser():
    parser = argparse.ArgumentParser(description='command line popularity checker')
    parser.add_argument('query', metavar='QUERY', type=str, nargs='*',
                        help='things of which you want to know popularity')
    parser.add_argument('-C', '--clear-cache', help='clear the cache',
                        action='store_true')
    parser.add_argument('-v', '--version', help='displays the current version of howpopular',
                        action='store_true')
    parser.add_argument('-H', '--histgram', help='display the histgram of popularity',
                        action='store_true')
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return

    if args['clear_cache']:
        _clear_cache()
        print('Cache cleared successfully')
        return

    if not args['query']:
        parser.print_help()
        return

    print(howpopular(args))

    # close the session to release connection
    howpopular_session.close()


if __name__ == '__main__':
    command_line_runner()
