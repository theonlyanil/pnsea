class EquityOptions:
    def __init__(self, session):
        self.session = session

    def fno_stocks_list(self):
        url = "https://www.nseindia.com/api/master-quote"
        return self.session.get(url).json()
    
    def option_chain(self, symbol):
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        return self.session.get(url).json()
    
class CommodityOptions:
    def __init__(self, session):
        self.session = session

    def commodity_options_list(self):
        url = "https://www.nseindia.com/api/quotes-commodity-derivatives-master"
        return self.session.get(url).json()