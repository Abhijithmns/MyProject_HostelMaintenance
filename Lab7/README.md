# L6_L7_07 — Hospital Triage Priority

Lab 7: Fuzz Testing with Hypothesis

## About

A set of property-based fuzz tests targeting patient vitals summaries, BMI calculations, and ward bed allocation descriptors to expose crashes on malformed data.

## Files

| File | Description |
|------|-------------|
| `processor.py` | Input-processing module, including fixes found during fuzz testing |
| `test_processor.py` | Property-based tests written with Hypothesis |
| `fuzzing_report.md` | Test approach, findings, fixes, and results |

## Run the tests

```bash
python -m pytest -q test_processor.py
```

Keep all your Lab 7 work in this `Lab7` folder.

Refer to the lab handout for instructions.
