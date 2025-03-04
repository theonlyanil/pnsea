# options.py
import streamlit as st
import pandas as pd
from pnsea import NSE
import plotly.graph_objects as go

nse = NSE()
cmp = nse.equity.info("NIFTY")['priceInfo']['lastPrice']

st.title(f"Options Chain Visualization @ {cmp}")
symbol = st.text_input("Enter Symbol", value="NIFTY")
expiry_date = st.date_input("Select Expiry Date", value=pd.to_datetime("2025-03-06")) #Default date
expiry_date_str = expiry_date.strftime("%d-%b-%Y")

try:
    data = nse.options.option_chain(symbol, expiry_date=expiry_date_str)

    if not data.empty:

        with st.expander("Full Data"):
            st.subheader("Option Chain Data")
            st.dataframe(data)

        # Visualization
        st.subheader("Option Chain Visualization")

        # Create a Plotly figure
        fig = go.Figure()
        # Add Call options (red)
        fig.add_trace(go.Bar(x=data['strikePrice'], y=data['CE_openInterest'], name='Call OI', marker_color='red'))

        # Add Put options (green)
        fig.add_trace(go.Bar(x=data['strikePrice'], y=data['PE_openInterest'], name='Put OI', marker_color='green'))

        # Update layout
        fig.update_layout(
            title=f"NIFTY Option Chain - {expiry_date_str}",
            xaxis_title="Strike Price",
            yaxis_title="OI / LTP",
            legend_title="Options",
            hovermode="x unified"
        )

        st.plotly_chart(fig)

        # Another Visualization (IV vs Strike Price)
        st.subheader("Implied Volatility vs Strike Price")

        fig_iv = go.Figure()
        fig_iv.add_trace(go.Scatter(x=data['strikePrice'], y=data['CE_impliedVolatility'], mode='lines+markers', name='Call IV', line=dict(color='red')))
        fig_iv.add_trace(go.Scatter(x=data['strikePrice'], y=data['PE_impliedVolatility'], mode='lines+markers', name='Put IV', line=dict(color='green')))

        fig_iv.update_layout(
            title=f"NIFTY Implied Volatility - {expiry_date_str}",
            xaxis_title="Strike Price",
            yaxis_title="Implied Volatility",
            legend_title="IV",
            hovermode="x unified"
        )

        st.plotly_chart(fig_iv)

    else:
        st.warning("No data found for the selected expiry date.")

except Exception as e:
    st.error(f"An error occurred: {e}")