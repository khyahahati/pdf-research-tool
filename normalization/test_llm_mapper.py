from normalization.llm_mapper import llm_map

test_labels = [
    "Total revenue from operations",
    "Other income",
    "Profit for the period/year",
    "Employee benefits cost",
    "Depreciation expense",
    "Some random line item"
]

mapping = llm_map(test_labels)

print("LLM Mapping Result:")
for k, v in mapping.items():
    print(f"{k}  →  {v}")
