# normalization/llm_mapper.py

import os
import json
from typing import Dict, List
from .schema import STANDARD_SCHEMA

try:
    import google.generativeai as genai
except ImportError:
    genai = None


def llm_map(labels: List[str]) -> Dict[str, str]:
    """
    Uses Gemini to map unresolved labels to STANDARD_SCHEMA.
    Returns mapping {original_label: standardized_label}
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or genai is None or not labels:
        return {}

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
You are a financial statement normalization assistant.

Map each input line item to EXACTLY ONE of the following standard schema items.

Standard schema:
{STANDARD_SCHEMA}

Rules:
- Only choose from the schema list.
- Do not invent new categories.
- If no reasonable match exists, return null.
- Return output strictly as a JSON dictionary.
- Do not include explanations.
- Output ONLY valid JSON.

Input labels:
{labels}
"""

        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0,
                "top_p": 1,
                "max_output_tokens": 2048
            }
        )

        text_output = response.text.strip()

        print("=== GEMINI RAW OUTPUT ===")
        print(text_output)
        print("=========================")

        # Remove markdown fences if present
        text_output = text_output.replace("```json", "").replace("```", "").strip()

        # Extract JSON safely
        import re
        json_match = re.search(r"\{.*\}", text_output, re.DOTALL)

        if not json_match:
            return {}

        parsed = json.loads(json_match.group())

        # Validate only allowed schema outputs
        clean_mapping = {}
        for original, mapped in parsed.items():
            if mapped in STANDARD_SCHEMA:
                clean_mapping[original] = mapped

        return clean_mapping

    except Exception as e:
        print("LLM parsing error:", e)
        return {}
