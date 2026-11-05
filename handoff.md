# Python Learning Handoff

**Each session:** read this file → recap → do next task → update this file (tick task, add learnings, set next).

**Me:** PHP/Laravel + Ruby/Rails dev, also knows JavaScript. Explain Python by contrast with PHP/Ruby/JS. ~10 min programs, all explanation in code comments. I run code myself before commit + push.

**Goal:** Python basics are step one toward AI engineering. Choose examples and topics that build toward that (e.g. JSON, calling APIs, working with data).

## Learned
- **S1 `01_guess_the_number.py`:** import, variables, print/input, `int()`, while/break, if/elif/else, f-strings, `+=` (no `++`)
- **S2 warm-up (in `01_`):** `try/except ValueError` (vs try/catch, begin/rescue), `continue` (Ruby `next`)
- **S2 `02_shopping_list.py`:** `def` (must be defined before it's called, no hoisting), explicit `return` (no implicit return like Ruby, else `None`), lists + `.append()`, `for x in list`, `len()`/`sum()`, `float()`, `{x:.2f}`, empty list is falsy (like PHP; truthy in Ruby/JS); built-ins need no import, only modules do
- **vs PHP/Ruby:** indentation = blocks; `True`/`False`/`None` case-sensitive; strict types (`int("abc")` → ValueError, no type juggling); `'` = `"`, interpolation only in f-strings (like JS template literals `` `${x}` ``)
- **vs JS:** `None` replaces both `null` and `undefined`; `==` is already strict (no `===`); `parseInt("abc")` → NaN in JS, but Python raises an error

## Tasks
- [x] S1: guessing game, pushed
- [x] S2: try/except warm-up + `02_shopping_list.py`, pushed. Also: renamed files to `01_`/`02_`, added AI-engineering roadmap (S6–S10)
- [ ] **NEXT** S3: dictionaries (tie-in: AI model messages are a list of dicts, e.g. `[{"role": "user", "content": "Hi"}]`)
- [ ] S4: read/write files
- [ ] S5: classes
- [ ] S6: modules and imports (first folder session: `06_modules/main.py` + `helpers.py`)
- [ ] S7: `pip` + virtual environments (vs Composer / Bundler / npm)
- [ ] S8: JSON + calling a web API over HTTP
- [ ] S9: type hints (vs PHP type declarations)
- [ ] S10: first AI model call: send a prompt, print the reply

## Notes
- If `git push` asks for a username: run `gh auth setup-git` once.
- File naming: one file per session in the repo root, numbered with a leading zero so it sorts right past 9: `01_...py`, `02_...py`, `03_...py`.
- A session with more than one file (e.g. when learning imports) gets its own folder: `06_modules/main.py` + `06_modules/helpers.py`. Run `python3 06_modules/main.py`. Files inside the folder must start with a letter, since Python can't `import` names that start with a digit.
