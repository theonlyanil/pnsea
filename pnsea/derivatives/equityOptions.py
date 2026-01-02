import pandas as pd
from .utils import extract_option_data
from ..constants import NSEEndpoints

class EquityOptions:
    def __init__(self, session):
        self.session = session

    def fno_stocks_list(self):
        """Returns a list of FNO stocks from the master quote endpoint."""
        return self.session.get(NSEEndpoints.EQ_FNO_STOCKS_LIST).json()

    """
        ENDPOINT_URL_EXAMPLE = https://www.nseindia.com/option-chain-contract-info?symbol=SBIN"
    """
    def expiry_dates(self, symbol):
        """Returns a list of available expiry dates for a given equity symbol."""
        # Using v3 contract info/expiry endpoint
        params = {"symbol": symbol}
        response = self.session.get(NSEEndpoints.EQ_EXPIRY_DATES, params=params)
        return response.json().get('expiryDates', [])
    
    """
    Fetches the option chain via v3 API with mandatory expiry handling.
    
    Args:
        symbol (str): The equity symbol (e.g., 'RELIANCE').
        expiry_date (str, optional): Expiry date (DD-MMM-YYYY). Uses nearest if None.
        strike_price (float, optional): Specific strike to filter the results.
        
    Returns:
        tuple: (DataFrame of chain, list of all expiry_dates, underlying_value)

    ENDPOINT_URL_EXAMPLE = https://www.nseindia.com/api/option-chain-v3?type=Equity&symbol=RELIANCE&expiry=27-Mar-2025
    """
    def option_chain(self, symbol, expiry_date=None, strike_price=None):
        # 1. Handle Mandatory Expiry Logic
        if not expiry_date:
            all_dates = self.expiry_dates(symbol)
            if not all_dates:
                raise ValueError(f"No expiry dates found for symbol: {symbol}")
            expiry_date = all_dates[0] 

        # 2. Build PARAMS for v3 API
        params = {"type": "Equity", "symbol": symbol, "expiry": expiry_date}

        # 3. Fetch Data
        response = self.session.get(NSEEndpoints.EQ_OPTION_CHAIN, params=params).json()
        
        # 4. Extract Metadata from 'records'
        records = response.get('records', {})
        underlying_value = records.get('underlyingValue', 0)
        all_expiry_dates = records.get('expiryDates', [])

        # 5. Extract Strike Rows from 'filtered'
        filtered_block = response.get('filtered', {})
        raw_rows = filtered_block.get('data', [])

        if not raw_rows:
            return pd.DataFrame(), all_expiry_dates, underlying_value

        # 6. Filter by Strike Price if requested
        if strike_price is not None:
            target = float(strike_price)
            raw_rows = [row for row in raw_rows if float(row.get('strikePrice')) == target]

        df = pd.DataFrame(raw_rows)

        # 7. Extract and Flatten CE/PE
        # Use .apply(pd.Series) or your utility, but handle missing keys safely
        ce_df = extract_option_data(df["CE"] if "CE" in df.columns else pd.Series([None]*len(df)))
        pe_df = extract_option_data(df["PE"] if "PE" in df.columns else pd.Series([None]*len(df)))
        
        ce_df = ce_df.add_prefix("CE_")
        pe_df = pe_df.add_prefix("PE_")

        # 8. Final Concatenation
        df_final = pd.concat([
            df[['strikePrice']].reset_index(drop=True),
            ce_df.reset_index(drop=True),
            pe_df.reset_index(drop=True)
        ], axis=1)

        return df_final, all_expiry_dates, underlying_value