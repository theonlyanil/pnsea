"""
This has nothing to do with PNSEA library.
This is a sandbox for testing and playing with Python code.
"""
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

sr = StealthSession()
sr.set_headers(custom_headers)
sr.fetch_cookies("https://www.nseindia.com/companies-listing/corporate-filings-insider-trading")
    

def all_stock_data():
        res = sr.get(url = "https://www.nseindia.com/api/live-analysis-stocksTraded")
        data = res.json()['total']['data']
        return data

if __name__ == "__main__":
        print(all_stock_data())