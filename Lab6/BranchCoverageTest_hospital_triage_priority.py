"""
Lab 6: Branch Coverage Test Suite
Target: hospital_triage_priority.py

This test suite is designed to achieve 100% branch coverage across all decision points,
control structures, compound conditionals, and edge-case boundaries in hospital_triage_priority.py.
"""

import pytest
from hospital_triage_priority import process_triage_wards, monitor_oxygen_manifolds


# ===========================================================================
# 1. Input Validation Branch Coverage
# ===========================================================================

def test_invalid_wards_type_branch():
    """Branch: not isinstance(wards, list) evaluates True."""
    with pytest.raises(ValueError, match="Invalid wards list or base acuity score"):
        process_triage_wards("string_not_list", 10)


def test_negative_default_acuity_branch():
    """Branch: default_acuity_score < 0 evaluates True."""
    with pytest.raises(ValueError, match="Invalid wards list or base acuity score"):
        process_triage_wards([], -1)


# ===========================================================================
# 2. Ward Loop & Ward-Level Decisions
# ===========================================================================

def test_empty_wards_list():
    """Branch: wards is empty list -> loop body not executed, returns NO_URGENT_CASES."""
    result = process_triage_wards([], 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_ward_is_not_accepting():
    """Branch: not ward.get('is_accepting', False) evaluates True -> continues to next ward."""
    wards = [
        {
            "is_accepting": False,
            "tier": "icu",
            "icu_standby": True,
            "patients": [{"spo2": 80, "hr": 140, "unconscious": True}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_ward_icu_standby_true_and_false():
    """Branch: ward.get('icu_standby', False) evaluated True (+25) and False (+0)."""
    # Ward with icu_standby True
    wards_with_standby = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": True,
            "patients": [{"spo2": 95, "hr": 75, "unconscious": False}]
        }
    ]
    res_standby = process_triage_wards(wards_with_standby, 10)
    assert res_standby["acuity_score"] == 35
    assert res_standby["status"] == "TRIAGE_STABLE"

    # Ward with icu_standby False
    wards_no_standby = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 95, "hr": 75, "unconscious": False}]
        }
    ]
    res_no_standby = process_triage_wards(wards_no_standby, 10)
    assert res_no_standby["acuity_score"] == 10
    assert res_no_standby["status"] == "TRIAGE_STABLE"


# ===========================================================================
# 3. Patient Vitals and Condition Branches
# ===========================================================================

def test_patient_invalid_spo2_branch():
    """Branch: spo2 <= 0 evaluates True (spo2 = 0) -> flagged and continue."""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 0, "hr": 80, "unconscious": False}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_patient_invalid_hr_branch():
    """Branch: heart_rate <= 0 evaluates True (hr = -5) -> flagged and continue."""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 95, "hr": -5, "unconscious": False}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_unconscious_outpatient_tier():
    """Branch: is_unconscious True AND ward_tier == 'outpatient' -> acuity=0 and break."""
    wards = [
        {
            "is_accepting": True,
            "tier": "outpatient",
            "icu_standby": False,
            "patients": [
                {"spo2": 95, "hr": 75, "unconscious": False},  # +10
                {"spo2": 95, "hr": 75, "unconscious": True},   # resets acuity=0, breaks
                {"spo2": 95, "hr": 75, "unconscious": False}   # skipped due to break
            ]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_unconscious_non_outpatient_tier():
    """Branch: is_unconscious True AND ward_tier != 'outpatient' -> +100."""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 95, "hr": 75, "unconscious": True}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 100
    assert result["status"] == "TRIAGE_STABLE"


def test_spo2_low_branch():
    """Branch: spo2 < 90 True (spo2 = 88, hr = 75) -> +60."""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 88, "hr": 75, "unconscious": False}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 60
    assert result["status"] == "TRIAGE_STABLE"


def test_hr_high_branch():
    """Branch: heart_rate > 120 True (spo2 = 95, hr = 135) -> +60."""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 95, "hr": 135, "unconscious": False}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 60
    assert result["status"] == "TRIAGE_STABLE"


def test_normal_vitals_boundary_values():
    """Boundary test: spo2=90, hr=120 -> neither < 90 nor > 120, gets default score."""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 90, "hr": 120, "unconscious": False}]
        }
    ]
    result = process_triage_wards(wards, 15)
    assert result["acuity_score"] == 15
    assert result["status"] == "TRIAGE_STABLE"


# ===========================================================================
# 4. Return Status Precedence Branches
# ===========================================================================

def test_ward_alert_precedence_over_zero_acuity():
    """Branch: flagged_entries > 4 is True -> returns WARD_ALERT even with 0 acuity."""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 0, "hr": 70, "unconscious": False}] * 5
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "WARD_ALERT"


def test_no_urgent_cases_status():
    """Branch: flagged_entries <= 4 and total_acuity == 0 -> NO_URGENT_CASES."""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": []
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_multiple_wards_combined_flow():
    """Branch: Multi-ward loop with mixed accepting/non-accepting and varied acuities."""
    wards = [
        {
            "is_accepting": False,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 80, "hr": 130, "unconscious": False}]
        },
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": True,
            "patients": [{"spo2": 85, "hr": 70, "unconscious": False}]  # 60 + 25 = 85
        },
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 98, "hr": 72, "unconscious": False}]  # + 10 = 95
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 95
    assert result["status"] == "TRIAGE_STABLE"


# ===========================================================================
# 5. Oxygen Manifold Monitoring Branch Coverage
# ===========================================================================

def test_monitor_oxygen_empty_sensor_streams():
    """Branch: not sensor_streams evaluates True -> NO_DATA."""
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_monitor_oxygen_empty_inner_manifold():
    """Branch: manifold is empty list -> inner loop body skipped."""
    assert monitor_oxygen_manifolds([[], []]) == "PRESSURE_NORMAL"


def test_monitor_oxygen_all_normal_pressures():
    """Branch: pressure_bar < 4.0 evaluates False for all readings."""
    assert monitor_oxygen_manifolds([[4.0, 4.5, 5.0], [4.1, 4.2]]) == "PRESSURE_NORMAL"


def test_monitor_oxygen_single_drop_no_failure():
    """Branch: pressure_bar < 4.0 True, but drop_streak < 2 -> resets on next normal reading."""
    assert monitor_oxygen_manifolds([[3.8, 4.5, 3.9]]) == "PRESSURE_NORMAL"


def test_monitor_oxygen_failure_on_first_manifold():
    """Branch: drop_streak >= 2 evaluates True on first manifold -> PRESSURE_FAILURE."""
    assert monitor_oxygen_manifolds([[3.9, 3.8, 5.0]]) == "PRESSURE_FAILURE"


def test_monitor_oxygen_failure_on_second_manifold():
    """Branch: first manifold normal, second manifold triggers drop_streak >= 2."""
    assert monitor_oxygen_manifolds([[5.0, 4.5], [3.5, 3.2]]) == "PRESSURE_FAILURE"
