# normalization/deterministic_mapper.py

import re
from typing import Dict, List
from .schema import STANDARD_SCHEMA


RULE_PATTERNS = {
    "Revenue from operations": [
        r"revenue from operations",
        r"total revenue",
        r"\brevenue\b"
    ],
    "Other income": [
        r"other income"
    ],
    "Total income": [
        r"total income"
    ],
    "Employee benefits expense": [
        r"employee benefits"
    ],
    "Finance costs": [
        r"finance cost",
        r"interest expense"
    ],
    "Depreciation and amortisation expense": [
        r"depreciation",
        r"amortisation"
    ],
    "Other expenses": [
        r"other expenses"
    ],
    "Total expenses": [
        r"total expenses"
    ],
    "Profit before exceptional items and tax": [
        r"profit before exceptional"
    ],
    "Exceptional items": [
        r"exceptional"
    ],
    "Profit before tax": [
        r"profit before tax"
    ],
    "Tax expense": [
        r"tax expense",
        r"current tax",
        r"deferred tax"
    ],
    "Profit after tax": [
        r"profit for the year",
        r"profit after tax",
        r"profit for the period"
    ],
    "Other comprehensive income": [
        r"other comprehensive income"
    ],
    "Total comprehensive income": [
        r"total comprehensive income"
    ]
}


def deterministic_map(labels: List[str]) -> Dict[str, str]:
    """
    Returns mapping: {original_label: standardized_label}
    Only maps labels that match rule patterns.
    """
    mapping = {}

    for label in labels:
        lower_label = label.lower()

        for standard, patterns in RULE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, lower_label):
                    mapping[label] = standard
                    break
            if label in mapping:
                break

    return mapping
