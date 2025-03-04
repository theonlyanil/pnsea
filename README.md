# PNSEA - Python NSE API

## Overview
PNSEA is a Python library for fetching data from the National Stock Exchange of India (NSE). It provides easy access to stock market data, options chains, insider trading reports, mutual fund data, and more.

## Features
- Fetch real-time equity data (CMP, historical data, market status, etc.).
- Get insider trading reports, pledged data, and SAST data.
- Retrieve option chain data for stocks and indices.
- Fetch mutual fund insider data.
- Autocomplete search queries for NSE symbols.
- Endpoint tester for API debugging.

## Installation
```bash
pip install pnsea
```

## Usage

### Initialize the NSE Instance
```python
from pnsea import NSE

nse = NSE()
```

### Fetch Equity Data
```python
# Get current market price of SBIN
print(nse.equity.info("SBIN")['priceInfo']['lastPrice'])

# Fetch historical data
print(nse.equity.history("SBIN", "01-02-2025", "14-02-2025"))
```

### Fetch Insider Trading Data
```python
# Get general insider trading data
print(nse.insider.insider_data())

# Get insider trading data for a specific company
print(nse.insider.insider_data("SBIN"))
```

### Fetch Option Chain Data
```python
# Get option chain for NIFTY
print(nse.options.option_chain("NIFTY"))

# Filter option chain by expiry date
print(nse.options.option_chain("NIFTY", expiry_date="06-Mar-2025"))

# Filter option chain by strike price
print(nse.options.option_chain("NIFTY", strike_price=22000))
```

### Fetch Mutual Fund Data
```python
# Get mutual fund insider data
print(nse.mf.mf_insider_data(from_date="01-01-2024", to_date="01-02-2025"))
```


### Autocomplete Search
```python
# Search for NSE symbols
print(nse.autocomplete("Info"))
```

## Author
Written by Anil Sardiwal

## License
MIT License