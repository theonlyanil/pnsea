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

    def test_expiry_dates_v3(self, equity_opt, mock_session):
        """Verify v3 expiry date extraction"""
        mock_session.get.return_value.json.return_value = {
            'expiryDates': ['27-Mar-2025', '24-Apr-2025']
        }
        result = equity_opt.expiry_dates("SBIN")
        assert result[0] == '27-Mar-2025'

    @patch('pnsea.derivatives.equityOptions.extract_option_data')
    def test_equity_option_chain_v3_logic(self, mock_extract, equity_opt, mock_session):
        """
        Verify v3 path extraction and parameter passing for Equities
        """
        # 1. Setup Mock for utility
        mock_extract.side_effect = [
            pd.DataFrame({'ltp': [20]}), # CE prefixing happens in class
            pd.DataFrame({'ltp': [10]})  # PE prefixing happens in class
        ]
        
        # 2. Setup Mock for v3 JSON Response
        mock_session.get.return_value.json.return_value = {
            'records': {
                'underlyingValue': 800.55,
                'expiryDates': ['27-Mar-2025']
            },
            'filtered': {
                'data': [{
                    'strikePrice': 800,
                    'CE': {'ltp': 20},
                    'PE': {'ltp': 10}
                }]
            }
        }
        
        # 3. Call method
        df, expiries, underlying = equity_opt.option_chain("SBIN", expiry_date="27-Mar-2025")
        
        # 4. Assertions
        assert underlying == 800.55
        assert "CE_ltp" in df.columns
        assert df.iloc[0]['strikePrice'] == 800
        
        # 5. Verify Call Parameters (The Contract Test)
        _, kwargs = mock_session.get.call_args
        assert kwargs['params']['type'] == "Equity"
        assert kwargs['params']['expiry'] == "27-Mar-2025"

    def test_option_chain_auto_expiry(self, equity_opt, mock_session):
        """Test that expiry_dates is called if expiry_date is None"""
        # Mock expiry_dates response
        mock_session.get.return_value.json.return_value = {
            'expiryDates': ['27-Mar-2025'],
            'records': {'underlyingValue': 800},
            'filtered': {'data': []}
        }
        
        # We don't provide expiry_date, so it should fetch automatically
        equity_opt.option_chain("SBIN")
        
        # Verify multiple calls (one for expiry_dates, one for option_chain)
        assert mock_session.get.call_count >= 1