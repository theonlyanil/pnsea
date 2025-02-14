class Equity:
    def __init__(self, session):
        self.session = session

    def info(self, symbol):
        url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        response = self.session.get(url)
        return response.json()
    
    def history(self, symbol, from_date, to_date):
        url = f"https://www.nseindia.com/api/historical/cm/equity?symbol={symbol}"
        params = dict()
        params['from'] = from_date
        params['to'] = to_date

        res = self.session.get(url, params=params)
        return res.json()
    
    def market_status(self):
        res = self.session.get("https://www.nseindia.com/api/marketStatus")
        return res.json()
        
    
    
class Insider:
    def __init__(self, session):
        self.session = session

    """
    Get Insider Data for a single company

    Input: 
    symbol: str: Symbol of the company

    """
    def insider_data(self, symbol, from_date=None, to_date=None):
        url = f"https://www.nseindia.com/api/corporates-pit?index=equities&symbol={symbol}"
        params = dict()
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date

        response = self.session.get(url, params=params)

        return response.json()
    
    """
    Get Insider Data for a single company
    
    Input: 
    symbol: str: Symbol of the company
    
    """
    def insider_data(self, symbol, from_date=None, to_date=None):
        url = f"https://www.nseindia.com/api/corporates-pit?index=equities&symbol={symbol}"
        params = dict()
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date

        response = self.session.get(url, params=params)

        return response.json()
    
    """
    Get Insider Data for a single company

    Input:
    start_date: str: Start Date in dd-mm-yyyy format
    end_date: str: End Date in dd-mm-yyyy format
    symbol: str: Symbol of the company

    """
    def single_co_insider_data(self, start_date, end_date, symbol):
        params = dict()
        params["symbol"] = symbol
        params["from_date"] = start_date
        params["to_date"] = end_date
        url = 'https://www.nseindia.com/api/corporates-pit?index=equities'
        response = self.session.get(url, params=params)
        return response.json()
    
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