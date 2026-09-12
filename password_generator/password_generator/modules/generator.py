"""
generator.py
Core password generation logic - kept separate from the GUI so it can be
tested and reasoned about on its own.

Uses `secrets` (not `random`) because `random` is not cryptographically
secure - it's predictable enough to be a security risk for anything like
passwords, tokens, or keys. `secrets` is built for exactly this purpose.
"""

import secrets
import string

UPPERCASE = string.ascii_uppercase
LOWERCASE = string.ascii_lowercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/"

# Characters that are easy to misread, especially in some fonts:
# capital O vs zero, lowercase l vs capital I vs digit 1, etc.
AMBIGUOUS = "0O1lI"


class PasswordGenerationError(ValueError):
    """Raised when the requested criteria can't produce a valid password."""


def validate_criteria(length: int, use_upper: bool, use_lower: bool,
                       use_digits: bool, use_symbols: bool) -> None:
    """Raises PasswordGenerationError with a clear message if criteria are invalid."""
    if length < 8:
        raise PasswordGenerationError("Password length must be at least 8 characters.")

    selected_count = sum([use_upper, use_lower, use_digits, use_symbols])
    if selected_count < 2:
        raise PasswordGenerationError(
            "Select at least 2 character types (uppercase, lowercase, "
            "numbers, symbols)."
        )

    if length < selected_count:
        raise PasswordGenerationError(
            f"Length must be at least {selected_count} to include one "
            f"character from each selected type."
        )


def _build_pool(use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous):
    """Build the character pool for each selected type, filtering ambiguous chars."""
    pools = {}
    if use_upper:
        pools["upper"] = UPPERCASE
    if use_lower:
        pools["lower"] = LOWERCASE
    if use_digits:
        pools["digits"] = DIGITS
    if use_symbols:
        pools["symbols"] = SYMBOLS

    if exclude_ambiguous:
        for key, chars in pools.items():
            filtered = "".join(c for c in chars if c not in AMBIGUOUS)
            # Only apply the filter if it leaves at least one character -
            # symbols/digits could theoretically be wiped out otherwise.
            pools[key] = filtered if filtered else chars

    return pools


def generate_password(length: int, use_upper: bool, use_lower: bool,
                       use_digits: bool, use_symbols: bool,
                       exclude_ambiguous: bool = False) -> str:
    """
    Generate a cryptographically secure password matching the given
    criteria. Guarantees at least one character from each selected type.
    """
    validate_criteria(length, use_upper, use_lower, use_digits, use_symbols)
    pools = _build_pool(use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous)

    # Guarantee at least one char from each selected type first.
    required_chars = [secrets.choice(chars) for chars in pools.values()]

    # Fill the remaining length from the combined pool of all selected types.
    combined_pool = "".join(pools.values())
    remaining_length = length - len(required_chars)
    remaining_chars = [secrets.choice(combined_pool) for _ in range(remaining_length)]

    all_chars = required_chars + remaining_chars

    # Shuffle securely so the guaranteed characters aren't always at the front.
    # secrets doesn't have a shuffle function, so we use SystemRandom, which
    # is backed by the same OS-level entropy source as secrets itself.
    secrets.SystemRandom().shuffle(all_chars)

    return "".join(all_chars)
