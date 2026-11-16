# 06_modules/chat_log.py
# Session 6, file 1 of 2: the ChatLog class from S5, moved into its own file.
# A file like this, meant to be imported, is called a MODULE. Every .py
# file is a module; there's nothing special to declare.
#
# You normally don't run this file. main.py imports it:
#     python3 06_modules/main.py
# But you CAN run it directly to try its self-test at the bottom:
#     python3 06_modules/chat_log.py
#
# The module name is the filename without ".py", so this is "chat_log".
# That's why files you import must start with a letter and use snake_case:
# "import 06_modules" would be a syntax error, like a variable named 06x.


# Importing a module RUNS it, top to bottom, the first time it's imported.
# This line proves it: you'll see it when main.py starts.
#
# __name__ is a variable Python sets in every file:
#   - "chat_log" when this file is imported
#   - "__main__" when you run this file directly
print(f"[chat_log.py is running, __name__ = {__name__!r}]")


# ---------------------------------------------------------------------------
# The class (same as S5, with the S5 comments trimmed)
# ---------------------------------------------------------------------------
# Defining things at the top level of a module (classes, functions,
# constants) is what makes them importable. Nothing needs to be "exported":
# everything at the top level is public.
#   JS:  you must write "export class ChatLog"
#   PHP/Ruby: a class is global once its file is loaded


class ChatLog:
    def __init__(self, path):
        self.path = path
        self.messages = []

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})

    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            for message in self.messages:
                f.write(f"{message['role']}: {message['content']}\n")

    def load(self):
        self.messages = []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                for line in f:
                    role, content = line.rstrip("\n").split(": ", 1)
                    self.add(role, content)
        except FileNotFoundError:
            pass

    def show(self):
        for message in self.messages:
            print(f"  {message['role']}: {message['content']}")

    def __len__(self):
        return len(self.messages)

    def __str__(self):
        return f"ChatLog({self.path}, {len(self)} messages)"


# ---------------------------------------------------------------------------
# The __main__ guard
# ---------------------------------------------------------------------------
# Code inside this "if" runs ONLY when you run this file directly, not when
# another file imports it. Without the guard, every "import chat_log" would
# also run this test.
#   Ruby: if __FILE__ == $0
#   Node: if (require.main === module)
#   PHP:  no built-in equivalent; an include always runs the whole file
#
# You'll see this guard at the bottom of most Python scripts.
if __name__ == "__main__":
    # A quick self-test. It never calls save(), so no file is written.
    test_log = ChatLog("test.txt")
    test_log.add("user", "hi")
    test_log.add("assistant", "hello!")
    print(test_log)
    test_log.show()
