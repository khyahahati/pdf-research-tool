# structuring/dataframe_builder.py

import pandas as pd
from typing import Dict, List, Optional
from normalization.schema import STANDARD_SCHEMA


def build_dataframe(
    normalized_data: Dict[str, Optional[List[float]]],
    headers: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Build structured income statement DataFrame.
    """

    # Determine number of columns from first non-null row
    num_columns = 0
    for values in normalized_data.values():
        if values:
            num_columns = len(values)
            break

    # Build rows
    structured_rows = []

    for line_item in STANDARD_SCHEMA:
        values = normalized_data.get(line_item)

        if values is None:
            row = [None] * num_columns
        else:
            # Adjust if column mismatch
            if len(values) != num_columns:
                values = values[:num_columns] + [None] * (num_columns - len(values))
            row = values

        structured_rows.append(row)

    df = pd.DataFrame(structured_rows, index=STANDARD_SCHEMA)

    # Assign headers if available
    if headers and len(headers) >= num_columns:
        df.columns = headers[:num_columns]
    else:
        df.columns = [f"Period_{i+1}" for i in range(num_columns)]

    df.index.name = "Line Item"

    return df
