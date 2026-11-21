# 07_packages.py
# Session 7: installing other people's code with pip, inside a virtual
# environment. The program itself is small: it checks WHICH Python is
# running, imports a package we installed (python-dotenv), and reads
# settings from a .env file, the same way Laravel does.
#
# Why this matters for AI engineering:
#   Every AI library comes from pip: requests (S8), anthropic (S10), numpy,
#   pandas... And every AI project keeps its API key in a .env file that
#   is never committed. This session sets up both for the rest of the course.


# ---------------------------------------------------------------------------
# Step 1: do these in the terminal, from the repo root
# ---------------------------------------------------------------------------
#
#   python3 -m venv .venv               # create the virtual environment
#   source .venv/bin/activate           # switch this terminal to use it
#   pip install -r requirements.txt     # install python-dotenv into it
#   cp .env.example .env                # just like a fresh Laravel app
#   python 07_packages.py               # run this file
#   deactivate                          # switch back when you're done
#
# Then try running it the wrong way, to see the error messages below:
#   deactivate
#   python3 07_packages.py
#   python3 -m pip install python-dotenv   # refused: "externally-managed-environment"
#
# What each piece is, compared with what you know:
#
#   pip               = composer / bundle / npm (the installer)
#   requirements.txt  = composer.json / Gemfile / package.json (the list)
#   .venv/            = vendor/ / node_modules/ (where packages end up)
#
# The big difference: Composer and npm install into the project folder by
# default. pip installs into whichever Python you run it with. Without a
# venv, that's the one Python shared by your whole machine, so two
# projects needing different versions of a package would fight.
# (Bundler has the same problem; it's why rbenv gemsets existed.)
#
# A venv is a folder (.venv/) with its own copy of the python command and
# its own empty package folder. "activate" just puts .venv/bin at the
# front of your PATH, so "python" and "pip" mean the venv's versions.
# You don't commit .venv/ (it's in .gitignore). You commit
# requirements.txt, and anyone can rebuild the venv from it.
#
# Your Python (from Homebrew) even refuses "pip install" outside a venv,
# so you can't break the shared one by accident. That's the
# "externally-managed-environment" error.
#
# Two pip commands worth knowing:
#   pip list      : what's installed in this venv
#   pip freeze    : the same, as exact "name==version" lines.
#                   "pip freeze > requirements.txt" writes the file for you,
#                   a bit like composer.lock / Gemfile.lock.
#
# (Newer projects often use pyproject.toml + a tool called uv instead, which
# feels much more like Composer/Bundler. Same ideas, so pip first.)


# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

# Standard library: ships with Python, works with or without a venv.
import os
import sys

# Third-party: only works if python-dotenv is installed in the Python
# that's running this file. If it isn't, the import raises
# ModuleNotFoundError, which we catch to print a helpful message.
#
# Note the names differ: you INSTALL "python-dotenv" but IMPORT "dotenv".
# The pip name is the package's name on PyPI (pypi.org, like Packagist or
# rubygems.org); the import name is the folder of code inside it.
# Same idea as Composer's "vlucas/phpdotenv" giving you the Dotenv namespace.
try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    print("python-dotenv isn't installed in this Python:")
    print(f"  {sys.executable}")
    print("Activate the venv first:  source .venv/bin/activate")
    print("Then install:             pip install -r requirements.txt")
    # sys.exit() stops the program, like PHP's exit(1). Any number other
    # than 0 tells the terminal "this failed".
    sys.exit(1)


# ---------------------------------------------------------------------------
# Which Python is running?
# ---------------------------------------------------------------------------
# sys.executable  : the full path of the python command running this file
# sys.prefix      : the folder that Python's packages come from
# sys.base_prefix : the folder of the "real" Python the venv was made from
# Inside a venv the last two differ. That's the standard way to check.

print(f"Python:  {sys.executable}")

if sys.prefix != sys.base_prefix:
    print("Running inside a virtual environment. Good.")
else:
    print("Not in a venv (you installed dotenv globally?). Use .venv instead.")


# ---------------------------------------------------------------------------
# Load the .env file
# ---------------------------------------------------------------------------
# load_dotenv() reads KEY=value lines from .env and puts them into the
# environment variables. It looks for .env next to this file first,
# then in parent folders (unlike open(), which uses the cwd, see S4).
# It returns True if it found a file, else False.
#
# Like Laravel, it doesn't overwrite a variable that's already set in the
# real environment, so a server can override what's in .env.

if not load_dotenv():
    print("\nNo .env file found. Create one:  cp .env.example .env")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Read environment variables
# ---------------------------------------------------------------------------
# os.environ is a dict-like object holding all environment variables
# (os is a standard library module for talking to the operating system).
#   PHP:     getenv("BOT_NAME")       Laravel: env("BOT_NAME", "Bot")
#   Ruby:    ENV.fetch("BOT_NAME", "Bot")
#   JS:      process.env.BOT_NAME ?? "Bot"
#   Python:  os.environ.get("BOT_NAME", "Bot")   (the dict .get from S3)
#
# Environment variables are ALWAYS strings, even "3" or "true".
# Convert them yourself: int(os.environ.get("MAX_TURNS", "3")).

bot_name = os.environ.get("BOT_NAME", "Bot")
max_turns = int(os.environ.get("MAX_TURNS", "3"))
api_key = os.environ.get("ANTHROPIC_API_KEY")

print(f"\n{bot_name} is ready (max {max_turns} turns).")

if api_key:
    # Never print a whole API key: terminals get screenshotted and logs
    # get shared. Show just the start.
    # api_key[:7] is a SLICE: the first 7 characters.
    #   PHP: substr($key, 0, 7)   Ruby: key[0, 7]   JS: key.slice(0, 7)
    print(f"API key loaded: {api_key[:7]}... ({len(api_key)} characters)")
else:
    print("ANTHROPIC_API_KEY isn't set in .env (you'll need it in S10).")


# ---------------------------------------------------------------------------
# A tiny chat, configured by .env
# ---------------------------------------------------------------------------
# Change BOT_NAME or MAX_TURNS in .env and run again: no code change needed.
# That's the point of config in .env (same as Laravel's config/ + .env).

turn = 0
while turn < max_turns:
    text = input("You: ")
    if text == "":
        break
    turn += 1
    print(f"{bot_name}: You said '{text}'. ({max_turns - turn} turns left)")

print(f"{bot_name}: Bye!")
