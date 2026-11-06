# 03_chat_log.py
# Session 3: a tiny pretend chatbot. You type messages, a "bot" answers from
# a dictionary of canned replies, and every message is saved in a chat log.
#
# How to run it:  python3 03_chat_log.py
#
# Why this matters for AI engineering:
#   When you call an AI model, you send the conversation as a LIST of DICTS:
#       [{"role": "user", "content": "Hi"},
#        {"role": "assistant", "content": "Hello!"}]
#   This program builds exactly that shape. In S10 you'll send a real one.
#
# Python basics used here:
#   - dict             : key -> value pairs, like {"role": "user"}
#   - d["key"]         : read a value (KeyError if the key is missing)
#   - d.get(k, default): read a value, or get the default if it's missing
#   - "key" in d       : check whether a key exists
#   - d["key"] = value : add or change a value
#   - for k, v in d.items() : loop over keys and values together
#   - list of dicts    : the chat log
#   - .lower() / .strip() : clean up text before using it as a key


# ---------------------------------------------------------------------------
# Dictionaries
# ---------------------------------------------------------------------------
# A dict maps keys to values. It's the Python version of:
#
#   PHP:   ["hello" => "Hi there!"]     (an associative array)
#   Ruby:  { "hello" => "Hi there!" }   (a Hash)
#   JS:    { hello: "Hi there!" }       (an object, or a Map)
#
# Two differences to watch:
#   - JS lets you write keys without quotes ({hello: 1}). Python doesn't:
#     {hello: 1} would look for a VARIABLE named hello. Quote your keys.
#   - Ruby code often uses symbols (:hello). Python has no symbols,
#     so string keys are the normal choice.
#
# Since Python 3.7, dicts remember the order you added keys (like PHP arrays).

REPLIES = {
    "hello": "Hi there! Ask me about python, php or ruby.",
    "python": "Python uses indentation instead of { } or end.",
    "php": "PHP puts $ in front of every variable. Python doesn't.",
    "ruby": "Ruby and Python both like snake_case names.",
}

# The ALL_CAPS name is only a convention meaning "don't change this".
# Python has no real constants (no PHP const / Ruby freeze by default).

FALLBACK = "I don't know that one. Try: " + ", ".join(REPLIES)
# ", ".join(...) glues strings together with ", " between them.
#   PHP: implode(", ", ...)   Ruby/JS: .join(", ")
# It's a method on the SEPARATOR, which surprises everyone at first.
# Looping over a dict (or joining it) gives you its KEYS.


def bot_reply(text):
    # Clean the input so "  Hello " and "HELLO" both match "hello".
    #   .strip() = PHP trim(), Ruby .strip, JS .trim()
    #   .lower() = PHP strtolower(), Ruby .downcase, JS .toLowerCase()
    key = text.strip().lower()

    # Three ways to read from a dict:
    #
    #   REPLIES["hello"]        -> the value, but CRASHES with KeyError
    #                              if the key is missing.
    #                              (PHP gives a warning + null, Ruby gives nil,
    #                              JS gives undefined. Python is strict again.)
    #
    #   REPLIES.get("hello")    -> the value, or None if missing. No crash.
    #
    #   REPLIES.get("hello", FALLBACK)
    #                           -> the value, or FALLBACK if missing.
    #                              (like PHP $a["k"] ?? $default,
    #                               Ruby h.fetch("k", default))
    return REPLIES.get(key, FALLBACK)


def show_log(log):
    print("\n--- Chat log ---")

    # Each message is a dict, so we read its fields with ["..."].
    #   PHP: $message["role"]   Ruby: message["role"]   JS: message.role
    # Python has no dot access for dicts: message.role would be an error.
    for message in log:
        print(f"{message['role']:>9}: {message['content']}")
        # Note the single quotes inside the f-string. Using " inside a
        # "..." f-string only works on Python 3.12+, so ' is the safe choice.
        # {...:>9} right-aligns the text in 9 characters, so the colons line up.


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

log = []  # a list that will hold one dict per message

print("Chat with the bot. Press Enter on an empty line to finish.")

while True:
    text = input("You: ")
    if text == "":
        break

    reply = bot_reply(text)
    print(f"Bot: {reply}")

    # Save both messages in the same shape an AI API expects.
    log.append({"role": "user", "content": text})
    log.append({"role": "assistant", "content": reply})

if not log:
    print("No messages.")
else:
    show_log(log)

    # Count messages per role, using a dict as a counter.
    counts = {}
    for message in log:
        role = message["role"]

        # "in" checks for a KEY (PHP isset / array_key_exists,
        # Ruby .key?, JS "key" in obj).
        if role in counts:
            counts[role] += 1
        else:
            counts[role] = 1  # assigning to a new key adds it

    # .items() gives (key, value) pairs, and "for k, v in" unpacks them.
    #   PHP:  foreach ($counts as $role => $n)
    #   Ruby: counts.each do |role, n|
    #   JS:   for (const [role, n] of Object.entries(counts))
    print("\nMessages per role:")
    for role, n in counts.items():
        print(f"  {role}: {n}")

    # Finally, print the raw list of dicts. This is what you'd send to a model.
    print("\nRaw log (what an AI API would receive):")
    print(log)
