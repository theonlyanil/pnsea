# pnsea/derivatives/commodityOptions.py
from ..constants import NSEEndpoints

class CommodityOptions:
    def __init__(self, session):
        self.session = session

    """ CAUTION: Not in use"""
    def commodity_options_list(self):
        url = NSEEndpoints.COMMODITY_OPTIONS_LIST
        #df = pd.DataFrame(self.session.get(url).json())
        #df.to_csv('h.csv')
        return self.session.get(url).json()