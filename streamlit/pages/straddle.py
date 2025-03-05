import streamlit as st
import pandas as pd
from pnsea import NSE
import plotly.graph_objects as go
import sqlite3
from datetime import datetime
import time

# Initialize NSE
nse = NSE()

# SQLite Database Configuration
db_path = 'straddle_data.db'

# Function to connect to SQLite
def connect_to_db():
    return sqlite3.connect(db_path)

# Function to create table if it doesn't exist (dynamic table names)
def create_table_if_not_exists(table_name):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            straddle_price REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert straddle price into SQLite (dynamic table names)
def insert_straddle_price(table_name, straddle_price):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = f"INSERT INTO {table_name} (timestamp, straddle_price) VALUES (?, ?)"
    cursor.execute(query, (datetime.now(), straddle_price))
    conn.commit()
    conn.close()

# Function to fetch straddle prices from SQLite (dynamic table names)
def fetch_straddle_prices(table_name, limit=100):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = f"SELECT timestamp, straddle_price FROM {table_name} ORDER BY timestamp DESC LIMIT ?"
    cursor.execute(query, (limit,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# Function to calculate ATM straddle price
def calculate_straddle_price(symbol, expiry_date_str):
    data, expiry_dates, cmp = nse.options.option_chain(symbol, expiry_date=expiry_date_str)
    if data.empty:
        return None

    # Find ATM Strike (Closest to CMP)
    strike_prices = sorted(data['strikePrice'])
    atm_strike = min(strike_prices, key=lambda x: abs(x - cmp))

    # Filter data for ATM strike
    atm_data = data[data['strikePrice'] == atm_strike].iloc[0]

    # Calculate straddle price (CE last price + PE last price)
    straddle_price = atm_data['CE_lastPrice'] + atm_data['PE_lastPrice']
    return straddle_price

# Streamlit App
st.title("Live Straddle Chart")

# Inputs
symbol = st.text_input("Enter Symbol", value="NIFTY")
expiry_date = st.date_input("Select Expiry Date", value=pd.to_datetime("2025-03-06"))
expiry_date_str = expiry_date.strftime("%d-%b-%Y")

# Placeholder for live chart
chart_placeholder = st.empty()

# Function to update the chart
def update_chart(symbol, expiry_date_str):
    counter = 0
    table_name = f"{symbol}_{expiry_date_str.replace('-', '_')}" #create dynamic table name
    create_table_if_not_exists(table_name) #create the table.

    while True:
        straddle_price = calculate_straddle_price(symbol, expiry_date_str)
        if straddle_price is None:
            st.error("Failed to calculate straddle price. Please check the symbol and expiry date.")
            time.sleep(60)
            continue

        insert_straddle_price(table_name, straddle_price)

        straddle_data = fetch_straddle_prices(table_name)
        if not straddle_data:
            st.warning("No data found in the database.")
            time.sleep(60)
            continue

        timestamps = [row[0] for row in straddle_data]
        prices = [row[1] for row in straddle_data]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=timestamps, y=prices, mode='lines+markers', name='Straddle Price'))

        fig.update_layout(
            title=f"Live Straddle Price for {symbol} ({expiry_date_str})",
            xaxis_title="Time",
            yaxis_title="Straddle Price",
            hovermode="x unified"
        )

        chart_placeholder.plotly_chart(fig, key=f"straddle_chart_{counter}")
        counter += 1

        time.sleep(60)

# Main logic (start the chart immediately)
update_chart(symbol, expiry_date_str)