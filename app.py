import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------------------------
# PAGE CONFIG
# ----------------------------------------

st.set_page_config(
    page_title="Crypto Dashboard",
    layout="wide"
)

st.title("📊 Crypto Analytics Dashboard")

# ----------------------------------------
# LOAD DATA
# ----------------------------------------

@st.cache_data
def load_data():

    crypto = pd.read_csv("Cryptofile.csv")
    sentiment = pd.read_csv("Sentiment_2026.csv")
    stacked = pd.read_csv("Stacked2026.csv")

    return crypto, sentiment, stacked


crypto, sentiment, stacked = load_data()

# ----------------------------------------
# CLEAN COLUMN NAMES
# ----------------------------------------

crypto.columns = crypto.columns.str.strip()
sentiment.columns = sentiment.columns.str.strip()
stacked.columns = stacked.columns.str.strip()

# ----------------------------------------
# AUTO DETECT COLUMNS
# ----------------------------------------

date_col = None
close_col = None
open_col = None
high_col = None
low_col = None
volume_col = None
ticker_col = None

for col in crypto.columns:

    c = col.lower()

    if "date" in c:
        date_col = col

    elif "close" in c:
        close_col = col

    elif "open" in c:
        open_col = col

    elif "high" in c:
        high_col = col

    elif "low" in c:
        low_col = col

    elif "volume" in c:
        volume_col = col

    elif "ticker" in c:
        ticker_col = col

# ----------------------------------------
# DATE CONVERT
# ----------------------------------------

if date_col:
    crypto[date_col] = pd.to_datetime(
        crypto[date_col],
        errors="coerce"
    )

# ----------------------------------------
# SIDEBAR FILTER
# ----------------------------------------

filtered_df = crypto.copy()

if ticker_col:

    tickers = st.sidebar.multiselect(
        "Select Ticker",
        options=crypto[ticker_col].dropna().unique(),
        default=crypto[ticker_col].dropna().unique()
    )

    filtered_df = filtered_df[
        filtered_df[ticker_col].isin(tickers)
    ]

# ----------------------------------------
# KPI CARDS
# ----------------------------------------

st.subheader("📌 KPIs")

c1, c2, c3 = st.columns(3)

if high_col:
    c1.metric(
        "Highest Price",
        round(filtered_df[high_col].max(), 2)
    )

if low_col:
    c2.metric(
        "Lowest Price",
        round(filtered_df[low_col].min(), 2)
    )

if close_col:
    c3.metric(
        "Average Close",
        round(filtered_df[close_col].mean(), 2)
    )

# ----------------------------------------
# LINE CHART
# ----------------------------------------

st.subheader("📈 Price Trend")

if date_col and close_col:

    fig = px.line(
        filtered_df,
        x=date_col,
        y=close_col,
        color=ticker_col if ticker_col else None,
        title="Close Price Trend"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ----------------------------------------
# CANDLESTICK CHART
# ----------------------------------------

st.subheader("🕯 Candlestick Chart")

required = [
    date_col,
    open_col,
    high_col,
    low_col,
    close_col
]

if all(required):

    fig2 = go.Figure(data=[go.Candlestick(
        x=filtered_df[date_col],
        open=filtered_df[open_col],
        high=filtered_df[high_col],
        low=filtered_df[low_col],
        close=filtered_df[close_col]
    )])

    fig2.update_layout(
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ----------------------------------------
# VOLUME CHART
# ----------------------------------------

st.subheader("📊 Trading Volume")

if volume_col and date_col:

    fig3 = px.bar(
        filtered_df,
        x=date_col,
        y=volume_col,
        color=ticker_col if ticker_col else None,
        title="Volume Analysis"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# ----------------------------------------
# SENTIMENT ANALYSIS
# ----------------------------------------

st.subheader("📰 Sentiment Analysis")

if "Sentiment" in sentiment.columns:

    fig4 = px.histogram(
        sentiment,
        x="Sentiment",
        color="ImpactLevel"
        if "ImpactLevel" in sentiment.columns
        else None,
        title="Sentiment Distribution"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# ----------------------------------------
# RAW DATA
# ----------------------------------------

st.subheader("📄 Dataset")

st.dataframe(filtered_df)
