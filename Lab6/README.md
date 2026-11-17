# L6_L7_07 — Hospital Triage Priority

Lab 6: Code and Branch Coverage Analysis

## About

A Python module that evaluates ward admission acuity based on patient vitals and consciousness, enforces ward capacity thresholds, and audits medical oxygen line pressure.

## Files & Deliverables

| File | Description |
|------|-------------|
| `hospital_triage_priority.py` | The module under test |
| `test_hospital_triage.py` | Full test suite |
| `CodeCoverageTest_hospital_triage_priority.py` | Targeted test cases for Code (Line) Coverage (100% achieved) |
| `BranchCoverageTest_hospital_triage_priority.py` | Targeted test cases for Branch Coverage (100% achieved) |
| `CodeCoverageTest_hospital_triage.py` | Compatibility test alias |
| `BranchCoverageTest_hospital_triage.py` | Compatibility test alias |
| `coverage_report.md` | Detailed analysis report covering lines, branches, and edge cases |
| `screenshots/code_coverage_analysis.png` | Terminal screenshot for code coverage analysis |
| `screenshots/branch_coverage_analysis.png` | Terminal screenshot for branch coverage analysis |

## Coverage Results

| Metric | Target | Achieved | Status |
|---|---|---|---|
| **Line Coverage** | $\ge 90\%$ | **100%** | **PASS** |
| **Branch Coverage** | $\ge 90\%$ | **100%** | **PASS** |

## Commands to Run Coverage

```bash
# Line Coverage
coverage run -m pytest CodeCoverageTest_hospital_triage_priority.py
coverage report -m

# Branch Coverage
coverage run --branch -m pytest BranchCoverageTest_hospital_triage_priority.py
coverage report -m
```

Refer to [coverage_report.md](coverage_report.md) for the complete analysis.
