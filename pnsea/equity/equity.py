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
        url = f"{NSEEndpoints.EQUITY_QUOTE}{symbol}"
        response = self.session.get(url)
        return response.json()
    
    """
    Get History for a single stock symbol
    Inputs:
    symbol: str: Symbol of the company (e.g. 'RELIANCE', 'SBIN')
    from_date: str: Start Date in dd-mm-yyyy format
    to_date: str: End Date in dd-mm-yyyy format
    series: str: Series type (default: 'EQ')
    """
    def history(self, symbol, from_date, to_date, series="EQ"):
        url = f"{NSEEndpoints.EQUITY_HISTORY}&symbol={symbol}&series={series}&fromDate={from_date}&toDate={to_date}"
        response = self.session.get(url)
        data = response.json()
        return pd.DataFrame(data if isinstance(data, list) else [])

    """
    Get History for an index (e.g. 'NIFTY 50', 'NIFTY BANK')
    Inputs:
    index_name: str: Name of the index
    from_date: str: Start Date in dd-mm-yyyy format
    to_date: str: End Date in dd-mm-yyyy format
    """
    def index_history(self, index_name, from_date, to_date):
        url = NSEEndpoints.INDEX_HISTORY
        params = {
            "indexType": index_name,
            "from": from_date,
            "to": to_date
        }
        response = self.session.get(url, params=params)
        data = response.json()
        return pd.DataFrame(data.get("data", []))
    
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
    
    def all_indices(self):
        """
        Fetches all NSE indices data.
        Returns a DataFrame with index names, last values, percentage changes, etc.
        """
        res = self.session.get(url=NSEEndpoints.ALL_INDICES)
        data = res.json().get('data', [])
        return pd.DataFrame(data)

    def find_index(self, index_name: str):
        """
        Finds specific index data by name (e.g., 'INDIA VIX', 'NIFTY 50').
        Returns a dictionary of index data.
        """
        df = self.all_indices()
        if df.empty:
            return {}
        
        filtered = df[df['index'] == index_name]
        if not filtered.empty:
            return filtered.iloc[0].to_dict()
        return {}
