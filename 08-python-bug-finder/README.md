# Python Bug Finder

A small linter for code that an AI produced. It checks for four issues:

- mutable default arguments (a common source of hard-to-find bugs)
- bare `except:` clauses
- comparisons to `None` using `==`
- use of `eval()`

It uses Python's built-in `ast` module, which reads the code's structure without running it.

**Skills shown:** Python debugging, static analysis, writing reviewable explanations of bugs.

## Run the tests

```
python3 -m unittest -v
```

## Example

```python
from bug_finder import find_issues

for line, message in find_issues(model_code):
    print(f"line {line}: {message}")
```
