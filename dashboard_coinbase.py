import streamlit as st
from supabase import create_client, Client
import pandas as pd
import plotly.express as px
import os

# --- CONFIG ---
SUPABASE_URL = "supabase_url"
SUPABASE_KEY = "supabase_key"
TABLE_NAME = "table_name"  # Replace with the actual name

# --- INIT SUPABASE ---
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- STREAMLIT CONFIG ---
st.set_page_config(page_title="Bitcoin Trade Dashboard", layout="wide")
st.title("📊 Real-Time Bitcoin Dashboard (Coinbase + Supabase)")

# --- FETCH DATA ---
@st.cache_data(ttl=30)  # refresh every 30s
def fetch_trades(limit=1000):
    response = supabase.table(TABLE_NAME).select("*").order("timestamp", desc=True).limit(limit).execute()
    data = response.data
    df = pd.DataFrame(data)
    if not df.empty:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

df = fetch_trades()

# --- METRICS ---
if not df.empty:
    total_volume = df['total_usd'].sum()
    latest_price = df.iloc[0]['price']
    latest_time = df.iloc[0]['timestamp']

    st.metric("💰 Total USD Traded", f"${total_volume:,.2f}")
    st.metric("📈 Latest BTC Price", f"${latest_price:,.2f}", delta=None)
    st.metric("🕒 Last Trade At", latest_time.strftime("%Y-%m-%d %H:%M:%S"))

    st.markdown("---")

    # --- TABLE VIEW ---
    st.subheader("📄 Recent Trades")
    st.dataframe(df[['timestamp', 'trade_id', 'price', 'size', 'total_usd']].head(20))

    # --- CHART ---
    st.subheader("📉 BTC Price Over Time")
    fig = px.line(df.sort_values("timestamp"), x="timestamp", y="price", title="BTC Price (last 1000 trades)")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No trade data found in Supabase yet.")

