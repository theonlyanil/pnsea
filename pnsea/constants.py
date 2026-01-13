# pnsea/constants.py

from typing import Final

class NSEEndpoints:
    # Base URL
    BASE_URL: Final = "https://www.nseindia.com"

    AUTOCOMPLETE = f"{BASE_URL}/api/search/autocomplete?q="

    # DERIVATIVES Endpoints
    # Commodity Derivatives Endpoints
    COMMODITY_OPTIONS_LIST: Final = f"{BASE_URL}/api/quotes-commodity-derivatives-master"

    # Equity Derivatives Endpoints
    EQ_FNO_STOCKS_LIST: Final = f"{BASE_URL}/api/master-quote"
    EQ_EXPIRY_DATES: Final = f"{BASE_URL}/api/option-chain-contract-info"
    EQ_OPTION_CHAIN: Final = f"{BASE_URL}/api/option-chain-v3"

    # Indices Derivatives Endpoints
    INDICES_OPTIONS_LIST: Final = f"{BASE_URL}/api/quote-derivative"
    INDICES_EXPIRY_DATES: Final = f"{BASE_URL}/api/option-chain-contract-info"
    INDICES_OPTION_CHAIN: Final = f"{BASE_URL}/api/option-chain-v3"


    # EQUITY Endpoints
    EQUITY_QUOTE: Final = f"{BASE_URL}/api/quote-equity"
    EQUITY_HISTORY: Final = f"{BASE_URL}/api/historical/cm/equity"
    MARKET_STATUS: Final = f"{BASE_URL}/api/marketStatus"
    ALL_STOCK_DATA: Final = f"{BASE_URL}/api/live-analysis-stocksTraded"
    EQ_PRICE_VOL_DEL_HISTORY: Final = f"{BASE_URL}/api/historicalOR/generateSecurityWiseHistoricalData"

    # EQUITY CORPORATE Endpoints
    INSIDER_DATA: Final = f"{BASE_URL}/api/corporates-pit"
    PLEDGED_DATA: Final = f"{BASE_URL}/api/corporate-pledgedata"
    SAST_DATA: Final = f"{BASE_URL}/api/corporate-sast-reg29"

    # MF Endpoints
    MF_INSIDER_DATA: Final = f"{BASE_URL}/api/corporate-event-disclosure"
