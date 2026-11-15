# python

Learning Python from scratch as a PHP/Laravel, Ruby/Rails and JavaScript developer, as the first step toward AI engineering.

Each session is one small program (about 10 minutes). The explanations live in the code comments and compare Python with PHP, Ruby and JS.

## Sessions

| # | Program | Topics |
|---|---------|--------|
| 1 | [`01_guess_the_number.py`](01_guess_the_number.py) | variables, input/print, `while`, `if`/`elif`, f-strings, `try`/`except` |
| 2 | [`02_shopping_list.py`](02_shopping_list.py) | functions, `return`, lists, `for` loops, `len()`/`sum()` |
| 3 | [`03_chat_log.py`](03_chat_log.py) | dictionaries, `.get()`, `.items()`, a list of dicts (the shape AI chat APIs use) |
| 4 | [`04_save_chat_log.py`](04_save_chat_log.py) | `open()`, `with`, read/write modes, `FileNotFoundError`, `.split()`, unpacking |

## Running

Requires Python 3. Run any session from the repo root:

```bash
python3 01_guess_the_number.py
```

`04_save_chat_log.py` writes `chat_log.txt` to the folder you run it from, because relative paths are relative to the current working directory, not to the script.

## How I practise

After each session I make a copy of the program that keeps only the comments. Then I retype the code from memory and `diff` it against the original to see what I forgot. These copies stay on my machine and aren't committed.

## Roadmap

Classes → modules → `pip` and virtual environments → JSON and web APIs → type hints → a first AI model call.

Progress and notes are tracked in [`handoff.md`](handoff.md).
