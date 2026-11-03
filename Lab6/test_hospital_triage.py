import pytest
from hospital_triage_priority import process_triage_wards, monitor_oxygen_manifolds


# ---------------------------------------------------------------------------
# process_triage_wards – existing example test
# ---------------------------------------------------------------------------

def test_single_normal_patient():
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


# ---------------------------------------------------------------------------
# process_triage_wards – input validation
# ---------------------------------------------------------------------------

def test_invalid_wards_not_a_list():
    """wards is not a list → ValueError"""
    with pytest.raises(ValueError):
        process_triage_wards("not_a_list", 10)


def test_invalid_negative_default_acuity():
    """default_acuity_score < 0 → ValueError"""
    with pytest.raises(ValueError):
        process_triage_wards([], -1)


# ---------------------------------------------------------------------------
# process_triage_wards – ward-level branches
# ---------------------------------------------------------------------------

def test_ward_not_accepting_is_skipped():
    """Ward with is_accepting=False must be skipped entirely → NO_URGENT_CASES"""
    wards = [
        {
            "is_accepting": False,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 50, "hr": 200, "unconscious": True}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_empty_wards_list():
    """Empty wards list → acuity 0, NO_URGENT_CASES"""
    result = process_triage_wards([], 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_icu_standby_adds_25():
    """icu_standby=True on an accepting ward adds 25 to total acuity"""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": True,
            "patients": [{"spo2": 98, "hr": 72, "unconscious": False}]
        }
    ]
    result = process_triage_wards(wards, 10)
    # 10 (normal patient) + 25 (icu_standby) = 35
    assert result["acuity_score"] == 35
    assert result["status"] == "TRIAGE_STABLE"


# ---------------------------------------------------------------------------
# process_triage_wards – patient-level branches
# ---------------------------------------------------------------------------

def test_patient_invalid_spo2_flagged():
    """spo2 <= 0 → flagged, patient skipped"""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 0, "hr": 72, "unconscious": False}]
        }
    ]
    result = process_triage_wards(wards, 10)
    # flagged_entries=1, acuity=0 → NO_URGENT_CASES
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_patient_invalid_hr_flagged():
    """hr <= 0 → flagged, patient skipped"""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 98, "hr": 0, "unconscious": False}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_unconscious_non_outpatient_adds_100():
    """Unconscious patient in a non-outpatient ward → +100 and flagged"""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 98, "hr": 72, "unconscious": True}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 100
    assert result["status"] == "TRIAGE_STABLE"


def test_unconscious_outpatient_resets_acuity_and_breaks():
    """Unconscious patient in outpatient ward → resets acuity to 0 and breaks inner loop"""
    wards = [
        {
            "is_accepting": True,
            "tier": "outpatient",
            "icu_standby": False,
            # First patient contributes acuity, second triggers the break
            "patients": [
                {"spo2": 98, "hr": 72, "unconscious": False},
                {"spo2": 98, "hr": 72, "unconscious": True},
                {"spo2": 98, "hr": 72, "unconscious": False},  # must NOT be processed
            ]
        }
    ]
    result = process_triage_wards(wards, 10)
    # acuity resets to 0 on the unconscious outpatient
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_low_spo2_adds_60():
    """spo2 < 90 (and conscious) → +60"""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 85, "hr": 72, "unconscious": False}]
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 60
    assert result["status"] == "TRIAGE_STABLE"


def test_high_hr_adds_60():
    """hr > 120 (and conscious, normal spo2) → +60"""
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


# ---------------------------------------------------------------------------
# process_triage_wards – status outcomes
# ---------------------------------------------------------------------------

def test_ward_alert_when_flagged_entries_exceed_4():
    """More than 4 flagged entries → WARD_ALERT"""
    # 5 patients with spo2=0 each get flagged
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 0, "hr": 72, "unconscious": False}] * 5
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["status"] == "WARD_ALERT"


def test_no_urgent_cases_when_acuity_zero():
    """All patients normal, acuity=0 after processing → NO_URGENT_CASES"""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": []
        }
    ]
    result = process_triage_wards(wards, 0)
    assert result["acuity_score"] == 0
    assert result["status"] == "NO_URGENT_CASES"


def test_multiple_wards_mixed():
    """Multiple accepting wards with mixed patients"""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 98, "hr": 72, "unconscious": False}]  # +10
        },
        {
            "is_accepting": False,
            "tier": "general",
            "icu_standby": True,
            "patients": [{"spo2": 50, "hr": 200, "unconscious": True}]  # skipped
        },
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": True,
            "patients": [{"spo2": 85, "hr": 72, "unconscious": False}]  # +60 +25
        },
    ]
    result = process_triage_wards(wards, 10)
    assert result["acuity_score"] == 10 + 60 + 25
    assert result["status"] == "TRIAGE_STABLE"


def test_ward_alert_takes_priority_over_zero_acuity():
    """WARD_ALERT is returned even when acuity happens to be 0"""
    wards = [
        {
            "is_accepting": True,
            "tier": "general",
            "icu_standby": False,
            "patients": [{"spo2": 0, "hr": 72, "unconscious": False}] * 5
        }
    ]
    result = process_triage_wards(wards, 10)
    assert result["status"] == "WARD_ALERT"


# ---------------------------------------------------------------------------
# monitor_oxygen_manifolds
# ---------------------------------------------------------------------------

def test_no_sensor_streams_returns_no_data():
    """Empty sensor_streams list → NO_DATA"""
    assert monitor_oxygen_manifolds([]) == "NO_DATA"


def test_all_pressures_normal():
    """All pressures >= 4.0 → PRESSURE_NORMAL"""
    assert monitor_oxygen_manifolds([[5.0, 4.5, 6.0], [4.0, 5.5]]) == "PRESSURE_NORMAL"


def test_single_drop_no_failure():
    """One reading below 4.0 resets streak; no consecutive pair → PRESSURE_NORMAL"""
    assert monitor_oxygen_manifolds([[3.9, 4.5, 3.8, 5.0]]) == "PRESSURE_NORMAL"


def test_consecutive_drops_trigger_failure():
    """Two consecutive readings < 4.0 → PRESSURE_FAILURE"""
    assert monitor_oxygen_manifolds([[5.0, 3.5, 3.5, 5.0]]) == "PRESSURE_FAILURE"


def test_failure_in_second_manifold():
    """First manifold OK, second has consecutive drops → PRESSURE_FAILURE"""
    assert monitor_oxygen_manifolds([[5.0, 4.0], [3.9, 3.8]]) == "PRESSURE_FAILURE"


def test_exactly_two_drops_at_start():
    """Failure triggered immediately on first two readings"""
    assert monitor_oxygen_manifolds([[3.0, 2.0, 5.0]]) == "PRESSURE_FAILURE"


def test_drop_streak_resets_on_normal():
    """Drop then normal resets streak; no failure"""
    assert monitor_oxygen_manifolds([[3.9, 4.1, 3.9, 4.1]]) == "PRESSURE_NORMAL"


def test_multiple_manifolds_all_normal():
    """Multiple manifolds, all above threshold → PRESSURE_NORMAL"""
    assert monitor_oxygen_manifolds([[6.0], [5.5], [4.0]]) == "PRESSURE_NORMAL"


def test_empty_manifold_list_items():
    """Manifold with no readings → treated as normal (no pressure readings)"""
    assert monitor_oxygen_manifolds([[], []]) == "PRESSURE_NORMAL"
