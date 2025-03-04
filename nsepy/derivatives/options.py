class EquityOptions:
    def __init__(self, session):
        self.session = session

    def fno_stocks_list(self):
        url = "https://www.nseindia.com/api/master-quote"
        return self.session.get(url).json()
    
    def option_chain(self, symbol, expiry_date=None, strike_price=None):
        """
        Filters options data for a specific expiry date and/or strike price.

        Args:
            symbol (str): The symbol of the index.
            expiry_date (str, optional): The expiry date to filter by. Defaults to None.
            strike_price (float, optional): The strike price to filter by. Defaults to None.

        Returns:
            list: A list of options data entries that match the filter criteria.
        """
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        data = self.session.get(url).json()['records']['data']

        filtered_data = data

        if expiry_date:
            filtered_data = [entry for entry in filtered_data if entry.get('expiryDate') == expiry_date]

        if strike_price is not None:  # Explicitly check for None
            filtered_data = [entry for entry in filtered_data if entry.get('strikePrice') == strike_price]

        return filtered_data

    
class CommodityOptions:
    def __init__(self, session):
        self.session = session

    def commodity_options_list(self):
        url = "https://www.nseindia.com/api/quotes-commodity-derivatives-master"
        return self.session.get(url).json()