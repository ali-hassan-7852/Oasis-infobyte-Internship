"""
strength.py
Scores a generated password as Weak / Medium / Strong based on length
and character diversity. This is a simple heuristic score for display
purposes, not a formal entropy calculation.
"""

import string


def score_password(password: str) -> str:
    length = len(password)

    diversity = 0
    if any(c in string.ascii_uppercase for c in password):
        diversity += 1
    if any(c in string.ascii_lowercase for c in password):
        diversity += 1
    if any(c in string.digits for c in password):
        diversity += 1
    if any(c not in string.ascii_letters + string.digits for c in password):
        diversity += 1

    # Simple weighted heuristic: length matters most, diversity adds on top.
    if length >= 16 and diversity >= 3:
        return "Strong"
    elif length >= 12 and diversity >= 2:
        return "Strong"
    elif length >= 8 and diversity >= 2:
        return "Medium"
    else:
        return "Weak"
