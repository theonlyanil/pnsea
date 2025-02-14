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



if __name__ == "__main__":
    nse = NSE()

    """
    Insider Data
    """
    #print(nse.insider_data("SBIN"))
    print(nse.equity.insider_data("INFY", from_date="11-12-2023", to_date="14-02-2025"))

    """
    Single Company Insider Data
    """
    #print(nse.single_co_insider_data("11-12-2020", "14-02-2025", "SBIN"))

    """
    Pledged Data
    """
    #print(nse.getPledgedData("SBIN"))

    """
    Sast Data
    """
    #print(nse.getSastData("SBIN"))