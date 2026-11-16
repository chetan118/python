# 06_modules/main.py
# Session 6, file 2 of 2: the S5 chatbot, but the ChatLog class now lives in
# chat_log.py next to this file, and we IMPORT it.
#
# How to run it (from the repo root):  python3 06_modules/main.py
# Then try:  python3 06_modules/chat_log.py   to see the __main__ guard at work.
#
# Why this matters for AI engineering:
#   Every AI library is a module you import. You'll write lines like these
#   all the time:
#       import anthropic
#       from anthropic import Anthropic
#       import numpy as np
#       import pandas as pd
#   Splitting your own code into modules works exactly the same way.
#
# Python basics used here:
#   - import module                 : load a module, use it as module.name
#   - from module import name       : pull one name in, use it as plain name
#   - import module as alias        : give the module a shorter name
#   - standard library modules      : come with Python, no install (S1's random)
#   - __name__ == "__main__"        : see the bottom of chat_log.py


# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
# Convention (PEP 8): all imports at the top, standard library first,
# your own modules last, with a blank line between the groups.

# Style 1: "import module". You keep the module name as a prefix:
# datetime.date.today(). Longer, but you always see where a name came from.
# datetime is in the standard library, so there's nothing to install
# (installing other people's modules with pip is S7).
import datetime

# Style 2: "import module as alias". Same as style 1 with a shorter prefix.
# It's the convention for some popular libraries: "import numpy as np".
import random as rnd

# Style 3: "from module import name". You use the name directly: ChatLog(...)
#   JS:   import { ChatLog } from "./chat_log.js";
#   PHP:  use App\ChatLog;   (plus Composer's autoloader to find the file)
#   Ruby: require_relative "chat_log"   (then ChatLog is just there)
#
# Python finds chat_log.py because the folder of the script you RUN
# (06_modules/) is searched for imports automatically.
# Careful: that's different from open() paths, which are relative to
# the folder you run the command FROM (S4).
#
# A module only RUNS once. If another file imported chat_log again, Python
# would hand back the copy it already loaded, without running it again.
from chat_log import ChatLog

# Avoid "from module import *". It dumps every name into this file, so
# you can't tell where anything came from (like PHP's extract()).


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

LOG_FILE = "chat_log.txt"

REPLIES = {
    "hello": "Hi there! Ask me about modules.",
    "modules": "Any .py file is a module. Import it by its filename.",
    "date": f"Today is {datetime.date.today()}.",
}
FALLBACK = "I don't know that one. Try: " + ", ".join(REPLIES)

GREETINGS = ["Welcome back!", "Good to see you again.", "Hello again!"]


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------
# The guard is here too. Nothing imports main.py today, but it's a good
# habit, and it means you could import its settings later without starting
# a chat.

if __name__ == "__main__":
    log = ChatLog(LOG_FILE)
    log.load()

    if len(log) > 0:
        print(rnd.choice(GREETINGS))
        print(f"Loaded {log}:")
        log.show()
    else:
        print("No saved chat yet. Starting fresh.")

    print("\nChat with the bot. Press Enter on an empty line to finish.")

    while True:
        text = input("You: ")
        if text == "":
            break

        reply = REPLIES.get(text.strip().lower(), FALLBACK)
        print(f"Bot: {reply}")

        log.add("user", text)
        log.add("assistant", reply)

    log.save()
    print(f"\nSaved {log}.")

# Importing chat_log.py also created a "__pycache__" folder next to it.
# Python stores a compiled copy of each imported module there so the next
# import starts faster (a bit like PHP's OPcache, but saved as files).
# It's safe to delete, and it belongs in .gitignore.
