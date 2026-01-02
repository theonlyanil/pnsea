import pytest
import pandas as pd
from unittest.mock import Mock, patch
from pnsea.mf.mf import MF

class TestMF:
    """Test suite for Mutual Fund (MF) class"""

    @pytest.fixture
    def mock_session(self):
        """Fixture to provide a mocked session object"""
        return Mock()

    @pytest.fixture
    def mf(self, mock_session):
        """Fixture to provide an MF instance with a mocked session"""
        return MF(mock_session)

    def test_mf_insider_data_basic(self, mf, mock_session):
        """Test mf_insider_data with basic index parameter"""
        # Mocking the JSON response you saw in your terminal
        mock_json = [
            {"ebdAppid": 99, "ebdMutualFundName": "SBI Mutual Fund", "ebdDiff": "00:00:05"},
            {"ebdAppid": 544, "ebdMutualFundName": "PPFAS Mutual Fund", "ebdDiff": "00:00:04"}
        ]
        mock_session.get.return_value.json.return_value = mock_json
        
        df = mf.mf_insider_data()
        
        # Verify result is a DataFrame and has the expected rows
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "ebdMutualFundName" in df.columns
        # Verify the session was called with the correct default 'index' param
        mock_session.get.assert_called_once()
        args, kwargs = mock_session.get.call_args
        assert kwargs['params']['index'] == "Ebddata"

    def test_mf_insider_data_with_filters(self, mf, mock_session):
        """Test if filters (dates, isin, symbol) are correctly passed to the API"""
        mock_session.get.return_value.json.return_value = []
        
        mf.mf_insider_data(
            symbol="PPFAS Mutual Fund", 
            from_date="01-02-2025", 
            to_date="02-02-2025",
            isin="INF879O01027"
        )
        
        # Extract the params passed to the mock
        _, kwargs = mock_session.get.call_args
        sent_params = kwargs['params']
        
        # Verify all optional params were mapped correctly
        assert sent_params['symbol'] == "PPFAS Mutual Fund"
        assert sent_params['from_date'] == "01-02-2025"
        assert sent_params['isin'] == "INF879O01027"
        assert sent_params['index'] == "Ebddata"

    def test_mf_insider_data_empty_response(self, mf, mock_session):
        """Test handling of empty or failed responses"""
        # Simulate a 403 or network failure returning None
        mock_session.get.return_value = None
        
        df = mf.mf_insider_data()
        
        # Ensure it returns an empty DataFrame instead of crashing
        assert isinstance(df, pd.DataFrame)
        assert df.empty