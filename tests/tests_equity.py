import pytest
import pandas as pd
from unittest.mock import Mock
from pnsea.equity.equity import Equity
from pnsea.equity.insider import Insider

class TestEquity:
    @pytest.fixture
    def mock_session(self):
        return Mock()

    @pytest.fixture
    def equity(self, mock_session):
        return Equity(mock_session)

    def test_info_call(self, equity, mock_session):
        """Verify info uses correct symbol parameter"""
        mock_session.get.return_value.json.return_value = {
            "equityResponse": [{"metaData": {"symbol": "SBIN", "companyName": "State Bank of India"}}]
        }
        
        result = equity.info("SBIN")
        assert result["equityResponse"][0]["metaData"]["symbol"] == "SBIN"

    def test_history_dataframe_structure(self, equity, mock_session):
        """Verify history correctly parses JSON into a DataFrame"""
        mock_data = [
            {
                "chSymbol": "RELIANCE",
                "chOpeningPrice": 1247.6,
                "chClosingPrice": 1240.4,
                "mtimestamp": "22-Sep-2026"
            }
        ]
        mock_session.get.return_value.json.return_value = mock_data
        
        df = equity.history("RELIANCE", "22-08-2026", "22-09-2026")
        
        assert isinstance(df, pd.DataFrame)
        assert df.iloc[0]["chClosingPrice"] == 1240.4

    def test_all_stock_data_parsing(self, equity, mock_session):
        """Verify the nested ['total']['data'] path"""
        mock_response = {"total": {"data": [{"symbol": "TCS"}, {"symbol": "INFY"}]}}
        mock_session.get.return_value.json.return_value = mock_response
        
        data = equity.all_stock_data()
        
        assert len(data) == 2
        assert data[0]["symbol"] == "TCS"


class TestInsider:
    @pytest.fixture
    def mock_session(self):
        return Mock()

    @pytest.fixture
    def insider(self, mock_session):
        return Insider(mock_session)

    def test_insider_data_with_filters(self, insider, mock_session):
        """Verify insider filters are passed in params"""
        mock_session.get.return_value.json.return_value = {"data": []}
        
        insider.insider_data(symbol="SBIN", from_date="01-01-2025", to_date="02-01-2025")
        
        _, kwargs = mock_session.get.call_args
        # This test ensures you are moving toward the dictionary-params pattern
        assert kwargs['params']['from_date'] == "01-01-2025"
        assert kwargs['params']['to_date'] == "02-01-2025"

    def test_insider_error_handling(self, insider, mock_session):
        """Verify that the try-except block returns an error dict on failure"""
        mock_session.get.side_effect = Exception("Connection Timeout")
        
        result = insider.insider_data(symbol="SBIN")
        
        assert "error" in result
        assert result["error"] == "Connection Timeout"

    def test_get_sast_data_parsing(self, insider, mock_session):
        """Verify SAST data conversion to DataFrame"""
        mock_response = {"data": [{"symbol": "SBIN", "reg": "29"}]}
        mock_session.get.return_value.json.return_value = mock_response
        
        df = insider.getSastData("SBIN")
        
        assert isinstance(df, pd.DataFrame)
        assert df.iloc[0]["symbol"] == "SBIN"

    def test_delivery_history_renaming(self, equity, mock_session):
        mock_json = {"data": [{"mTIMESTAMP": "15-Dec-2025", "CH_OPENING_PRICE": 1551.2, "COP_DELIV_PERC": 67.98}]}
        mock_session.get.return_value.json.return_value = mock_json
        
        df = equity.delivery_history("RELIANCE", "13-12-2025", "13-01-2026")
        
        # Assert new column names exist
        assert "Date" in df.columns
        assert "Open" in df.columns
        assert "Delivery_Pct" in df.columns
        
        # Assert old names are gone
        assert "mTIMESTAMP" not in df.columns