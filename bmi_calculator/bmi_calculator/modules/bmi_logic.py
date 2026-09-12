"""
bmi_logic.py
Core BMI calculation, classification, and input validation - kept
separate from the GUI and database layers so it can be tested on its own.
"""


class InputValidationError(ValueError):
    """Raised when weight/height input fails validation, with a
    user-facing message explaining what's wrong."""


CATEGORY_UNDERWEIGHT = "Underweight"
CATEGORY_NORMAL = "Normal"
CATEGORY_OVERWEIGHT = "Overweight"
CATEGORY_OBESE = "Obese"

# Color used for GUI feedback per category.
CATEGORY_COLORS = {
    CATEGORY_UNDERWEIGHT: "#2f7dd1",  # blue
    CATEGORY_NORMAL: "#2fa84f",       # green
    CATEGORY_OVERWEIGHT: "#e0972c",   # orange
    CATEGORY_OBESE: "#d9453c",        # red
}


def parse_and_validate(weight_str: str, height_str: str) -> tuple[float, float]:
    """
    Parse weight (kg) and height (m) from raw string input and validate.
    Raises InputValidationError with a clear message on any problem.
    Returns (weight, height) as floats if valid.
    """
    weight_str = (weight_str or "").strip()
    height_str = (height_str or "").strip()

    if not weight_str or not height_str:
        raise InputValidationError("Please enter both weight and height.")

    try:
        weight = float(weight_str)
    except ValueError:
        raise InputValidationError(f"'{weight_str}' isn't a valid number for weight.")

    try:
        height = float(height_str)
    except ValueError:
        raise InputValidationError(f"'{height_str}' isn't a valid number for height.")

    if weight <= 0:
        raise InputValidationError("Weight must be a positive number.")
    if height <= 0:
        raise InputValidationError("Height must be a positive number.")

    # Sanity bounds to catch obvious mistakes (e.g. entering height in cm).
    if height > 3:
        raise InputValidationError(
            "Height looks too large - enter it in meters (e.g. 1.75), not centimeters."
        )
    if weight > 500:
        raise InputValidationError("Weight looks too large - please check the value (in kg).")

    return weight, height


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """BMI = weight (kg) / height (m) squared, rounded to 2 decimal places."""
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 2)


def classify_bmi(bmi: float) -> str:
    """Classify a BMI value into the standard WHO-style categories."""
    if bmi < 18.5:
        return CATEGORY_UNDERWEIGHT
    elif bmi < 25:
        return CATEGORY_NORMAL
    elif bmi < 30:
        return CATEGORY_OVERWEIGHT
    else:
        return CATEGORY_OBESE
