"""
Lab 6: Code Coverage Test Suite
Target: hospital_triage_priority.py

This test suite is designed to achieve >90% code (line) coverage across all functions
and statements in hospital_triage_priority.py.
"""

import pytest
from hospital_triage_priority import process_triage_wards, monitor_oxygen_manifolds


# ===========================================================================
# 1. Input Validation Tests
# ===========================================================================

def test_invalid_wards_not_a_list():
    """Line coverage for invalid wards type (raises ValueError)."""
    with pytest.raises(ValueError):
        process_triage_wards("invalid_type", 10)


def test_invalid_negative_default_acuity():
    """Line coverage for negative default acuity score (raises ValueError)."""
    with pytest.raises(ValueError):
        process_triage_wards([], -5)


# ===========================================================================
# 2. Ward and Patient Processing Tests
# ===========================================================================

def test_single_normal_patient():
    """Line coverage for normal patient receiving default acuity score."""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 98, "hr": 72, "unconscious": False}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 10
    assert result["status"] == "TRIAGE_STABLE"


def test_ward_not_accepting_skipped():
    """Line coverage for ward skipping when is_accepting is False."""
    wards = [
        {
            "is_accepting": False,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 95, "hr": 80, "unconscious": False}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_patient_invalid_vitals_flagged():
    """Line coverage for invalid vitals flagging (spo2 <= 0 or hr <= 0)."""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [
                {"spo2": 0, "hr": 75, "unconscious": False},
                {"spo2": 95, "hr": 0, "unconscious": False}
            ]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_unconscious_general_ward():
    """Line coverage for unconscious patient in non-outpatient ward (+100 acuity)."""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 95, "hr": 80, "unconscious": True}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 100
    assert result["status"] == "TRIAGE_STABLE"


def test_unconscious_outpatient_ward():
    """Line coverage for unconscious patient in outpatient tier (resets acuity to 0 and breaks)."""
    wards = [
        {
            "is_accepting": True,
            "tier": "outpatient",
            "icu_standby": False,
            "patients": [
                {"spo2": 95, "hr": 80, "unconscious": False},
                {"spo2": 95, "hr": 80, "unconscious": True},
                {"spo2": 95, "hr": 80, "unconscious": False}
            ]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_low_spo2_urgent():
    """Line coverage for conscious patient with low spo2 (< 90) adding +60."""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 85, "hr": 75, "unconscious": False}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 60
    assert result["status"] == "TRIAGE_STABLE"


def test_high_hr_urgent():
    """Line coverage for conscious patient with high hr (> 120) adding +60."""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 95, "hr": 130, "unconscious": False}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 60
    assert result["status"] == "TRIAGE_STABLE"


def test_icu_standby_bonus():
    """Line coverage for icu_standby adding 25 to total acuity."""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": True,
            "patients": [{"spo2": 95, "hr": 75, "unconscious": False}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 35
    assert result["status"] == "TRIAGE_STABLE"


def test_ward_alert_flagged_entries():
    """Line coverage for flagged_entries > 4 triggering WARD_ALERT."""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 0, "hr": 70, "unconscious": False}] * 5
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["status"] == "WARD_ALERT"


# ===========================================================================
# 3. Oxygen Manifold Monitor Tests
# ===========================================================================

def test_monitor_oxygen_empty_data():
    """Line coverage for empty sensor streams returning NO_DATA."""
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_monitor_oxygen_normal():
    """Line coverage for normal manifold pressures returning PRESSURE_NORMAL."""
    assert monitor_oxygen_manifolds([[5.0, 4.5, 4.2]]) == "PRESSURE_NORMAL"


def test_monitor_oxygen_failure():
    """Line coverage for consecutive low pressure readings returning PRESSURE_FAILURE."""
    assert monitor_oxygen_manifolds([[5.0, 3.5, 3.8, 5.0]]) == "PRESSURE_FAILURE"


def test_monitor_oxygen_streak_reset():
    """Line coverage for streak resetting to 0 when pressure returns to normal."""
    assert monitor_oxygen_manifolds([[3.8, 4.2, 3.5]]) == "PRESSURE_NORMAL"
