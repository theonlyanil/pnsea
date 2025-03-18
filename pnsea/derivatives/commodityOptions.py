class CommodityOptions:
    def __init__(self, session):
        self.session = session

    """ CAUTION: Not in use"""
    def commodity_options_list(self):
        url = "https://www.nseindia.com/api/quotes-commodity-derivatives-master"
        #df = pd.DataFrame(self.session.get(url).json())
        #df.to_csv('h.csv')
        return self.session.get(url).json()