import pandas as pd

"""Insider Class"""
class Insider:
    def __init__(self, session):
        self.session = session

    """
    Get Insider Data for a single company

    Input: 
    symbol: str: Symbol of the company

    """
    def single_co_insider_data(self, symbol, from_date=None, to_date=None):
        url = f"https://www.nseindia.com/api/corporates-pit?index=equities&symbol={symbol}"
        params = dict()
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date

        response = self.session.get(url, params=params)

        return response.json()
    
    """
    Get Insider Data of all companies

    Input:
    start_date: str: Start Date in dd-mm-yyyy format
    end_date: str: End Date in dd-mm-yyyy format
    symbol: str: Symbol of the company

    """
    def insider_data(self, start_date=None, end_date=None):
        params = dict()
        if start_date:
            params["from_date"] = start_date
        if end_date:
            params["to_date"] = end_date
        url = 'https://www.nseindia.com/api/corporates-pit?index=equities'
        data = self.session.get(url, params=params).json()['data']
        df = pd.DataFrame(data)
        return df
    
    """
    Get Pledged Data for a single company
    """
    def getPledgedData(self, symbol):
        url = f"https://www.nseindia.com/api/corporate-pledgedata?index=equities&symbol={symbol}"
        response = self.session.get(url)
        return response.json()
    
    """
    Get Sast Data for a single company
    """
    def getSastData(self, symbol, from_date=None, to_date=None):
        url = "https://www.nseindia.com/api/corporate-sast-reg29"
        params = dict()
        params["index"] = 'equities'
        params["symbol"] = symbol
        if from_date and to_date:
            params["from_date"] = from_date
            params["to_date"] = to_date

        response = self.session.get(url, params=params)
        return response.json()