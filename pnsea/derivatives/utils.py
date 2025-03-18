import pandas as pd

# Define the required fields to extract for both CE and PE
required_fields = [
    "openInterest",
    "changeinOpenInterest",
    "impliedVolatility",
    "lastPrice",
    "totalTradedVolume",
    "bidQty",
    "bidprice",
    "askQty",
    "askPrice",
]

# Function to extract required fields from a dictionary column
def extract_option_data(option_series):
    extracted_data = []
    for option_dict in option_series:
        if isinstance(option_dict, dict):
            extracted_data.append({key: option_dict.get(key, None) for key in required_fields})
        else:
            extracted_data.append({key: None for key in required_fields})
    return pd.DataFrame(extracted_data)