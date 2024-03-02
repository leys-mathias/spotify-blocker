"""Helper functions"""

import re

def regexify(value: str) -> re.Pattern:
    """Transforms a string value to a compiled RegEx pattern that matches this
    string when it appears as a standalone word or set of words (ignores capitalization).
    
    Args:
        value (str): Input string value.

    Returns:
        re.Pattern: Compiled RegEx pattern.
    """
    pattern = rf"\b({value})\b"
    compiled_pattern = re.compile(pattern, re.IGNORECASE)
    return compiled_pattern
