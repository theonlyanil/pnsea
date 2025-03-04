import pandas as pd
"""Insider Class"""
class Insider:
    def __init__(self, session):
        self.session = session

    def insider_data(self, symbol=None, from_date=None, to_date=None):
        """
        Get Insider Data for a single company or all companies.
        
        Parameters:
        - symbol (str, optional): Symbol of the company. If None, fetches data for all companies.
        - from_date (str, optional): Start Date in dd-mm-yyyy format.
        - to_date (str, optional): End Date in dd-mm-yyyy format.

        Returns:
        - dict or list: JSON response containing insider data.
        """
        
        url = "https://www.nseindia.com/api/corporates-pit?index=equities"
        
        # Append symbol parameter if filtering by a single company
        if symbol:
            url += f"&symbol={symbol}"
        
        params = {}
        if from_date:
            params["from_date"] = from_date
        if to_date:
            params["to_date"] = to_date

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()  # Raise an error for HTTP errors (4xx, 5xx)
            data = response.json()
            
            # Make df out of 'data' key directly if present, else return full response
            df = pd.DataFrame(data.get("data", data))
            
            return df
        
        except Exception as e:
            return {"error": str(e)}

    
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
        df = pd.DataFrame(response.json()['data'])
        return df