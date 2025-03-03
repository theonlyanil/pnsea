class EquityOptions:
    def __init__(self, session):
        self.session = session

    def fno_stocks_list(self):
        url = "https://www.nseindia.com/api/master-quote"
        return self.session.get(url).json()
    
    def option_chain_raw(self, symbol):
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        return self.session.get(url).json()

    def option_chain(self, symbol, strike=None):
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        data = self.session.get(url).json()
        if strike:
            return data['records']['data'][strike]
        return data['records']['data']

    def chain_by_expiry(self, symbol, expiry_date):
        """Filter options data for a specific expiry date."""
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        data = self.session.get(url).json()['records']['data']
        return [entry for entry in data if entry.get('expiryDate') == expiry_date]

    def chain_by_strike(self, symbol, strike_price):
        """Filter options data for a specific strike price."""
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        data = self.session.get(url).json()['records']['data']
        return [entry for entry in data if entry.get('strikePrice') == strike_price]

    
class CommodityOptions:
    def __init__(self, session):
        self.session = session

    def commodity_options_list(self):
        url = "https://www.nseindia.com/api/quotes-commodity-derivatives-master"
        return self.session.get(url).json()