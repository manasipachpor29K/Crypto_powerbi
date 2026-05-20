import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Crypto Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

@st.cache_data
def load_data():

    crypto = pd.read_csv("Cryptofile.csv")
    sentiment = pd.read_csv("Sentiment_2026.csv")
    stacked = pd.read_csv("Stacked2026.csv")

    # Convert Date Columns
    for df in [crypto, sentiment, stacked]:

        for col in df.columns:

            if "date" in col.lower():

                try:
                    df[col] = pd.to_datetime(df[col])
                except:
                    pass

    return crypto, sentiment, stacked


crypto, sentiment, stacked = load_data()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("📌 Crypto Dashboard")

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

# ---------------------------------------------------
# FILTERS
# ---------------------------------------------------

filtered_crypto = crypto.copy()

if "Ticker" in crypto.columns:

    ticker = st.sidebar.multiselect(
        "Select Ticker",
        options=sorted(crypto["Ticker"].dropna().unique()),
        default=sorted(crypto["Ticker"].dropna().unique())
    )

    filtered_crypto = filtered_crypto[
        filtered_crypto["Ticker"].isin(ticker)
    ]

if "Market_Type" in crypto.columns:

    market = st.sidebar.multiselect(
        "Market Type",
        options=sorted(crypto["Market_Type"].dropna().unique()),
        default=sorted(crypto["Market_Type"].dropna().unique())
    )

    filtered_crypto = filtered_crypto[
        filtered_crypto["Market_Type"].isin(market)
    ]

if "Category" in crypto.columns:

    category = st.sidebar.multiselect(
        "Category",
        options=sorted(crypto["Category"].dropna().unique()),
        default=sorted(crypto["Category"].dropna().unique())
    )

    filtered_crypto = filtered_crypto[
        filtered_crypto["Category"].isin(category)
    ]

# ---------------------------------------------------
# PAGE 1 — EXECUTIVE OVERVIEW
# ---------------------------------------------------

