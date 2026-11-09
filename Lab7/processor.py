import math


def parse_vitals_summary(vitals_csv):
    """
    Parses a CSV string of patient vitals in format 'HR,SpO2,Temp'.
    Returns a formatted summary string with triage priority ('CRITICAL' or 'STABLE')
    or an informative error string if inputs are malformed or invalid.
    """
    if vitals_csv is None or not isinstance(vitals_csv, str):
        return "Error: Invalid vitals data. Input must be a non-empty string in format 'HR,SpO2,Temp'."

    parts = [p.strip() for p in vitals_csv.split(',')]
    if len(parts) != 3:
        return "Error: Invalid vitals format. Expected 3 comma-separated values 'HR,SpO2,Temp'."

    try:
        hr = float(parts[0])
        spo2 = float(parts[1])
        temp = float(parts[2])
    except (ValueError, TypeError):
        return "Error: Non-numeric vitals values. HR, SpO2, and Temp must be valid numbers."

    if any(math.isnan(val) or math.isinf(val) for val in (hr, spo2, temp)):
        return "Error: Vitals values cannot be NaN or Infinite."

    if not (0 < hr <= 300):
        return f"Error: Heart rate {hr} is out of physiological range (1-300 bpm)."

    if not (0.0 <= spo2 <= 100.0):
        return f"Error: SpO2 {spo2}% is out of valid range (0-100%)."

    if not (20.0 <= temp <= 50.0):
        return f"Error: Body temperature {temp}°C is out of physiological range (20-50°C)."

    critical = hr > 120 or spo2 < 90 or temp > 39.0
    return f"Vitals: HR={hr}, SpO2={spo2}% - {'CRITICAL' if critical else 'STABLE'}"


def compute_patient_bmi(bmi_string):
    """
    Computes BMI from a string in format 'weight/height' (e.g., '70/1.75').
    Returns the rounded BMI value (2 decimal places) or an informative error string.
    """
    if bmi_string is None or not isinstance(bmi_string, str):
        return "Error: Invalid BMI data. Input must be a string in format 'weight/height'."

    parts = [p.strip() for p in bmi_string.split('/')]
    if len(parts) != 2:
        return "Error: Invalid BMI format. Expected 'weight/height' (e.g. '70/1.75')."

    try:
        weight = float(parts[0])
        height = float(parts[1])
    except (ValueError, TypeError):
        return "Error: Non-numeric BMI values. Weight and height must be valid numbers."

    if math.isnan(weight) or math.isinf(weight) or math.isnan(height) or math.isinf(height):
        return "Error: Weight and height cannot be NaN or Infinite."

    if weight <= 0 or height <= 0:
        return "Error: Weight and height must be strictly positive numbers."

    if height > 3.0 or weight > 1000.0:
        return "Error: Weight or height is outside plausible human measurements."

    try:
        bmi = weight / (height ** 2)
        if math.isnan(bmi) or math.isinf(bmi):
            return "Error: Computed BMI is invalid."
        return round(bmi, 2)
    except (ZeroDivisionError, OverflowError):
        return "Error: Math error in BMI calculation."


def assign_ward_bed(allocation_code):
    """
    Assigns a ward and bed number based on allocation code 'WARD-BED' (e.g. 'ICU-05').
    Returns formatted assignment string or an informative error string.
    """
    if allocation_code is None or not isinstance(allocation_code, str):
        return "Error: Invalid allocation code. Input must be a string in format 'WARD-BED'."

    parts = [p.strip() for p in allocation_code.strip().split('-')]
    if len(parts) != 2:
        return "Error: Invalid allocation code format. Expected 'WARD-BED' (e.g. 'ICU-05')."

    ward, bed_str = parts[0].upper(), parts[1]

    ward_names = {
        "ER": "Emergency Room",
        "ICU": "Intensive Care Unit",
        "GEN": "General Ward",
        "PED": "Pediatrics"
    }

    if ward not in ward_names:
        valid_wards = ", ".join(ward_names.keys())
        return f"Error: Unknown ward code '{ward}'. Valid wards are: {valid_wards}."

    try:
        bed_num = int(bed_str)
    except (ValueError, TypeError):
        return "Error: Invalid bed number. Bed number must be an integer."

    if bed_num <= 0:
        return "Error: Bed number must be a positive integer."

    return f"{ward_names[ward]} Bed #{bed_num}"


def main():
    print("==== Running parse_vitals_summary ====")
    v_input = input("Enter vitals (HR,SpO2,Temp): ")
    print("Summary:", parse_vitals_summary(v_input))

    print("\n==== Running compute_patient_bmi ====")
    b_input = input("Enter weight/height (e.g. 70/1.75): ")
    print("BMI:", compute_patient_bmi(b_input))

    print("\n==== Running assign_ward_bed ====")
    w_input = input("Enter allocation (e.g. ICU-05): ")
    print("Assignment:", assign_ward_bed(w_input))


if __name__ == "__main__":
    main()
