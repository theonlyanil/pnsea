# pnsea/nse.py
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

from .constants import NSEEndpoints  # Assuming you named it this

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
    AutoCompletes the query and returns in JSON format
    """
    def autocomplete(self, query: str):
        url = f"{NSEEndpoints.AUTOCOMPLETE}{query}"
        return self.session.get(url).json()

    """TODO: REMOVE IN PRODUCTION -- Endpoint Tester"""
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