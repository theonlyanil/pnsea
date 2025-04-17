"""
Just a test usage file. Not to be used in production.
"""
import pandas as pd
from nse import NSE

if __name__ == "__main__":
  nse = NSE()
  """Session Data"""
  #print(nse.session_info())

  """Endpoint Tester"""
  #print(nse.endpoint_tester("https://www.nseindia.com/api/historical/foCPV?from=01-02-2025&to=15-02-2025&instrumentType=OPTIDX&symbol=NIFTY&year=2025&expiryDate=20-Feb-2025&optionType=CE").json())
  #print(nse.endpoint_tester("https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY").json())

  """Autocomplete"""
  #print(nse.autocomplete("info"))

  # Equity Examples
  """INFO"""
  #print(nse.equity.info("SBIN")) #Info
  #print(nse.equity.info("SBIN")['priceInfo']['lastPrice']) # CMP
  #print(nse.equity.info("SBIN")['info']) #Info

  """All Stocks Data"""
  #print(nse.equity.all_stocks_data())
  
  """History"""
  #print(nse.equity.history("ESCORTS", "01-02-2025", "14-02-2025"))

  """Market Status"""
  #print(nse.equity.market_status())

  """
  Insider Data
  """
  #print(nse.insider.insider_data())    #All Insider Data
  #print(nse.insider.insider_data(from_date="11-12-2023", to_date="14-02-2025"))  #All Insider Data with date range
  #print(nse.insider.insider_data("SBIN"))  # Insider Data for a single company
  #print(nse.insider.insider_data("INFY", from_date="11-12-2023", to_date="14-02-2025")) # Insider Data for a single company with date range

  """
  Pledged Data
  """
  #print(nse.insider.getPledgedData("ESCORTS"))  # Pledged Data for a single company

  """
  Sast Data
  """
  #print(nse.insider.getSastData("ESCORTS"))
  #print(nse.insider.getSastData("INFY", from_date="01-01-2024", to_date="01-02-2025"))

  """MF Insider Data"""
  #print(nse.mf.mf_insider_data(from_date="01-02-2025", to_date="02-02-2025"))
  #print(nse.mf.mf_insider_data(isin="INF879O01027"))
  #print(nse.mf.mf_insider_data(symbol="PPFAS Mutual Fund"))

  """ Indices Options"""
  #print(nse.options.option_chain("NIFTY")[0]) #Option Chain - all data
  #print(nse.options.option_chain("NIFTY", expiry_date="06-Mar-2025")[0]) #Option Chain - by expiry date
  #print(nse.options.option_chain("NIFTY", strike_price=22000)[0]) #Option Chain - by strike price
  #print(nse.options.option_chain("NIFTY", expiry_date="06-Mar-2025", strike_price=22000)[0]) #Option Chain - by expiry date & strike price
  #print(nse.options.option_chain("NIFTY")[1]) #Option Chain - All Expiries
  #print(nse.options.option_chain("NIFTY")[2]) #Option Chain - Underlying Value
  #print(nse.options.expiry_dates("NIFTY")) #Expiry Dates
  #option_chain, expiry_dates, underlying_value = nse.options.option_chain("NIFTY")
  #print(nse.options.get_indices()) #Indices List
   
  """ Equity Options """
  #print(nse.equityOptions.fno_stocks_list()) #FNO Stocks List
  #print(nse.equityOptions.option_chain("SBIN")[0]) #Option Chain - all data
  #print(nse.equityOptions.option_chain("SBIN", expiry_date="27-Mar-2025")[0]) #Option Chain - by expiry date
  #print(nse.equityOptions.option_chain("SBIN", strike_price=800)[0]) #Option Chain - by strike price
  #print(nse.equityOptions.option_chain("SBIN", expiry_date="27-Mar-2025", strike_price=800)[0]) #Option Chain - by expiry date & strike price
  #print(nse.equityOptions.option_chain("SBIN")[1]) #Option Chain - All Expiries
  #print(nse.equityOptions.option_chain("SBIN")[2]) #Option Chain - Underlying Value
  #print(nse.equityOptions.expiry_dates("SBIN")) #Expiry Dates
  #option_chain, expiry_dates, underlying_value = nse.equityOptions.option_chain("SBIN")

  """ Commodity Options """
  #print(nse.commodity_options.commodity_options_list()) # Not in usage