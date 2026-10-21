# Phase 8 — Python from Absolute Basics (for a JavaScript Developer)

*Research date: 2026-10-09. Official docs were fetched on this date. Python and its tools move steadily, so always check the "current" docs linked below before trusting any older tutorial.*

## Why this phase matters

Every later phase of this roadmap (FastAPI, LLM APIs, RAG, agents) is written mostly in Python. You already know how to program, so you do not need to learn "what a loop is". You need to learn how Python is different from JavaScript, so your JS habits do not cause bugs. This phase is deliberately about the language, tooling and testing, not about data science. You will not touch NumPy or pandas here. Be honest with yourself: Python is easy to start and easy to write badly. The goal of Weeks 10 and 11 is to write Python that other Python developers would call normal ("Pythonic").

## Prerequisites and "skip test"

You can skip a topic only if you can DEMONSTRATE it, not just say you know it.

- Skip "Install and run" if you can create a project folder, make an isolated environment, install a package, and run a script from the terminal without looking anything up.
- Skip "Functions" if you can explain, with code, the difference between `*args` and `**kwargs` and why `def f(x=[])` is a bug.
- Skip "Classes" if you can write a class with inheritance and a dataclass, and explain when you would choose composition.
- Skip "pytest" if you can write a parametrized test and a fixture from memory.
- Nobody should skip "References and copying", "Generators" and "async". They are where JS developers get surprised.

## Concepts explained

> **Tip:** Read this phase with a terminal open. Type every example. Python is learned by running it, and the REPL (interactive prompt) gives you an answer in one second.

> **Honest note:** The mental model for the whole phase: Python has **no braces, no semicolons, no `const`, no `undefined`, and no `this`**. Indentation is the syntax. Names are labels stuck on objects. Almost everything else maps to something you already know.

### 1. Install, run scripts, REPL and CLI

**[Must learn now]**

