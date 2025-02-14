"""
NSEPY - NSE Python API

Written by Anil Sardiwal
"""

from nsesession import NSESession
from equity.equity import Equity, Insider
from derivatives.options import Options

class NSE:
    def __init__(self):
        self.session = NSESession()

        self.equity = Equity(self.session)
        self.insider = Insider(self.session)
        self.options = Options(self.session)

    
    def autocomplete(self, query):
        url = f"https://www.nseindia.com/api/search/autocomplete?q={query}"
        return self.session.get(url).json()

    def nse_endpoint_tester(self, endpoint_url):
        res = self.session.get(endpoint_url)
        return res.json()


if __name__ == "__main__":
    nse = NSE()

    """Endpoint Tester"""
    print(nse.nse_endpoint_tester("https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050&nometa=true"))

    """Autocomplete"""
    #print(nse.autocomplete("Info"))

    # Equity Examples
    """CMP"""
    #print(nse.equity.info("SBIN"))

    """History"""
    #print(nse.equity.history("SBIN", "01-02-2025", "14-02-2025"))

    """Market Status"""
    #print(nse.equity.market_status())

    """
    Insider Data
    """
    #print(nse.insider.insider_data("SBIN"))
    #print(nse.insider.insider_data("INFY", from_date="11-12-2023", to_date="14-02-2025"))

    """
    Single Company Insider Data
    """
    #print(nse.insider.single_co_insider_data("11-12-2020", "14-02-2025", "SBIN"))

    """
    Pledged Data
    """
    #print(nse.insider.getPledgedData("SBIN"))

    """
    Sast Data
    """
    #print(nse.getSastData("SBIN"))
    #print(nse.insider.getSastData("INFY", from_date="01-01-2024", to_date="01-02-2025"))