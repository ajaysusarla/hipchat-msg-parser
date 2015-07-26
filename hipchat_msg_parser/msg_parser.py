import re
import json
from .utils import is_url, get_title
import concurrent.futures

class MsgParser(object):
    def __init__(self):
        self._mentions = []
        self._emoticons = []
        self._links = []
        self._tokens = []

        # regex for emoticons:
        self._emoticon_regex = re.compile('\(([a-zA-Z0-9]{1,15})\)',
                                          re.IGNORECASE)

    def _process_links(self, links):
        # https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor-example
        data = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_link = {executor.submit(get_title, link, 60): link for link in links}
            for future in concurrent.futures.as_completed(future_link):
                url = future_link[future]
                try:
                    title = future.result()
                except Exception:
                    title = ""
                finally:
                    link = {}
                    link["url"] = url
                    link["title"] = title
                    data.append(link)

        return data

    def tokenize(self, msg):
        for tok in msg.split():
            if tok.startswith("@"):
                self.mentions(tok)
            elif tok.startswith("("):
                self.emoticons(tok)
            elif is_url(tok):
                self.links(tok)
            else:
                # normal text - do nothing!
                pass

    def mentions(self, token):
        self._mentions.append(token.strip('@'))

    def emoticons(self, token):
        match = self._emoticon_regex.match(token)
        if match:
            self._emoticons.append(match.group(1))

    def links(self, token):
        self._links.append(token)

    def genparse(self):
        parsed_msg = {}
        if len(self._mentions):
            parsed_msg["mentions"] = self._mentions
        if len(self._emoticons):
            parsed_msg["emoticons"] = self._emoticons
        if len(self._links):
            data = self._process_links(self._links)
            parsed_msg["links"] = data

        return json.dumps(parsed_msg, indent=2)

