import re
import json
from .utils import is_url, get_title

class MsgParser(object):
    def __init__(self):
        self._mentions = []
        self._emoticons = []
        self._links = []

        self._emoticon_regex = re.compile('\(([a-zA-Z0-9]{1,15})\)', re.IGNORECASE)

    def parse(self, msg):
        for tok in msg.split():
            if tok.startswith("@"):
                self.mentions(tok)
            elif tok.startswith("("):
                self.emoticons(tok)
            elif is_url(tok):
                self.links(tok)
            else:
                # normal text
                pass


    def mentions(self, token):
        self._mentions.append(token.strip('@'))

    def emoticons(self, token):
        match = self._emoticon_regex.match(token)
        if match:
            self._emoticons.append(match.group(1))

    def links(self, token):
        link = {}
        link["url"] = token
        link["title"] = get_title(token)

        self._links.append(link)

    def report(self):
        parsed_msg = {}
        if len(self._mentions):
            parsed_msg["mentions"] = self._mentions
        if len(self._emoticons):
            parsed_msg["emoticons"] = self._emoticons
        if len(self._links):
            parsed_msg["links"] = self._links

        return json.dumps(parsed_msg, indent=2)
