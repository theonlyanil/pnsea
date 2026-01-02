import pytest
import pandas as pd
from unittest.mock import Mock, patch
from pnsea.derivatives.indicesOptions import IndicesOptions
from pnsea.derivatives.equityOptions import EquityOptions

class TestIndicesOptions:
    @pytest.fixture
    def mock_session(self):
        return Mock()

    @pytest.fixture
    def indices(self, mock_session):
        return IndicesOptions(mock_session)

    def test_get_indices(self, indices, mock_session):
        """Verify extraction of index symbol list"""
        mock_session.get.return_value.json.return_value = {
            'allSymbol': ['NIFTY', 'BANKNIFTY', 'FINNIFTY']
        }
        result = indices.get_indices()
        assert 'NIFTY' in result
        assert len(result) == 3

    def test_expiry_dates(self, indices, mock_session):
        """Verify extraction of expiry dates list"""
        mock_session.get.return_value.json.return_value = {
            'expiryDates': ['09-Jan-2026', '16-Jan-2026']
        }
        result = indices.expiry_dates("NIFTY")
        assert result[0] == '09-Jan-2026'

    @patch('pnsea.derivatives.indicesOptions.extract_option_data')
    def test_option_chain_v3_parsing(self, mock_extract, indices, mock_session):
        """Tests the complex v3 path: records for meta, filtered for data"""
        # Mocking the extract utility to return simple DataFrames
        mock_extract.side_effect = [
            pd.DataFrame({'lastPrice': [100]}), # CE
            pd.DataFrame({'lastPrice': [50]})   # PE
        ]
        
        # Mock the v3 API response
        mock_session.get.return_value.json.return_value = {
            'records': {
                'underlyingValue': 24000.50,
                'expiryDates': ['09-Jan-2026']
            },
            'filtered': {
                'data': [{
                    'strikePrice': 24000,
                    'CE': {'lastPrice': 100},
                    'PE': {'lastPrice': 50}
                }]
            }
        }
        
        # Call with explicit expiry to skip the internal expiry_dates call
        df, expiries, underlying = indices.option_chain("NIFTY", expiry_date="09-Jan-2026")
        
        assert isinstance(df, pd.DataFrame)
        assert underlying == 24000.50
        assert "CE_lastPrice" in df.columns
        assert df.iloc[0]['strikePrice'] == 24000

class TestEquityOptions:
    @pytest.fixture
    def mock_session(self):
        return Mock()

    @pytest.fixture
    def equity_opt(self, mock_session):
        return EquityOptions(mock_session)

    def test_fno_stocks_list(self, equity_opt, mock_session):
        mock_session.get.return_value.json.return_value = ["SBIN", "RELIANCE"]
        result = equity_opt.fno_stocks_list()
        assert "SBIN" in result

    @patch('pnsea.derivatives.equityOptions.extract_option_data')
    def test_equity_option_chain_filtering(self, mock_extract, equity_opt, mock_session):
        """Verify filtering by strike price and flattening"""
        mock_extract.side_effect = [
            pd.DataFrame({'ltp': [10]}), # PE
            pd.DataFrame({'ltp': [20]})  # CE
        ]
        
        mock_session.get.return_value.json.return_value = {
            'records': {
                'underlyingValue': 800,
                'expiryDates': ['27-Mar-2025'],
                'data': [
                    {'strikePrice': 800, 'expiryDate': '27-Mar-2025', 'CE': {}, 'PE': {}},
                    {'strikePrice': 810, 'expiryDate': '27-Mar-2025', 'CE': {}, 'PE': {}}
                ]
            }
        }
        
        # Test strike price filtering
        df, _, _ = equity_opt.option_chain("SBIN", strike_price=800)
        
        assert len(df) == 1
        assert "CE_ltp" in df.columns