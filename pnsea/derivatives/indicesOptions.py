# pnsea/derivatives/indicesOptions.py
import pandas as pd
from .utils import extract_option_data

from ..constants import NSEEndpoints

class IndicesOptions:
    def __init__(self, session):
        self.session = session

    def get_indices(self):
        url = f"{NSEEndpoints.INDICES_OPTIONS_LIST}?symbol=NIFTY"
        data = self.session.get(url).json()['allSymbol']
        return data
    
    def expiry_dates(self, symbol):
        url = f"{NSEEndpoints.INDICES_EXPIRY_DATES}?symbol={symbol}"
        return self.session.get(url).json()['expiryDates']
    
    def option_chain(self, symbol, expiry_date=None, strike_price=None):
        """
        Fetches option chain via v3 API. 
        Pulls metadata from 'records' and actual strike rows from 'filtered'.
        """
        # 1. Handle Default Expiry
        if not expiry_date:
            all_dates = self.expiry_dates(symbol)
            if not all_dates:
                raise ValueError(f"Could not fetch expiry dates for {symbol}")
            expiry_date = all_dates[0]

        # 2. Call the v3 API
        url = f"{NSEEndpoints.INDICES_OPTION_CHAIN}?type=Indices&symbol={symbol}&expiry={expiry_date}"
        response = self.session.get(url).json()
        
        # 3. Path Extraction - EXACTLY as per your full JSON
        # Metadata is in 'records'
        records_meta = response.get('records', {})
        underlying_value = records_meta.get('underlyingValue', 0)
        all_expiry_dates = records_meta.get('expiryDates', [])

        # Actual strike rows are in 'filtered' -> 'data'
        filtered_block = response.get('filtered', {})
        raw_rows = filtered_block.get('data', [])

        if not raw_rows:
            return pd.DataFrame(), all_expiry_dates, underlying_value

        # 4. Filter by Strike Price if requested
        # strikePrice IS at the top level of each row in filtered['data']
        if strike_price is not None:
            target = float(strike_price)
            raw_rows = [row for row in raw_rows if float(row.get('strikePrice')) == target]

        df = pd.DataFrame(raw_rows)

        # 5. Extract and Flatten CE/PE
        # We pass the Series of dicts to your extract_option_data utility
        ce_df = extract_option_data(df["CE"]).add_prefix("CE_")
        pe_df = extract_option_data(df["PE"]).add_prefix("PE_")

        # 6. Final Concatenation
        # We keep the top-level strikePrice and join it with the flattened columns
        df_final = pd.concat([
            df[['strikePrice']].reset_index(drop=True),
            ce_df.reset_index(drop=True),
            pe_df.reset_index(drop=True)
        ], axis=1)

        # df_final.to_csv("option_chain_debug.csv", index=False)  # Debugging line


        return df_final, all_expiry_dates, underlying_value