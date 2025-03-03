"""
Just a test usage file. Not to be used in production.
"""

from nse import NSE

# Flatten the nested dictionaries
def flatten_json(nested_json, prefix=''):
    flattened = {}
    for key, value in nested_json.items():
        new_key = f"{prefix}{key}" if prefix else key
        if isinstance(value, dict):
            flattened.update(flatten_json(value, new_key + '_'))
        elif isinstance(value, list):
          if len(value)>0 and isinstance(value[0],dict):
            for i, item in enumerate(value):
              for k,v in flatten_json(item, new_key+f'_{i}_').items():
                flattened[k] = v
          else:
            flattened[new_key] = value
        else:
            flattened[new_key] = value
    return flattened

if __name__ == "__main__":
    nse = NSE()

    """Endpoint Tester"""
    #print(nse.endpoint_tester("https://www.nseindia.com/api/historical/foCPV?from=01-02-2025&to=15-02-2025&instrumentType=OPTIDX&symbol=NIFTY&year=2025&expiryDate=20-Feb-2025&optionType=CE").json())

    """Autocomplete"""
    #print(nse.autocomplete("info"))

    # Equity Examples
    """CMP"""
    flattened_data = flatten_json(nse.equity.info("SBIN"))
    import pandas as pd
    df = pd.DataFrame([flattened_data])
    print(df['info_symbol'])

    """History"""
    #print(nse.equity.history("SBIN", "01-02-2025", "14-02-2025"))

    """Market Status"""
    #print(nse.equity.market_status())

    """
    Insider Data
    """
    #print(nse.insider.insider_data())
    #print(nse.insider.insider_data(from_date="11-12-2023", to_date="14-02-2025"))
    #print(nse.insider.insider_data("SBIN"))
    #print(nse.insider.insider_data("INFY", from_date="11-12-2023", to_date="14-02-2025"))

    """
    Single Company Insider Data
    """
    #print(nse.insider.single_co_insider_data("11-12-2020", "14-02-2025", "SBIN"))

    """
    Pledged Data
    """
    #print(nse.insider.getPledgedData("SBIN"))

    """
    Sast Data
    """
    #print(nse.getSastData("SBIN"))
    #print(nse.insider.getSastData("INFY", from_date="01-01-2024", to_date="01-02-2025"))

    """MF Insider Data"""
    #print(nse.mf.mf_insider_data(from_date="01-01-2024", to_date="01-02-2025"))
    #print(nse.mf.mf_insider_data(isin="INF879O01027"))
    #print(nse.mf.mf_insider_data(symbol="PPFAS Mutual Fund"))

    """Options"""
