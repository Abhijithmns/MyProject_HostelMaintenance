# Lab 5 – Reflection

## 1. What surprised you most about the issues the tools found?

The most surprising finding was how quietly the **mutable default argument** (`logs=[]`) could have caused a subtle data-corruption bug. At first glance the function signature looks perfectly ordinary; without a tool or careful reading of PEP 8 notes, it is easy to miss the fact that the default list is shared across every call. Static analysis (Pylint W0102) flagged it immediately, while manual testing alone might never have revealed it because the demo only calls `add_trip_log` with the same route IDs in sequence.

## 2. Were there any issues the tools *missed* that you spotted by reading the code or running it?

Yes – two important runtime bugs were not flagged by any tool:

- **Negative passenger counts** (`-6`) and **non-integer values** (`"full"`) were accepted without complaint. The tools see valid Python syntax and cannot know that the domain requires positive integers, so they raised no warning. Running the program and reading the output was the only way to catch this.
- **The `KeyError` crash** on line 58 (`average_load("R3")` after `remove_route("R3")`) is a logic error that tools cannot infer statically – they cannot track which keys are present at runtime. The crash only became visible by actually executing the script.

## 3. How did fixing the issues change your view of "working" code?

Before this exercise, "working" meant "produces output without crashing". After fixing the issues, "working" means the code is **correct, robust, readable, and maintainable**:

- *Correct*: results are logically valid (no negative passenger counts, no stale references to deleted routes).
- *Robust*: unexpected inputs are caught and reported gracefully rather than causing silent data corruption or unhandled exceptions.
- *Readable*: consistent naming (`assign_driver` vs `assignDriver`), f-strings, and docstrings make the intent clear to future readers.
- *Maintainable*: removing the `global` statement and using context managers means less state to reason about and no resource leaks.

A program that "works" under the happy path may still be a liability in production.

## 4. Which tool was most useful, and why?

**Pylint** was the most useful overall. It reported the highest number of distinct issues (18 messages covering bugs, style, and design smells) and provided both a human-readable explanation and a numeric score (6.25 → 10.00) that made progress easy to measure. Flake8 was a fast and complementary PEP 8 checker, and Bandit was valuable for security-specific patterns (bare except, `random` for non-crypto use). But neither Flake8 nor Bandit surfaced the mutable-default-argument bug or the unnecessary `global` statement – both of which Pylint caught. For a general-purpose code-quality workflow, Pylint gives the broadest coverage.
