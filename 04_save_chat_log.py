# 04_save_chat_log.py
# Session 4: the S3 chatbot, but the chat log is SAVED to a file when you quit
# and LOADED back next time. Run it twice and the bot "remembers" the old chat.
#
# How to run it:  python3 04_save_chat_log.py   (then run it again!)
#
# Why this matters for AI engineering:
#   AI models remember nothing between calls. Every app that "remembers" a
#   conversation is doing what this file does: store the messages somewhere,
#   load them back, and send the whole history again next time.
#
# Python basics used here:
#   - open(path, mode)      : open a file, "r" = read, "w" = write, "a" = append
#   - with ... as f:        : closes the file for you when the block ends
#   - f.write(text)         : write text (you add the "\n" yourself)
#   - for line in f:        : read a file one line at a time
#   - FileNotFoundError     : the error you get opening a file that isn't there
#   - .split(": ", 1)       : cut a string into a list, at most 1 cut
#   - a, b = some_list      : unpack a 2-item list into 2 variables


# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------

# A relative path is relative to the folder you RUN the command from
# (the "current working directory"), not the folder the .py file is in.
# Same as PHP's fopen("chat_log.txt") or Ruby's File.open("chat_log.txt").
LOG_FILE = "chat_log.txt"

# A smaller version of the S3 replies, so this file stays about files.
REPLIES = {
    "hello": "Hi there! Ask me about files.",
    "files": "open() + with = the file closes itself.",
}
FALLBACK = "I don't know that one. Try: " + ", ".join(REPLIES)


# ---------------------------------------------------------------------------
# Writing a file
# ---------------------------------------------------------------------------
# Each message becomes one line of text, like:
#     user: hello
#     assistant: Hi there! Ask me about files.


def save_log(path, log):
    # open() with "w" creates the file, or EMPTIES it if it already exists.
    # Use "a" (append) to add to the end instead. Same letters as PHP's fopen().
    #
    # "with" closes the file automatically when the indented block ends,
    # even if an error happens inside it.
    #
    #   Python:  with open(path, "w") as f: ...
    #   PHP:     $f = fopen($path, "w"); ... fclose($f);   (you close it)
    #   Ruby:    File.open(path, "w") do |f| ... end      (closes itself, like Python)
    #   JS:      fs.writeFileSync(path, text)             (Node, all at once)
    #
    # encoding="utf-8" makes the file the same on every computer.
    # Without it, Windows may use a different default and break emojis or accents.
    with open(path, "w", encoding="utf-8") as f:
        for message in log:
            # write() does NOT add a newline (unlike print), so add "\n" yourself.
            # It's like PHP's fwrite(), not like Ruby's puts.
            f.write(f"{message['role']}: {message['content']}\n")

    # The file is already closed here, because we left the "with" block.


# ---------------------------------------------------------------------------
# Reading a file
# ---------------------------------------------------------------------------


def load_log(path):
    log = []

    # The first run has no file yet. Opening a missing file for reading
    # raises FileNotFoundError, so we catch it and start with an empty log.
    #   PHP gives a warning and returns false, Ruby raises Errno::ENOENT,
    #   Node's readFileSync throws an error with code "ENOENT".
    try:
        with open(path, "r", encoding="utf-8") as f:
            # Looping over a file gives you one line at a time, "\n" included.
            # (To get the whole file as one string: f.read(),
            #  like PHP's file_get_contents() or Ruby's File.read.)
            for line in f:
                # rstrip("\n") removes the newline from the end only.
                line = line.rstrip("\n")

                # split(": ", 1) cuts at the FIRST ": " only, so a message
                # like "note: this: works" still splits into exactly 2 parts:
                #   "user: note: this: works" -> ["user", "note: this: works"]
                #   PHP: explode(": ", $line, 2)   Ruby: line.split(": ", 2)
                # (Careful: Python's number is "max cuts", PHP/Ruby's is "max parts".)
                #
                # "role, content = [...]" unpacks the list into two variables.
                # Same idea as "for k, v in d.items()" from S3.
                #   PHP: [$role, $content] = ...   JS: const [role, content] = ...
                role, content = line.split(": ", 1)

                log.append({"role": role, "content": content})
    except FileNotFoundError:
        pass  # "pass" means "do nothing". Python needs SOMETHING in a block.

    return log


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

log = load_log(LOG_FILE)

if log:
    print(f"Loaded {len(log)} messages from last time:")
    for message in log:
        print(f"  {message['role']}: {message['content']}")
else:
    print("No saved chat yet. Starting fresh.")

print("\nChat with the bot. Press Enter on an empty line to finish.")

while True:
    text = input("You: ")
    if text == "":
        break

    reply = REPLIES.get(text.strip().lower(), FALLBACK)
    print(f"Bot: {reply}")

    log.append({"role": "user", "content": text})
    log.append({"role": "assistant", "content": reply})

save_log(LOG_FILE, log)
print(f"\nSaved {len(log)} messages to {LOG_FILE}. Run me again to see them.")

# Plain text works here, but it's fragile: a message with a newline in it
# would break the "one message per line" rule. In S8 you'll save the same
# list of dicts as JSON instead, the format AI APIs actually use.
