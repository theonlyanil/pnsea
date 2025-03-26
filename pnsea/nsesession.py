from stealthkit import StealthSession

custom_headers = {
    "Referer": "https://www.nseindia.com",
    "Accept": "application/json",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "method": "GET",
    "scheme": "https",
    }

class NSESession(StealthSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_headers(custom_headers)
        self.fetch_cookies("https://www.nseindia.com/companies-listing/corporate-filings-insider-trading")

    def getHeaders(self):
        return self.session.headers