Python is an interpreted language. You write a `.py` file and run it with `python file.py`. The REPL (Read-Eval-Print Loop) is like the browser DevTools console: type a line, get an answer. Install Python from the official python.org downloads page, or let `uv` install it for you (see topic 18). On macOS and Linux the command is often `python3`; on Windows it is `python` or `py`. The [Python Tutorial](https://docs.python.org/3/tutorial/index.html) is the official starting point.

| JavaScript | Python |
| --- | --- |
| `node file.js` | `python file.py` |
| `node` (REPL) | `python` (REPL), `exit()` to leave |
| `process.argv` | `sys.argv` |
| `console.log(x)` | `print(x)` |
| `npx tool` | `uvx tool` (with uv) |

```python
# hello.py
import sys
print("Hello", sys.argv[1:])
```

Run it with `python hello.py Surat`.

**Common mistake:** running `pip install` into the system Python. Always use a virtual environment (topic 18).

**Interview questions:** What is the difference between a script and a module? What does `if __name__ == "__main__":` do?

**Exercise:** write a script that prints the arguments given on the command line, then run it with and without arguments.

### 2. Syntax, indentation, variables and naming

**[Must learn now]**

Python uses indentation (4 spaces by convention) to mark blocks, the way JS uses `{}`. A colon `:` opens a block. Variables are created by assignment; there is no `let/const/var`. Naming follows PEP 8: `snake_case` for variables and functions, `PascalCase` for classes, `UPPER_CASE` for constants (a convention only, Python will not stop you from changing it).

| JavaScript | Python |
| --- | --- |
| `const userName = "a";` | `user_name = "a"` |
| `// comment` | `# comment` |
| `/* block */` | no block comment; use `#` lines or a docstring |
| `if (x) { ... }` | `if x:` then an indented block |
| `a = b = 0` | `a = b = 0` (same) |
| `[a, b] = [b, a]` | `a, b = b, a` |

```python
price = 120
tax_rate = 0.18
total = price * (1 + tax_rate)
a, b = 1, 2
a, b = b, a   # swap without a temp variable
```

Analogy: a Python variable is a sticky label on a box. Moving the label does not copy the box (important in topic 7).

**Common mistake:** mixing tabs and spaces, or changing indentation mid-block. Let your editor insert 4 spaces and run a formatter (`ruff format`).

**Interview questions:** What is PEP 8? Why does Python use indentation? Are Python constants really constant?

**Exercise:** write 10 lines of variable assignments, including a swap and a multiple assignment, and fix one deliberate IndentationError.

### 3. Strings, numbers, booleans, None, conversion and operators

**[Must learn now]**

Python has `str`, `int`, `float`, `bool` and `None`. Integers have no size limit. There is no `undefined`; `None` is the single "nothing" value (closest to JS `null`). `True`/`False` are capitalised. Python does NOT coerce silently: `"5" + 3` raises a `TypeError`, where JS would give `"53"`. You convert explicitly with `int()`, `str()`, `float()`, `bool()`.

| JavaScript | Python |
| --- | --- |
| `null` and `undefined` | `None` only |
| `true && false` | `True and False` |
| `!x` | `not x` |
| `===` | `==` (value) and `is` (identity, use for `None`) |
| `7 / 2` is 3.5 | `7 / 2` is 3.5; `7 // 2` is 3 (floor); `7 % 2` is 1 |
| `2 ** 3` | `2 ** 3` |
| `"5" * 1` is 5 | `int("5")`; `"5" * 3` is `"555"` |
| `typeof x` | `type(x)` |

Truthiness: falsy values are `False`, `None`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `()`. In Python an empty list is falsy, while in JS `[]` is truthy. This is a classic trap.

```python
if not items:        # True for an empty list, unlike JS
    print("empty")
x = None
if x is None:        # use "is" for None
    print("nothing")
```

**Common mistake:** using `== None` instead of `is None`, and expecting `[]` to be truthy.

**Interview questions:** `is` vs `==`? What are the falsy values? What does `//` do with negative numbers?

**Exercise:** convert user input strings to numbers safely, and predict the result of `bool()` on ten different values before running it.

### 4. Conditions and loops

**[Must learn now]**

`if / elif / else` (not `else if`). Loops are `for item in iterable:` and `while condition:`. There is no C-style `for (i=0;...)`. Use `range(n)` for counting and `enumerate()` when you need an index. `break` and `continue` work as in JS. A loop can have an `else` that runs when no `break` happened (rarely needed).

| JavaScript | Python |
| --- | --- |
| `for (const x of arr)` | `for x in items:` |
| `for (let i=0;i<n;i++)` | `for i in range(n):` |
| `arr.forEach((x,i)=>...)` | `for i, x in enumerate(items):` |
| `cond ? a : b` | `a if cond else b` |
| `switch` | `match` / `case` (structural pattern matching) |
| `for (const k in obj)` | `for k in d:` (keys) or `for k, v in d.items():` |

```python
for i, name in enumerate(["a", "b"], start=1):
    print(i, name)
label = "adult" if age >= 18 else "minor"
```

**Common mistake:** modifying a list while looping over it. Loop over a copy or build a new list.

**Interview questions:** `range` vs `enumerate`? What does `for...else` do?

**Exercise:** FizzBuzz three ways: for loop, while loop, and one using `match`.

### 5. Lists, tuples, sets, dicts, slicing and comprehensions

**[Must learn now]**

- `list` = JS array (ordered, mutable). `tuple` = fixed list (immutable, can be a dict key). `set` = unique values, fast membership. `dict` = JS object/Map (keys keep insertion order).
- Slicing: `items[start:stop:step]`, stop is excluded, negative indexes count from the end.
- Comprehensions replace `map`/`filter` chains: `[x*2 for x in nums if x > 0]`.

| JavaScript | Python |
| --- | --- |
| `arr.push(x)` | `items.append(x)` |
| `arr.length` | `len(items)` |
| `arr.slice(1,3)` | `items[1:3]` |
| `arr.at(-1)` | `items[-1]` |
| `arr.map(f)` | `[f(x) for x in items]` |
| `arr.filter(f)` | `[x for x in items if f(x)]` |
| `arr.includes(x)` | `x in items` |
| `{...a, ...b}` | `{**a, **b}` (or the dict merge operator) |
| `obj.key ?? "d"` | `d.get("key", "d")` |
| `Object.entries(o)` | `d.items()` |
| `new Set(arr)` | `set(items)` |
| `arr.sort()` | `items.sort()` (in place) or `sorted(items)` (new list) |
| `arr.reduce(...)` | `functools.reduce` or, better, `sum`, `max`, loops |

```python
nums = [3, -1, 4]
doubled = [n * 2 for n in nums if n > 0]
by_len = {w: len(w) for w in ["a", "bb"]}   # dict comprehension
unique = {1, 2, 2}                           # {1, 2}
first, *rest = [1, 2, 3]                     # unpacking, like destructuring
```

**Common mistake:** `d["missing"]` raises `KeyError` (JS gives `undefined`). Use `d.get()`. Also, `list.sort()` returns `None`.

**Interview questions:** list vs tuple? Why are sets fast? Why can a list not be a dict key?

**Exercise:** given a list of order dicts, produce total per customer using a dict and then using `collections.Counter`/`defaultdict`.

### 6. Functions, defaults, keyword args, `*args` and `**kwargs`

**[Must learn now]**

Functions use `def`. Arguments can be positional or keyword. `*args` collects extra positional arguments into a tuple, `**kwargs` collects extra keyword arguments into a dict. `lambda` exists but is limited to one expression. Functions are first-class values, as in JS.

| JavaScript | Python |
| --- | --- |
| `function f(a, b=1) {}` | `def f(a, b=1):` |
| `(...args) =>` | `def f(*args):` |
| `({a, b}) =>` (options object) | `def f(*, a, b):` (keyword-only after `*`) |
| `x => x*2` | `lambda x: x*2` |
| implicit `undefined` return | implicit `None` return |

```python
def send(to, *, subject="Hi", retries=3, **extra):
    return {"to": to, "subject": subject, "retries": retries, **extra}

send("a@b.com", subject="Yo", priority="high")
```

> **Warning:** Default values are evaluated ONCE when the function is defined. `def add(x, items=[])` shares one list across all calls. Use `items=None` and create the list inside.

**Interview questions:** What is the mutable default argument bug? What does the bare `*` in a signature mean? What is a first-class function?

**Exercise:** write `summarize(*numbers, precision=2, **labels)` and call it five different ways.

### 7. Scope, mutability, references and copying

**[Must learn now]**

Python scope is LEGB: Local, Enclosing, Global, Built-in. Assigning inside a function creates a local variable unless you declare `global` or `nonlocal` (avoid both when possible). Mutable objects: list, dict, set. Immutable: str, int, float, tuple, bool, None. Passing a list to a function passes a reference, so the function can change your list. Same as JS arrays and objects.

| JavaScript | Python |
| --- | --- |
| `const b = a` (reference copy) | `b = a` (same) |
| `[...a]` shallow copy | `a.copy()` or `list(a)` or `a[:]` |
| `structuredClone(a)` | `copy.deepcopy(a)` |
| `Object.freeze` | tuples, `frozenset`, frozen dataclasses |

```python
import copy
a = [[1], [2]]
b = a.copy()          # shallow: inner lists shared
c = copy.deepcopy(a)  # independent
b[0].append(9)        # a also changes!
```

**Common mistake:** `[[0]*3]*3` creates three references to the same row. Use `[[0]*3 for _ in range(3)]`.

**Interview questions:** shallow vs deep copy? Which built-in types are immutable? What is LEGB?

**Exercise:** predict, then run, five snippets that mutate shared lists. Fix each one.

### 8. f-strings and string handling

**[Must learn now]**

f-strings are Python's template literals: `f"Hello {name}"`. They accept any expression and format specs: `f"{price:.2f}"`, `f"{n:,}"`, `f"{name!r}"`, and `f"{x=}"` for quick debugging.

| JavaScript | Python |
| --- | --- |
| `` `Hi ${name}` `` | `f"Hi {name}"` |
| `s.trim()` | `s.strip()` |
| `s.split(",")` | `s.split(",")` |
| `arr.join(",")` | `",".join(items)` (note the order) |
| `s.includes("a")` | `"a" in s` |
| `s.padStart(5,"0")` | `s.zfill(5)` or `f"{n:05d}"` |

**Common mistake:** using `+` to build long strings in loops; use `"".join(parts)`. Never build SQL with f-strings (SQL injection, Phase 14).

**Interview questions:** f-string vs `.format()`? Are strings mutable?

**Exercise:** print a receipt table with aligned columns using only f-string format specs.

### 9. Modules, imports and packages

**[Must learn now]**

Any `.py` file is a module. A folder of modules is a package (an `__init__.py` file is conventional, and required for some tools). Import with `import x`, `from x import y`. Python resolves imports from the standard library, installed packages, and your project root. Avoid circular imports by moving shared code to a third module.

| JavaScript | Python |
| --- | --- |
| `import {a} from "./m.js"` | `from m import a` |
| `import * as m from "./m"` | `import m` |
| `export` | everything at module top level is importable |
| `package.json` | `pyproject.toml` |
| `node_modules` | `.venv` (site-packages) |

**Common mistake:** naming your own file `random.py` or `json.py`, which shadows the standard library. Another: running a file inside a package directly instead of with `python -m package.module`.

**Interview questions:** module vs package? What is a circular import and how do you fix it? What does `__init__.py` do?

**Exercise:** split a script into `app/main.py`, `app/utils.py`, `app/models.py` and run it with `python -m app.main`.

### 10. File handling, context managers, JSON and CSV

**[Must learn now]**

Use `pathlib.Path` for paths and the `with` statement for files, so they close even if an error happens. A context manager is an object that sets something up and cleans up afterwards, like a hotel room: you get a key, and the room is reset when you leave. `json` and `csv` are in the standard library.

```python
from pathlib import Path
import csv, json

path = Path("data") / "orders.csv"
with path.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
Path("out.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
```

| JavaScript | Python |
| --- | --- |
| `fs.readFileSync(p,"utf8")` | `Path(p).read_text(encoding="utf-8")` |
| `JSON.parse(s)` | `json.loads(s)` |
| `JSON.stringify(o)` | `json.dumps(o)` |
| `path.join(a,b)` | `Path(a) / b` |
| `try { } finally { close }` | `with open(...) as f:` |

You can write your own with `contextlib.contextmanager` or a class with `__enter__`/`__exit__`.

**Common mistake:** forgetting `encoding="utf-8"` (breaks on Windows) and `newline=""` for CSV. Also, `json.dumps` cannot serialize `datetime` or `Decimal` without help.

**Interview questions:** Why use `with`? How do you handle a 5 GB CSV (iterate rows, do not `list()` it)?

**Exercise:** read a CSV of orders, skip bad rows, write good rows to JSON. This is the seed of Project 3.

### 11. Exceptions and custom exceptions

**[Must learn now]**

`try / except / else / finally`. Catch specific exceptions, never a bare `except:`. Use `raise` to throw, `raise ... from err` to keep the cause. Create custom exceptions by subclassing `Exception`. Python culture prefers "ask forgiveness" (EAFP): try it and catch the error, rather than checking everything first.

| JavaScript | Python |
| --- | --- |
| `try {} catch (e) {}` | `try: ... except ValueError as e:` |
| `throw new Error("x")` | `raise ValueError("x")` |
| `finally {}` | `finally:` |
| `class MyErr extends Error` | `class MyErr(Exception):` |

```python
class OrderNotFound(Exception):
    def __init__(self, order_id: int):
        super().__init__(f"Order {order_id} not found")
        self.order_id = order_id
```

**Common mistake:** `except Exception: pass` hides bugs. Log or re-raise.

**Interview questions:** `else` vs `finally` in try? What is exception chaining? EAFP vs LBYL?

**Exercise:** write `parse_amount(text)` that raises a custom `InvalidAmount` and a caller that logs and continues.

### 12. Classes, objects, inheritance and composition

**[Must learn now]**

Python classes use `self` explicitly (JS `this` is implicit and changes by call site; Python's `self` is just the first argument and never changes). `__init__` is the constructor. Methods starting with `_` are "private by convention". Prefer composition ("has a") over deep inheritance ("is a"): give an `OrderService` a repository object rather than extending one.

| JavaScript | Python |
| --- | --- |
| `constructor(a) { this.a = a }` | `def __init__(self, a): self.a = a` |
| `class B extends A` | `class B(A):` and `super().__init__()` |
| `static m()` | `@staticmethod` / `@classmethod` |
| getter `get x()` | `@property` |
| `toString()` | `__str__` / `__repr__` |
| `#private` | `_name` (convention) |

```python
class Cart:
    def __init__(self, pricing):      # composition: inject collaborator
        self._items = []
        self._pricing = pricing

    def add(self, sku: str, qty: int = 1) -> None:
        self._items.append((sku, qty))

    @property
    def total(self) -> float:
        return sum(self._pricing.price(s) * q for s, q in self._items)
```

**Common mistake:** putting a mutable object as a class attribute (shared by all instances) instead of in `__init__`.

**Interview questions:** class attribute vs instance attribute? `@classmethod` vs `@staticmethod`? Composition vs inheritance? What is MRO?

**Exercise:** model `Product`, `Order`, `OrderItem` classes with a `total` property. Then replace inheritance with composition in one place.

### 13. Dataclasses and enums

**[Must learn now]**

`@dataclass` generates `__init__`, `__repr__` and `__eq__` for plain data holders. Use `frozen=True` for immutability. `enum.Enum` (or `StrEnum`) gives named constants, a good replacement for string literals like `"pending"`. Pydantic models (Phase 9) are the validated cousin of dataclasses. Docs: [dataclasses](https://docs.python.org/3/library/dataclasses.html), [enum](https://docs.python.org/3/library/enum.html).

```python
from dataclasses import dataclass, field
from enum import StrEnum

class Status(StrEnum):
    PENDING = "pending"
    PAID = "paid"

@dataclass(frozen=True)
class Order:
    id: int
    status: Status = Status.PENDING
    tags: list[str] = field(default_factory=list)
```

| JavaScript / TS | Python |
| --- | --- |
| `type Order = {...}` | `@dataclass class Order` |
| TS `enum` / union of strings | `Enum` / `StrEnum` |
| `Object.freeze` | `frozen=True` |

**Common mistake:** `tags: list = []` in a dataclass raises an error on purpose; use `field(default_factory=list)`. Note that dataclasses do not validate types at runtime.

**Interview questions:** dataclass vs plain class? Dataclass vs Pydantic model? Why `default_factory`?

**Exercise:** convert a dict-based order to a dataclass with a `Status` enum, and serialize it with `dataclasses.asdict`.

### 14. Iterators and generators

**[Must learn now]**

An iterable can be looped over. A generator is a function that uses `yield` to produce values one at a time, pausing between them, like a vending machine that gives one snack per press instead of dumping the whole stock. Generators keep memory use low for big files and streams, and they are the idea behind FastAPI `yield` dependencies and streaming responses.

```python
def read_lines(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\n")

errors = (l for l in read_lines("app.log") if "ERROR" in l)  # generator expression
```

Closest JS: generator functions `function*`, and async iterators.

**Common mistake:** a generator can be consumed only once. Converting to a list defeats the memory savings.

**Interview questions:** iterator vs iterable vs generator? What does `yield` do? Generator expression vs list comprehension?

**Exercise:** write a generator that yields batches of 100 rows from a CSV.

### 15. Decorators (practical)

**[Learn during projects]**

A decorator is a function that takes a function and returns an improved one, like putting a case on a phone. `@name` above a `def` is shorthand for `f = name(f)`. FastAPI routes (`@app.get`), `@property`, `@dataclass`, `@pytest.fixture` are all decorators. Use `functools.wraps` so the wrapped function keeps its name and docs ([functools](https://docs.python.org/3/library/functools.html)).

```python
import functools, time

def timed(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return fn(*args, **kwargs)
        finally:
            print(f"{fn.__name__} took {time.perf_counter() - start:.3f}s")
    return wrapper
```

JS comparison: higher-order functions (JS decorators are a newer, separate feature); in Python decorators are everyday.

**Common mistake:** forgetting `functools.wraps`, which breaks FastAPI signatures and pytest names.

**Interview questions:** How does a decorator work? How do you write one that takes arguments?

**Exercise:** write `@retry(times=3)` that retries a function on exception.

### 16. Type hints, unions, generics and static checking

**[Must learn now]**

Type hints are annotations like `def f(x: int) -> str`. Python does NOT enforce them at runtime. Tools like `mypy` or `pyright` check them statically (like `tsc`), and frameworks like Pydantic and FastAPI READ them at runtime to validate data. That second point is why hints matter so much in Phase 9. Modern syntax: `list[int]`, `dict[str, int]`, `int | None`. Generics use `TypeVar` or newer generic syntax (check which your Python version supports in the [typing docs](https://docs.python.org/3/library/typing.html)). Hints are optional; add them to function signatures first. See also [mypy docs](https://mypy.readthedocs.io/en/stable/).

| TypeScript | Python |
| --- | --- |
| `string or null` (union) | `str or None` written as `str` then a vertical bar then `None` |
| `Array<number>` | `list[int]` |
| `Record<string, number>` | `dict[str, int]` |
| `interface` | `Protocol` or `TypedDict` |
| `Partial<T>` | no direct equivalent (Pydantic models do this job) |
| `tsc --noEmit` | `mypy .` or `pyright` |

**Common mistake:** believing hints protect you at runtime. They do not, unless a library validates them.

**Interview questions:** Are type hints enforced? `Optional[X]` vs `X | None`? What is a `Protocol`?

**Exercise:** annotate all functions in your Topic 10 script and make `mypy` pass.

### 17. Logging

**[Must learn now]**

Use the `logging` module, not `print`, for anything beyond a toy. Loggers have levels (DEBUG, INFO, WARNING, ERROR, CRITICAL), names, and handlers (console, file). Use `logging.getLogger(__name__)` in each module and configure once at the app entry point. Never log secrets or full request bodies with personal data. Docs: [Logging HOWTO](https://docs.python.org/3/howto/logging.html).

```python
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger(__name__)
log.info("loaded %d rows", len(rows))
log.exception("failed to parse row")   # includes stack trace
```

JS comparison: `console.log` vs libraries like pino/winston.

**Common mistake:** calling `logging.basicConfig` inside library code; and using f-strings in log calls (use `%s` args so formatting is skipped when the level is off).

**Interview questions:** Why `getLogger(__name__)`? Difference between `error` and `exception`?

**Exercise:** add file and console logging to Topic 10's script, with an ERROR line for each bad row.

### 18. Virtual environments, pip, pyproject.toml and uv

**[Must learn now]**

A virtual environment is a private `node_modules` for Python: a folder (usually `.venv`) holding one project's packages so projects do not clash. Two supported workflows:

- **Standard library way:** `python -m venv .venv`, activate it, `pip install package`. Documented at [docs.python.org venv](https://docs.python.org/3/library/venv.html) and [packaging.python.org](https://packaging.python.org/en/latest/tutorials/installing-packages/). Works everywhere.
- **uv (what the current FastAPI docs recommend):** `uv init`, `uv add requests`, `uv run python main.py`, `uv sync`. It creates `.venv`, writes dependencies to `pyproject.toml` and exact versions to `uv.lock`, and can install Python itself. See the [uv project guide](https://docs.astral.sh/uv/guides/projects/).

`pyproject.toml` is the single project file (like `package.json`): name, Python version, dependencies, and tool settings. See [writing pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/). `requirements.txt` still exists and is fine for simple apps and Docker, but `pyproject.toml` plus a lockfile is the modern direction.

| npm | uv | pip |
| --- | --- | --- |
| `npm init` | `uv init` | write `pyproject.toml` by hand |
| `npm install x` | `uv add x` | `pip install x` (does not record it) |
| `npm ci` | `uv sync` | `pip install -r requirements.txt` |
| `package-lock.json` | `uv.lock` | `pip freeze > requirements.txt` |
| `npx` / `npm run` | `uvx` / `uv run` | n/a |

> **Honest note:** Pick ONE workflow and stay with it. This handbook uses `uv` in examples because the official FastAPI docs recommend it; every command has a plain `venv` + `pip` equivalent.

**Common mistake:** committing `.venv` to Git (add it to `.gitignore`), or installing globally.

**Interview questions:** Why virtual environments? What is a lockfile? `requirements.txt` vs `pyproject.toml`?

**Exercise:** create a fresh project, add `httpx` and `pytest` (dev dependency), delete `.venv`, and rebuild it from the lockfile.

### 19. async functions, coroutines and asyncio

**[Must learn now]**

`async def` defines a coroutine; `await` pauses it until another coroutine finishes. This feels like JS, with one big difference: **in JS a Promise starts running as soon as it is created. In Python a coroutine does nothing until you `await` it or schedule it.** And there is no event loop running for you: you start one with `asyncio.run(main())`. `asyncio.gather` is `Promise.all`; `asyncio.TaskGroup` (modern) is safer structured concurrency; `asyncio.wait_for` adds a timeout. Docs: [asyncio](https://docs.python.org/3/library/asyncio.html).

| JavaScript | Python |
| --- | --- |
| `async function f()` | `async def f():` |
| `await p` | `await coro` |
| `Promise.all([a,b])` | `await asyncio.gather(a(), b())` |
| `Promise.race` | `asyncio.wait(..., return_when=FIRST_COMPLETED)` |
| `setTimeout` | `await asyncio.sleep(1)` |
| event loop always running | `asyncio.run(main())` |

```python
import asyncio, httpx

async def fetch(client, url):
    r = await client.get(url, timeout=10)
    r.raise_for_status()
    return r.json()

async def main():
    async with httpx.AsyncClient() as client:
        results = await asyncio.gather(*(fetch(client, u) for u in URLS))

asyncio.run(main())
```

> **Warning:** Calling blocking code (`time.sleep`, `requests.get`, heavy CPU work) inside `async def` freezes the whole event loop, exactly like blocking Node's single thread.

**Interview questions:** coroutine vs task? Why does a blocking call hurt async code? `gather` vs `TaskGroup`?

**Exercise:** fetch 5 URLs sequentially, then concurrently with `gather`, and compare timings.

### 20. HTTP requests

**[Must learn now]**

Python's standard library has `urllib`, but real projects use a client library. `requests` is the classic sync one. `httpx` has a near-identical API and supports both sync and async, and it is also what FastAPI's test client uses, so prefer `httpx`. Always set a timeout, always check the status, and handle network errors. Docs: [HTTPX](https://www.python-httpx.org/), [HTTPX async](https://www.python-httpx.org/async/).

| JavaScript | Python (httpx) |
| --- | --- |
| `fetch(url)` | `httpx.get(url, timeout=10)` |
| `res.ok` / manual check | `r.raise_for_status()` |
| `res.json()` | `r.json()` |
| `AbortController` | `timeout=` argument |

```python
import httpx
try:
    r = httpx.get("https://api.example.com/items", params={"page": 1}, timeout=10)
    r.raise_for_status()
except httpx.HTTPStatusError as e:
    log.error("bad status %s", e.response.status_code)
except httpx.RequestError as e:
    log.error("network error %s", e)
```

**Common mistake:** no timeout (requests can hang forever) and treating a 404/500 as success (fetch and httpx do not throw on HTTP error codes by themselves).

**Interview questions:** Why timeouts? Sync vs async client? What is a retry with backoff?

**Exercise:** call a public JSON API, handle 4xx/5xx, timeouts, and retry twice with a short delay.

### 21. Unit testing and pytest

**[Must learn now]**

pytest finds files named `test_*.py` and functions named `test_*`. You use plain `assert`. Fixtures (`@pytest.fixture`) provide reusable setup, like a prepared workbench passed in by name. `@pytest.mark.parametrize` runs one test over many inputs. `monkeypatch` swaps functions or environment variables temporarily; `tmp_path` gives a temporary folder.

| JavaScript (Jest/Vitest) | Python (pytest) |
| --- | --- |
| `expect(a).toBe(b)` | `assert a == b` |
| `expect(fn).toThrow()` | `with pytest.raises(ValueError):` |
| `beforeEach` | fixture |
| `test.each` | `@pytest.mark.parametrize` |
| `jest.mock` | `monkeypatch` / `unittest.mock` |

```python
import pytest

@pytest.mark.parametrize("text,expected", [("10", 10), (" 7 ", 7)])
def test_parse_amount(text, expected):
    assert parse_amount(text) == expected

def test_parse_amount_rejects_junk():
    with pytest.raises(InvalidAmount):
        parse_amount("abc")
```

Official docs: [getting started](https://docs.pytest.org/en/stable/getting-started.html), [fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html), [parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html), [monkeypatch](https://docs.pytest.org/en/stable/how-to/monkeypatch.html).

**Common mistake:** tests that depend on each other's order or on real network/files. Use `tmp_path` and mock the network.

**Interview questions:** What is a fixture and its scope? Unit vs integration test? When do you mock?

**Exercise:** write 8 tests for your Topic 10 parser, including 3 parametrized, 1 using `tmp_path`, and 1 using `monkeypatch`.

### 22. Project structure

**[Must learn now]**

A small Python project that grows well:

```text
my_tool/
  pyproject.toml
  uv.lock
  README.md
  .gitignore
  src/my_tool/
    __init__.py
    cli.py        # argument parsing and entry point only
    reader.py     # input parsing
    validate.py   # rules
    report.py     # summaries
    api_client.py # external HTTP calls
  tests/
    test_validate.py
    conftest.py   # shared fixtures
  data/           # sample inputs (small)
```

Why: `src/` layout stops tests importing uncommitted code by accident; `tests/` is separate from code; each module has one job; I/O (files, HTTP) is kept at the edges so the logic is easy to test. Use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.

**Common mistake:** one 600-line `main.py`.

**Interview questions:** Why separate I/O from logic? What goes in `conftest.py`?

**Exercise:** restructure your Topic 10 script into this layout and run its tests with `uv run pytest`.

### 23. JavaScript vs Python: the differences that bite

**[Must learn now]**

| Topic | JavaScript | Python |
| --- | --- | --- |
| Blocks | `{ }` | indentation |
| Equality | `===` strict | `==` does no type coercion |
| Empty list truthiness | truthy | falsy |
| Missing dict key | `undefined` | `KeyError` |
| Missing value | `null`, `undefined` | `None` |
| Integer division | none | `//` |
| Strings | `"a" + 1` works | `TypeError` |
| `this` | dynamic | explicit `self`, never changes |
| Concurrency | single thread + event loop always on | threads, processes, and opt-in `asyncio` |
| Package manager | npm | pip / uv |
| Hoisting | functions and var hoisted | names exist only after assignment |
| Async start | promise runs immediately | coroutine runs only when awaited |
| Immutability | `const` (binding only) | no constants; tuples and frozen types |

> **Honest note:** The Global Interpreter Lock (GIL) means CPU-bound Python threads do not run in parallel in the standard build. For web backends this rarely matters because the work is I/O waiting, which async and threads handle fine. Do not go down this hole in this phase.

**Exercise:** take 5 snippets of your own JS and rewrite them in Python without translating line by line; use comprehensions, `with`, and f-strings.

## Resource table

| Topic | Subtopics | Official documentation | Recommended video/course | Level | Estimated time | Practice task |
| --- | --- | --- | --- | --- | --- | --- |
| Python basics | syntax, types, control flow, collections, functions | [Python Tutorial](https://docs.python.org/3/tutorial/index.html), [Data structures](https://docs.python.org/3/tutorial/datastructures.html) | [Python for Beginners – Full Course (freeCodeCamp.org, English)](https://www.youtube.com/watch?v=eWRfhZUzrAc); Hindi: [Python for Beginners (Full Course) #100DaysOfCode (CodeWithHarry, Hindi)](https://www.youtube.com/playlist?list=PLu0W_9lII9agwh1XjRt242xIpHhPT2llg) | Beginner | 5-6 h (watch selectively) | Topics 1-8 exercises |
| Errors, files, JSON/CSV | exceptions, pathlib, with, csv, json | [Errors](https://docs.python.org/3/tutorial/errors.html), [Input/output](https://docs.python.org/3/tutorial/inputoutput.html), [csv](https://docs.python.org/3/library/csv.html), [json](https://docs.python.org/3/library/json.html), [pathlib](https://docs.python.org/3/library/pathlib.html) | No video verified for this topic; use the official documentation above. | Beginner | 2 h | CSV to validated JSON |
| OOP, dataclasses, enums | classes, inheritance, composition | [Classes](https://docs.python.org/3/tutorial/classes.html), [dataclasses](https://docs.python.org/3/library/dataclasses.html), [enum](https://docs.python.org/3/library/enum.html) | [Python OOP Tutorial 1: Classes and Instances (Corey Schafer, English)](https://www.youtube.com/watch?v=ZDa-Z5JzLYM) | Beginner-Intermediate | 2-3 h | Order/OrderItem model |
| Iterators, decorators | generators, functools | [Functional HOWTO](https://docs.python.org/3/howto/functional.html), [functools](https://docs.python.org/3/library/functools.html), [contextlib](https://docs.python.org/3/library/contextlib.html) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | `@retry` decorator |
| Typing | hints, generics, mypy | [typing](https://docs.python.org/3/library/typing.html), [mypy docs](https://mypy.readthedocs.io/en/stable/) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Annotate a script and pass mypy |
| Logging | levels, handlers | [Logging HOWTO](https://docs.python.org/3/howto/logging.html), [logging](https://docs.python.org/3/library/logging.html) | No video verified for this topic; use the official documentation above. | Beginner | 1 h | Log bad rows to a file |
| Environments and packaging | venv, pip, pyproject, uv, ruff | [venv](https://docs.python.org/3/library/venv.html), [Installing packages](https://packaging.python.org/en/latest/tutorials/installing-packages/), [pyproject.toml guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/), [uv](https://docs.astral.sh/uv/), [uv projects](https://docs.astral.sh/uv/guides/projects/), [Ruff](https://docs.astral.sh/ruff/) | No video verified for this topic; use the official documentation above. | Beginner | 1.5 h | Rebuild env from lockfile |
| asyncio and HTTP | coroutines, gather, httpx | [asyncio](https://docs.python.org/3/library/asyncio.html), [HTTPX](https://www.python-httpx.org/), [HTTPX async](https://www.python-httpx.org/async/) | No video verified for this topic; use the official documentation above. | Intermediate | 2-3 h | Concurrent fetch with timeouts |
| Testing | pytest fixtures, parametrize, monkeypatch | [pytest docs](https://docs.pytest.org/en/stable/), [fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html) | [Pytest Tutorial – How to Test Python Code (freeCodeCamp.org, English)](https://www.youtube.com/watch?v=cHYq1MRoyI0) | Beginner-Intermediate | 2-3 h | 8 tests for the parser |

## Verification notes

- **Python for Beginners – Full Course [Programming Tutorial]**, freeCodeCamp.org: oEmbed returned this exact title and channel. Language: English (from title and channel; not otherwise checked). Duration NOT verified.
- **Python for Beginners (Full Course) | #100DaysOfCode Programming Tutorial in Hindi**, CodeWithHarry: playlist oEmbed returned this exact title and channel. Language Hindi comes from the title. Duration, number of videos and whether it is up to date NOT verified. It teaches `pip`, not `uv`.
- **Python OOP Tutorial 1: Classes and Instances**, Corey Schafer: oEmbed returned this title and channel. It is the first of a series; the other parts were not individually checked. Duration NOT verified. OOP basics are stable, but use topic 13 for dataclasses.
- **Pytest Tutorial – How to Test Python Code**, freeCodeCamp.org: oEmbed returned this title and channel. Duration NOT verified. The docs are the source of truth for newer pytest features.
- No video was verified for logging, typing, packaging, uv or asyncio. The docs above are the source.
- Why the YouTube duration is missing: my shell could not connect to youtube.com directly, so I verified titles and channels through a fetch tool that retrieved the oEmbed JSON. I could not read `lengthSeconds`.
- All documentation URLs in this phase returned HTTP 200 when fetched on 2026-10-09.

## Hands-on exercises

1. Port a small JS utility you wrote (for example a debounce, a groupBy, or a CSV parser) to idiomatic Python. Write 6 pytest tests.
2. Build a command-line "expense summarizer": read a CSV, validate, print totals per category with f-strings, write a JSON report, log errors.
3. Write a generator pipeline: read a large log file lazily, filter ERROR lines, count by hour.
4. Write an async script that fetches 20 URLs with a concurrency limit (use `asyncio.Semaphore`) and a per-request timeout.
5. Create a package with the `src/` layout, a `pyproject.toml`, a `ruff` and `mypy` setup, and a passing `pytest` run. Commit it with a `.gitignore`.

## Checkpoint

Explain (out loud, in your own words):
- Why `def f(x=[])` is a bug and how to fix it.
- Shallow vs deep copy, with an example.
- Why a coroutine does nothing until awaited.
- Why type hints do not stop wrong types at runtime, and who reads them.

Modify code: take a function that uses a for loop to build a list and rewrite it as a comprehension; then as a generator.

Debug: a script raises `KeyError` on a CSV row with a missing column. Find the line, handle it with a custom exception, and log it.

Write tests: for a `validate_order(row)` function, write parametrized tests for valid, missing-field, negative-quantity, and bad-date cases.

**Ready to move on when** you can: build a project from scratch with a virtual environment and lockfile, write a typed, tested, logged script of 150 lines without copying, and explain the table in topic 23 from memory.

## Week plan

### Week 10 — Python Part 1: Syntax to Functions, Collections, Files, Errors  (estimated hours: 9)

**Learning objectives**
- Run Python scripts, use the REPL, and manage an isolated environment with `uv` or `venv`.
- Write functions, loops, comprehensions and use lists, dicts, sets and tuples fluently.
- Read and write files, JSON and CSV safely, and handle errors with specific exceptions.
- Predict the JS-vs-Python behaviour differences (truthiness, `KeyError`, `None`, references).

**Topics and subtopics**
- **[Must learn now]** Install, REPL, running scripts, `pyproject.toml` and environments (topics 1, 18)
- **[Must learn now]** Syntax, variables, types, conversion, operators, truthiness (2, 3)
- **[Must learn now]** Conditions, loops, `match` (4)
- **[Must learn now]** Lists, tuples, sets, dicts, slicing, comprehensions (5)
- **[Must learn now]** Functions, defaults, `*args`/`**kwargs`, scope, copying (6, 7)
- **[Must learn now]** f-strings, modules and imports (8, 9)
- **[Must learn now]** Files, `with`, `pathlib`, JSON, CSV, exceptions (10, 11)
- **[Learn later if needed]** `global`/`nonlocal`, `for...else`, `lambda` beyond one-liners

**Small prerequisite concepts**
- Terminal basics and PATH (Phase 0).
- What a package manager and a lockfile are (you know this from npm).
- Reading a stack trace from the bottom up (Python prints the error last).

**Reading**
- [Python Tutorial, sections 3-8](https://docs.python.org/3/tutorial/index.html)
- [Data structures](https://docs.python.org/3/tutorial/datastructures.html), [Errors](https://docs.python.org/3/tutorial/errors.html), [Input/output](https://docs.python.org/3/tutorial/inputoutput.html)
- [uv projects guide](https://docs.astral.sh/uv/guides/projects/)

**Video**
- [Python for Beginners – Full Course [Programming Tutorial]](https://www.youtube.com/watch?v=eWRfhZUzrAc), freeCodeCamp.org, English, duration not verified. Watch only the parts you need (skip what the skip test lets you skip).
- Hindi option: [Python for Beginners (Full Course) | #100DaysOfCode Programming Tutorial in Hindi](https://www.youtube.com/playlist?list=PLu0W_9lII9agwh1XjRt242xIpHhPT2llg), CodeWithHarry, Hindi, playlist, duration not verified.

**Hands-on exercises**
1. Do the exercise at the end of topics 1 to 11 (about 20 minutes each).
2. Rewrite five JS snippets from your own code in Python.
3. Write `clean_rows(path)` that reads a CSV, strips whitespace, drops empty rows and returns a list of dicts.
4. Write `group_by(items, key)` and compare with `collections.defaultdict`.
5. Break things on purpose: trigger `KeyError`, `TypeError`, `IndentationError`, `ModuleNotFoundError`, and read each message.

**What you must build**
A small `csv_to_json` command-line script in its own `uv` project: reads a CSV, validates each row, writes valid rows to JSON, prints a count of rejected rows. Committed to Git with a `.gitignore` that excludes `.venv`.

**Completion checklist**
- [ ] Python installed, REPL used, script run from terminal
- [ ] Project has `pyproject.toml`, `.venv` ignored in Git
- [ ] All exercises for topics 1-11 done
- [ ] I can explain truthiness differences from JS
- [ ] I can explain the mutable default argument bug
- [ ] `csv_to_json` works on a messy file

**Self-test**
1. What does `[] == False` return, and what does `bool([])` return?
2. How do you safely read a missing key from a dict?
3. Why use `with open(...)`?
4. What is the output of `a = [1]; b = a; b.append(2); print(a)` and why?
5. What is the difference between `sort()` and `sorted()`?

**Common mistakes**
- Using the system Python and `pip install` without an environment.
- Writing JS-style loops with index counters instead of `for x in items` and `enumerate`.
- Catching `Exception` and doing nothing.
- Forgetting `encoding="utf-8"`.

**Ready to continue when**
- You can write the `csv_to_json` script without copying, in under 45 minutes.
- You can run it, read any error it throws, and fix it.

**Slower-track option**
Cut `match`, `lambda` and `for...else`. Spend two sessions on topics 5, 6 and 7 only. Do exercises 1, 3 and the build. Move the 20-minute exercises for topics 8 and 9 to Week 11.

### Week 11 — Python Part 2: OOP, Typing, Async, pytest, plus Project 3  (estimated hours: 10)

**Learning objectives**
- Model data with classes, dataclasses and enums; choose composition over inheritance.
- Use generators, decorators, type hints and logging.
- Write async code with `asyncio` and `httpx`, with timeouts.
- Test with pytest (fixtures, parametrize, monkeypatch) and finish Project 3.

**Topics and subtopics**
- **[Must learn now]** Classes, inheritance, composition, `@property` (12)
- **[Must learn now]** Dataclasses and enums (13)
- **[Must learn now]** Iterators and generators (14)
- **[Learn during projects]** Decorators (15)
- **[Must learn now]** Type hints and `mypy` (16)
- **[Must learn now]** Logging (17)
- **[Must learn now]** asyncio basics, HTTP requests with `httpx` (19, 20)
- **[Must learn now]** pytest and project structure (21, 22)
- **[Learn later if needed]** Metaclasses, descriptors, threads vs processes, free-threading, advanced generics

**Small prerequisite concepts**
- Week 10 content.
- What a unit test is (Phase 1 testing basics).
- What an HTTP status code is (Phase 0 and 3).

**Reading**
- [Classes](https://docs.python.org/3/tutorial/classes.html), [dataclasses](https://docs.python.org/3/library/dataclasses.html), [enum](https://docs.python.org/3/library/enum.html)
- [typing](https://docs.python.org/3/library/typing.html), [Logging HOWTO](https://docs.python.org/3/howto/logging.html)
- [asyncio](https://docs.python.org/3/library/asyncio.html), [HTTPX](https://www.python-httpx.org/)
- [pytest getting started](https://docs.pytest.org/en/stable/getting-started.html), [fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html), [parametrize](https://docs.pytest.org/en/stable/how-to/parametrize.html)

**Video**
- [Python OOP Tutorial 1: Classes and Instances](https://www.youtube.com/watch?v=ZDa-Z5JzLYM), Corey Schafer, English, duration not verified.
- [Pytest Tutorial – How to Test Python Code](https://www.youtube.com/watch?v=cHYq1MRoyI0), freeCodeCamp.org, English, duration not verified.

**Hands-on exercises**
1. Do the exercises for topics 12 to 22.
2. Convert your Week 10 script to use a dataclass plus `StrEnum`.
3. Add logging and type hints and make `mypy` pass.
4. Write 15 pytest tests including parametrize, a fixture, `tmp_path` and a mocked HTTP call (`httpx.MockTransport`).
5. Write an async version of the API-call step with a concurrency limit.

**What you must build**
**Project 3** (spec below): the Python data utility, with tests passing and a README.

**Completion checklist**
- [ ] Classes, dataclass and enum used in the project
- [ ] A generator streams rows
- [ ] Logging goes to console and file
- [ ] `mypy` and `ruff` pass
- [ ] 15+ pytest tests pass, network is mocked
- [ ] README written; repo pushed to GitHub
- [ ] I can explain why a coroutine needs `await`

**Self-test**
1. When would you choose composition over inheritance? Give an example.
2. What does `@dataclass` generate?
3. What happens if you call an `async def` function without `await`?
4. What is a fixture and when would you use `scope="session"`?
5. Do type hints validate at runtime? Who uses them at runtime?

**Common mistakes**
- Using `requests` inside `async def`.
- Tests that call real APIs.
- Mutable default values in dataclasses.
- Skipping type hints on public functions, so Phase 9 feels magical later.

**Ready to continue when**
- Project 3 passes its acceptance criteria.
- You can add a new validation rule plus a test in under 15 minutes without help.

**Slower-track option**
Skip decorators and the async exercise; write sync `httpx` calls in Project 3. Treat asyncio as "read and run the example" now, then practise it in Week 12 when FastAPI forces it. Reduce tests to 10.

> **Honest note:** Do not let Python Phase drag past two weeks. You will practise the rest inside FastAPI. The aim here is a working foundation, not mastery.

# Project 3 — Python Data Utility: Order File Validator and Reporter

## Problem statement and real-world use case

A small shop receives order exports from several sellers as CSV and JSON files. The files are messy: missing columns, bad dates, negative quantities, duplicate order IDs, prices as text. Someone currently cleans them by hand in a spreadsheet. You will build a command-line tool that reads the files, validates every row, writes a clean file and a rejected-rows file, prints a summary, and enriches totals by calling an external HTTP API (for example, a currency-rate API of your choice, or a tiny local mock server you write yourself). This is a typical "glue script" task that Python backend and AI engineers do every week, and it is the seed of the Project 4 import feature.

## Requirements and user stories

- As an operator, I run one command with an input path and get a clean file, a rejects file and a printed summary.
- As an operator, I can see why each row was rejected (row number, field, reason).
- As an operator, I can pass a currency and get totals converted using live rates, with the tool still working (with a warning) if the API is down.
- As a developer, I can run tests without internet.
- As a developer, I can read a log file to debug a bad run.

## MVP vs advanced features

| Level | Features |
| --- | --- |
| MVP | Read CSV and JSON; validate required fields, types, ranges; write `clean.json` and `rejects.csv`; summary with counts and totals per customer and per status; logging to console and file; 15+ tests |
| Advanced | Async enrichment with concurrency limit and timeouts; retry with backoff; stream huge files with generators; `--dry-run`; progress bar; config via `pyproject.toml` or env; packaged as an installable command (`[project.scripts]`) |

## Suggested architecture

Keep I/O at the edges and pure logic in the middle: `cli` calls `readers` (generators of raw rows), then `validate` (pure functions returning a validated `Order` or a `RowError`), then `report` (pure summary), then `writers`. `api_client` is the only module that touches the network and is injected so tests can replace it.

## Folder structure

```text
order_check/
  pyproject.toml
  uv.lock
  README.md
  .gitignore
  src/order_check/
    __init__.py
    cli.py          # argparse entry point, wires everything
    models.py       # Order dataclass, Status StrEnum, RowError
    readers.py      # csv/json readers as generators
    validate.py     # pure validation rules
    report.py       # summaries (totals, counts)
    writers.py      # clean json + rejects csv
    api_client.py   # httpx client, timeouts, retries
    logging_conf.py # one logging setup function
    errors.py       # custom exceptions
  tests/
    conftest.py     # fixtures: sample files, fake transport
    test_validate.py
    test_readers.py
    test_report.py
    test_api_client.py
    test_cli.py
  data/sample_orders.csv   # small, includes bad rows
```

## Data schema (input and output)

There is no database. The "schema" is the file contract.

| Field | Type | Rule |
| --- | --- | --- |
| order_id | string | required, unique within file |
| customer_email | string | required, contains one @ |
| status | enum | one of pending, paid, shipped, cancelled |
| quantity | int | required, 1 to 1000 |
| unit_price | decimal | required, greater than 0, two decimals max |
| ordered_at | ISO date | required, not in the future |
| currency | string | three letters, default INR |

Outputs: `clean.json` (list of validated orders), `rejects.csv` (original row plus `row_number`, `field`, `reason`), and a summary printed and logged.

## Commands and external calls (instead of API endpoints)

| Command or call | Purpose | Notes |
| --- | --- | --- |
| `order-check validate FILE` | Validate and write outputs | exit code 0 if all valid, 1 if some rejected, 2 on fatal error |
| `order-check summary FILE` | Print totals only | no files written |
| `order-check validate FILE --currency USD` | Convert totals | calls rates API |
| GET rates API (your choice) | Fetch exchange rate | timeout 10 s, retry 2 times, never block the run on failure |

## Packages and setup

- Python (current stable 3.x), `uv` or `venv`+`pip`.
- Runtime: `httpx`. Standard library: `argparse`, `csv`, `json`, `logging`, `pathlib`, `dataclasses`, `decimal`, `asyncio`.
- Dev: `pytest`, `ruff`, `mypy`.
- Setup: `uv init`, `uv add httpx`, `uv add --dev pytest ruff mypy`, then `uv run pytest`.

## Implementation milestones

1. **Skeleton.** `uv` project, `src/` layout, a failing `test_smoke`, `ruff`, `mypy` configured in `pyproject.toml`. Commit.
2. **Models.** `Order` dataclass, `Status` enum, `RowError`. Tests for the enum and equality.
3. **Readers.** CSV reader as a generator of dicts with row numbers; JSON reader. Test with `tmp_path`.
4. **Validation.** One small pure function per rule; combine into `validate_row`. Parametrized tests, at least 10 cases. Use `Decimal` for money.
5. **Writers and report.** Clean JSON, rejects CSV, summary totals per customer and status.
6. **CLI.** `argparse` subcommands, exit codes, log setup (console INFO, file DEBUG).
7. **API enrichment.** `api_client` with timeouts and retry; inject it; test with `httpx.MockTransport`; failure path logs a WARNING and continues.
8. **Polish.** README, type hints everywhere, `mypy` clean, sample data.
9. **Advanced (optional).** Async fetching with `Semaphore`; streaming; installable script.

## Test cases

- Valid row passes; each missing field produces one specific `RowError`.
- Quantity 0, 1001, "abc", "1.5" rejected.
- Price "10.999" rejected; price "10.50" parsed exactly as Decimal.
- Duplicate `order_id` flagged on the second occurrence only.
- Future date rejected; bad date format rejected.
- Empty file; header only; file with BOM; non-UTF-8 file gives a clear fatal error.
- CLI exit codes (0, 1, 2) using `subprocess` or calling `main(argv)`.
- API 500, timeout and invalid JSON: tool still finishes and warns.
- Large file test: generator does not load everything (assert on a lazy iterator).

## Security checklist

- Never execute or `eval` file content; parse only.
- Do not follow arbitrary paths from file content; treat paths as untrusted if added later (use `Path.resolve()` and check the parent).
- Limit file size or rows to avoid memory exhaustion.
- Keep API keys in environment variables, never in code or the repo; add `.env` to `.gitignore`.
- Do not log full rows containing personal data (emails); log row numbers and reasons.
- Pin dependencies through the lockfile; run `uv` or `pip` audit tools occasionally.
- Use HTTPS only for the API call; always set timeouts.

## Deployment plan

This is a tool, not a service. Options in order of effort: (1) run with `uv run` from the repo; (2) install as a command with `uv tool install .` or `pipx`; (3) build a wheel with `uv build` and attach it to a GitHub release; (4) optional scheduled run via cron or a GitHub Actions workflow on a sample file. Docker is not needed here.

## README structure

1. What it does (one paragraph and a before/after example).
2. Install and run (copy-paste commands).
3. Input file format and validation rules (table).
4. Output files and exit codes.
5. Configuration (env vars, flags).
6. Architecture sketch (one paragraph on the module layout).
7. Running tests and linters.
8. Limitations and next steps.

## Acceptance criteria

- [ ] Running on `data/sample_orders.csv` yields the expected clean and rejects counts (documented in the README).
- [ ] Every rejected row has a row number, field and reason.
- [ ] Works with both CSV and JSON input.
- [ ] Tool completes when the rates API is down and logs a warning.
- [ ] `uv run pytest` passes with 15 or more tests and no network access.
- [ ] `ruff check`, `ruff format --check` and `mypy` pass.
- [ ] No secrets or `.venv` in the Git history.
- [ ] I can explain every module and why it exists.

## Common mistakes

- Using `float` for money.
- One giant function for read, validate and write, so nothing can be tested.
- Tests that hit the real internet.
- A bare `except` that swallows row errors.
- Loading a whole file into memory when a generator would do.
- Printing instead of logging.

## Interview questions

- Why use `Decimal` for money? What is wrong with `0.1 + 0.2`?
- How would you process a 10 GB file with limited memory?
- How do you test code that calls an HTTP API?
- When would you make the API step async? What is the risk of an unbounded `gather`?
- How would you make the tool idempotent and safe to re-run?
- Explain your exit-code design.

# Phase 9 — FastAPI and Production Backend

*Research date: 2026-10-09. FastAPI, Pydantic, SQLAlchemy, Alembic, pytest and uv documentation pages were fetched on this date. FastAPI changes quickly; the current docs always win over any video.*

## Why this phase matters

FastAPI is the most common modern way to write Python web APIs, and it is the base for almost every AI backend you will build later (LLM calls, RAG, agents). It is a good fit for you because it feels like Express with types: you declare what data you expect, and the framework validates it, documents it and rejects bad input. The risk is that tutorials make it look too easy. A real backend also needs a database, migrations, authentication, tests, logging and a deployment plan, and that is the real work of this phase. FastAPI does not guarantee you a job, but a clean, tested, deployed FastAPI project is strong evidence of backend skill.

## Prerequisites and "skip test"

- Phase 8 finished: type hints, dataclasses, `pytest`, `venv`/`uv`, basic `async`.
- Phase 6 (Express concepts: routing, middleware, JWT, RBAC) and Phase 7 (PostgreSQL, joins, indexes, transactions, migrations).
- Skip test: you can create a `uv` project, run a FastAPI app with `fastapi dev`, add a Pydantic-validated POST endpoint, and write a `TestClient` test for it from memory. You can also explain what a primary key, foreign key and transaction are. If you cannot, do the Phase 7 SQL exercises first.

## Concepts explained

> **Outdated?:** Many popular FastAPI videos are from 2021 to 2023. They commonly use Pydantic v1 syntax (`orm_mode`, `.dict()`, `@validator`, `class Config`), `@app.on_event("startup")`, `passlib` for passwords, `Optional[X]`, and the old non-`Annotated` style of `Depends`. Pydantic v2 renamed these (see topic 5 and the [migration guide](https://pydantic.dev/docs/validation/latest/get-started/migration/)). FastAPI's current docs use `Annotated`, `lifespan`, `pwdlib` with Argon2, and `fastapi dev`. Use older videos for the ideas, and copy syntax only from the current docs.

### 1. Create and run an app, and the CLI

**[Must learn now]**

Current docs recommend creating the project with `uv`, installing `fastapi[standard]` (which includes the `fastapi` command and Uvicorn), and running `uv run fastapi dev` for development (auto-reload) and `fastapi run` for production. See [the FastAPI tutorial intro](https://fastapi.tiangolo.com/tutorial/) and [First steps](https://fastapi.tiangolo.com/tutorial/first-steps/). The plain `venv` + `pip install "fastapi[standard]"` route also works. In `pyproject.toml` you can set `[tool.fastapi] entrypoint = "app.main:app"` so tools find your app.

```bash
uv init orders-api --bare && cd orders-api
uv add "fastapi[standard]"
uv run fastapi dev
```

Analogy: `fastapi dev` is like `next dev`; `fastapi run` is like `next start`.

**Common mistake:** using `fastapi dev` (auto-reload) in production.

**Interview questions:** What does `fastapi dev` vs `fastapi run` do? What is the `app` object?

### 2. ASGI, Uvicorn and what each one does

**[Must learn now]**

ASGI is the standard interface between a Python async web server and a Python web app, like the contract between Node's `http` server and Express. **Uvicorn** is the ASGI server: it accepts network connections and speaks HTTP. **FastAPI** is the application framework (routing, validation, docs) built on **Starlette** (the lower-level web toolkit) and **Pydantic** (data validation). A reverse proxy such as Nginx or a cloud load balancer sits in front. See the [ASGI spec](https://asgi.readthedocs.io/en/latest/) and [Uvicorn deployment](https://uvicorn.dev/deployment/).

| Express world | FastAPI world |
| --- | --- |
| Node `http` server | Uvicorn (ASGI server) |
| Express | FastAPI on Starlette |
| `zod` / `joi` | Pydantic |
| `swagger-jsdoc` | built-in OpenAPI |
| `nodemon` | `fastapi dev` auto-reload |
| `pm2` cluster | `--workers` or several containers |

**Common mistake:** thinking FastAPI itself serves HTTP.

**Interview questions:** WSGI vs ASGI? What does Uvicorn do that FastAPI does not?

### 3. Routes and HTTP methods

**[Must learn now]**

A path operation is a function plus a decorator: `@app.get("/orders")`. Use `get`, `post`, `put`, `patch`, `delete`. Follow REST naming from Phase 6: nouns in URLs, verbs in methods. See [First steps](https://fastapi.tiangolo.com/tutorial/first-steps/).

```python
@app.get("/health")
def health():
    return {"status": "ok"}
```

**Common mistake:** order of routes: `/orders/me` must be declared before `/orders/{order_id}`.

**Interview questions:** PUT vs PATCH? What makes an endpoint idempotent?

### 4. Path parameters, query parameters and request bodies

**[Must learn now]**

Type hints do the parsing. A name in the path becomes a path parameter; a simple type not in the path becomes a query parameter; a Pydantic model becomes the JSON body. Bad input gives an automatic `422` response listing every problem. Docs: [path params](https://fastapi.tiangolo.com/tutorial/path-params/), [query params](https://fastapi.tiangolo.com/tutorial/query-params/), [request body](https://fastapi.tiangolo.com/tutorial/body/).

```python
@app.get("/orders/{order_id}")
def get_order(order_id: int, include_items: bool = False): ...

@app.post("/orders", status_code=201)
def create_order(payload: OrderCreate): ...
```

| Express | FastAPI |
| --- | --- |
| `req.params.id` (string) | `order_id: int` (parsed and validated) |
| `req.query.page` (string) | `page: int = 1` |
| `req.body` + manual validation | `payload: OrderCreate` |

**Common mistake:** returning 400 manually for things FastAPI already rejects with 422.

**Interview questions:** How does FastAPI decide path vs query vs body? Why 422?

### 5. Pydantic models and validation (v2)

**[Must learn now]**

Pydantic models are classes that validate and convert data. Think of a customs officer who checks and labels every parcel before it enters your code. Docs: [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/), [validators](https://docs.pydantic.dev/latest/concepts/validators/).

```python
from pydantic import BaseModel, Field, field_validator

class OrderItemIn(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    quantity: int = Field(ge=1, le=1000)

class OrderCreate(BaseModel):
    items: list[OrderItemIn] = Field(min_length=1)
    note: str | None = None

    @field_validator("note")
    @classmethod
    def strip_note(cls, v):
        return v.strip() if v else v
```

> **Warning (v1 vs v2):** `.dict()` is now `.model_dump()`, `.json()` is `.model_dump_json()`, `parse_obj` is `model_validate`, `@validator` is `@field_validator`, `class Config: orm_mode = True` is `model_config = ConfigDict(from_attributes=True)`, and `BaseSettings` moved to the separate `pydantic-settings` package. `EmailStr` needs the `email-validator` extra. If a video uses the v1 names, translate with the migration guide.

**Common mistake:** using one model for input, database and output. Split them (topic 6).

**Interview questions:** Pydantic vs dataclass? Validation vs serialization? What does `from_attributes` do?

### 6. Response models and status codes

**[Must learn now]**

A response model says what the client may see. It filters out fields such as `password_hash`. The standard pattern: `OrderCreate` (input), `OrderUpdate` (all optional), `OrderRead` (output), and the database table model. Declare `response_model` (or the return type annotation) and `status_code`. Docs: [response model](https://fastapi.tiangolo.com/tutorial/response-model/), [status codes](https://fastapi.tiangolo.com/tutorial/response-status-code/).

```python
@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(payload: OrderCreate, ...): ...
```

Use: 200 OK, 201 Created, 204 No Content (delete), 400 bad request, 401 not authenticated, 403 not allowed, 404 not found, 409 conflict, 422 validation, 429 rate limit.

**Common mistake:** returning the ORM object including the password hash because no response model was set.

**Interview questions:** 401 vs 403? 404 vs 403 for another user's resource (prefer 404 to avoid leaking existence; state this design choice)? Why separate read and create schemas?

### 7. OpenAPI docs

**[Must learn now]**

FastAPI generates an OpenAPI schema from your code and serves interactive docs at `/docs` (Swagger UI) and `/redoc`. Add `tags`, `summary`, `description`, examples and `responses={404: ...}` to make the docs useful. The OpenAPI JSON can generate typed TypeScript clients for your React app. See [metadata and docs URLs](https://fastapi.tiangolo.com/tutorial/metadata/).

**Common mistake:** exposing `/docs` in production without thinking; decide to protect or disable it.

**Interview questions:** What is OpenAPI? How could a frontend use it?

### 8. Routers and modular structure

**[Must learn now]**

`APIRouter` is a mini-app (like `express.Router()`). One router per resource, included in `main.py` with `include_router`. Router-level `prefix`, `tags` and `dependencies` avoid repetition. Docs: [Bigger applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/). See topic 30 for the full folder layout.

**Common mistake:** importing the `router` variable by name from several modules, which overwrites it; import the modules instead (`from .routers import items, users`), as the docs show.

**Interview questions:** How do you version an API? (prefix `/api/v1`.) In what order do router dependencies run?

### 9. Dependencies and dependency injection

**[Must learn now]**

A dependency is a function FastAPI calls for you and whose result it passes into your endpoint. Analogy: a restaurant waiter who brings what you need to the table before you eat. Use it for: database session, current user, settings, pagination parameters, permission checks. Dependencies can depend on other dependencies. Dependencies with `yield` run cleanup after the response (close the session). Use `Annotated` aliases for short signatures. Docs: [Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/), [dependencies with yield](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/).

```python
SessionDep = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.get("/me")
def me(user: CurrentUser): return user
```

| Express | FastAPI |
| --- | --- |
| middleware that sets `req.user` | `Depends(get_current_user)` |
| `app.locals.db` | `Depends(get_session)` |
| per-route middleware list | `dependencies=[Depends(...)]` |

**Common mistake:** creating a database session at import time as a global.

**Interview questions:** Dependency vs middleware? Why is DI good for testing?

### 10. Configuration and settings

**[Must learn now]**

Read configuration from environment variables with `pydantic-settings`. A `Settings` class validates types and fails fast at startup if something is missing. Provide it through a cached dependency (`lru_cache`) so tests can override it. Never commit `.env`. Docs: [Settings and environment variables](https://fastapi.tiangolo.com/advanced/settings/), [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/).

```python
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    database_url: str
    jwt_secret: SecretStr
    access_token_minutes: int = 15
```

**Common mistake:** hard-coding secrets or reading `os.environ` in many places.

**Interview questions:** Why validate config at startup? How do you handle secrets in production (secret manager, not files in the image)?

### 11. PostgreSQL integration

**[Must learn now]**

You need a database driver plus an ORM or query layer. For PostgreSQL with SQLAlchemy the common drivers are `psycopg` (v3, sync and async) and `asyncpg` (async only). Run PostgreSQL locally with Docker (`postgres` image) or a managed free tier. Connection string shape: `postgresql+psycopg://user:pass@host:5432/dbname` (check the [SQLAlchemy docs](https://docs.sqlalchemy.org/en/20/) for the exact driver name). Keep SQLite for quick experiments only; its behaviour differs from PostgreSQL in types, constraints and concurrency, so test against Postgres.

**Common mistake:** developing on SQLite and discovering Postgres differences in production.

**Interview questions:** Why a connection pool? What is a DSN?

### 12. SQLAlchemy vs SQLModel: how to choose

**[Must learn now]**

- **SQLAlchemy 2.0** is the standard Python database toolkit and ORM. In 2.0 style you declare models with `DeclarativeBase`, `Mapped[...]` and `mapped_column(...)`, and you query with `select()`. Docs: [SQLAlchemy 2.0 tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html), [ORM quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html).
- **SQLModel** is a library by the author of FastAPI that sits on top of SQLAlchemy and Pydantic. One class can be both a table and a validation model. The current FastAPI SQL-databases tutorial uses it. Docs: [SQLModel](https://sqlmodel.tiangolo.com/), [FastAPI SQL databases tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/).

| Question | SQLAlchemy 2.0 + separate Pydantic schemas | SQLModel |
| --- | --- | --- |
| Learning curve | steeper, more verbose | gentler for small CRUD |
| Depth of docs and community | largest | smaller; relies on SQLAlchemy docs for advanced needs |
| Complex queries, joins, CTEs, locking | full control and well documented | possible, you drop to SQLAlchemy constructs |
| Separation of API and DB models | forced and clear | optional; easy to leak fields if you reuse one class |
| Transferable to other jobs | very high | partly |
| Migrations with Alembic | standard | works (it is SQLAlchemy metadata) |
| Fit for a long-lived production service | strong | fine for small to medium; check maintenance activity before committing |

> **Honest note (my recommendation, not a rule):** Use **SQLAlchemy 2.0 with separate Pydantic schemas** for Project 4. You will meet SQLAlchemy in most Python backend jobs, the separation of DB and API models is a good habit, and everything you learn about sessions, loading and transactions also applies if you later use SQLModel. SQLModel is a valid choice for small apps and follows the official FastAPI tutorial; because it is built on SQLAlchemy, switching later is possible but not free. Whichever you choose, do not mix both in one project.

**Common mistake:** copying SQLAlchemy 1.x tutorials (`declarative_base()`, `session.query(...)`) which are legacy style; the 2.0 docs use `select()`.

**Interview questions:** ORM vs raw SQL trade-offs? What is the N+1 query problem and how does `selectinload` help?

### 13. Sessions and transactions

**[Must learn now]**

A SQLAlchemy `Session` tracks objects you load or add and talks to the database in a transaction. Pattern: one session per request via a `yield` dependency; `commit()` once per business operation; `rollback()` on error. Do multi-step writes (create order + items + stock decrement) in ONE transaction so they succeed or fail together. For concurrency (two people buying the last item), use constraints, `SELECT ... FOR UPDATE` (`with_for_update()`), or an atomic `UPDATE ... SET stock = stock - :n WHERE stock >= :n`. Docs: [Session basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html), [Transactions](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html).

```python
def get_session():
    with SessionLocal() as session:
        yield session

def place_order(session, user_id, payload):
    ...  # add order, items, adjust stock
    session.commit()  # one commit for the whole business operation
```

**Common mistake:** committing inside every helper function, which breaks atomicity.

**Interview questions:** What is ACID? What does `flush` do vs `commit`? What is a lost update and how do you prevent it?

### 14. Alembic migrations

**[Must learn now]**

Alembic tracks schema changes as versioned Python scripts (like Prisma/Knex migrations). Workflow: change models, run `alembic revision --autogenerate -m "add orders"`, READ the generated script, run `alembic upgrade head`. `alembic downgrade -1` goes back one step. Set `target_metadata = Base.metadata` in `env.py` and read the database URL from your settings, not from `alembic.ini`. Docs: [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html), [autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html), [cookbook](https://alembic.sqlalchemy.org/en/latest/cookbook.html).

Autogenerate detects table and column additions/removals, nullability, basic index/FK changes and type changes. It does NOT detect table or column renames (they appear as drop and add, which loses data if you run them blindly) and anonymous constraints, so give constraints names through a naming convention. Use `alembic check` in CI to fail when models and migrations disagree. Never edit a migration that has run in a shared environment; add a new one.

**Common mistake:** `Base.metadata.create_all()` in production instead of migrations, or running unreviewed autogenerated scripts.

**Interview questions:** How do you rename a column safely? How do you deploy a migration with zero downtime (expand, migrate data, contract)? What if a migration fails halfway?

### 15. Authentication: password hashing and tokens

**[Must learn now]**

Authentication proves who you are. Flow (matches Phase 6): register, hash the password, login, return a signed JWT access token, protect routes with a dependency that decodes it. The current FastAPI docs use **PyJWT** (`import jwt`) for tokens and **pwdlib** with **Argon2** for password hashing (older tutorials use `python-jose` and `passlib` with bcrypt; the docs now mention passlib only for handling legacy hashes). FastAPI's `OAuth2PasswordBearer` and `OAuth2PasswordRequestForm` plug auth into the docs UI ("Authorize" button). Docs: [Security intro](https://fastapi.tiangolo.com/tutorial/security/), [OAuth2 with Password, Bearer with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), [PyJWT](https://pyjwt.readthedocs.io/en/stable/), [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html).

Rules: short-lived access tokens (for example 15 minutes), a refresh token rotated and stored hashed server-side, an `exp` claim, explicit `algorithms=[...]` on decode, secret from env, the same error for "unknown user" and "wrong password", and rate limits on login. If your React app uses cookies, use `HttpOnly`, `Secure`, `SameSite` and think about CSRF; for a pure API with bearer tokens, store tokens carefully on the client (Phase 14 covers trade-offs).

**Common mistake:** putting sensitive data in a JWT (it is only encoded, not encrypted), a long-lived access token, or a default secret.

**Interview questions:** Why hash instead of encrypt passwords? Why Argon2 or bcrypt rather than SHA-256? Access vs refresh token? How do you revoke a JWT?

### 16. Authorization: RBAC and resource-level permissions

**[Must learn now]**

Authorization decides what you may do. Two layers: **role checks** (RBAC: `admin`, `staff`, `customer`) done with a dependency such as `require_role("admin")`, and **resource-level checks** (is this order yours?) done in the service by filtering queries with the user's id or comparing `order.user_id`. Always check on the server; hiding a button in React is not security. Return 404 instead of 403 for someone else's resource when you do not want to confirm it exists (a design choice, state it in your README).

```python
def require_role(*roles: Role):
    def checker(user: CurrentUser):
        if user.role not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Not allowed")
        return user
    return checker
```

**Common mistake:** authorizing only at the route and forgetting list endpoints, which then leak other users' data (broken object-level authorization, the top item of the [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x00-header/)).

**Interview questions:** RBAC vs ABAC? What is IDOR/BOLA and how do you prevent it?

### 17. Async vs sync

**[Must learn now]**

FastAPI supports both. `async def` endpoints run on the event loop and must never block. Plain `def` endpoints run in a worker threadpool, so blocking calls are safe there. Rule from the docs ([Concurrency and async/await](https://fastapi.tiangolo.com/async/)): if your libraries support `await`, use `async def`; if they do not (or you are unsure), use `def`. With SQLAlchemy you can use the sync engine with `def` endpoints, or the async engine (`create_async_engine`, `AsyncSession`, driver `asyncpg` or async `psycopg`) with `async def`. The async setup has extra rules: one `AsyncSession` per task, `expire_on_commit=False`, no implicit lazy loading, and `await engine.dispose()` ([SQLAlchemy asyncio docs](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)).

> **Honest note:** Start Project 4 with **sync SQLAlchemy and `def` endpoints**. It is simpler and fast enough for most business apps. Use `async def` when you call many external services (LLM APIs in Phase 11, HTTP calls, WebSockets, streaming). Mixing is allowed. Do not use `async def` and then call blocking code inside it.

**Common mistake:** `async def` with `requests.get` or `time.sleep`, which freezes every request.

**Interview questions:** What happens to a blocking call in `async def`? When does async not make things faster (CPU-bound work)?

### 18. Error handling and custom exceptions

**[Must learn now]**

Raise `HTTPException` for simple cases. For a clean design, raise domain exceptions in services (`OrderNotFound`, `InsufficientStock`) and register `@app.exception_handler(...)` functions that map them to HTTP responses with one consistent JSON shape, for example `{"error": {"code": "ORDER_NOT_FOUND", "message": "...", "request_id": "..."}}`. Also add a catch-all handler that logs the stack trace and returns a generic 500 with no internals. Docs: [Handling errors](https://fastapi.tiangolo.com/tutorial/handling-errors/).

**Common mistake:** returning stack traces or SQL errors to clients; raising `HTTPException` deep inside the database layer.

**Interview questions:** Why keep HTTP out of the service layer? How do you make errors consistent?

### 19. Pagination, filtering and sorting

**[Must learn now]**

Never return unbounded lists. Offset pagination (`limit`, `offset` or `page`, `page_size`) is simple; keyset (cursor) pagination (`created_at < :cursor`) is faster and stable for large or changing tables. Cap `limit` (for example max 100) with `Query(le=100)`. Whitelist sortable columns; never pass a raw column name from the client into SQL. Put these query parameters in one dependency and reuse it. Return `items`, `total`, `limit`, `offset`. Add an index to match your filters and sorts (Phase 7).

```python
def pagination(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    return {"limit": limit, "offset": offset}

PageDep = Annotated[dict, Depends(pagination)]
```

**Common mistake:** `ORDER BY` on user input directly, and counting with `len(all_rows)`.

**Interview questions:** Offset vs keyset pagination? How do you paginate while rows are being inserted?

### 20. File uploads

**[Learn during projects]**

Use `UploadFile` (needs the `python-multipart` package, which comes with `fastapi[standard]`). Validate size, content type AND file signature if it matters, generate your own file name (never trust the client's), and store in object storage (S3) rather than the app disk in production. Stream large files in chunks. Docs: [Request files](https://fastapi.tiangolo.com/tutorial/request-files/).

**Common mistake:** trusting `filename` (path traversal such as `../../etc/passwd`) and reading a huge file fully into memory.

**Interview questions:** How do you limit upload size? Why store files outside the database/app server?

### 21. Background tasks and queues

**[Learn during projects]**

`BackgroundTasks` runs small work after the response is sent (send an email, write an audit row) in the same process. It is not durable: if the server restarts, the task is lost, and it has no retries. For reliable or long jobs use a real queue and a worker (Celery, RQ, ARQ, Dramatiq, or a cloud queue like SQS) with retries, visibility and idempotency. Rule of thumb: if losing the job is acceptable and it takes under a few seconds, `BackgroundTasks`; otherwise a queue. Docs: [Background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/).

**Common mistake:** putting a 5-minute report job in `BackgroundTasks`.

**Interview questions:** Why make jobs idempotent? What is at-least-once delivery?

### 22. WebSockets and streaming responses

**[Learn during projects]**

WebSockets give a two-way persistent connection (live order status, chat). Use `@app.websocket("/ws")`, `await websocket.accept()`, handle `WebSocketDisconnect`, authenticate on connect (token in query string or first message), and use a connection manager for broadcast. For one-way server-to-client streams (LLM tokens in Phase 11), use `StreamingResponse` with a generator, or Server-Sent Events: FastAPI added built-in SSE support in version 0.135.0 (`EventSourceResponse` from `fastapi.sse`, with automatic keep-alive pings). Check your installed version before using it; older tutorials hand-write `text/event-stream`. Docs: [WebSockets](https://fastapi.tiangolo.com/advanced/websockets/), [Custom response / streaming](https://fastapi.tiangolo.com/advanced/custom-response/), [Server-Sent Events](https://fastapi.tiangolo.com/tutorial/server-sent-events/).

| Need | Use |
| --- | --- |
| Two-way real time | WebSocket |
| One-way live updates or LLM tokens | SSE or StreamingResponse |
| Big file download | StreamingResponse / FileResponse |
| Simple polling is enough | plain GET every N seconds |

**Common mistake:** keeping per-connection state only in memory when you run more than one worker (messages will not reach clients on other workers; use Redis pub/sub).

**Interview questions:** WebSocket vs SSE? How do you scale WebSockets across instances?

### 23. Logging and request tracing

**[Must learn now]**

Use Python `logging` (or `structlog`) configured once at startup, emit JSON logs in production, and add a **request ID**: a middleware reads `X-Request-ID` or generates a UUID, stores it in a `contextvars.ContextVar`, adds it to every log line and to the response header. Log method, path, status and duration; never log passwords, tokens or full personal data. Docs: [Middleware](https://fastapi.tiangolo.com/tutorial/middleware/), [Python logging HOWTO](https://docs.python.org/3/howto/logging.html).

**Common mistake:** `print()` debugging, and logging request bodies that contain secrets.

**Interview questions:** What is a correlation ID and why is it useful? Logs vs metrics vs traces?

### 24. pytest and API integration tests

**[Must learn now]**

`TestClient` (from `fastapi.testclient`, needs `httpx`) calls your app in-process without a network. Test the whole path: HTTP request, validation, auth, database, response. Use fixtures for the client, a clean database, and an authenticated user per role. Test status codes AND bodies AND database state. Test unhappy paths: 401, 403, 404, 409, 422. Docs: [Testing](https://fastapi.tiangolo.com/tutorial/testing/), [pytest fixtures](https://docs.pytest.org/en/stable/how-to/fixtures.html). For async endpoints/tests use `httpx.AsyncClient` with an ASGI transport and an async test plugin (see the FastAPI testing docs for the current recipe).

```python
def test_create_order_requires_auth(client):
    r = client.post("/api/v1/orders", json={"items": [{"sku": "A1", "quantity": 1}]})
    assert r.status_code == 401
```

**Common mistake:** only testing the happy path; tests that share state and depend on order.

**Interview questions:** Unit vs integration test in a FastAPI app? What belongs in `conftest.py`?

### 25. Dependency overrides and test databases

**[Must learn now]**

`app.dependency_overrides[get_session] = override` replaces a dependency during tests. Reset it afterwards (`app.dependency_overrides.clear()` or a fixture with `yield`). Docs: [Testing dependencies with overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/). Test-database options:

| Approach | Pros | Cons |
| --- | --- | --- |
| Separate Postgres database, schema built with Alembic or `create_all`, truncate between tests | realistic | slower |
| Wrap each test in a transaction and roll back | fast, isolated | care needed if code calls `commit()` (use a savepoint pattern) |
| Throwaway Postgres in Docker per test run (for example testcontainers) | clean, CI-friendly | needs Docker |
| SQLite in memory | very fast | different SQL behaviour from Postgres; avoid for real confidence |

Recommended for Project 4: one dedicated test Postgres database (Docker Compose service), schema built by running Alembic migrations once per session, and each test isolated by rollback or truncate. Also override `get_settings` and any external service (email, payment, LLM) with fakes.

```python
@pytest.fixture
def client(db_session):
    app.dependency_overrides[get_session] = lambda: db_session
    yield TestClient(app)
    app.dependency_overrides.clear()
```

**Common mistake:** running tests against your development database; forgetting to clear overrides, so tests leak into each other.

**Interview questions:** How do you isolate DB tests? Why test migrations?

### 26. CORS and security

**[Must learn now]**

CORS is a browser rule, not an API firewall. Use `CORSMiddleware` with an explicit list of allowed origins from settings; avoid `allow_origins=["*"]` combined with credentials. Also: HTTPS only, secure headers at the proxy, rate limiting (a library such as `slowapi`, or at the gateway), input validation via Pydantic, parameterized queries (the ORM does this; never build SQL with f-strings), request size limits, `TrustedHostMiddleware`, and disabling debug in production. Docs: [CORS](https://fastapi.tiangolo.com/tutorial/cors/), [OWASP Top 10](https://owasp.org/www-project-top-ten/). Phase 14 expands this into a full checklist.

**Common mistake:** "fixing" CORS errors by allowing everything.

**Interview questions:** What does CORS protect and what does it not? What is a preflight request?

### 27. Timeouts, retries and connection pooling

**[Learn during projects]**

Everything that leaves your process needs a timeout: HTTP calls (`httpx` timeout), database statements (`statement_timeout`), and pool waits. Retry only safe/idempotent operations, with exponential backoff and jitter, and a retry limit. The SQLAlchemy engine keeps a connection pool; tune `pool_size`, `max_overflow`, `pool_timeout` and use `pool_pre_ping=True` to survive dropped connections. Total connections = (pool_size + max_overflow) x number of worker processes; keep it under PostgreSQL's `max_connections`, or use a pooler like PgBouncer. Docs: [Connection pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html).

**Common mistake:** unlimited retries during an outage (a retry storm), and one engine per request.

**Interview questions:** What is backoff with jitter? Why can too many workers exhaust the database?

### 28. Health checks and graceful shutdown

**[Must learn now]**

Expose `/health/live` (process is up, no dependencies) and `/health/ready` (can reach the database). Load balancers and Docker use them. Use FastAPI's **lifespan** handler (an async context manager passed to `FastAPI(lifespan=...)`) to create resources at startup and dispose of them at shutdown (for example `engine.dispose()`); this replaces the old `@app.on_event` hooks. Orchestrators send SIGTERM; a well-behaved ASGI server stops accepting new connections and lets in-flight requests finish. Check the Uvicorn docs for a graceful-shutdown timeout option for your version (I did not find it on the deployment page), and set your container's stop timeout to match. Docs: [Lifespan events](https://fastapi.tiangolo.com/advanced/events/).

**Common mistake:** a readiness check that always returns 200, or doing slow work in startup so the container is killed before it is ready.

**Interview questions:** Liveness vs readiness? What happens to in-flight requests on deploy?

### 29. Production config and deployment

**[Must learn now]**

Production checklist: `fastapi run` (no reload), a container image, multiple workers or replicas (each process has its own memory), a reverse proxy or load balancer terminating HTTPS, `--proxy-headers` behind a proxy, environment-based settings, migrations run as a separate release step (not on every app start with several replicas), structured logs to stdout, health checks, and secrets from a secret manager. Docs: [FastAPI deployment](https://fastapi.tiangolo.com/deployment/), [FastAPI with Docker](https://fastapi.tiangolo.com/deployment/docker/), [Uvicorn deployment](https://uvicorn.dev/deployment/), [uv in Docker](https://docs.astral.sh/uv/guides/integration/docker/). Full Docker/AWS steps are in Phase 15.

**Common mistake:** running migrations from every replica at start, causing races; baking `.env` into the image.

**Interview questions:** How many workers? (Depends on CPU and memory; measure.) How do you roll back a bad deploy?

### 30. Maintainable project structure: why each folder exists

**[Must learn now]**

```text
orders-api/
  pyproject.toml            # dependencies, tool config, fastapi entrypoint
  uv.lock
  alembic.ini
  Dockerfile
  docker-compose.yml        # api + postgres (+ test db)
  .env.example              # documented variables, no real secrets
  migrations/               # Alembic versions: history of schema changes
  app/
    main.py                 # create app, lifespan, middleware, include routers
    api/
      deps.py               # shared dependencies: session, current user, role checks, pagination
      v1/routers/           # thin HTTP layer: parse, call service, return schema
        auth.py orders.py products.py users.py health.py
    core/
      config.py             # Settings (pydantic-settings)
      security.py           # hashing, JWT create/verify
      logging.py            # logging setup, request-id middleware
      errors.py             # domain exceptions + handlers
    db/
      base.py               # DeclarativeBase and naming convention
      session.py            # engine, SessionLocal, get_session
    models/                 # SQLAlchemy tables (what the DB looks like)
    schemas/                # Pydantic models (what the API accepts and returns)
    services/               # business rules and transactions (no HTTP here)
    repositories/           # optional: query code if services get big
  tests/
    conftest.py             # app, db, client, auth fixtures
    api/ services/          # tests mirror the app
```

| Folder | Why it exists |
| --- | --- |
| `routers` | Keep HTTP details (status codes, params) away from business logic |
| `schemas` | The public contract; separate from DB so you never leak columns |
| `models` | One place that mirrors the database; Alembic reads it |
| `services` | Rules like "cannot cancel a shipped order"; testable without HTTP |
| `repositories` | Optional layer; add it only when queries get repetitive |
| `core` | Cross-cutting concerns: config, security, logging, errors |
| `db` | Engine and session lifecycle in one place |
| `migrations` | Reviewable, reversible schema history |
| `tests` | Mirrors app layout so tests are easy to find |

> **Honest note:** Do not add repository and service layers on day one for a 3-endpoint app. Start with routers + services + models + schemas. Add layers when you feel real pain, and explain why in your README. Group by layer (as above) for small apps; group by feature (`orders/`, `users/` each with router, schemas, service) when the app grows.

**Interview questions:** Why separate schemas from models? Layered vs feature-based structure? Where does a transaction boundary belong?

## Resource table

| Topic | Subtopics | Official documentation | Recommended video/course | Level | Estimated time | Practice task |
| --- | --- | --- | --- | --- | --- | --- |
| Getting started | install, `fastapi dev`, routes, params, body | [Tutorial](https://fastapi.tiangolo.com/tutorial/), [First steps](https://fastapi.tiangolo.com/tutorial/first-steps/), [Path params](https://fastapi.tiangolo.com/tutorial/path-params/), [Query params](https://fastapi.tiangolo.com/tutorial/query-params/), [Body](https://fastapi.tiangolo.com/tutorial/body/) | [FastAPI Course for Beginners (freeCodeCamp.org, English)](https://www.youtube.com/watch?v=tLKKmouUams) | Beginner | 3-4 h | CRUD for products in memory |
| Pydantic and responses | models, validators, response_model, status codes | [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/), [Validators](https://docs.pydantic.dev/latest/concepts/validators/), [Migration guide](https://pydantic.dev/docs/validation/latest/get-started/migration/), [Response model](https://fastapi.tiangolo.com/tutorial/response-model/) | No video verified for this topic; use the official documentation above. | Beginner | 2 h | Split Create/Read/Update schemas |
| Structure and DI | routers, dependencies, settings, yield | [Bigger applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/), [Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/), [Settings](https://fastapi.tiangolo.com/advanced/settings/) | No video verified for this topic; use the official documentation above. | Intermediate | 3 h | Refactor to routers + settings |
| Database | PostgreSQL, SQLAlchemy 2.0, SQLModel, sessions | [SQLAlchemy 2.0 tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html), [ORM quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html), [Session basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html), [SQLModel](https://sqlmodel.tiangolo.com/), [FastAPI SQL databases](https://fastapi.tiangolo.com/tutorial/sql-databases/) | [Python API Development - Comprehensive Course for Beginners (freeCodeCamp.org, English)](https://www.youtube.com/watch?v=0sOvCWFmrtA) (DB, auth and testing sections only; see warning) | Intermediate | 4-5 h | Orders tables + CRUD with Postgres |
| Migrations | Alembic revisions, autogenerate | [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html), [Autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html), [Cookbook](https://alembic.sqlalchemy.org/en/latest/cookbook.html) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Add a column and rename one safely |
| Auth and RBAC | OAuth2 password flow, JWT, Argon2, roles | [Security](https://fastapi.tiangolo.com/tutorial/security/), [OAuth2 + JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), [PyJWT](https://pyjwt.readthedocs.io/en/stable/), [OWASP password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) | No video verified for this topic; use the official documentation above. | Intermediate | 4 h | Register/login + admin-only route |
| Errors, async | exception handlers, async vs def | [Handling errors](https://fastapi.tiangolo.com/tutorial/handling-errors/), [Async](https://fastapi.tiangolo.com/async/) | No video verified for this topic; use the official documentation above. | Intermediate | 2 h | Uniform error JSON |
| Files, background, real time | uploads, BackgroundTasks, WebSocket, SSE | [Request files](https://fastapi.tiangolo.com/tutorial/request-files/), [Background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/), [WebSockets](https://fastapi.tiangolo.com/advanced/websockets/), [SSE](https://fastapi.tiangolo.com/tutorial/server-sent-events/) | No video verified for this topic; use the official documentation above. | Intermediate | 3 h | Upload invoice + status stream |
| Testing | TestClient, overrides, test DB | [Testing](https://fastapi.tiangolo.com/tutorial/testing/), [Testing dependencies](https://fastapi.tiangolo.com/advanced/testing-dependencies/), [pytest docs](https://docs.pytest.org/en/stable/) | [Pytest Tutorial – How to Test Python Code (freeCodeCamp.org, English)](https://www.youtube.com/watch?v=cHYq1MRoyI0) (general pytest only) | Intermediate | 3 h | 30 API tests |
| Production | CORS, logging, pooling, health, lifespan, deploy | [CORS](https://fastapi.tiangolo.com/tutorial/cors/), [Middleware](https://fastapi.tiangolo.com/tutorial/middleware/), [Lifespan](https://fastapi.tiangolo.com/advanced/events/), [Deployment](https://fastapi.tiangolo.com/deployment/), [Docker](https://fastapi.tiangolo.com/deployment/docker/), [Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html), [Uvicorn](https://uvicorn.dev/deployment/) | No video verified for this topic; use the official documentation above. | Intermediate-Advanced | 4 h | Dockerize and add health checks |
| Hindi FastAPI | n/a | n/a | No Hindi FastAPI video verified for this topic; use the official documentation above. | n/a | n/a | n/a |

## Verification notes

- **FastAPI Course for Beginners**, freeCodeCamp.org: oEmbed returned this exact title and channel. Language English (from title/channel). Duration NOT verified. The ID came from a freeCodeCamp announcement page that describes it as a short crash course; its FastAPI and Pydantic versions were NOT checked, so treat syntax as possibly dated.
- **Python API Development - Comprehensive Course for Beginners**, freeCodeCamp.org: oEmbed returned this exact title and channel. The freeCodeCamp announcement URL describes a 19-hour course (the video's own duration was NOT verified) building a social-media-style API with SQL, SQLAlchemy and auth. **Warning: this course is from the Pydantic v1 era.** Expect `orm_mode`, `.dict()`, `passlib`, `python-jose`, `@app.on_event`, and SQLAlchemy 1.x style. Its ideas (auth flow, DB integration, testing with fixtures, deployment) are still useful; do not copy the code. I did not watch the full video, so I cannot vouch for every section.
- **Pytest Tutorial – How to Test Python Code**, freeCodeCamp.org: oEmbed verified title and channel; duration NOT verified; it covers general pytest, not FastAPI.
- A Hindi FastAPI video was searched for; none could be verified, so none is listed.
- Docs facts checked by fetching the pages on 2026-10-09: FastAPI install via `uv add "fastapi[standard]"` and `uv run fastapi dev`/`fastapi run`; the SQL databases tutorial uses SQLModel; `pwdlib` with Argon2 and `PyJWT` in the OAuth2 JWT tutorial; `pydantic-settings` and `lru_cache` in settings; `dependency_overrides` and clearing overrides; SSE added in FastAPI 0.135.0; Alembic autogenerate limitations; SQLAlchemy asyncio rules; Pydantic v2 rename list; Uvicorn deployment page (workers, proxy headers, gunicorn note).
- NOT verified in docs: Uvicorn's graceful-shutdown timeout flag name, specific current version numbers of FastAPI, Pydantic, SQLAlchemy and Python (check PyPI before pinning), and whether older FastAPI releases still accept Pydantic v1 (check the FastAPI release notes).

## Hands-on exercises

1. Build an in-memory Items CRUD API; read the generated `/docs`; make every endpoint return a proper `response_model`.
2. Break validation on purpose and read the 422 body. Add a custom `field_validator`.
3. Add a Postgres container via Docker Compose, define two related tables with SQLAlchemy 2.0, and write an Alembic migration. Rename a column by hand-editing an autogenerated migration.
4. Implement register, login, `GET /me`, and an admin-only endpoint. Write tests for 401 and 403.
5. Write a request-ID middleware and confirm every log line for one request shares the ID.
6. Add pagination (limit/offset with caps) and a whitelisted sort to a list endpoint.
7. Write a test that overrides the session dependency with a rolled-back transaction, and one that overrides `get_settings`.
8. Add a `/health/ready` endpoint that queries the DB, then stop Postgres and watch it fail.

## Checkpoint

Explain:
- The roles of Uvicorn, Starlette, FastAPI and Pydantic.
- Why `def` and `async def` endpoints behave differently and what happens if you block in `async def`.
- SQLAlchemy vs SQLModel and which you chose and why.
- What `Depends` does and how overrides help tests.

Modify code: change an endpoint to return only `id` and `status` using a response model; add a new nullable column with a migration; add a `manager` role.

Debug: a user can fetch another user's order by changing the ID in the URL (fix with resource-level authorization); the app hangs under load (find the blocking call in `async def`); a test passes alone and fails in the suite (shared state or leftover overrides).

Write tests: login success and failure; admin vs customer access; creating an order rolls back all items when one item fails; pagination cap enforced.

**Ready to move on when** you can build a new authenticated CRUD resource with migration and tests from a blank folder in about 3 hours without copy-pasting, and explain every folder in your structure.

## Week plan

### Week 12 — FastAPI Part 1: Routes, Pydantic, Dependencies, Structure  (estimated hours: 9)

**Learning objectives**
- Create and run a FastAPI app with `uv` and `fastapi dev`.
- Validate input and shape output with Pydantic v2 models and response models.
- Split an app into routers, a dependencies module, and settings.
- Use dependency injection confidently.

**Topics and subtopics**
- **[Must learn now]** Create/run, ASGI and Uvicorn roles (topics 1, 2)
- **[Must learn now]** Routes, path/query/body parameters (3, 4)
- **[Must learn now]** Pydantic models, response models, status codes (5, 6)
- **[Must learn now]** OpenAPI docs (7)
- **[Must learn now]** Routers, dependencies, settings (8, 9, 10)
- **[Must learn now]** Error handling and custom exceptions (18)
- **[Must learn now]** Async vs sync (17)
- **[Learn later if needed]** Custom OpenAPI tweaks, advanced middleware, GraphQL, templates

**Small prerequisite concepts**
- Type hints and `Annotated` basics (Phase 8).
- HTTP methods, status codes, headers (Phase 0 and 3).
- JSON serialization.

**Reading**
- [FastAPI tutorial](https://fastapi.tiangolo.com/tutorial/) (work in order through path params, query params, body, response model, dependencies, bigger applications, handling errors)
- [Pydantic models](https://docs.pydantic.dev/latest/concepts/models/) and the [v1 to v2 migration guide](https://pydantic.dev/docs/validation/latest/get-started/migration/)
- [Concurrency and async/await](https://fastapi.tiangolo.com/async/)

**Video**
- [FastAPI Course for Beginners](https://www.youtube.com/watch?v=tLKKmouUams), freeCodeCamp.org, English, duration not verified. Watch for orientation, then follow the docs; syntax may be dated.

**Hands-on exercises**
1. Follow the docs tutorial and type every example yourself (the docs themselves recommend typing it).
2. Build an in-memory Products CRUD with Create/Update/Read schemas.
3. Add router modules, `prefix="/api/v1"`, and a `deps.py` with a pagination dependency.
4. Add a `Settings` class; override it in a test.
5. Add one domain exception and a handler that returns the standard error JSON.

**What you must build**
A Products API (no database yet): routers, schemas, settings, error handler, 10 pytest tests with `TestClient`. This becomes the starter skeleton for Project 4.

**Completion checklist**
- [ ] `uv run fastapi dev` works and `/docs` shows tagged endpoints
- [ ] Separate Create/Update/Read schemas
- [ ] At least two reusable dependencies
- [ ] Settings loaded from environment
- [ ] Error responses have one consistent shape
- [ ] 10 tests pass
- [ ] I can explain the difference between `def` and `async def` endpoints

**Self-test**
1. How does FastAPI decide whether a parameter is path, query or body?
2. Why return 422 and who produces it?
3. What does `response_model` protect you from?
4. What is a `yield` dependency used for?
5. Name three Pydantic v1 names that changed in v2.

**Common mistakes**
- Copying Pydantic v1 code from old videos.
- One model for everything.
- Putting business logic in route functions.
- Using `async def` and then calling blocking code.

**Ready to continue when**
- You can add a new resource with its router, schemas and tests without looking at the previous one.
- You can explain the request lifecycle: Uvicorn, middleware, dependencies, validation, handler, response model.

**Slower-track option**
Skip custom exception handlers and settings overrides this week (move them to Week 14). Build only Products CRUD with Create/Read schemas and 6 tests. Watch no video.

### Week 13 — FastAPI Part 2: PostgreSQL, SQLAlchemy/SQLModel, Alembic, Auth and RBAC  (estimated hours: 10)

**Learning objectives**
- Connect FastAPI to PostgreSQL with SQLAlchemy 2.0 (or SQLModel) and a per-request session.
- Manage schema changes with Alembic.
- Implement password hashing, JWT login and role-based plus resource-level authorization.
- Paginate, filter and sort safely.

**Topics and subtopics**
- **[Must learn now]** PostgreSQL integration, connection strings, Docker Compose (11)
- **[Must learn now]** SQLAlchemy vs SQLModel decision (12)
- **[Must learn now]** Sessions and transactions (13)
- **[Must learn now]** Alembic (14)
- **[Must learn now]** Authentication: hashing and tokens (15)
- **[Must learn now]** RBAC and resource-level permissions (16)
- **[Must learn now]** Pagination, filtering, sorting (19)
- **[Learn during projects]** Refresh tokens, file uploads (20)
- **[Learn later if needed]** Async SQLAlchemy, OAuth social login, multi-tenant row-level security

**Small prerequisite concepts**
- Phase 7: primary/foreign keys, joins, indexes, transactions.
- Docker basics to run Postgres (one command; full Docker comes in Phase 15).
- Difference between authentication and authorization (Phase 6).

**Reading**
- [SQLAlchemy 2.0 tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html), [Session basics](https://docs.sqlalchemy.org/en/20/orm/session_basics.html), [Transactions](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html)
- [FastAPI SQL databases (SQLModel)](https://fastapi.tiangolo.com/tutorial/sql-databases/) and [SQLModel](https://sqlmodel.tiangolo.com/) (read to compare)
- [Alembic tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html), [autogenerate](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
- [OAuth2 with Password, Bearer with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), [OWASP password storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)

**Video**
- [Python API Development - Comprehensive Course for Beginners](https://www.youtube.com/watch?v=0sOvCWFmrtA), freeCodeCamp.org, English, duration not verified. Pydantic v1 era: use only the database/auth/testing ideas, copy code only from current docs.

**Hands-on exercises**
1. Start Postgres with Docker Compose; connect with `psql` or a GUI.
2. Define `User`, `Product`, `Order`, `OrderItem` with SQLAlchemy 2.0 style models.
3. Create the first Alembic migration; apply, downgrade, apply again; read the SQL it ran.
4. Replace the in-memory store with services using a `yield` session dependency.
5. Implement register/login with Argon2 and JWT; add `CurrentUser` and `require_role` dependencies.
6. Add owner-only access to orders and prove it with a test that user B gets 404 for user A's order.
7. Add pagination with a cap, a status filter and a whitelisted sort.

**What you must build**
Project 4 milestones 1 to 5 (see spec): database, migrations, auth and roles, products and orders CRUD with ownership rules.

**Completion checklist**
- [ ] Chose SQLAlchemy or SQLModel and wrote down why in the README
- [ ] Schema managed only by Alembic migrations
- [ ] Passwords hashed with Argon2 (or bcrypt), never stored in plain text
- [ ] JWT has expiry and uses an explicit algorithm
- [ ] Role dependency and owner check both exist
- [ ] List endpoints are paginated with a hard cap
- [ ] Order creation is one transaction

**Self-test**
1. Why does autogenerate not detect a column rename, and what do you do?
2. Why one session per request?
3. Why return the same message for wrong email and wrong password?
4. What is broken object-level authorization?
5. Why must multi-row writes share one transaction?

**Common mistakes**
- Using `create_all()` instead of migrations.
- Following SQLAlchemy 1.x tutorials.
- Committing in repository helpers.
- Putting the JWT secret in code.
- Forgetting to filter list endpoints by owner.

**Ready to continue when**
- Migrations run from an empty database to current head with one command.
- A customer cannot read or modify another customer's order, proven by tests.

**Slower-track option**
Use SQLModel and the official FastAPI SQL tutorial directly (less code to learn), skip refresh tokens and uploads, and do offset pagination only. Auth can be access-token only. Move the Alembic rename exercise to Week 14.

### Week 14 — FastAPI Finish: Tests, Logging, Background Tasks, Streaming, plus Project 4  (estimated hours: 10)

**Learning objectives**
- Write an integration test suite with dependency overrides and a test database.
- Add logging with request IDs, health checks and graceful lifespan handling.
- Use background tasks and understand when a queue is needed; try a WebSocket or SSE stream.
- Containerize and finish Project 4.

**Topics and subtopics**
- **[Must learn now]** pytest and integration tests (24)
- **[Must learn now]** Dependency overrides and test DBs (25)
- **[Must learn now]** Logging and request tracing (23)
- **[Must learn now]** CORS and security basics (26)
- **[Must learn now]** Health checks, lifespan, production config (28, 29)
- **[Learn during projects]** Timeouts, retries and pooling (27)
- **[Learn during projects]** Background tasks and queues (21)
- **[Learn during projects]** WebSockets and streaming (22)
- **[Learn later if needed]** Celery or other task queues, Redis pub/sub, PgBouncer, Kubernetes

**Small prerequisite concepts**
- Fixtures and parametrize (Week 11).
- Docker image vs container (Phase 15 preview).
- What a reverse proxy does.

**Reading**
- [Testing](https://fastapi.tiangolo.com/tutorial/testing/), [Testing dependencies](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [Middleware](https://fastapi.tiangolo.com/tutorial/middleware/), [Lifespan events](https://fastapi.tiangolo.com/advanced/events/), [CORS](https://fastapi.tiangolo.com/tutorial/cors/)
- [Background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/), [WebSockets](https://fastapi.tiangolo.com/advanced/websockets/), [Server-Sent Events](https://fastapi.tiangolo.com/tutorial/server-sent-events/)
- [Deployment](https://fastapi.tiangolo.com/deployment/), [Docker](https://fastapi.tiangolo.com/deployment/docker/), [Connection pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)

**Video**
- [Pytest Tutorial – How to Test Python Code](https://www.youtube.com/watch?v=cHYq1MRoyI0), freeCodeCamp.org, English, duration not verified (revision of pytest basics only).
- No other video verified for this week; use the official documentation above.

**Hands-on exercises**
1. Build the test fixtures: test DB, per-test rollback, client, `customer_token` and `admin_token`.
2. Write at least 30 tests across auth, products, orders, authorization and validation.
3. Add request-ID middleware and structured logs; confirm no password or token appears in logs.
4. Add `/health/live` and `/health/ready` and a lifespan that disposes the engine.
5. Add a background task that writes an audit-log row or a fake "email sent" log when an order is created.
6. Add an SSE or WebSocket endpoint that pushes order status changes (optional if time is short).
7. Write a Dockerfile and `docker-compose.yml` (API + Postgres), run `alembic upgrade head` as a separate step, and hit `/docs`.

**What you must build**
**Project 4** finished: tests, logging, Docker Compose, README, and a deployed or deploy-ready version.

**Completion checklist**
- [ ] 30+ tests pass in CI-like conditions (`uv run pytest`)
- [ ] Tests never touch the development database
- [ ] Request ID in logs and in response headers
- [ ] Health endpoints work and readiness fails when DB is down
- [ ] CORS limited to configured origins
- [ ] Docker Compose brings up the whole stack
- [ ] README complete, security checklist reviewed
- [ ] Code pushed to GitHub with a clean history

**Self-test**
1. How does `dependency_overrides` work and how do you reset it?
2. Why is `BackgroundTasks` not a job queue?
3. Liveness vs readiness?
4. Why can too many workers exhaust Postgres connections?
5. WebSocket vs SSE: when each?

**Common mistakes**
- Tests sharing a database with development.
- Leaving overrides in place between tests.
- Running migrations from every replica on start.
- Mock-heavy tests that prove nothing.
- Ignoring unhappy-path tests.

**Ready to continue when**
- Project 4 meets all acceptance criteria.
- You can explain every layer and every security control in it for 10 minutes without notes.

**Slower-track option**
Cut WebSocket/SSE, retries and pooling tuning. Keep: 20 tests (auth, orders, authorization), logging with request ID, health check, Docker Compose. Spill deployment to Week 15 evenings, but do not start Phase 10 until the tests pass.

> **Honest note:** If Weeks 12 to 14 feel too fast, take a fourth week here. FastAPI with a database is the foundation under Projects 5, 6 and 7. A solid Project 4 saves you time later.

# Project 4 — FastAPI Order Management Backend

## Problem statement and real-world use case

A small online business sells products and takes orders. Customers need to register, browse products, place orders and track them. Staff need to manage products and move orders through a lifecycle (pending, paid, shipped, delivered, cancelled). Admins manage users and roles. You will build the backend API that a React/Next.js frontend (like your Project 1 dashboard) can call. This is the same domain as Project 2 (Node/Express) on purpose: building it again in FastAPI lets you compare the two stacks honestly, and this API becomes the base for Project 6 (AI order and refund assistant).

## Requirements and user stories

- As a visitor, I can register and log in.
- As a customer, I can list products, create an order with several items, view only my orders, and cancel my order while it is still pending.
- As staff, I can create and edit products, view all orders and change an order's status along allowed transitions.
- As an admin, I can manage users and roles and see an audit log.
- As a frontend developer, I can read the OpenAPI docs and get consistent errors and pagination.
- As an operator, I can see structured logs with request IDs, check health, and deploy with Docker.

## MVP vs advanced features

| Level | Features |
| --- | --- |
| MVP | Auth (register, login, `me`); roles customer, staff, admin; products CRUD (soft delete); orders with items; stock check in one transaction; status transitions; pagination, filter, sort; Alembic migrations; 30+ tests; logging with request ID; health checks; OpenAPI docs; Docker Compose |
| Advanced | Refresh tokens with rotation; idempotency key on order creation; invoice PDF upload to object storage; background task for emails/audit; SSE or WebSocket status updates; rate limiting; keyset pagination; async SQLAlchemy; CI pipeline; deployment to a cloud VM or container service; export to CSV |

## Suggested architecture

Layered monolith: **router** (HTTP) calls **service** (business rules and the transaction boundary), which uses **models** through a per-request **session**. **Schemas** define the public contract. **Core** holds settings, security, logging and errors. PostgreSQL is the only datastore. Order placement runs in one transaction that locks product rows or uses an atomic stock update, writes the order, items and an audit row, then commits.

```text
Client -> Reverse proxy (HTTPS) -> Uvicorn/FastAPI
          -> middleware (request id, CORS, logging)
          -> router -> dependencies (session, current user, role)
          -> service -> SQLAlchemy -> PostgreSQL
```

## Folder structure

Use the structure from Phase 9, topic 30: `app/main.py`, `app/api/deps.py`, `app/api/v1/routers/`, `app/core/`, `app/db/`, `app/models/`, `app/schemas/`, `app/services/`, `migrations/`, `tests/`, plus `Dockerfile`, `docker-compose.yml`, `.env.example`, `pyproject.toml` and `uv.lock`. Write a one-line "why this folder exists" for each in your README.

## DB schema / ERD

| Table | Key columns | Notes |
| --- | --- | --- |
| users | id, email (unique), password_hash, role, is_active, created_at | role is an enum: customer, staff, admin |
| products | id, sku (unique), name, description, price_cents or numeric(12,2), stock_quantity, is_active, created_at, updated_at | check constraint stock_quantity >= 0; never use float for money |
| orders | id, user_id (FK users), status, total_amount, currency, idempotency_key (unique per user, nullable), created_at, updated_at | index on (user_id, created_at) and on status |
| order_items | id, order_id (FK), product_id (FK), quantity, unit_price (snapshot of price at order time) | check quantity > 0; unique (order_id, product_id) |
| order_status_history | id, order_id (FK), from_status, to_status, changed_by (FK users), changed_at | audit trail of transitions |
| audit_log (advanced) | id, actor_id, action, entity, entity_id, created_at | append-only |

Relationships: users 1-N orders; orders 1-N order_items; products 1-N order_items (so orders M-N products through order_items); orders 1-N order_status_history. Draw the ERD yourself in the README (Mermaid or an image) before writing models.

Allowed status transitions: pending to paid or cancelled; paid to shipped or cancelled (with stock restore); shipped to delivered. Everything else returns 409.

## API endpoints

| Method | Path | Auth | Purpose |
| --- | --- | --- | --- |
| POST | /api/v1/auth/register | public | Create customer account |
| POST | /api/v1/auth/login | public | Return access token (and refresh token if built) |
| GET | /api/v1/users/me | any user | Current user profile |
| GET | /api/v1/users | admin | List users, paginated |
| PATCH | /api/v1/users/{id}/role | admin | Change role |
| GET | /api/v1/products | public or any user | List, search, filter, sort, paginate |
| GET | /api/v1/products/{id} | public or any user | Product detail |
| POST | /api/v1/products | staff, admin | Create product |
| PATCH | /api/v1/products/{id} | staff, admin | Update product |
| DELETE | /api/v1/products/{id} | admin | Soft delete (set inactive) |
| POST | /api/v1/orders | customer | Create order (items list) |
| GET | /api/v1/orders | customer: own; staff/admin: all | List with status/date filters, pagination |
| GET | /api/v1/orders/{id} | owner, staff, admin | Order detail with items |
| POST | /api/v1/orders/{id}/cancel | owner (pending only), staff, admin | Cancel and restore stock |
| PATCH | /api/v1/orders/{id}/status | staff, admin | Move along allowed transitions |
| GET | /api/v1/orders/{id}/history | owner, staff, admin | Status history |
| GET | /health/live | public | Process is up |
| GET | /health/ready | public | Database reachable |

Standard list response: `{ "items": [...], "total": 120, "limit": 20, "offset": 0 }`. Standard error: `{ "error": { "code": "...", "message": "...", "request_id": "..." } }`.

## Packages and setup

- Runtime: `fastapi[standard]`, `sqlalchemy` (2.x), `alembic`, a PostgreSQL driver (`psycopg[binary]` or `asyncpg` if you go async), `pydantic-settings`, `pyjwt`, `pwdlib[argon2]`, `email-validator`.
- Alternative: `sqlmodel` instead of separate SQLAlchemy models and schemas (state your reason).
- Dev: `pytest`, `httpx`, `ruff`, `mypy`, optionally `pytest-cov`.
- Services: PostgreSQL via Docker Compose (one dev DB, one test DB).
- Setup: `uv init`, `uv add ...`, `docker compose up -d db`, `uv run alembic upgrade head`, `uv run fastapi dev`.

## Implementation milestones

1. **Skeleton.** `uv` project, folder layout, settings, health endpoint, first test, `ruff`/`mypy` config, Git. Commit.
2. **Database.** Docker Compose Postgres; engine and session dependency; models for all tables; first Alembic migration; seed script for an admin user (read credentials from env).
3. **Auth.** Register/login, Argon2 hashing, JWT with expiry, `CurrentUser`, `require_role`. Tests for success, wrong password, expired token, no token.
4. **Products.** CRUD with schemas, search and filter, pagination with a cap, whitelisted sort, soft delete. Tests for each role.
5. **Orders.** Create order in one transaction with stock check (atomic update or row lock), price snapshot, total computed server-side (never trust client prices). Owner-only reads. Tests including "insufficient stock rolls back everything" and a concurrency test if you can.
6. **Order lifecycle.** Status transitions table, history rows, cancel with stock restore, 409 for illegal transitions.
7. **Cross-cutting.** Error handlers, request-ID middleware, structured logging, CORS from settings, lifespan, health/ready.
8. **Test suite.** Test DB, rollback or truncate fixtures, token fixtures per role, 30+ tests, coverage report used as a hint, not a goal.
9. **Docker and docs.** Dockerfile (non-root user, no dev dependencies), Compose, `.env.example`, README, OpenAPI tags and examples.
10. **Advanced (pick two).** Idempotency key, background audit task, SSE status stream, rate limiting on login, CI workflow, cloud deploy.

## Test cases

- Auth: register duplicate email gives 409; weak password gives 422; login wrong password gives 401 with the same message as unknown email; expired or tampered token gives 401; inactive user cannot log in.
- Authorization: customer cannot call staff endpoints (403); customer A gets 404 for customer B's order; list endpoint returns only own orders for customers; admin can change roles; staff cannot.
- Validation: negative quantity, zero items, unknown product, oversized `limit`, bad sort field all rejected with the right status.
- Orders: total equals sum of snapshot prices times quantities; client-supplied price ignored; insufficient stock leaves stock unchanged and creates no order; cancel restores stock exactly once; double cancel returns 409.
- Concurrency: two simultaneous orders for the last unit, only one succeeds.
- Lifecycle: every allowed transition works and writes history; every illegal one returns 409.
- Migrations: `alembic upgrade head` on an empty DB succeeds; `alembic check` reports no drift.
- Infra: `/health/ready` returns 503 when the DB is unreachable; every response carries a request ID; logs contain no password or token.

## Security checklist

Prioritized, highest first:

1. Authorize every endpoint, including list endpoints; filter by owner (broken object-level authorization is the top API risk).
2. Hash passwords with Argon2 or bcrypt; never log or return hashes.
3. Secrets (JWT secret, DB password) only from environment or a secret manager; strong random JWT secret; `.env` ignored by Git.
4. Short-lived access tokens; explicit algorithm on decode; check `exp`.
5. Server-side calculation of prices and totals; ignore client-sent amounts and roles.
6. Pydantic validation on every input; bounds on lengths, quantities and `limit`.
7. ORM or parameterized queries only; whitelist sort and filter fields.
8. Rate limit login and registration; consider lockout or backoff.
9. CORS with an explicit origin list; HTTPS only in production.
10. Generic error messages to clients; details only in logs; no stack traces in responses.
11. Do not allow self-assigned roles at registration; seed the first admin out of band.
12. Docker image runs as non-root; minimal base image; dependencies pinned by lockfile and scanned.
13. Logs without personal data or tokens; request IDs for tracing.
14. Back up the database and test a restore.
15. Disable or protect `/docs` in production if the API is not public.

## Deployment plan

1. Containerize: multi-stage or `uv`-based Dockerfile; run `fastapi run`; non-root user. See [FastAPI with Docker](https://fastapi.tiangolo.com/deployment/docker/) and [uv in Docker](https://docs.astral.sh/uv/guides/integration/docker/).
2. Local: `docker compose up` with API and Postgres; migration as a one-off command.
3. Choose one target (Phase 15 teaches AWS): a small VM with Docker Compose and a reverse proxy, or a managed container service with a managed PostgreSQL. A free-tier or low-cost platform is fine for a portfolio demo; check current pricing yourself.
4. Run `alembic upgrade head` as a release step before starting new containers.
5. Put HTTPS in front (load balancer or reverse proxy); set `--proxy-headers` as needed.
6. Configure env vars and secrets in the platform; confirm health checks.
7. Smoke test with the OpenAPI docs and a script; keep logs viewable.
8. Write down the rollback steps (previous image tag, migration downgrade or forward-fix).

## README structure

1. Title, one-paragraph summary, screenshot of `/docs`.
2. Features and roles table.
3. Architecture diagram and "why each folder exists".
4. ERD and status transition diagram.
5. Tech choices and decisions (SQLAlchemy vs SQLModel, sync vs async, why).
6. Quick start (Docker Compose) and local dev with `uv`.
7. Environment variables table (`.env.example`).
8. API overview table (link to `/docs`).
9. Running tests; how the test database works.
10. Security notes (what is covered, what is not).
11. Deployment notes and rollback.
12. Limitations and next steps.

## Acceptance criteria

- [ ] All MVP endpoints in the table work and appear in OpenAPI with tags and examples.
- [ ] Database changes are made only through Alembic; an empty DB reaches head in one command.
- [ ] Roles and ownership rules are enforced and proven by tests.
- [ ] Order creation is atomic; stock never goes negative.
- [ ] 30 or more tests pass against a separate test database; none call external services.
- [ ] `ruff`, `mypy` and `pytest` pass.
- [ ] Logs are structured with request IDs; secrets never appear in logs.
- [ ] `docker compose up` starts a working stack; health endpoints behave correctly.
- [ ] README meets the structure above, and every item in the security checklist is marked done or explained.
- [ ] I can explain every design decision and walk through one request end to end.

## Common mistakes

- Trusting client-sent prices, totals or roles.
- One Pydantic/ORM model for everything, leaking `password_hash`.
- `create_all()` in production instead of Alembic.
- Committing inside helper functions so a failure leaves half an order.
- Returning all orders to customers (missing owner filter).
- Using float for money.
- Blocking calls inside `async def`.
- Tests that use the dev database, or share state.
- Over-engineering (repositories, events, microservices) before the MVP works.

## Interview questions

- Walk me through what happens from the HTTP request to the database for `POST /orders`.
- How do you prevent overselling when two customers buy the last item?
- SQLAlchemy vs SQLModel: which did you choose and why?
- How does dependency injection help with testing in FastAPI?
- How do you test a database-backed endpoint without polluting data?
- How do you do a safe migration that renames a column?
- Explain authentication vs authorization in your API. How do you prevent one user reading another's order?
- Where is the transaction boundary and why?
- Sync vs async endpoints: what did you pick and what are the risks?
- How would you scale this to many users? What would you change first?
- How would you add idempotency to order creation?
- What would you monitor in production?

## Sources

Every URL below was fetched by me (with `curl` returning HTTP 200, or through a fetch tool for page content) on 2026-10-09. YouTube items were verified through the oEmbed endpoint using a fetch tool, because my shell could not reach youtube.com directly.

**Python and packaging**
- https://docs.python.org/3/tutorial/index.html
- https://docs.python.org/3/tutorial/datastructures.html
- https://docs.python.org/3/tutorial/classes.html
- https://docs.python.org/3/tutorial/errors.html
- https://docs.python.org/3/tutorial/inputoutput.html
- https://docs.python.org/3/library/venv.html
- https://docs.python.org/3/library/asyncio.html
- https://docs.python.org/3/library/typing.html
- https://docs.python.org/3/library/dataclasses.html
- https://docs.python.org/3/library/enum.html
- https://docs.python.org/3/library/csv.html
- https://docs.python.org/3/library/json.html
- https://docs.python.org/3/library/pathlib.html
- https://docs.python.org/3/library/functools.html
- https://docs.python.org/3/library/contextlib.html
- https://docs.python.org/3/library/logging.html
- https://docs.python.org/3/howto/logging.html
- https://docs.python.org/3/howto/functional.html
- https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
- https://packaging.python.org/en/latest/tutorials/installing-packages/
- https://docs.astral.sh/uv/
- https://docs.astral.sh/uv/guides/projects/
- https://docs.astral.sh/uv/guides/integration/docker/
- https://docs.astral.sh/ruff/
- https://mypy.readthedocs.io/en/stable/
- https://www.python-httpx.org/
- https://www.python-httpx.org/async/

**pytest**
- https://docs.pytest.org/en/stable/
- https://docs.pytest.org/en/stable/getting-started.html
- https://docs.pytest.org/en/stable/how-to/fixtures.html
- https://docs.pytest.org/en/stable/how-to/parametrize.html
- https://docs.pytest.org/en/stable/how-to/monkeypatch.html

**FastAPI, Pydantic, Uvicorn, ASGI**
- https://fastapi.tiangolo.com/tutorial/
- https://fastapi.tiangolo.com/tutorial/first-steps/
- https://fastapi.tiangolo.com/tutorial/path-params/
- https://fastapi.tiangolo.com/tutorial/query-params/
- https://fastapi.tiangolo.com/tutorial/body/
- https://fastapi.tiangolo.com/tutorial/response-model/
- https://fastapi.tiangolo.com/tutorial/response-status-code/
- https://fastapi.tiangolo.com/tutorial/dependencies/
- https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
- https://fastapi.tiangolo.com/tutorial/handling-errors/
- https://fastapi.tiangolo.com/tutorial/security/
- https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- https://fastapi.tiangolo.com/tutorial/cors/
- https://fastapi.tiangolo.com/tutorial/background-tasks/
- https://fastapi.tiangolo.com/tutorial/testing/
- https://fastapi.tiangolo.com/tutorial/sql-databases/
- https://fastapi.tiangolo.com/tutorial/bigger-applications/
- https://fastapi.tiangolo.com/tutorial/request-files/
- https://fastapi.tiangolo.com/tutorial/middleware/
- https://fastapi.tiangolo.com/tutorial/metadata/
- https://fastapi.tiangolo.com/tutorial/server-sent-events/
- https://fastapi.tiangolo.com/advanced/testing-dependencies/
- https://fastapi.tiangolo.com/advanced/settings/
- https://fastapi.tiangolo.com/advanced/websockets/
- https://fastapi.tiangolo.com/advanced/custom-response/
- https://fastapi.tiangolo.com/advanced/events/
- https://fastapi.tiangolo.com/async/
- https://fastapi.tiangolo.com/deployment/
- https://fastapi.tiangolo.com/deployment/docker/
- https://docs.pydantic.dev/latest/concepts/models/
- https://docs.pydantic.dev/latest/concepts/validators/
- https://docs.pydantic.dev/latest/concepts/pydantic_settings/
- https://pydantic.dev/docs/validation/latest/get-started/migration/
- https://uvicorn.dev/deployment/
- https://asgi.readthedocs.io/en/latest/
- https://pyjwt.readthedocs.io/en/stable/

**Database**
- https://docs.sqlalchemy.org/en/20/
- https://docs.sqlalchemy.org/en/20/tutorial/index.html
- https://docs.sqlalchemy.org/en/20/orm/quickstart.html
- https://docs.sqlalchemy.org/en/20/orm/session_basics.html
- https://docs.sqlalchemy.org/en/20/orm/session_transaction.html
- https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- https://docs.sqlalchemy.org/en/20/core/pooling.html
- https://alembic.sqlalchemy.org/en/latest/tutorial.html
- https://alembic.sqlalchemy.org/en/latest/autogenerate.html
- https://alembic.sqlalchemy.org/en/latest/cookbook.html
- https://sqlmodel.tiangolo.com/

**Security**
- https://owasp.org/www-project-top-ten/
- https://owasp.org/API-Security/editions/2023/en/0x00-header/
- https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html

**Videos (oEmbed verified; durations not verified)**
- https://www.youtube.com/watch?v=eWRfhZUzrAc (Python for Beginners – Full Course, freeCodeCamp.org)
- https://www.youtube.com/playlist?list=PLu0W_9lII9agwh1XjRt242xIpHhPT2llg (Python for Beginners (Full Course) Hindi, CodeWithHarry)
- https://www.youtube.com/watch?v=ZDa-Z5JzLYM (Python OOP Tutorial 1, Corey Schafer)
- https://www.youtube.com/watch?v=cHYq1MRoyI0 (Pytest Tutorial, freeCodeCamp.org)
- https://www.youtube.com/watch?v=tLKKmouUams (FastAPI Course for Beginners, freeCodeCamp.org)
- https://www.youtube.com/watch?v=0sOvCWFmrtA (Python API Development - Comprehensive Course for Beginners, freeCodeCamp.org)

**Discovery pages used to find video IDs**
- https://www.freecodecamp.org/news/creating-apis-with-python-free-19-hour-course/
- https://www.freecodecamp.org/news/fastapi-helps-you-develop-apis-quickly
- https://www.freecodecamp.org/news/testing-in-python-with-pytest/
- https://www.freecodecamp.org/news/python-programming-course/
