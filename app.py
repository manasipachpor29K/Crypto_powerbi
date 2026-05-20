# app.py

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(
    page_title="Crypto Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

@st.cache_data

def load_data():
    crypto = pd.read_csv("Cryptofile.csv")
    sentiment = pd.read_csv("Sentiment_2026.csv")
    stacked = pd.read_csv("Stacked2026.csv")

    if 'Date' in crypto.columns:
        crypto['Date'] = pd.to_datetime(crypto['Date'])

    return crypto, sentiment, stacked

crypto, sentiment, stacked = load_data()

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------

st.sidebar.title("📊 Crypto Dashboard")

if 'Ticker' in crypto.columns:
    selected_ticker = st.sidebar.multiselect(
        "Select Ticker",
        crypto['Ticker'].dropna().unique(),
        default=crypto['Ticker'].dropna().unique()
    )

    crypto = crypto[crypto['Ticker'].isin(selected_ticker)]

if 'Market_Type' in crypto.columns:
    selected_market = st.sidebar.multiselect(
        "Select Market Type",
        crypto['Market_Type'].dropna().unique(),
        default=crypto['Market_Type'].dropna().unique()
    )

    crypto = crypto[crypto['Market_Type'].isin(selected_market)]

if 'Category' in crypto.columns:
    selected_category = st.sidebar.multiselect(
        "Select Category",
        crypto['Category'].dropna().unique(),
        default=crypto['Category'].dropna().unique()
    )

    crypto = crypto[crypto['Category'].isin(selected_category)]

# -------------------------------------------------
# PAGE NAVIGATION
# -------------------------------------------------

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Price Explorer",
        "Forecasting",
        "Risk & Volatility",
        "Forecast Insights",
        "Sentiment Analysis",
        "Market Correlation",
        "Feature Explainability",
        "Forecast Comparison",
        "Key Influencers",
        "Strategy Backtest",
        "Interactive Explorer"
    ]
)

# -------------------------------------------------
# PAGE 1
# -------------------------------------------------

if page == "Executive Overview":

    st.title("📈 Executive Overview")

    c1, c2, c3, c4 = st.columns(4)

    if 'High' in crypto.columns:
        c1.metric("Highest Peak Price", f"{crypto['High'].max():,.2f}")

    if 'Close' in crypto.columns:
        c2.metric("Latest Close Price", f"{crypto['Close'].iloc[-1]:,.2f}")

    if 'Ticker' in crypto.columns:
        c3.metric("Most Volatile Ticker", str(crypto['Ticker'].mode()[0]))

    if 'Close' in crypto.columns:
        c4.metric("Average Close", f"{crypto['Close'].mean():,.2f}")

    if 'Date' in crypto.columns and 'Close' in crypto.columns:

        fig = px.line(
            crypto,
            x='Date',
            y='Close',
            color='Ticker' if 'Ticker' in crypto.columns else None,
            title='Average Close Price Over Time'
        )

        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# PAGE 2
# -------------------------------------------------

elif page == "Price Explorer":

    st.title("📊 Price Explorer & Candlesticks")

    if all(col in crypto.columns for col in ['Date','Open','High','Low','Close']):

        fig = go.Figure(data=[go.Candlestick(
            x=crypto['Date'],
            open=crypto['Open'],
            high=crypto['High'],
            low=crypto['Low'],
            close=crypto['Close']
        )])

        fig.update_layout(title='Candlestick Chart')

        st.plotly_chart(fig, use_container_width=True)

    if 'Volume' in crypto.columns:

        fig2 = px.bar(
            crypto,
            x='Date',
            y='Volume',
            title='Trading Volume'
        )

        st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------
# PAGE 3
# -------------------------------------------------

elif page == "Forecasting":

    st.title("🔮 Forecasting Dashboard")

    if 'Forecast' in stacked.columns:

        fig = px.line(
            stacked,
            x='Date',
            y='Forecast',
            color='Model' if 'Model' in stacked.columns else None,
            title='Forecast Comparison'
        )

        st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    if 'MAE' in stacked.columns:
        col1.metric("MAE", f"{stacked['MAE'].mean():,.2f}")

    if 'RMSE' in stacked.columns:
        col2.metric("RMSE", f"{stacked['RMSE'].mean():,.2f}")

# -------------------------------------------------
# PAGE 4
# -------------------------------------------------

elif page == "Risk & Volatility":

    st.title("⚠ Risk & Volatility")

    if 'Volatility' in crypto.columns:

        fig = px.line(
            crypto,
            x='Date',
            y='Volatility',
            color='Ticker' if 'Ticker' in crypto.columns else None,
            title='Volatility Trend'
        )

        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# PAGE 5
# -------------------------------------------------

elif page == "Forecast Insights":

    st.title("📌 Forecast Insights")

    if 'Forecast' in stacked.columns:

        fig = px.area(
            stacked,
            x='Date',
            y='Forecast',
            title='Forecast Growth'
        )

        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# PAGE 6
# -------------------------------------------------

elif page == "Sentiment Analysis":

    st.title("📰 Sentiment & News Impact")

    if 'Sentiment' in sentiment.columns:

        fig = px.histogram(
            sentiment,
            x='Sentiment',
            color='ImpactLevel' if 'ImpactLevel' in sentiment.columns else None,
            title='Sentiment Distribution'
        )

        st.plotly_chart(fig, use_container_width=True)

    if 'source' in sentiment.columns:

        fig2 = px.bar(
            sentiment,
            x='source',
            y='NewsImpact' if 'NewsImpact' in sentiment.columns else None,
            title='News Impact by Source'
        )

        st.plotly_chart(fig2, use_container_width=True)

# -------------------------------------------------
# PAGE 7
# -------------------------------------------------

elif page == "Market Correlation":

    st.title("🔗 Correlations & Market Structure")

    numeric_cols = crypto.select_dtypes(include='number')

    corr = numeric_cols.corr()

    fig = px.imshow(corr, text_auto=True)

    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# PAGE 8
# -------------------------------------------------

elif page == "Feature Explainability":

    st.title("📌 Feature Importance & Explainability")

    if 'Close' in crypto.columns and 'Volume' in crypto.columns:

        fig = px.scatter(
            crypto,
            x='Volume',
            y='Close',
            color='Ticker' if 'Ticker' in crypto.columns else None,
            title='Close vs Volume'
        )

        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# PAGE 9
# -------------------------------------------------

elif page == "Forecast Comparison":

    st.title("📊 Forecast Model Comparison")

    if 'Forecast' in stacked.columns:

        fig = px.line(
            stacked,
            x='Date',
            y='Forecast',
            color='Model' if 'Model' in stacked.columns else None,
            title='Model Forecasts'
        )

        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# PAGE 10
# -------------------------------------------------

elif page == "Key Influencers":

    st.title("⭐ Key Influencers")

    st.dataframe(crypto.describe())

# -------------------------------------------------
# PAGE 11
# -------------------------------------------------

elif page == "Strategy Backtest":

    st.title("📈 Strategy Backtest & Performance")

    if 'Daily_Return' in crypto.columns:

        fig = px.line(
            crypto,
            x='Date',
            y='Daily_Return',
            color='Ticker' if 'Ticker' in crypto.columns else None,
            title='Daily Returns'
        )

        st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------
# PAGE 12
# -------------------------------------------------

elif page == "Interactive Explorer":

    st.title("🎯 Interactive Explorer")

    st.dataframe(crypto)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.sidebar.markdown("---")
st.sidebar.info("Power BI Clone using Streamlit")
```

streamlit.io/cloud](https://streamlit.io/cloud)
