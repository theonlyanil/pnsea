# pnsea/equity/equity.py

import pandas as pd
from ..constants import NSEEndpoints

"""Equity Module"""
class Equity:
    def __init__(self, session):
        self.session = session

    """
    Get Info for a single company
    """
    def info(self, symbol):
        url = f"{NSEEndpoints.EQUITY_QUOTE}?symbol={symbol}"
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
        url = f"{NSEEndpoints.EQUITY_HISTORY}?symbol={symbol}"
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
    
    def delivery_history(self, symbol, from_date, to_date, type="priceVolumeDeliverable", series="EQ"):
        """
        Fetches historical price, volume, and delivery data.
        Essential for tracking institutional accumulation.

        INPUT:
        symbol: str : Stock symbol
        from_date: str : Start date in 'dd-mm-yyyy' format
        to_date: str : End date in 'dd-mm-yyyy' format
        type: str : Type of data to fetch (default: 'priceVolumeDeliverable')
        series: str : Series type (default: 'EQ')
        """
        # 1. Standardize the parameters
        params = {
            'from': from_date,
            'to': to_date,
            'symbol': symbol,
            'type': type,
            'series': series
        }

        # 2. Call the endpoint (Clean URL via dictionary params)
        response = self.session.get(NSEEndpoints.EQ_PRICE_VOL_DEL_HISTORY, params=params)
        data = response.json()

        if 'data' not in data or not data['data']:
            return pd.DataFrame()

        # 3. Process into a Professional DataFrame
        df = pd.DataFrame(data['data'])

        # 4. Data Type Cleanup - Convert timestamps to proper datetime objects
        if 'mTIMESTAMP' in df.columns:
            df['mTIMESTAMP'] = pd.to_datetime(df['mTIMESTAMP'], dayfirst=True)
        

        # Ensure delivery percentage is a float for calculations
        if 'COP_DELIV_PERC' in df.columns:
            df['COP_DELIV_PERC'] = pd.to_numeric(df['COP_DELIV_PERC'], errors='coerce')

        # 5. Rename columns for clarity
        mapping = {
            'mTIMESTAMP': 'Date',
            'CH_OPENING_PRICE': 'Open',
            'CH_TRADE_HIGH_PRICE': 'High',
            'CH_TRADE_LOW_PRICE': 'Low',
            'CH_CLOSING_PRICE': 'Close',
            'CH_TOT_TRADED_QTY': 'Volume',
            'COP_DELIV_QTY': 'Delivery_Qty',
            'COP_DELIV_PERC': 'Delivery_Pct',
            'VWAP': 'VWAP'
        }

        df = df[list(mapping.keys())].rename(columns=mapping)

        return df
    
    """Get Market Status"""
    def market_status(self):
        res = self.session.get(url = NSEEndpoints.MARKET_STATUS)
        return res.json()
    
    
    def all_stock_data(self):
        res = self.session.get(url = NSEEndpoints.ALL_STOCK_DATA)
        data = res.json()['total']['data']
        return data
