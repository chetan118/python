# Python Learning Handoff

**Each session:** read this file → recap → do next task → update this file (tick task, add learnings, set next).

**Me:** PHP/Laravel + Ruby/Rails dev, also knows JavaScript. Explain Python by contrast with PHP/Ruby/JS. ~10 min programs, all explanation in code comments. I run code myself before commit + push.

## Learned
- **S1 `guess_the_number.py`:** import, variables, print/input, `int()`, while/break, if/elif/else, f-strings, `+=` (no `++`)
- **vs PHP/Ruby:** indentation = blocks; `True`/`False`/`None` case-sensitive; strict types (`int("abc")` → ValueError, no type juggling); `'` = `"`, interpolation only in f-strings (like JS template literals `` `${x}` ``)
- **vs JS:** `None` replaces both `null` and `undefined`; `==` is already strict (no `===`); `parseInt("abc")` → NaN in JS, but Python raises an error

## Tasks
- [x] S1: guessing game, pushed
- [ ] S2: warm-up: `try/except ValueError` in guessing game; then `shopping_list.py`: `def`, lists, `for` loop, `sum()`
- [ ] S3: dictionaries
- [ ] S4: read/write files
- [ ] S5: classes

## Notes
- If `git push` asks for a username: run `gh auth setup-git` once.
