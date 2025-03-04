import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from pnsea import NSE

nse = NSE()
st.title(f"Payoffs")
symbol = st.text_input("Enter Symbol", value="NIFTY")
expiry_date = st.date_input("Select Expiry Date", value=pd.to_datetime("2025-03-06")) #Default date
expiry_date_str = expiry_date.strftime("%d-%b-%Y")

# Load Option Chain Data
data, expiry_dates, cmp = nse.options.option_chain(symbol, expiry_date=expiry_date_str)

# User selects strategy
strategy = st.selectbox("Select an Options Strategy", ["Long Straddle", "Short Straddle", "Bull Call Spread", "Bear Put Spread", "Custom"])

# Find ATM Strike
atm_strike = min(data['strikePrice'], key=lambda x: abs(x - cmp))

# Get closest Call and Put Prices
atm_call_price = data.loc[data['strikePrice'] == atm_strike, 'CE_lastPrice'].values[0]
atm_put_price = data.loc[data['strikePrice'] == atm_strike, 'PE_lastPrice'].values[0]

# Define Payoff Calculation Function
def option_payoff(stock_prices, strike, premium, option_type, position):
    """ Calculate option payoff for given strike, premium, and type. """
    if option_type == "call":
        payoff = np.maximum(stock_prices - strike, 0) - premium
    else:  # put
        payoff = np.maximum(strike - stock_prices, 0) - premium
    
    return payoff if position == "long" else -payoff

# Define price range from ATM - 10 strikes to ATM + 10 strikes
strike_interval = 50  # Assuming strikes are in 50-point intervals
price_range = np.linspace(atm_strike - 10 * strike_interval, 
                          atm_strike + 10 * strike_interval, 
                          100)

# Calculate Payoff for Selected Strategy
if strategy == "Long Straddle":
    payoff = (option_payoff(price_range, atm_strike, atm_call_price, "call", "long") + 
              option_payoff(price_range, atm_strike, atm_put_price, "put", "long"))
    
elif strategy == "Short Straddle":
    payoff = (option_payoff(price_range, atm_strike, atm_call_price, "call", "short") + 
              option_payoff(price_range, atm_strike, atm_put_price, "put", "short"))

elif strategy == "Bull Call Spread":
    higher_strike = atm_strike + 100  # Next available higher strike
    higher_call_price = data.loc[data['strikePrice'] == higher_strike, 'CE_lastPrice'].values[0]
    
    payoff = (option_payoff(price_range, atm_strike, atm_call_price, "call", "long") + 
              option_payoff(price_range, higher_strike, higher_call_price, "call", "short"))

elif strategy == "Bear Put Spread":
    lower_strike = atm_strike - 100  # Next available lower strike
    lower_put_price = data.loc[data['strikePrice'] == lower_strike, 'PE_lastPrice'].values[0]
    
    payoff = (option_payoff(price_range, atm_strike, atm_put_price, "put", "long") + 
              option_payoff(price_range, lower_strike, lower_put_price, "put", "short"))

elif strategy == "Custom":
    strike_1 = st.number_input("Long Strike 1", value=atm_strike, step=50)
    strike_2 = st.number_input("Short Strike 2", value=atm_strike + 100, step=50)
    price_1 = data.loc[data['strikePrice'] == strike_1, 'CE_lastPrice'].values[0]
    price_2 = data.loc[data['strikePrice'] == strike_2, 'CE_lastPrice'].values[0]

    strike_3 = st.number_input("Long Strike 3", value=atm_strike - 100, step=50)
    strike_4 = st.number_input("Short Strike 4", value=atm_strike, step=50)
    price_3 = data.loc[data['strikePrice'] == strike_3, 'PE_lastPrice'].values[0]
    price_4 = data.loc[data['strikePrice'] == strike_4, 'PE_lastPrice'].values[0]
    
    payoff = (option_payoff(price_range, strike_1, price_1, "call", "long") +
              option_payoff(price_range, strike_2, price_2, "call", "short") +
              option_payoff(price_range, strike_3, price_3, "put", "long") +
              option_payoff(price_range, strike_4, price_4, "put", "short"))


# Plot Payoff Graph
fig = go.Figure()
fig.add_trace(go.Scatter(x=price_range, y=payoff, mode='lines', name=strategy, line=dict(color='blue')))

# Add Vertical Line for ATM Strike
fig.add_shape(
    type="line",
    x0=atm_strike, x1=atm_strike,  # Vertical line at ATM strike
    y0=min(payoff), y1=max(payoff),  # Full height of the payoff chart
    line=dict(color="blue", dash="dash"),
)

fig.update_layout(
    title=f"{strategy} Payoff at Expiry",
    xaxis_title="Stock Price at Expiry",
    yaxis_title="Profit / Loss",
    hovermode="x unified",
    xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True, zeroline=True, zerolinewidth=2, zerolinecolor='gray'),
)

st.plotly_chart(fig)
