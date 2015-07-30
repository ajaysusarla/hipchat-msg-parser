#-------------------------------------
# hipchat_msg_parser: msg_parser.py
#-------------------------------------

import logging
import re
import json
import string
from .utils import is_url, get_title
import concurrent.futures

class TokenType(object):
    TEXT = "text"
    EMOTICON = "emoticons"
    MENTION = "mentions"
    LINK = "links"

class Token(object):
    """
    This class represents the tokens generated after a scan.
    """
    def __str__(self):
        return "Token(%s,%r)" % (self.type, self.value)
    def __repr__(self):
        return str(self)


class MsgParser(object):
    """
    The MsgParser class, parses a HipChat message into tokens
    which are then processed to generate a dict of all tokens or
    just tokens with special content(mentions, emoticons, links).
    """
    def __init__(self):
        self._tokens = []
        self.logger = logging.getLogger("hipchat_msg_parser.msg_parser")

        # regex for emoticons:
        self._is_emoticon = re.compile('\(([a-zA-Z0-9()]{1,15})\)',
                                       re.IGNORECASE)

        # Stripping mentions of special characters in the begining and end
        tab = string.maketrans('','')
        self.trans_tab = tab.translate(tab,\
            '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')


    def _add_token(self, t_type, t_value):
        tok = Token()
        tok.type = t_type
        tok.value = t_value

        self._tokens.append(tok)


    def _text(self, token):
        if len(self._tokens) and self._tokens[-1].type == TokenType.TEXT:
            self._tokens[-1].value = " ".join([self._tokens[-1].value,
                                               token])
        else:
            self._add_token(TokenType.TEXT, token)


    def _mention(self, token):
        self._add_token(TokenType.MENTION, token.strip(self.trans_tab))


    def _emoticon(self, token):
        self._add_token(TokenType.EMOTICON, token)


    def _link(self, token):
        self._add_token(TokenType.LINK, token)


    def _process_links(self, links):
        future_link = {}
        self.logger.debug("Processing links.")
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            for pos in links:
                link = self._tokens[pos].value
                future_link[executor.submit(get_title, link, 20)] = (link, pos)

            for future in concurrent.futures.as_completed(future_link):
                url, pos = future_link[future]
                try:
                    title = future.result()
                except Exception:
                    title = ""
                finally:
                    info = {}
                    info["url"] = url
                    info["title"] = title
                    self._tokens[pos].value = info


    def _tokenize(self, msg):
        self.logger.debug("Generating tokens.")

        link_tokens_pos = []

        for word in msg.split():
            if word.startswith("@"):
                self._mention(word)
            elif word.startswith("("):
                match = self._is_emoticon.match(word)
                if match:
                    self._emoticon(match.group(1))
                else:
                    self._text(word)
            elif is_url(word):
                self._link(word)
                link_tokens_pos.append(len(self._tokens) - 1)
            else:
                self._text(word)


        self._process_links(link_tokens_pos)

        return self._tokens


    def _genparse(self, tokens):
        self.logger.debug("Generating dict of special content tokens.")
        data = {}
        for tok in tokens:
            if tok.type is not TokenType.TEXT:
                try:
                    data[tok.type].append(tok.value)
                except KeyError:
                    data[tok.type] = []
                    data[tok.type].append(tok.value)

        return data

    def _genparse_list_all(self, tokens):
        self.logger.debug("Generating list of all tokens.")
        data = []
        for tok in tokens:
            val = {}
            val["type"] = tok.type
            val["value"] = tok.value
            data.append(val)

        return data


    def parse(self, msg, list_all=False):
        if self._tokens:
            self.logger.debug("Freeing tokens list.")
            del self._tokens[:]

        tokens = self._tokenize(msg)
        if list_all:
            data = self._genparse_list_all(tokens)
        else:
            data = self._genparse(tokens)

        return json.dumps(data, indent=2)
