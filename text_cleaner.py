"""
text_cleaner.py
Module 2: Text Extraction and Cleaning
- Convert text to lowercase for comparison
- Remove unnecessary symbols and repeated spaces
- Keep important technical symbols such as C++, C#, and .NET
"""

import re

# Technical tokens that must survive cleaning even though they contain
# punctuation (e.g. C++ , C#, .NET). We protect them before stripping
# symbols, then restore them afterwards.
PROTECTED_TOKENS = ["c++", "c#", ".net", "node.js", "asp.net"]


def protect_tokens(text: str) -> str:
    """Replace protected tokens with safe placeholders so they survive
    symbol stripping."""
    for i, token in enumerate(PROTECTED_TOKENS):
        placeholder = f"__PROTECTED_{i}__"
        text = text.replace(token, placeholder)
    return text


def restore_tokens(text: str) -> str:
    for i, token in enumerate(PROTECTED_TOKENS):
        placeholder = f"__PROTECTED_{i}__"
        text = text.replace(placeholder, token)
    return text


def clean_text(raw_text: str) -> str:
    """
    Clean raw resume text:
    1. Lowercase everything
    2. Protect technical symbols (C++, C#, .NET)
    3. Remove unwanted punctuation/symbols
    4. Collapse repeated whitespace
    """
    if not raw_text:
        return ""

    text = raw_text.lower()
    text = protect_tokens(text)

    # Remove bullets, special characters, but keep letters, numbers,
    # spaces, and the underscores used by our placeholders.
    text = re.sub(r"[^a-z0-9_\s]", " ", text)

    # Collapse multiple spaces/newlines/tabs into a single space
    text = re.sub(r"\s+", " ", text).strip()

    text = restore_tokens(text)
    return text


if __name__ == "__main__":
    sample = "Skilled in Python, C++, C#, .NET!!  Worked on ML   projects.\n\n• Data Analysis"
    print(clean_text(sample))
