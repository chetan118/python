# Python Learning Handoff

**Each session:** read this file → recap → do next task → make its practice copy in `practice/` → update this file (tick task, add learnings, set next).

**Me:** PHP/Laravel + Ruby/Rails dev, also knows JavaScript. Explain Python by contrast with PHP/Ruby/JS. ~10 min programs, all explanation in code comments. I run code myself before commit + push.

**Goal:** Python basics are step one toward AI engineering. Choose examples and topics that build toward that (e.g. JSON, calling APIs, working with data).

## Learned
- **S1 `01_guess_the_number.py`:** import, variables, print/input, `int()`, while/break, if/elif/else, f-strings, `+=` (no `++`)
- **S2 warm-up (in `01_`):** `try/except ValueError` (vs try/catch, begin/rescue), `continue` (Ruby `next`)
- **S2 `02_shopping_list.py`:** `def` (must be defined before it's called, no hoisting), explicit `return` (no implicit return like Ruby, else `None`), lists + `.append()`, `for x in list`, `len()`/`sum()`, `float()`, `{x:.2f}`, empty list is falsy (like PHP; truthy in Ruby/JS); built-ins need no import, only modules do
- **S3 `03_chat_log.py`:** dicts (= PHP assoc array / Ruby Hash / JS object), keys must be quoted, `d["k"]` raises KeyError if missing (no null/nil/undefined), `.get(k, default)` (like PHP `??`), `in` checks keys, `.items()` + `for k, v in`, dict as counter, list of dicts = AI chat `messages` shape, `.strip()`/`.lower()`, `", ".join(...)` (method on the separator), no dot access on dicts, ALL_CAPS = constant by convention only. Q&A: f-strings can hold any expression, e.g. `{bot_reply(text)}`, but store a result you use twice (AI calls cost money and aren't repeatable); **function** `len(x)` vs **method** `x.lower()` (like PHP `strtolower($s)` vs `$obj->method()`)
- **Recall practice (before S4):** retyped S1 and S2 from comments-only copies in `practice/` (ignored locally via `.git/info/exclude`, not committed). S1: forgot the `input("Your guess: ")` prompt text. S2: matched. 03 and 04 practice files made, not done yet.
- **S4 `04_save_chat_log.py`:** `open(path, mode)` with `"r"`/`"w"` (empties the file)/`"a"`, `with ... as f:` closes the file for you (like a Ruby `File.open` block, unlike PHP `fopen`/`fclose`), `encoding="utf-8"`, `f.write()` adds no `\n`, `for line in f` + `.rstrip("\n")`, `f.read()` = `file_get_contents`, `FileNotFoundError`, `pass`, `.split(": ", 1)` (max CUTS; PHP/Ruby limit = max PARTS), unpacking `a, b = [x, y]`, relative paths are relative to the cwd. Plain text breaks on newlines, so JSON comes in S8.
- **vs PHP/Ruby:** indentation = blocks; `True`/`False`/`None` case-sensitive; strict types (`int("abc")` → ValueError, no type juggling); `'` = `"`, interpolation only in f-strings (like JS template literals `` `${x}` ``)
- **vs JS:** `None` replaces both `null` and `undefined`; `==` is already strict (no `===`); `parseInt("abc")` → NaN in JS, but Python raises an error

## Tasks
- [x] S1: guessing game, pushed
- [x] S2: try/except warm-up + `02_shopping_list.py`, pushed. Also: renamed files to `01_`/`02_`, added AI-engineering roadmap (S6–S10)
- [x] S3: dictionaries, `03_chat_log.py` (pretend chatbot building an AI-style messages list)
- [x] S4: read/write files, `04_save_chat_log.py` (S3 chatbot that saves the log to `chat_log.txt` and loads it back). Also added `.gitignore` (`chat_log.txt`); `practice/` is in the local `.git/info/exclude` instead
- [ ] **NEXT** S5: classes (tie-in idea: a `ChatLog` class wrapping the S4 save/load functions)
- [ ] Optional: finish `practice/03_chat_log.py` and `practice/04_save_chat_log.py`
- [ ] S6: modules and imports (first folder session: `06_modules/main.py` + `helpers.py`)
- [ ] S7: `pip` + virtual environments (vs Composer / Bundler / npm)
- [ ] S8: JSON + calling a web API over HTTP
- [ ] S9: type hints (vs PHP type declarations)
- [ ] S10: first AI model call: send a prompt, print the reply

## Notes
- If `git push` asks for a username: run `gh auth setup-git` once.
- File naming: one file per session in the repo root, numbered with a leading zero so it sorts right past 9: `01_...py`, `02_...py`, `03_...py`.
- A session with more than one file (e.g. when learning imports) gets its own folder: `06_modules/main.py` + `06_modules/helpers.py`. Run `python3 06_modules/main.py`. Files inside the folder must start with a letter, since Python can't `import` names that start with a digit.
- Each session, also add a row for the new file to the Sessions table in `README.md`.
- **Recall practice:** after each session, make a comments-only copy of the new file in `practice/` (same name), so I can retype the code from memory and `diff` it against the original. Rules: keep every comment word for word with its indentation, turn each code line into a blank line, put a trailing comment on its own line, and add a header line naming the original file. Script: `python3 practice/make_practice.py 05_xxx.py practice/05_xxx.py`. `practice/` (script included) is ignored by `.git/info/exclude`, so it stays on this machine and is never committed. On a fresh clone, add `practice/` there again and rebuild the script from the rules above.
