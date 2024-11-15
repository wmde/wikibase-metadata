"""Clean String"""

import re


def clean_string(input_str: str) -> str:
    """Clean String"""

    stripped = re.sub(r"[ ]{2,}|[ ]", r" ", input_str).strip()
    if len(stripped) < 2:
        return stripped.upper()

    first_cap = stripped[0].upper() + stripped[1:]
    return first_cap
