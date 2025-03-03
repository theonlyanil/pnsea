"""
NSEPY - NSE Python API

Written by Anil Sardiwal
"""
import pandas as pd

from nsesession import NSESession
from equity.equity import Equity
from equity.insider import Insider
from derivatives.options import EquityOptions, CommodityOptions
from mf.mf import MF

class NSE:
    def __init__(self):
        self.session = NSESession()

        self.equity = Equity(self.session)
        self.insider = Insider(self.session)
        self.options = EquityOptions(self.session)
        self.commodity_options = CommodityOptions(self.session)
        self.mf = MF(self.session)

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
    data = nse.endpoint_tester("https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY").json()['records']['data']
    df = (pd.DataFrame(data))
    df.to_csv("h.csv")
    

    """Autocomplete"""
    #print(nse.autocomplete("Info"))