import pytest
from hipchat_msg_parser.msg_parser import MsgParser
import json


def test_msg_parser_no_special_content():
    msg = "This is a normal message."
    mp = MsgParser()
    mp.parse(msg)
    ret = mp.report()

    assert ret == '{}'


def test_msg_parser_mentions():
    msg = "@foo This is a message."
    mp = MsgParser()
    mp.parse(msg)
    ret = mp.report()

    assert json.loads(ret) == {'mentions': ['foo']}


def test_msg_parser_emoticons():
    msg = "let us drink (coffee)."
    mp = MsgParser()
    mp.parse(msg)
    ret = mp.report()

    assert json.loads(ret) == {'emoticons': ['coffee']}


def test_msg_parser_links(monkeypatch):
    msg = "follow this link http://foo.com/bar"

    monkeypatch.setattr("hipchat_msg_parser.msg_parser.get_title",
                        lambda x: "Foo")
    mp = MsgParser()
    mp.parse(msg)
    ret = mp.report()

    assert json.loads(ret) == {'links': [{'title': 'Foo', 'url': 'http://foo.com/bar'}]}
