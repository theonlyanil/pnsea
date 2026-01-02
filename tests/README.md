PNSEA Test Suite Documentation
==============================

This directory contains the unit tests for the **PNSEA** (Python NSE API) library. These tests use `pytest` and `unittest.mock` to verify the logic of individual modules without making real network requests to the NSE servers.

Test Structure
--------------

| **File** | **Module Tested** | **Description** |
| --- | --- | --- |
| `tests_mf.py` | `pnsea.mf.mf` | Verifies Mutual Fund insider data and parameter mapping. |
| `test_equity_insider.py` | `pnsea.equity` | Verifies Equity quotes, historical data, and Corporate Insider data. |
| `test_derivatives.py` | `pnsea.derivatives` | Verifies Index/Equity option chains and v3 API path extraction. |

* * * * *

Prerequisites
-------------

Ensure you have the development dependencies installed:

Bash

```
pip install pytest pandas stealthkit

```

* * * * *

Running the Tests
-----------------

### 1\. Local Development Mode (Recommended)

Since the library may be installed in your global site-packages, use `PYTHONPATH=.` to ensure the tests run against your **local changes** rather than the installed version. Run these commands from the project root.

**Run all tests:**

Bash

```
PYTHONPATH=. pytest tests/ -v

```

**Run a specific test file:**

Bash

```
PYTHONPATH=. pytest tests/tests_mf.py -v

```

### 2\. Editable Install Mode

Alternatively, you can install the project in editable mode so that `pytest` always picks up your local directory:

Bash

```
pip install -e .
pytest -v

```

* * * * *

Testing Strategy
----------------

-   **Mocking:** We use `unittest.mock` to simulate `NSESession` responses. This ensures tests are fast, deterministic, and do not trigger NSE rate limits or maintenance blocks.

-   **DataFrames:** Most tests assert that the returned object is a `pandas.DataFrame` and contains expected column headers (e.g., `CE_lastPrice`).

-   **Error Handling:** Tests include scenarios for empty JSON responses and network exceptions to ensure the library fails gracefully with an error dictionary instead of crashing.

* * * * *

Adding New Tests
----------------

When adding a new feature (e.g., a new endpoint in `constants.py`), follow these steps:

1.  Create a mock JSON response mirroring the actual NSE API output.

2.  Use a fixture to provide a mocked session.

3.  Assert that the URL parameters are mapped correctly using `mock_session.get.call_args`.