import pytest
from mock import MagicMock
from hipchat_msg_parser.utils import is_url, get_title


def test_is_url():
    assert is_url("www.something.com") == False
    assert is_url("http://foo.com/bar") == True
    assert is_url("invalid") == False

def test_get_title_unsupported_scheme():
    assert get_title("ftp://foo.com/bar") == ""

def test_get_title_bs4_raises_exception(monkeypatch):
    class MockBS4(object):
        def __init__(self, url, mode):
            raise Exception

    def mock_urlopen(url, timeout):
        assert url == "http://foo.com"

    monkeypatch.setattr("hipchat_msg_parser.utils.urllib2.urlopen", mock_urlopen)
    monkeypatch.setattr("hipchat_msg_parser.utils.BeautifulSoup", MockBS4)

    assert get_title("http://foo.com") == ""


def test_get_title_bs4_valid_title(monkeypatch):

    def mock_urlopen(url, timeout):
        assert url == "http://foo.com"
        return "<html><title>FooBar</title></html>"

    monkeypatch.setattr("hipchat_msg_parser.utils.urllib2.urlopen", mock_urlopen)
    #monkeypatch.setattr("hipchat_msg_parser.utils.BeautifulSoup", MagicMock())

    assert get_title("http://foo.com") == "FooBar"
