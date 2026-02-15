# structuring/header_parser.py

import re
from typing import List, Tuple, Optional


def extract_period_headers(text: str) -> List[str]:
    """
    Extract period headers like 'Quarter ended March 31, 2025'
    """
    headers = []

    for line in text.split("\n"):
        lower = line.lower()

        if "quarter ended" in lower or "year ended" in lower:
            headers.append(line.strip())

    return headers


def detect_currency_and_unit(text: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Detect currency (INR, USD, etc.) and unit (crores, millions, lakhs).
    """

    currency = None
    unit = None

    lower_text = text.lower()

    # Currency detection
    if "₹" in text or "inr" in lower_text or "rs." in lower_text:
        currency = "INR"
    elif "$" in text or "usd" in lower_text:
        currency = "USD"
    elif "€" in text:
        currency = "EUR"

    # Unit detection
    if "crore" in lower_text:
        unit = "crores"
    elif "million" in lower_text:
        unit = "millions"
    elif "lakh" in lower_text:
        unit = "lakhs"

    return currency, unit
