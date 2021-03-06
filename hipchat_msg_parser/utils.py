#-------------------------------------
# hipchat_msg_parser: utils.py
#-------------------------------------

import logging
import rfc3987
from bs4 import BeautifulSoup
import urllib2
from urlparse import urlparse

logger = logging.getLogger("hipchat_msg_parser.utils")

def is_url(url):
    """
    Returns True if `url` is an IRI as specified in the RFC 3987
    (https://www.ietf.org/rfc/rfc3987.txt)
    """
    try:
        rfc3987.parse(url, rule='IRI')
        return True
    except ValueError:
        logger.warning("%s is not a valid url.", url)
        return False


def get_title(url, timeout=60):
    """
    Returns the title of the HTML page pointed to by `url`.
    """
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme not in ['http', 'https']:
            return ""

        soup = BeautifulSoup(urllib2.urlopen(url, timeout=timeout), "html.parser")

        return soup.title.string if soup.title.string else ""
    except:
        logger.warning("Could not get title of %s.", url)
        return ""
