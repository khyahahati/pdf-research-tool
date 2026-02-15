import camelot
import re
from pdf2image import convert_from_path
import pytesseract
import warnings
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class ExtractionResult:
    data: Dict[str, List[float]]
    method: str            # "camelot" or "ocr"
    raw_text: Optional[str] = None


# Suppress Camelot warnings (they're noisy but not fatal)
warnings.filterwarnings("ignore")


# ⚠️ SET YOUR TESSERACT PATH HERE
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# -----------------------------
# 1. Clean Numbers
# -----------------------------
def clean_number(value):
    if not value:
        return None

    value = str(value).replace(",", "").strip()

    if re.match(r"\(.*\)", value):
        value = "-" + value.strip("()")

    try:
        return float(value)
    except:
        return None
def clean_line_item(line):
    # Remove leading numbering / roman numerals / symbols
    line = re.sub(r"^[\W\dIVXivx_|().\s]+", "", line)
    return line.strip()



# -----------------------------
# 2. Income Row Detection
# -----------------------------
INCOME_LINE_KEYWORDS = [
    "revenue",
    "income",
    "expense",
    "profit",
    "loss",
    "tax",
    "earnings"
]


def is_income_line(line):
    return any(word in line.lower() for word in INCOME_LINE_KEYWORDS)


# -----------------------------
# 3. Parse Camelot Tables
# -----------------------------
def parse_income_statement(tables):
    data = {}

    for table in tables:
        df = table.df

        for _, row in df.iterrows():
            line_item = str(row[0]).strip()

            if not line_item or line_item.lower() == "particulars":
                continue

            if not is_income_line(line_item):
                continue

            numeric_values = [clean_number(val) for val in row[1:]]

            if any(v is not None for v in numeric_values):
                if line_item not in data:
                    data[line_item] = numeric_values

    return data


# -----------------------------
# 4. OCR Extraction
# -----------------------------
def ocr_extract_text(pdf_path):
    
    pages = convert_from_path(pdf_path)

    full_text = ""

    for page in pages:
        text = pytesseract.image_to_string(page)
        full_text += text + "\n"

    return full_text


# -----------------------------
# 5. Parse OCR Text
# -----------------------------
def parse_ocr_text(text):
    data = {}

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        if not is_income_line(line):
            continue

        parts = line.split()

        numbers = [clean_number(p) for p in parts]
        numbers = [n for n in numbers if n is not None]

        if numbers:
    # Remove leading small number if likely row index
            if len(numbers) > 1 and numbers[0] < 100:
                numbers = numbers[1:]

            cleaned_label = clean_line_item(line)
            data[cleaned_label] = numbers


    return data
# -----------------------------
# 6. Filter Core Income Statement Block
# -----------------------------
def filter_income_statement_block(data_dict):
    keys = list(data_dict.keys())

    start_index = None
    end_index = None

    for i, key in enumerate(keys):
        key_lower = key.lower()

        # Start at first true revenue line
        if "revenue from operations" in key_lower or "(a) revenue" in key_lower:
            if start_index is None:
                start_index = i

        # Stop at total comprehensive income
        if "total comprehensive income" in key_lower:
            end_index = i
            break

    if start_index is not None and end_index is not None:
        filtered_keys = keys[start_index:end_index + 1]
        return {k: data_dict[k] for k in filtered_keys}

    return data_dict


# -----------------------------
# 6. Main Extraction Pipeline
# -----------------------------
def extract_income_statement(pdf_path) -> Optional[ExtractionResult]:

    # Try Camelot first
    try:
        tables = camelot.read_pdf(pdf_path, pages="all", flavor="stream")
    except Exception:
        tables = None

    if tables and tables.n > 0:
        structured_data = parse_income_statement(tables)

        if structured_data:
            return ExtractionResult(
                data=structured_data,
                method="camelot",
                raw_text=None
            )

    # Fallback to OCR
    try:
        text = ocr_extract_text(pdf_path)
    except Exception:
        return None

    if not text:
        return None

    structured_data = parse_ocr_text(text)
    structured_data = filter_income_statement_block(structured_data)

    if not structured_data:
        return None

    return ExtractionResult(
        data=structured_data,
        method="ocr",
        raw_text=text
    )





