# nsepy

A Python library for accessing historical data from the National Stock Exchange (NSE) of India.

## Features

*   Fetch historical stock prices.
*   Fetch data for indices.
*   Simple and easy-to-use interface.

## Installation

```bash
pip install nsepy
```

## Usage

```python
import nsepy
import datetime
from nsepy import NSE
from nsepy.utils import flatten_json
import pandas as pd

nse = NSE()

# Get historical data for a stock
start = datetime.datetime(2024, 1, 1)
end = datetime.datetime(2024, 1, 31)
data = nsepy.get_history(symbol="INFY", start=start, end=end)
print(data)

# Get historical data for an index
data = nsepy.get_history(symbol="NIFTY", start=start, end=end, index=True)
print(data)

# Get Company Info
flattened_data = flatten_json(nse.equity.info("SBIN"))
df = pd.DataFrame([flattened_data])
print(df['info_symbol'])

# Get Market Status
print(nse.equity.market_status())

# Get Insider Data
print(nse.insider.insider_data("SBIN"))

# Get Single Company Insider Data
print(nse.insider.single_co_insider_data("11-12-2020", "14-02-2025", "SBIN"))

# Get Pledged Data
print(nse.insider.getPledgedData("SBIN"))

# Get Sast Data
print(nse.insider.getSastData("INFY", from_date="01-01-2024", to_date="01-02-2025"))

# Get MF Insider Data
print(nse.mf.mf_insider_data(isin="INF879O01027"))
```
