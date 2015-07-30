# -*- coding: utf-8 -*-
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


def test_sg_parser_emoticons_more_than_15_characters_long():
    msg = "this contains an emoticon (foobarthisthatsomethingelse) that is long."
    mp = MsgParser()
    ret = mp.parse(msg)

    assert json.loads(ret) == {}


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


def test_msg_parser_incomplete_parantheses():
    msg = "This message has an incomplete (parantheses."

    mp = MsgParser()
    ret = mp.parse(msg)

    assert ret == '{}'


def test_msg_parser_with_no_links():
    msg = "Hello @joe, let us drink (coffee) at starbucks."
    mp = MsgParser()
    ret = mp.parse(msg)

    assert json.loads(ret) == {'emoticons': ['coffee'], 'mentions': ['joe']}


def test_msg_parser_with_mentions_ending_in_punctuations():
    msg = "@ant, @bat: @cat--, @dog."
    mp = MsgParser()
    ret = mp.parse(msg)

    assert json.loads(ret) == {'mentions': ['ant', 'bat', 'cat', 'dog']}


def test_msg_parser_with_unbalanced_parans():
    msg = "((some text here."
    mp = MsgParser()
    ret = mp.parse(msg)

    assert json.loads(ret) == {}


def test_msg_parser_with_nested_parans_for_emoticons():
    msg = "((emoticon1)) (emoticon2) (((((emoticon3))))) ((not-an-emoticon."
    mp = MsgParser()
    ret = mp.parse(msg)

    assert json.loads(ret) == {'emoticons' : ['(emoticon1)',
                                              'emoticon2',
                                              '((((emoticon3))']}

# Currently don't support UTF-8, this test should break when we fix the code.
def test_msg_parser_utf8_mentions_not_supported():
    msg = "@ƒ∂ßßå∫√çΩ fails the mention parsing."
    mp = MsgParser()
    ret = mp.parse(msg)

    assert json.loads(ret) == {'mentions': ['']}

# Currently don't support UTF-8, this test should break when we fix the code.
def test_msg_parser_utf8_emoticons_not_supported():
    msg = "what is this (ƒ∂ßßå∫√çΩ)."
    mp = MsgParser()
    ret = mp.parse(msg)

    assert json.loads(ret) == {}


# Currently don't support UTF-8, this test should break when we fix the code.
def test_msg_parser_parse_all_utf8_not_supported():
    msg = "@ƒ∂ß (ßå∫√çΩ) will not parse mentions."
    mp = MsgParser()
    ret = mp.parse(msg, list_all=True)
    #import pdb
    #pdb.set_trace()

    a = '[\n  {\n    "type": "mentions", \n    "value": ""\n  }, \n  {\n    "type": "text", \n    "value": "(\\u00df\\u00e5\\u222b\\u221a\\u00e7\\u03a9) will not parse mentions."\n  }\n]'
    assert json.loads(ret) == json.loads(a)
