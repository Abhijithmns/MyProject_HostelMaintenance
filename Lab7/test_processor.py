import math

from hypothesis import given, settings, strategies as st

from processor import parse_vitals_summary, compute_patient_bmi, assign_ward_bed


# Text is deliberately broad here. It includes whitespace, emoji, control
# characters, commas, and very long-looking numeric strings -- the sort of
# values a form field can receive after copy/paste or a bad integration.
arbitrary_input = st.one_of(
    st.none(),
    st.text(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.lists(st.text(), max_size=4),
)


@settings(max_examples=250)
@given(arbitrary_input)
def test_vitals_parser_returns_a_useful_string_for_messy_input(value):
    """The triage form must not turn malformed input into an exception."""
    result = parse_vitals_summary(value)
    assert isinstance(result, str)
    assert result.startswith(("Vitals:", "Error:"))


@settings(max_examples=250)
@given(arbitrary_input)
def test_bmi_calculator_never_returns_a_non_finite_number(value):
    """A BMI result is either an explanation or a real, finite measurement."""
    result = compute_patient_bmi(value)
    if isinstance(result, str):
        assert result.startswith("Error:")
    else:
        assert isinstance(result, float)
        assert math.isfinite(result)
        assert result > 0


@settings(max_examples=250)
@given(arbitrary_input)
def test_bed_assignment_always_has_a_clear_outcome(value):
    """Bad allocation codes should be rejected instead of being guessed at."""
    result = assign_ward_bed(value)
    assert isinstance(result, str)
    assert result.startswith(("Error:", "Emergency Room Bed #", "Intensive Care Unit Bed #",
                             "General Ward Bed #", "Pediatrics Bed #"))


@given(
    hr=st.floats(min_value=1, max_value=300, allow_nan=False, allow_infinity=False),
    spo2=st.floats(min_value=0, max_value=100, allow_nan=False, allow_infinity=False),
    temp=st.floats(min_value=20, max_value=50, allow_nan=False, allow_infinity=False),
)
def test_valid_vitals_keep_their_triage_decision(hr, spo2, temp):
    """Valid readings have only the two expected outcomes."""
    result = parse_vitals_summary(f"{hr},{spo2},{temp}")
    expected = "CRITICAL" if hr > 120 or spo2 < 90 or temp > 39 else "STABLE"
    assert result.endswith(expected)


def test_blank_fields_and_python_style_bed_numbers_are_rejected():
    """Regression checks for the two issues found while fuzzing."""
    assert parse_vitals_summary("   ").startswith("Error: Invalid vitals data")
    assert compute_patient_bmi("\t").startswith("Error: Invalid BMI data")
    assert assign_ward_bed("ICU-1_0") == "Error: Invalid bed number. Bed number must be an integer."
    assert assign_ward_bed("ICU-05") == "Intensive Care Unit Bed #5"
