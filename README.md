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
| 5 | [`05_chat_log_class.py`](05_chat_log_class.py) | classes, `__init__`, `self`, methods, `__len__`/`__str__` |
| 6 | [`06_modules/`](06_modules/) | modules, `import` / `from ... import` / `as`, standard library, `if __name__ == "__main__":` |
| 7 | [`07_packages.py`](07_packages.py) | `pip`, virtual environments, `requirements.txt`, `.env` files, `os.environ` |
| 8 | [`08_json_api/`](08_json_api/) | JSON (`json.dump`/`load`/`dumps`/`loads`), HTTP POST with `requests`, `timeout`, `raise_for_status()`, `RequestException` |
| 9 | [`09_type_hints.py`](09_type_hints.py) | type hints, `list[...]`/`dict[...]`, `X \| None`, `Literal`, `TypedDict`, `Any`, checking with mypy |

## Running

Requires Python 3. Run any session from the repo root:

```bash
python3 01_guess_the_number.py
python3 06_modules/main.py   # folder sessions: run main.py
```

From session 7 on, run sessions inside the virtual environment (packages are listed in `requirements.txt`):

```bash
python3 -m venv .venv               # once
source .venv/bin/activate           # each new terminal
pip install -r requirements.txt     # once, and whenever requirements.txt changes
cp .env.example .env                # once, then edit .env
python 07_packages.py
```

Sessions 4–6 all save to and load from the same `chat_log.txt`, so a chat saved in one session loads in the next. Session 8 switches to `chat_log.json`, and session 9 writes its own `typed_chat_log.json`. Each file goes in the folder you run from, because relative paths are relative to the current working directory, not to the script.

## How I practise

After each session I make a copy of the program that keeps only the comments. Then I retype the code from memory and `diff` it against the original to see what I forgot. These copies stay on my machine and aren't committed.

## Roadmap

A first AI model call.

Progress and notes are tracked in [`handoff.md`](handoff.md).
