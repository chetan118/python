# 08_json_api/chat_log.py
# Session 8, file 1 of 2: the ChatLog class from S6, but save() and load()
# now use JSON instead of "role: content" lines.
#
# The rest of the class is unchanged, and main.py uses it exactly the same
# way (add, load, save, show, len). That's the payoff promised in S5:
# change HOW a class does its job, and the code using it doesn't notice.
#
# You can run this file directly to try its self-test (no file is written):
#     python 08_json_api/chat_log.py
#
# Why this matters for AI engineering:
#   JSON is how programs talk to AI APIs. The request you send is JSON, the
#   reply you get back is JSON, and our list of {"role": ..., "content": ...}
#   dicts is exactly what goes inside the request.


# json is in the standard library: nothing to pip install.
import json


# ---------------------------------------------------------------------------
# JSON in four functions
# ---------------------------------------------------------------------------
#                      to JSON text            from JSON text
#   PHP:               json_encode($x)         json_decode($s, true)
#   Ruby:              JSON.generate(x)        JSON.parse(s)
#   JS:                JSON.stringify(x)       JSON.parse(s)
#   Python (string):   json.dumps(x)           json.loads(s)
#   Python (file):     json.dump(x, f)         json.load(f)
#
# The "s" in dumps/loads stands for "string". Without the "s", they write
# to / read from an open file directly.
#
# How Python values map to JSON:
#   dict  <->  {"object": ...}        True / False  <->  true / false
#   list  <->  ["array"]              None          <->  null
#   str   <->  "string"               int / float   <->  number
#
# Reading JSON always gives you dicts, like PHP's json_decode($s, true)
# WITH the true (assoc arrays, not stdClass objects). So you read the
# result with data["key"], never data.key (no dot access on dicts, S3).


# ---------------------------------------------------------------------------
# The class (same as S6, except save and load)
# ---------------------------------------------------------------------------


class ChatLog:
    def __init__(self, path):
        self.path = path
        self.messages = []

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})

    # save(): the whole list goes into the file in ONE call. No loop, no
    # "\n", no f-string: json.dump turns the list of dicts into JSON text.
    #   indent=2           : pretty-print, one item per line
    #                        (PHP: JSON_PRETTY_PRINT)
    #   ensure_ascii=False : keep "café" as it is instead of "café"
    #                        (PHP: JSON_UNESCAPED_UNICODE)
    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, indent=2, ensure_ascii=False)

    # load(): one call reads the file back into a list of dicts. No split()
    # and no unpacking: JSON marks where each message starts and ends, so
    # a ": " or a newline inside a message can't break it (that was the
    # weak spot of the S4 text format).
    def load(self):
        self.messages = []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.messages = json.load(f)
        except FileNotFoundError:
            pass
        # One try can have several except blocks, checked top to bottom
        # (like several catch blocks in PHP, or rescue lines in Ruby).
        #
        # A file that isn't valid JSON (half-written, broken by hand...)
        # raises json.JSONDecodeError. Python RAISES, like Ruby's
        # JSON::ParserError. PHP's json_decode just returns null unless you
        # pass JSON_THROW_ON_ERROR.
        # Careful: starting fresh means the next save() overwrites that file.
        except json.JSONDecodeError:
            print(f"{self.path} isn't valid JSON. Starting fresh.")

    def show(self):
        for message in self.messages:
            print(f"  {message['role']}: {message['content']}")

    def __len__(self):
        return len(self.messages)

    def __str__(self):
        return f"ChatLog({self.path}, {len(self)} messages)"


# ---------------------------------------------------------------------------
# Self-test: dumps and loads, without touching a file
# ---------------------------------------------------------------------------
# Runs only when you run this file directly, not when main.py imports it (S6).

if __name__ == "__main__":
    test_log = ChatLog("test.json")
    # Two messages that would break the S4 text format: a newline, and
    # quotes plus ": " inside the text.
    test_log.add("user", "line one\nline two")
    test_log.add("assistant", 'She said "hi": ok')

    # dumps() gives the JSON as a STRING, so we can look at it. See how the
    # newline became \n and the quotes became \" inside the JSON text.
    text = json.dumps(test_log.messages, indent=2)
    print(text)

    # loads() turns the string back into a list of dicts.
    back = json.loads(text)

    # == compares lists and dicts by VALUE, item by item (like PHP's ==
    # on arrays). In JS, [] == [] is false, because it compares references.
    print("Round trip OK:", back == test_log.messages)

    # type() tells you what something is.
    #   PHP: get_debug_type($x)   Ruby: x.class   JS: typeof x (roughly)
    print(type(back), type(back[0]))
