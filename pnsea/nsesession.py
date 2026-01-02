# pnsea/nsesession.py

from stealthkit import StealthSession

ANY_NSE_URL = "https://www.nseindia.com/market-data/all-upcoming-issues-ipo"

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
        self.fetch_cookies(ANY_NSE_URL)

    def getHeaders(self):
        return self.session.headers
    
    def get_session_details(self):
        return {
            "headers": self.headers,
            "cookies": self.cookies.get_dict(),
            "proxy": self.proxies
        }