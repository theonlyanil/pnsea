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

class EquityOptions:
    def __init__(self, session):
        self.session = session

    def fno_stocks_list(self):
        # Returns a list of FNO stocks
        url = "https://www.nseindia.com/api/master-quote"
        return self.session.get(url).json()
    
    def option_chain(self, symbol, expiry_date=None, strike_price=None):
        """
        Filters options data for a specific expiry date and/or strike price.

        Args:
            symbol (str): The symbol of the index.
            expiry_date (str, optional): The expiry date to filter by. Defaults to None.
            strike_price (float, optional): The strike price to filter by. Defaults to None.

        Returns:
            list: A list of options data entries that match the filter criteria.
        """
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        data = self.session.get(url).json()['records']['data']

        filtered_data = data

        if expiry_date:
            filtered_data = [entry for entry in filtered_data if entry.get('expiryDate') == expiry_date]

        if strike_price is not None:  # Explicitly check for None
            filtered_data = [entry for entry in filtered_data if entry.get('strikePrice') == strike_price]

        df = pd.DataFrame(filtered_data)

        # Extract data for both PE and CE
        pe_df = extract_option_data(df["PE"])
        ce_df = extract_option_data(df["CE"])

        # Rename columns to avoid confusion
        pe_df.columns = [f"PE_{col}" for col in pe_df.columns]
        ce_df.columns = [f"CE_{col}" for col in ce_df.columns]

        # Combine with the original DataFrame
        df_final = pd.concat([df, pe_df, ce_df], axis=1)

        # Drop the original PE and CE columns (optional)
        df_final = df_final.drop(columns=["PE", "CE"])

        # Return the final DataFrame
        return df_final

    
class CommodityOptions:
    def __init__(self, session):
        self.session = session

    """ CAUTION: Not in use"""
    def commodity_options_list(self):
        url = "https://www.nseindia.com/api/quotes-commodity-derivatives-master"
        #df = pd.DataFrame(self.session.get(url).json())
        #df.to_csv('h.csv')
        return self.session.get(url).json()
    
# Function to extract required fields from a dictionary column
def extract_option_data(option_series):
    extracted_data = []
    for option_dict in option_series:
        if isinstance(option_dict, dict):
            extracted_data.append({key: option_dict.get(key, None) for key in required_fields})
        else:
            extracted_data.append({key: None for key in required_fields})
    return pd.DataFrame(extracted_data)