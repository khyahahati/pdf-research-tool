# normalization/normalizer.py

from typing import Dict, List, Optional
from .schema import STANDARD_SCHEMA
from .deterministic_mapper import deterministic_map
from .llm_mapper import llm_map


def normalize(
    extracted_data: Dict[str, List[float]],
    use_llm: bool = True
) -> Dict[str, Optional[List[float]]]:
    """
    Returns standardized income statement dictionary
    with all STANDARD_SCHEMA keys present.
    """

    labels = list(extracted_data.keys())

    # Step 1 — Deterministic mapping
    mapping = deterministic_map(labels)

    # Step 2 — Identify unresolved labels
    unresolved = [label for label in labels if label not in mapping]

    # Step 3 — LLM mapping (optional)
    if use_llm and unresolved:
        llm_results = llm_map(unresolved)

        # Only accept valid mappings
        for original, mapped in llm_results.items():
            if mapped in STANDARD_SCHEMA:
                mapping[original] = mapped

    # Step 4 — Build normalized output
    normalized_data = {key: None for key in STANDARD_SCHEMA}

    for original_label, values in extracted_data.items():
        standard_label = mapping.get(original_label)

        if standard_label:
            normalized_data[standard_label] = values

    return normalized_data
