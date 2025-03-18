import pandas as pd
from .utils import extract_option_data

class EquityOptions:
    def __init__(self, session):
        self.session = session

    def fno_stocks_list(self):
        # Returns a list of FNO stocks
        url = "https://www.nseindia.com/api/master-quote"
        return self.session.get(url).json()
    
    def expiry_dates(self, symbol):
        # Returns a list of expiry dates for a given symbol
        url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}"
        return self.session.get(url).json()['records']['expiryDates']
    
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
        url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}"
        records = self.session.get(url).json()['records']
        data = records['data']

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

        # Expiry Dates
        expiry_dates = records['expiryDates']

        # Underlying Value
        underlying_value = records['underlyingValue']
        # Return the final DataFrame
        return df_final, expiry_dates, underlying_value
