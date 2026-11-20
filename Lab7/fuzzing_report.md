# Lab 7 — Fuzz Testing Notes

**Module:** `processor.py`  
**Tool:** Hypothesis 6.170.15  
**Run:** 20 November 2026

## What I tested

I used property-based tests instead of a short list of hand-picked bad inputs. The three public functions were each given a mix of ordinary text, blank strings, Unicode, punctuation-heavy strings, `None`, numbers, floats (including `nan` and infinity), and small lists. The aim was simple: user input must never crash the triage helper, and a successful result must still make sense.

The suite also generates valid vital readings separately. That check makes sure the critical/stable decision agrees with the rule in the implementation, rather than only checking that the function survives bad input.

## Bugs found and fixed

| Finding | Why it mattered | Fix |
|---|---|---|
| A blank vitals field returned a “non-numeric” message even though the function's contract says the input must be non-empty. | It was not a crash, but it sends the user to correct the wrong thing. | Empty and whitespace-only values are now caught at the input boundary with the intended message. The same guard was added for BMI and ward allocation input. |
| `assign_ward_bed("ICU-1_0")` returned `Intensive Care Unit Bed #10`. | Python's `int()` accepts underscores. That is useful in source code, but a patient-facing ward identifier should not quietly reinterpret it. | Bed numbers now require ASCII decimal digits before conversion. `ICU-05` still works; `ICU-1_0`, `ICU-+5`, and `ICU-2.5` are rejected. |

## Test properties

1. Malformed vitals always give either a formatted summary or an `Error:` message; they do not raise an exception.
2. BMI either gives an `Error:` message or a positive, finite floating-point value.
3. Ward allocation always gives a known assignment or an `Error:` message.
4. Valid vital readings are labelled `CRITICAL` exactly when heart rate is above 120, SpO2 is below 90, or temperature is above 39°C.
5. Regression checks keep the blank-field and bed-number fixes from coming back.

## Result

`pytest -q test_processor.py` completed successfully: **5 passed**. Each fuzz property runs 250 generated examples, in addition to the focused regression checks.

## Files submitted

- `processor.py` — input-validation fixes
- `test_processor.py` — Hypothesis properties and regression checks
- `fuzzing_report.md` — this record of the run and fixes
