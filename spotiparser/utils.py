import re

def clean_number(value: str) -> int:
    """Strip commas and non-digit chars from play count strings"""
    if not value:
        return 0
    cleaned = re.sub(r'[^0-9]', '', value)
    return int(cleaned) if cleaned else 0

