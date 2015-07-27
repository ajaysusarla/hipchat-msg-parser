import pytest
from hipchat_msg_parser.msg_parser import MsgParser
import json


def test_msg_parser_no_special_content():
    msg = "This is a normal message."
    mp = MsgParser()
    ret = mp.parse(msg)

    assert ret == '{}'


def test_msg_parser_mentions():
    msg = "@foo This is a message."
    mp = MsgParser()
    ret = mp.parse(msg)

    assert json.loads(ret) == {'mentions': ['foo']}


def test_msg_parser_emoticons():
    msg = "let us drink (coffee)."
    mp = MsgParser()
    ret = mp.parse(msg)

    assert json.loads(ret) == {'emoticons': ['coffee']}


def test_msg_parser_links(monkeypatch):
    msg = "follow this link http://foo.com/bar"

    monkeypatch.setattr("hipchat_msg_parser.msg_parser.get_title",
                        lambda x, t: "Foo")
    mp = MsgParser()
    ret = mp.parse(msg)

    assert json.loads(ret) == {'links': [{'title': 'Foo', 'url': 'http://foo.com/bar'}]}


def test_msg_parser_all_tokens(monkeypatch):
    msg = "@foo get some (awesome) content from http://bar.com/"

    monkeypatch.setattr("hipchat_msg_parser.msg_parser.get_title",
                        lambda x, t: "Bar")
    mp = MsgParser()
    ret = mp.parse(msg, list_all=True)

    data = [{'type': 'mentions', 'value': 'foo'},
            {'type': 'text', 'value': 'get some'},
            {'type': 'emoticons', 'value': 'awesome'},
            {'type': 'text', 'value': 'content from'},
            {'type': 'links', 'value': {'title': 'Bar', 'url': 'http://bar.com/'}}]

    assert json.loads(ret) == data
