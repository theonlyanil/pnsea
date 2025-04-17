"""
NSEPY - NSE Python API

Written by Anil Sardiwal
"""
import pandas as pd

from .nsesession import NSESession
from .equity.equity import Equity
from .equity.insider import Insider
from .derivatives.indicesOptions import IndicesOptions
from .derivatives.equityOptions import EquityOptions
from .derivatives.commodityOptions import CommodityOptions
from .mf.mf import MF

class NSE:
    def __init__(self):
        self.session = NSESession()

        self.equity = Equity(self.session)
        self.insider = Insider(self.session)
        self.options = IndicesOptions(self.session)
        self.equityOptions = EquityOptions(self.session)
        self.commodity_options = CommodityOptions(self.session)
        self.mf = MF(self.session)

    """
    TODO Fix or Move to NSESession
    Get NSESession object data
    """
    def session_info(self):
        """
        Returns a dictionary containing all attributes of the self.session object.
        """
        session_data = {}
        for attr_name in dir(self.session):
            # Avoid including special methods (starting with __) and attributes that might cause errors
            if not attr_name.startswith("__") and not callable(getattr(self.session, attr_name)):
                try:
                    session_data[attr_name] = getattr(self.session, attr_name)
                except Exception as e:
                    print(f"Warning: Could not access attribute '{attr_name}' due to error: {e}")
                    # Optionally handle the error differently, e.g., log it or skip the attribute

        return session_data

    """
    AutoCompletes the query and returns in JSON format
    """
    def autocomplete(self, query):
        url = f"https://www.nseindia.com/api/search/autocomplete?q={query}"
        return self.session.get(url).json()

    """Endpoint Tester"""
    def endpoint_tester(self, endpoint_url):
        res = self.session.get(endpoint_url)
        return res

if __name__ == "__main__":
    nse = NSE()

    """Endpoint Tester"""
    #data = nse.endpoint_tester("https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY").json()['records']['data']
    #df = (pd.DataFrame(data))
    #df.to_csv("h.csv")
    

    """Autocomplete"""
    #print(nse.autocomplete("Info"))