from nse import NSE

if __name__ == "__main__":
    nse = NSE()

    """Endpoint Tester"""
    #print(nse.endpoint_tester("https://www.nseindia.com/api/historical/foCPV?from=01-02-2025&to=15-02-2025&instrumentType=OPTIDX&symbol=NIFTY&year=2025&expiryDate=20-Feb-2025&optionType=CE").json())

    """Autocomplete"""
    #print(nse.autocomplete("info"))

    # Equity Examples
    """CMP"""
    #print(nse.equity.info("SBIN"))

    """History"""
    #print(nse.equity.history("SBIN", "01-02-2025", "14-02-2025"))

    """Market Status"""
    #print(nse.equity.market_status())

    """
    Insider Data
    """
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
    #print(nse.options.fno_stocks_list())