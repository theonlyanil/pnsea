class Options:
    def __init__(self, session):
        self.session = session

    def fno_stocks_list(self):
        url = "https://www.nseindia.com/api/master-quote"
        return self.session.get(url).json()