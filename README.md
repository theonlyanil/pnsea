PNSEA - Python NSE API (v1.0.0)
===============================

**PNSEA** is a high-performance, stealthy Python library for fetching data from the National Stock Exchange of India (NSE). Powered by **Stealthkit** to bypass rate limits and blocks.

🛠 Usage Reference
------------------

### Initialize

Python

```
from pnsea import NSE
nse = NSE()

```

### 🔍 Discovery & Debugging

Python

```
# Autocomplete search for symbols
print(nse.autocomplete("info"))

# Endpoint Tester (Debug any NSE API URL directly through the stealth session)
url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
print(nse.endpoint_tester(url).json())

```

### 📈 Equity Data

Python

```
# Get CMP (Current Market Price)
print(nse.equity.info("SBIN")['priceInfo']['lastPrice'])

# Get Full Info or specific blocks
print(nse.equity.info("SBIN"))
print(nse.equity.info("SBIN")['info'])

# All Stocks Snapshot & Market Status
print(nse.equity.all_stocks_data())
print(nse.equity.market_status())

# Historical Data (Returns DataFrame)
print(nse.equity.history("ESCORTS", "01-02-2025", "14-02-2025"))

# --- Institutional Tracking (Price & Delivery) ---

# Fetch historical data including Delivery Quantity & %
# Returns: DataFrame with 'COP_DELIV_PERC', 'COP_DELIV_QTY', etc.
df_delivery = nse.equity.delivery_history("RELIANCE", "13-12-2025", "13-01-2026")
df_delivery = nse.equity.delivery_history("RELIANCE", "13-12-2025", "13-01-2026", type="deliverable", series="ALL")
df_delivery = nse.equity.delivery_history("RELIANCE", "13-12-2025", "13-01-2026", type="priceVolume", series="EQ")

# Example: Filter for high institutional accumulation (> 60% delivery)
high_delivery = df_delivery[df_delivery['COP_DELIV_PERC'] > 60]
print(high_delivery[['mTIMESTAMP', 'CH_CLOSING_PRICE', 'COP_DELIV_PERC']])

```

### 🏢 Insider Trading & Corporate Actions

Python

```
# Insider Trading (All or Filtered)
print(nse.insider.insider_data())
print(nse.insider.insider_data("SBIN"))
print(nse.insider.insider_data("INFY", from_date="11-12-2023", to_date="14-02-2025"))

# Pledged Data
print(nse.insider.getPledgedData("ESCORTS"))

# SAST Data
print(nse.insider.getSastData("ESCORTS"))
print(nse.insider.getSastData("INFY", from_date="01-01-2024", to_date="01-02-2025"))

```

### 📉 Indices Options (NIFTY, BANKNIFTY, etc.)

Python

```
# Returns: [0] DataFrame, [1] Expiries List, [2] Underlying Value
print(nse.options.option_chain("NIFTY")[0])

# Filtered Calls
print(nse.options.option_chain("NIFTY", expiry_date="06-Mar-2025")[0])
print(nse.options.option_chain("NIFTY", strike_price=22000)[0])

# Helpers
print(nse.options.expiry_dates("NIFTY"))
print(nse.options.get_indices())

```

### 🏎 Equity Options (Stock FnO)

Python

```
# Get list of all FNO Stocks
print(nse.equityOptions.fno_stocks_list())

# Option Chain for Stocks
print(nse.equityOptions.option_chain("SBIN")[0])
print(nse.equityOptions.option_chain("SBIN", expiry_date="27-Mar-2025", strike_price=800)[0])

# Helpers
print(nse.equityOptions.expiry_dates("SBIN"))

```

### 💰 Mutual Fund Insider Data

Python

```
# Filter by date, ISIN, or Symbol
print(nse.mf.mf_insider_data(from_date="01-02-2025", to_date="02-02-2025"))
print(nse.mf.mf_insider_data(isin="INF879O01027"))
print(nse.mf.mf_insider_data(symbol="PPFAS Mutual Fund"))

```

* * * * *

🛡 Why PNSEA?
-------------

1.  **Human-like Fingerprinting:** Uses `stealthkit` to rotate TLS and headers, preventing `403 Forbidden` errors.

2.  **Analysis Ready:** Complex nested JSON is automatically flattened into Pandas DataFrames.

3.  **v3 API Support:** Uses the most modern NSE endpoints for speed and reliability.