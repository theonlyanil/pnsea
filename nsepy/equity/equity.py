import pandas as pd
"""Equity Module"""
class Equity:
    def __init__(self, session):
        self.session = session

    """
    Get Info for a single company
    """
    def info(self, symbol):
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        response = self.session.get(url)
        #df = pd.DataFrame(response.json())
        #return df
        return response.json()
    
    """
    Get History for a single company
    Inputs:
    symbol: str: Symbol of the company
    from_date: str: Start Date in dd-mm-yyyy format
    to_date: str: End Date in dd-mm-yyyy format
    """
    def history(self, symbol, from_date, to_date):
        url = f"https://www.nseindia.com/api/historical/cm/equity?symbol={symbol}"
        params = dict()
        params['from'] = from_date
        params['to'] = to_date

        res = self.session.get(url, params=params)
        return res.json()
    
    """Get Market Status"""
    def market_status(self):
        res = self.session.get("https://www.nseindia.com/api/marketStatus")
        return res.json()