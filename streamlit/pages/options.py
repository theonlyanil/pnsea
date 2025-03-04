# options.py
import streamlit as st
import pandas as pd
from pnsea import NSE
import plotly.graph_objects as go

nse = NSE()

st.title(f"Options Chain Visualization")
symbol = st.text_input("Enter Symbol", value="NIFTY")
expiry_date = st.date_input("Select Expiry Date", value=pd.to_datetime("2025-03-06")) #Default date
expiry_date_str = expiry_date.strftime("%d-%b-%Y")
try:
    data, expiry_dates, cmp = nse.options.option_chain(symbol, expiry_date=expiry_date_str)
    st.write(f"Current Market Price: {cmp}")

    if not data.empty:
        with st.expander("Full Data"):
            st.subheader("Option Chain Data")
            st.dataframe(data)

        # Visualization
        st.subheader("Option Chain Visualization")

        strike_prices = sorted(data['strikePrice'])  # Get all available strike prices
        ce_oi = data['CE_openInterest']  # Call Open Interest
        pe_oi = data['PE_openInterest']  # Put Open Interest

        # Find ATM Strike (Closest to CMP)
        atm_strike = min(strike_prices, key=lambda x: abs(x - cmp))

        # Streamlit slider to select the range of strikes
        num_strikes = st.slider("Select number of strikes (centered on ATM)", 2, len(strike_prices), 20, step=2)

        # Determine the filtered range of strikes dynamically
        half_range = num_strikes // 2
        filtered_strikes = [sp for sp in strike_prices if atm_strike - half_range * 50 <= sp <= atm_strike + half_range * 50]

        # Filter data based on selected strikes
        filtered_indices = [i for i, sp in enumerate(strike_prices) if sp in filtered_strikes]

        filtered_data = {
            'strikePrice': [strike_prices[i] for i in filtered_indices],
            'CE_openInterest': [ce_oi[i] for i in filtered_indices],
            'PE_openInterest': [pe_oi[i] for i in filtered_indices]
        }

        st.subheader("PCR")
        data['PCR'] = data['PE_openInterest'].sum() / data['CE_openInterest'].sum()
        st.write(f"PCR: {data['PCR'].mean()}")


        # Create Plotly figure
        fig = go.Figure()

        # Add Call OI (red)
        fig.add_trace(go.Bar(x=filtered_data['strikePrice'], y=filtered_data['CE_openInterest'], name='Call OI', marker_color='red'))

        # Add Put OI (green)
        fig.add_trace(go.Bar(x=filtered_data['strikePrice'], y=filtered_data['PE_openInterest'], name='Put OI', marker_color='green'))

        # Add Vertical Line for ATM Strike
        fig.add_vline(
            x=atm_strike,
            line_dash="dash",
            line_color="blue",
            annotation_text="ATM Strike",
            annotation_position="top"
        )

        # Update Layout
        fig.update_layout(
            title=f"NIFTY Option Chain",
            xaxis_title="Strike Price",
            yaxis_title="Open Interest",
            legend_title="Options",
            hovermode="x unified"
        )

        # Display in Streamlit
        st.plotly_chart(fig)

        # Another Visualization (IV vs Strike Price)
        st.subheader("Implied Volatility Curve")

        # Slider to select number of strikes (centered around the ATM strike)
        num_strikes_iv = st.slider("Select number of strikes (centered on ATM)", 2, len(data['strikePrice']), 30, step=2)

        # Find ATM Strike (closest to CMP)
        atm_strike = min(data['strikePrice'], key=lambda x: abs(x - cmp))

        # Determine the filtered range of strikes dynamically
        half_range = num_strikes_iv // 2
        filtered_strikes_iv = [sp for sp in data['strikePrice'] if atm_strike - half_range * 50 <= sp <= atm_strike + half_range * 50]

        # Filter IV data based on selected strikes
        filtered_ce_iv = [data['CE_impliedVolatility'][i] for i, sp in enumerate(data['strikePrice']) if sp in filtered_strikes_iv]
        filtered_pe_iv = [data['PE_impliedVolatility'][i] for i, sp in enumerate(data['strikePrice']) if sp in filtered_strikes_iv]

        fig_iv = go.Figure()

        # Add Call IV (red)
        fig_iv.add_trace(go.Scatter(x=filtered_strikes_iv, y=filtered_ce_iv, mode='lines+markers', name='Call IV', line=dict(color='red')))

        # Add Put IV (green)
        fig_iv.add_trace(go.Scatter(x=filtered_strikes_iv, y=filtered_pe_iv, mode='lines+markers', name='Put IV', line=dict(color='green')))

        # Add Vertical Line for ATM Strike
        fig_iv.add_vline(
            x=atm_strike,
            line_dash="dash",
            line_color="blue",
            annotation_text="ATM Strike",
            annotation_position="top"
        )

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