"""
NSEPY - NSE Python API

Written by Anil Sardiwal
"""

from nsesession import NSESession
from equity.equity import Equity, Insider
from derivatives.options import Options
from mf.mf import MF

class NSE:
    def __init__(self):
        self.session = NSESession()

        self.equity = Equity(self.session)
        self.insider = Insider(self.session)
        self.options = Options(self.session)
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
    print(nse.endpoint_tester("https://www.nseindia.com/api/historical/foCPV?from=01-02-2025&to=15-02-2025&instrumentType=OPTIDX&symbol=NIFTY&year=2025&expiryDate=20-Feb-2025&optionType=CE").json())


    """Autocomplete"""
    #print(nse.autocomplete("Info"))