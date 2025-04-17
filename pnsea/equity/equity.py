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

        data = self.session.get(url, params=params).json()

        # Extract relevant columns
        columns = [
            "CH_TIMESTAMP", "CH_TRADE_HIGH_PRICE", "CH_TRADE_LOW_PRICE", "CH_OPENING_PRICE",
            "CH_CLOSING_PRICE", "CH_LAST_TRADED_PRICE", "CH_PREVIOUS_CLS_PRICE",
            "CH_TOT_TRADED_QTY", "CH_TOT_TRADED_VAL", "CH_52WEEK_HIGH_PRICE",
            "CH_52WEEK_LOW_PRICE", "CH_TOTAL_TRADES", "VWAP"
        ]

        # Create DataFrame
        df = pd.DataFrame([{col: entry.get(col, None) for col in columns} for entry in data["data"]])
        return df
    
    """Get Market Status"""
    def market_status(self):
        res = self.session.get("https://www.nseindia.com/api/marketStatus")
        return res.json()
    
    
    def all_stock_data(self):
        res = self.session.get(url = "https://www.nseindia.com/api/live-analysis-stocksTraded")
        data = res.json()['total']['data']
        return data
