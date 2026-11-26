# 09_type_hints.py
# Session 9: type hints. A smaller ChatLog with a type written on every
# parameter, return value and attribute, and a function that builds an
# AI-style request payload. Then we break the types on purpose to see who
# notices (spoiler: not Python).
#
# How to run it (venv active, from the repo root):
#     pip install -r requirements.txt     # installs mypy (new this session)
#     python 09_type_hints.py             # runs fine, even the WRONG lines
#     mypy 09_type_hints.py               # the type checker finds them
#
# Why this matters for AI engineering:
#   AI libraries are typed throughout. The anthropic SDK (S10) describes a
#   chat message with exactly the kind of TypedDict defined below, so your
#   editor can autocomplete "role" and "content" and warn about a typo
#   before you spend money on an API call.


# ---------------------------------------------------------------------------
# The big difference from PHP: hints are NOT checked when the code runs
# ---------------------------------------------------------------------------
# PHP checks declared types at runtime: pass an int where a string is
# declared and you get a TypeError (always with strict_types=1; without it,
# PHP first tries to convert the value).
#
# Python never checks them. They're notes for TOOLS:
#   - your editor (VS Code's Pylance) uses them for autocomplete and squiggles
#   - mypy reads the whole file and reports mismatches, like PHPStan/Larastan
#   - Python itself just stores them and moves on
#
# So Python hints behave like TypeScript types (gone when the code runs)
# or Ruby's Sorbet/RBS, not like PHP's type declarations.
#
# They're optional, so you can add them one function at a time. Every file
# before this one ran fine without any.


# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
# str, int, list, dict, None need no import. A few special types live in
# the standard library module "typing".
import json
from typing import Any, Literal, TypedDict


# ---------------------------------------------------------------------------
# Naming the types we'll reuse
# ---------------------------------------------------------------------------

# Literal: only these exact values are allowed (like a PHP enum, or the
# TypeScript union "user" | "assistant"). Giving it a name makes a type
# alias, so the hints below can just say Role.
Role = Literal["user", "assistant"]


# TypedDict describes the KEYS a dict must have, and the type of each value.
# At runtime a Message is still a plain dict ({"role": ..., "content": ...},
# as in S3), so data["role"] still works, json.dump still writes it, and
# there's no Message(...) object to create.
#   PHPStan:     array{role: string, content: string}
#   TypeScript:  type Message = { role: Role; content: string }
class Message(TypedDict):
    role: Role
    content: str


# ---------------------------------------------------------------------------
# The class, with hints
# ---------------------------------------------------------------------------
# The shape of a hint, side by side:
#   PHP:         function add(string $role, string $content): void
#   TypeScript:  add(role: string, content: string): void
#   Python:      def add(self, role: str, content: str) -> None:
#
# "name: type" for each parameter, "-> type" for the return value.
# "-> None" is PHP's ": void". self never gets a hint (its type is obvious).


class ChatLog:
    # __init__ never returns anything, so it's always "-> None".
    def __init__(self, path: str) -> None:
        self.path = path
        # Python can see that path is a str, but an empty list could hold
        # anything, so we say what goes in it.
        #   list[Message]   = a list of Message dicts
        #   dict[str, int]  = a dict with str keys and int values
        # PHP can only say "array"; PHPStan docblocks say list<Message>.
        self.messages: list[Message] = []

    # role is a Role, so mypy flags log.add("usr", ...) as a typo.
    def add(self, role: Role, content: str) -> None:
        self.messages.append({"role": role, "content": content})

    # "Message | None" means "a Message, or None if nothing matches".
    #   PHP:  ?array  or  array|null       TypeScript:  Message | null
    def find(self, word: str) -> Message | None:
        for message in self.messages:
            if word in message["content"]:
                return message
        return None

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.messages, f, indent=2, ensure_ascii=False)

    def __len__(self) -> int:
        return len(self.messages)


# ---------------------------------------------------------------------------
# A function with a default value and a mixed-type return
# ---------------------------------------------------------------------------
# With a default, the hint goes BEFORE the "=":  max_tokens: int = 100
#   PHP:  int $maxTokens = 100
#
# The payload mixes str, int and a list, so its values are typed Any:
# "anything goes, don't check" (PHP's mixed, TypeScript's any).
# Use Any sparingly: it switches checking off for those values.
def build_payload(messages: list[Message], max_tokens: int = 100) -> dict[str, Any]:
    return {
        "model": "echo-bot",
        "max_tokens": max_tokens,
        "messages": messages,
    }


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # A new file, so the S8 chat_log.json stays as it was.
    log = ChatLog("typed_chat_log.json")
    log.add("user", "What is a type hint?")
    log.add("assistant", "A note about types that Python itself ignores.")

    print("Payload:", build_payload(log.messages, max_tokens=50))

    found = log.find("ignores")
    # found is "Message | None", so check before using it. mypy flags
    # found["role"] without this if, because found could be None. (The
    # same habit as checking for null in PHP, but here a tool enforces it.)
    if found is not None:
        print("Found:", found["role"], "said", found["content"])

    # Hints are stored, not checked. They're just data on the function:
    print("Hints on add():", ChatLog.add.__annotations__)

    # ---- Breaking the types on purpose --------------------------------------
    # Each line marked WRONG runs without an error. Python doesn't look at
    # the hints. Run "mypy 09_type_hints.py" and it reports every one.

    log.add("robot", 42)  # WRONG: "robot" isn't a Role, 42 isn't a str
    count: int = "two"  # WRONG: a hint on a plain variable, ignored too
    print(build_payload(log.messages, max_tokens="lots"))  # WRONG: not an int

    print(f"Still running: {len(log)} messages, count is {count}.")

    log.save()
    print(f"Saved to {log.path}. Now try:  mypy 09_type_hints.py")
