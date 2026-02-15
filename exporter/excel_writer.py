import pandas as pd
from typing import Optional


def export_to_excel(
    df: pd.DataFrame,
    output_path: str,
    currency: Optional[str],
    unit: Optional[str],
    extraction_method: str
):
    """
    Export structured income statement to Excel with metadata sheet.
    """

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:

        # Main income statement
        df.to_excel(writer, sheet_name="Income Statement")

        # Metadata sheet
        metadata = pd.DataFrame({
            "Field": ["Currency", "Unit", "Extraction Method"],
            "Value": [currency, unit, extraction_method]
        })

        metadata.to_excel(writer, sheet_name="Metadata", index=False)