if page == "Executive Overview":

    st.title("📈 Executive Overview")

    c1, c2, c3, c4 = st.columns(4)

    if "High" in filtered_crypto.columns:
        c1.metric(
            "Highest Peak Price",
            f"{filtered_crypto['High'].max():,.2f}"
        )

    if "Close" in filtered_crypto.columns:
        c2.metric(
            "Latest Close Price",
            f"{filtered_crypto['Close'].iloc[-1]:,.2f}"
        )

    if "Ticker" in filtered_crypto.columns:
        c3.metric(
            "Most Volatile Ticker",
            filtered_crypto["Ticker"].mode()[0]
        )

    if "Close" in filtered_crypto.columns:
        c4.metric(
            "Average Close",
            f"{filtered_crypto['Close'].mean():,.2f}"
        )

    if "Date" in filtered_crypto.columns:

        fig = px.line(
            filtered_crypto,
            x="Date",
            y="Close",
            color="Ticker",
            title="Average Close Price Over Time"
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# PAGE 2 — PRICE EXPLORER
# ---------------------------------------------------

elif page == "Price Explorer":

    st.title("📊 Price Explorer")

    required_cols = [
        "Date",
        "Open",
        "High",
        "Low",
        "Close"
    ]

    if all(col in filtered_crypto.columns for col in required_cols):

        fig = go.Figure(data=[go.Candlestick(
            x=filtered_crypto["Date"],
            open=filtered_crypto["Open"],
            high=filtered_crypto["High"],
            low=filtered_crypto["Low"],
            close=filtered_crypto["Close"]
        )])

        fig.update_layout(
            title="Candlestick Chart",
            xaxis_rangeslider_visible=False
        )

        st.plotly_chart(fig, use_container_width=True)

    if "Volume" in filtered_crypto.columns:

        fig2 = px.bar(
            filtered_crypto,
            x="Date",
            y="Volume",
            color="Ticker",
            title="Trading Volume"
        )

        st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# PAGE 3 — FORECASTING
# ---------------------------------------------------

elif page == "Forecasting":

    st.title("🔮 Forecasting Dashboard")

    if "Forecast" in stacked.columns:

        if "Model" in stacked.columns:

            model = st.sidebar.multiselect(
                "Forecast Models",
                options=stacked["Model"].unique(),
                default=stacked["Model"].unique()
            )

            filtered_stack = stacked[
                stacked["Model"].isin(model)
            ]

        else:
            filtered_stack = stacked

        fig = px.line(
            filtered_stack,
            x=filtered_stack.columns[0],
            y="Forecast",
            color="Model" if "Model" in filtered_stack.columns else None,
            title="Forecast Comparison"
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# PAGE 4 — RISK & VOLATILITY
# ---------------------------------------------------

elif page == "Risk & Volatility":

    st.title("⚠ Risk & Volatility")

    if "Volatility" in filtered_crypto.columns:

        fig = px.line(
            filtered_crypto,
            x="Date",
            y="Volatility",
            color="Ticker",
            title="Volatility Trend"
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# PAGE 5 — FORECAST INSIGHTS
# ---------------------------------------------------

elif page == "Forecast Insights":

    st.title("📌 Forecast Insights")

    if "Forecast" in stacked.columns:

        fig = px.area(
            stacked,
            x=stacked.columns[0],
            y="Forecast",
            title="Forecast Growth"
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# PAGE 6 — SENTIMENT ANALYSIS
# ---------------------------------------------------

elif page == "Sentiment Analysis":

    st.title("📰 Sentiment Analysis")

    if "Sentiment" in sentiment.columns:

        fig = px.histogram(
            sentiment,
            x="Sentiment",
            color="ImpactLevel" if "ImpactLevel" in sentiment.columns else None,
            title="Sentiment Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    if "source" in sentiment.columns:

        y_col = (
            "NewsImpact"
            if "NewsImpact" in sentiment.columns
            else sentiment.columns[1]
        )

        fig2 = px.bar(
            sentiment,
            x="source",
            y=y_col,
            title="News Impact by Source"
        )

        st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# PAGE 7 — MARKET CORRELATION
# ---------------------------------------------------

elif page == "Market Correlation":

    st.title("🔗 Market Correlation")

    numeric_df = filtered_crypto.select_dtypes(include="number")

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=True,
        title="Correlation Heatmap"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# PAGE 8 — FEATURE EXPLAINABILITY
# ---------------------------------------------------

elif page == "Feature Explainability":

    st.title("📌 Feature Explainability")

    if "Volume" in filtered_crypto.columns:

        fig = px.scatter(
            filtered_crypto,
            x="Volume",
            y="Close",
            color="Ticker",
            title="Close vs Volume"
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# PAGE 9 — FORECAST COMPARISON
# ---------------------------------------------------

elif page == "Forecast Comparison":

    st.title("📊 Forecast Comparison")

    if "Forecast" in stacked.columns:

        fig = px.line(
            stacked,
            x=stacked.columns[0],
            y="Forecast",
            color="Model" if "Model" in stacked.columns else None,
            title="Forecast Models"
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# PAGE 10 — KEY INFLUENCERS
# ---------------------------------------------------

elif page == "Key Influencers":

    st.title("⭐ Key Influencers")

    st.dataframe(filtered_crypto.describe())

# ---------------------------------------------------
# PAGE 11 — STRATEGY BACKTEST
# ---------------------------------------------------

elif page == "Strategy Backtest":

    st.title("📈 Strategy Backtest")

    if "Daily_Return" in filtered_crypto.columns:

        fig = px.line(
            filtered_crypto,
            x="Date",
            y="Daily_Return",
            color="Ticker",
            title="Daily Return Analysis"
        )

        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# PAGE 12 — INTERACTIVE EXPLORER
# ---------------------------------------------------

elif page == "Interactive Explorer":

    st.title("🎯 Interactive Explorer")

    st.dataframe(filtered_crypto)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.sidebar.markdown("---")
st.sidebar.success("Power BI Clone using Streamlit")
