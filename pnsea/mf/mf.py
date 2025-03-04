import pandas as pd
class MF:
    def __init__(self, session):
        self.session = session

    """
    Event Based Disclosure of Mutual Funds
    Tells which employees of the MF have bought or sold the shares of the MF

    URL = https://www.nseindia.com/companies-listing/corporate-filings-EBD

    Parameters:
    symbol: str - Symbol of the Mutual Fund
    from_date: str - Start date of the data to be fetched
    to_date: str - End date of the data to be fetched
    isin: str - ISIN of the Mutual Fund
    """ 
    def mf_insider_data(self, symbol=None, from_date=None, to_date=None, isin=None):
        url = f"https://www.nseindia.com/api/corporate-event-disclosure?index=Ebddata"
        if from_date and to_date:
            url += f"&from_date={from_date}&to_date={to_date}"
        if isin:
            url += f"&isin={isin}"
        if symbol:
            url += f"&symbol={symbol}"

        data = self.session.get(url).json()
        df = pd.DataFrame(data)
        return df