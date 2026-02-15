# main.py

import os
from extract_income_statement import extract_income_statement
from normalization.normalizer import normalize
from structuring.header_parser import extract_period_headers, detect_currency_and_unit
from structuring.dataframe_builder import build_dataframe
from exporter.excel_writer import export_to_excel


def run_pipeline(pdf_path: str, output_path: str = "output.xlsx"):

    print("Starting pipeline...")
    print("PDF:", pdf_path)

    # 1️⃣ Extraction
    result = extract_income_statement(pdf_path)

    if not result:
        print("❌ Extraction failed.")
        return None

    print("✅ Extraction method:", result.method)

    # 2️⃣ Normalization (Hybrid)
    normalized = normalize(result.data, use_llm=True)

    if not normalized:
        print("❌ Normalization failed.")
        return None

    print("✅ Normalization complete.")

    # 3️⃣ Header + Metadata Parsing
    headers = []
    currency = None
    unit = None

    if result.raw_text:
        headers = extract_period_headers(result.raw_text)
        currency, unit = detect_currency_and_unit(result.raw_text)

    print("Detected Currency:", currency)
    print("Detected Unit:", unit)

    # 4️⃣ DataFrame Build
    df = build_dataframe(normalized, headers)

    print("✅ DataFrame constructed.")
    print(df)

    # 5️⃣ Export to Excel
    try:
        export_to_excel(
            df=df,
            output_path=output_path,
            currency=currency,
            unit=unit,
            extraction_method=result.method
        )
        print(f"✅ Excel exported successfully → {output_path}")
    except Exception as e:
        print("❌ Excel export failed:", e)

    return df


if __name__ == "__main__":
    pdf_path = r"C:\Users\user\Desktop\New folder\input2.pdf"
    run_pipeline(pdf_path, output_path="test_output.xlsx")
