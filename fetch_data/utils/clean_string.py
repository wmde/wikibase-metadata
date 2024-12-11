"""Clean String"""

import re


def clean_string(input_str: str) -> str:
    """
    Cleans the input string by normalizing whitespace and adjusting capitalization.
    - Collapses multiple spaces and replaces non-breaking spaces with single spaces.
    - Trims leading and trailing spaces.
    - Converts the string to uppercase if its length is less than 2.
    - Ensures the first character is capitalized while keeping the rest unchanged.
    """

    stripped = re.sub(r"[ ]{2,}|[ ]", r" ", input_str).strip()
    if len(stripped) < 2:
        return stripped.upper()

    first_cap = stripped[0].upper() + stripped[1:]
    return first_cap
