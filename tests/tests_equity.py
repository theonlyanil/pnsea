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
        mock_session.get.return_value.json.return_value = {"symbol": "SBIN", "price": 800}
        
        result = equity.info("SBIN")
        
        assert result["symbol"] == "SBIN"
        # We check if 'symbol=SBIN' was in the URL or params
        args, kwargs = mock_session.get.call_args
        assert "symbol=SBIN" in args[0] or kwargs.get('params', {}).get('symbol') == "SBIN"

    def test_history_dataframe_structure(self, equity, mock_session):
        """Verify history correctly parses nested JSON into a DataFrame"""
        mock_data = {
            "data": [{
                "CH_TIMESTAMP": "2025-01-01",
                "CH_CLOSING_PRICE": 100,
                "VWAP": 100.5,
                "CH_OPENING_PRICE": 99
                # Other keys omitted for brevity as .get() handles them
            }]
        }
        mock_session.get.return_value.json.return_value = mock_data
        
        df = equity.history("SBIN", "01-01-2025", "02-01-2025")
        
        assert isinstance(df, pd.DataFrame)
        assert df.iloc[0]["CH_CLOSING_PRICE"] == 100
        assert "CH_TOTAL_TRADES" in df.columns # Should exist as None due to list comprehension

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