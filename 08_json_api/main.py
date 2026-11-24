# 08_json_api/main.py
# Session 8, file 2 of 2: the S6 chatbot, now saving to chat_log.json, and
# its replies come from a real web server over HTTP.
#
# How to run it (venv active, from the repo root):
#     pip install -r requirements.txt     # installs requests (new this session)
#     python 08_json_api/main.py
# Then look at the saved file:   cat chat_log.json
#
# Why this matters for AI engineering:
#   Calling an AI model means "POST some JSON to a URL, get JSON back".
#   This program does exactly that, against httpbin.org: a free test server
#   that sends back whatever you send it (an "echo" server). No account, no
#   API key. In S10 the URL becomes Anthropic's, and the reply comes from a
#   model instead of an echo.
#
# Python basics used here:
#   - requests.post(url, json=..., timeout=...)  : send JSON over HTTP
#   - response.raise_for_status()                : turn 4xx/5xx into an error
#   - response.json()                            : JSON reply -> dict
#   - requests.RequestException                  : catch any network error
#   - nested access: data["json"]["messages"][-1]["content"]
#   - list.pop()                                 : remove the last item


# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
# Third-party first (installed with pip, S7), then our own module (S6).
#
# requests is THE Python library for HTTP: Python's version of Laravel's
# Http facade (which wraps Guzzle), Ruby's Faraday, or JS's fetch.
# This time the pip name and the import name are the same: "requests".
import requests

from chat_log import ChatLog


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

# A new file. S4-S6 used chat_log.txt; that one stays as it was.
LOG_FILE = "chat_log.json"

ECHO_URL = "https://httpbin.org/post"


# ---------------------------------------------------------------------------
# Talking to the server
# ---------------------------------------------------------------------------


def ask_server(messages):
    # The request body: a plain dict shaped like a real AI API request
    # (which model, a reply length limit, and the conversation so far).
    # httpbin ignores "model" and "max_tokens"; they're here so S10 looks
    # familiar.
    payload = {
        "model": "echo-bot",
        "max_tokens": 100,
        "messages": messages,
    }

    # requests.post() sends an HTTP POST and WAITS for the reply.
    #   Laravel:  Http::timeout(10)->post($url, $payload)
    #   Ruby:     Faraday.post(url, payload.to_json, "Content-Type" => "application/json")
    #   JS:       await fetch(url, { method: "POST",
    #                                headers: { "Content-Type": "application/json" },
    #                                body: JSON.stringify(payload) })
    #
    # json=payload does two jobs for you: it runs json.dumps(payload) to
    # make the body, and sets the header "Content-Type: application/json".
    # Like Laravel's Http::post; with fetch you do both yourself.
    #
    # There's no await: requests is synchronous. The line simply blocks
    # until the reply arrives, like PHP and Ruby (unlike JS's fetch).
    #
    # timeout=10 means "give up after 10 seconds". requests has NO default
    # timeout, so without it a stuck server would hang your program
    # forever. Always pass one.
    #
    # (For a GET with a query string:
    #     requests.get(url, params={"q": "python"}, timeout=10)
    #  sends url?q=python, like Http::get($url, ["q" => "python"]).)
    response = requests.post(ECHO_URL, json=payload, timeout=10)

    # response.status_code is the HTTP status as an int: 200, 404, 503...
    # raise_for_status() raises requests.HTTPError for any 4xx or 5xx and
    # does nothing for 2xx, like Laravel's ->throw(). Without it, an error
    # page would reach .json() below and fail there, more confusingly.
    response.raise_for_status()

    # .json() parses the reply body: JSON text -> dicts and lists. It calls
    # json.loads() for you, like Laravel's ->json() or JS's res.json().
    return response.json()


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------
# The ChatLog lines (ChatLog(...), load, len, show, add, save) are the same
# as in S6, even though save and load now write JSON.

if __name__ == "__main__":
    log = ChatLog(LOG_FILE)
    log.load()

    if len(log) > 0:
        print(f"Loaded {log}:")
        log.show()
    else:
        print("No saved chat yet. Starting fresh.")

    print("\nChat with the echo server. Press Enter on an empty line to finish.")

    while True:
        text = input("You: ")
        if text == "":
            break

        # Add the user's message FIRST, so the request carries the whole
        # conversation, this message included. AI APIs work the same way:
        # they remember nothing between calls, so every request sends the
        # full history.
        log.add("user", text)

        try:
            data = ask_server(log.messages)
        # RequestException is the parent class of every requests error:
        # no network, DNS failure, timeout, and the HTTPError from
        # raise_for_status(). Catching the parent catches them all, like
        # catching a base exception class in PHP.
        # "as error" puts the exception in a variable
        # (PHP: catch (Exception $e)   Ruby: rescue => e   JS: catch (e)).
        except requests.RequestException as error:
            print(f"Bot: (couldn't reach the server: {error})")
            # The message got no reply, so take it back out of the log.
            # .pop() removes and returns the LAST item
            # (PHP: array_pop($arr)   Ruby/JS: arr.pop).
            log.messages.pop()
            continue

        # data is the echo server's reply, already a dict. Trimmed, it
        # looks like this:
        #   {
        #     "json": {"model": "echo-bot", "max_tokens": 100,
        #              "messages": [{"role": "user", "content": "hi"}]},
        #     "headers": {"Content-Type": "application/json", ...},
        #     "url": "https://httpbin.org/post",
        #     ...
        #   }
        # "json" holds what the server received from us, already parsed.
        # Dig in one key or index at a time, just like a nested PHP array:
        #   PHP:     $data["json"]["messages"]
        #   Python:  data["json"]["messages"]
        echoed = data["json"]["messages"]

        # [-1] is the LAST item: negative indexes count from the end.
        #   PHP: end($arr)   Ruby: arr[-1]   JS: arr.at(-1)
        last = echoed[-1]["content"]
        content_type = data["headers"]["Content-Type"]

        reply = (
            f"The server got {len(echoed)} messages as {content_type}. "
            f"Your last one: '{last}'"
        )
        # (Parentheses let one expression span several lines. Two strings
        # side by side are joined into one, so this is a single f-string.)

        print(f"Bot: {reply}")
        log.add("assistant", reply)

    log.save()
    print(f"\nSaved {log}. Have a look:  cat {LOG_FILE}")
