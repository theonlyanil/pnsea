import pandas as pd
from ..constants import NSEEndpoints

class MF:
    def __init__(self, session):
        self.session = session

    """
    Event Based Disclosure of Mutual Funds
    Tells which employees of the MF have bought or sold the shares of the MF

    URL = https://www.nseindia.com/companies-listing/corporate-filings-EBD

    Parameters:
    symbol: str - Symbol of the Mutual Fund
    from_date: str - Start date of the data to be fetched (DD-MM-YYYY)
    to_date: str - End date of the data to be fetched (DD-MM-YYYY)
    isin: str - ISIN of the Mutual Fund
    """ 
    def mf_insider_data(self, symbol=None, from_date=None, to_date=None, isin=None):
        # 1. Define the mandatory parameters
        params = {"index": "Ebddata"}

        # 2. Map optional arguments to their API keys
        # This approach is much cleaner than multiple if/url += statements
        optional_params = {
            "from_date": from_date,
            "to_date": to_date,
            "isin": isin,
            "symbol": symbol
        }

        # 3. Update the dict only if the value is provided (not None)
        params.update({k: v for k, v in optional_params.items() if v is not None})

        # 4. Use the session's 'params' argument to handle URL encoding safely
        response = self.session.get(NSEEndpoints.MF_INSIDER_DATA, params=params)
        
        # 5. Handle potential errors and return DataFrame
        if response:
            data = response.json()
            # If the API returns a list under a specific key, check for it.
            # Usually, NSE returns data in a 'data' key or as a direct list.
            return pd.DataFrame(data.get('data', data) if isinstance(data, dict) else data)
            
        return pd.DataFrame()