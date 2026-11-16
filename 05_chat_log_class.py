# 05_chat_log_class.py
# Session 5: the S4 chatbot again, but the chat log is now a CLASS. The
# save/load functions from S4 become methods on a ChatLog object that keeps
# its own messages and its own file path.
#
# How to run it:  python3 05_chat_log_class.py
# It uses the same chat_log.txt format as S4, so it loads the chat you saved there.
#
# Why this matters for AI engineering:
#   AI SDKs are classes. You create a client object, then call its methods:
#       client = anthropic.Anthropic()
#       client.messages.create(...)
#   Reading code like that, and wrapping your own chat history in a class,
#   starts here.
#
# Python basics used here:
#   - class Name:              : define a class (names are PascalCase)
#   - def __init__(self, ...)  : the constructor, runs when you create an object
#   - self                     : the object itself, written out in every method
#   - self.name = value        : create/set an attribute (no declarations needed)
#   - Name(...)                : create an object (no "new" keyword)
#   - __len__ / __str__        : "dunder" methods that len() and print() use


# ---------------------------------------------------------------------------
# Settings (same as S4)
# ---------------------------------------------------------------------------

LOG_FILE = "chat_log.txt"

REPLIES = {
    "hello": "Hi there! Ask me about classes.",
    "classes": "A class bundles data (attributes) with the code that uses it (methods).",
}
FALLBACK = "I don't know that one. Try: " + ", ".join(REPLIES)


# ---------------------------------------------------------------------------
# The class
# ---------------------------------------------------------------------------
#   Python:  class ChatLog:
#   PHP:     class ChatLog { ... }
#   Ruby:    class ChatLog ... end
#   JS:      class ChatLog { ... }
#
# No braces or "end": like everything else in Python, the indented block
# under "class ChatLog:" IS the class.


class ChatLog:
    # __init__ is the constructor. It runs automatically when you write
    # ChatLog("chat_log.txt").
    #   PHP: __construct()   Ruby: initialize   JS: constructor()
    #
    # "self" is the new object. Python passes it in as the FIRST parameter
    # of every method, and you have to write it out yourself.
    #   PHP: $this   Ruby: self (implicit)   JS: this (implicit)
    #
    # __init__ never returns anything. Its job is to set up self.
    def __init__(self, path):
        # Attributes are created just by assigning to self.something.
        # Nothing is declared up front (unlike PHP's "private string $path;").
        #   PHP: $this->path = $path;   Ruby: @path = path   JS: this.path = path
        #
        # Watch out: "path = path" without "self." would only make a local
        # variable that disappears when __init__ ends. That's the most common
        # beginner bug with classes.
        self.path = path
        self.messages = []

    # A method is just a function defined inside the class. It always takes
    # self first, so it can reach the object's attributes.
    def add(self, role, content):
        self.messages.append({"role": role, "content": content})

    # S4's save_log(path, log), as a method. It doesn't need any arguments
    # now, because the object already knows its own path and messages.
    def save(self):
        with open(self.path, "w", encoding="utf-8") as f:
            for message in self.messages:
                f.write(f"{message['role']}: {message['content']}\n")

    # S4's load_log(path), as a method. Instead of returning a new list,
    # it fills self.messages.
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

    # -----------------------------------------------------------------------
    # "Dunder" (double underscore) methods
    # -----------------------------------------------------------------------
    # Python calls these for you behind the scenes, like PHP's magic methods.
    # You've already used one: __init__.
    #
    # In S3 you learned that len(x) is a FUNCTION and x.lower() is a METHOD.
    # Under the hood, len(x) just calls x.__len__(). Define __len__ and
    # len() works on your own objects too.
    def __len__(self):
        return len(self.messages)

    # __str__ is what print() and f-strings show for the object.
    #   PHP: __toString()   Ruby: to_s   JS: toString()
    # Without it, print(log) shows something like <__main__.ChatLog object at 0x7f...>
    def __str__(self):
        return f"ChatLog({self.path}, {len(self)} messages)"


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

# Creating an object: call the class like a function. There's no "new".
#   PHP: $log = new ChatLog("chat_log.txt");
#   Ruby: log = ChatLog.new("chat_log.txt")
#   JS: const log = new ChatLog("chat_log.txt");
log = ChatLog(LOG_FILE)

# log.load() is really ChatLog.load(log): Python fills in self for you.
log.load()

if len(log) > 0:
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

# The payoff of the class: the main program only says WHAT to do (add, save,
# load). HOW the messages are stored lives in one place. In S8 you'll switch
# save() and load() to JSON, and nothing in the main program has to change.
#
# Later: inheritance (class Child(Parent):) and @dataclass, which writes
# __init__ and friends for you.
