import rfc3987
from bs4 import BeautifulSoup
import urllib2
from urlparse import urlparse


def is_url(url):
    """
    Returns True if `url` is an IRI as specified in the RFC 3987
    (https://www.ietf.org/rfc/rfc3987.txt)
    """
    try:
        rfc3987.parse(url, rule='IRI')
        return True
    except ValueError:
        return False


def get_title(url):
    """
    Returns the title of the HTML page pointed to by `url`.
    """
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ['http', 'https']:
            return ""

        soup = BeautifulSoup(urllib2.urlopen(url), "html.parser")

        return soup.title.string if soup.title.string else ""
    except:
        return ""
