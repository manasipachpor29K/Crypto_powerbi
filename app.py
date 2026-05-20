# app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Power BI Dashboard Clone",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "Dashboard 1",
        "Dashboard 2",
        "Dashboard 3",
        "Dashboard 4",
        "Dashboard 5",
        "Dashboard 6",
        "Dashboard 7",
        "Dashboard 8",
        "Dashboard 9",
        "Dashboard 10",
        "Dashboard 11",
        "Dashboard 12"
    ]
)

# -----------------------------------
# DASHBOARD 1
# -----------------------------------

if page == "Dashboard 1":

    st.title("📈 Sales Dashboard")

    df = pd.DataFrame({
        'Category': ['A', 'B', 'C', 'D'],
        'Sales': [100, 200, 150, 300]
    })

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Sales", "₹10,00,000")
    c2.metric("Profit", "₹2,50,000")
    c3.metric("Growth", "15%")

    fig = px.bar(df, x='Category', y='Sales', title='Sales by Category')

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df)

# -----------------------------------
# DASHBOARD 2
# -----------------------------------

elif page == "Dashboard 2":

    st.title("📊 Revenue Dashboard")

    df = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
        'Revenue': [400, 600, 700, 900]
    })

    fig = px.line(
        df,
        x='Month',
        y='Revenue',
        markers=True,
        title="Monthly Revenue"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df)

# -----------------------------------
# DASHBOARD 3
# -----------------------------------

elif page == "Dashboard 3":

    st.title("👨‍💼 Employee Dashboard")

    df = pd.DataFrame({
        'Department': ['HR', 'IT', 'Sales', 'Finance'],
        'Employees': [20, 45, 30, 15]
    })

    fig = px.pie(
        df,
        names='Department',
        values='Employees',
        title="Department Employees"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# DASHBOARD 4
# -----------------------------------

elif page == "Dashboard 4":

    st.title("💰 Profit Dashboard")

    df = pd.DataFrame({
        'Region': ['North', 'South', 'East', 'West'],
        'Profit': [250, 300, 150, 400]
    })

    fig = px.bar(
        df,
        x='Region',
        y='Profit',
        color='Region',
        title="Profit by Region"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# DASHBOARD 5
# -----------------------------------

elif page == "Dashboard 5":

    st.title("📦 Orders Dashboard")

    df = pd.DataFrame({
        'Product': ['P1', 'P2', 'P3', 'P4'],
        'Orders': [100, 250, 180, 90]
    })

    fig = px.funnel(
        df,
        x='Orders',
        y='Product',
        title="Product Orders Funnel"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# DASHBOARD 6
# -----------------------------------

elif page == "Dashboard 6":

    st.title("👥 User Growth Dashboard")

    df = pd.DataFrame({
        'Date': pd.date_range(start='2025-01-01', periods=10),
        'Users': [10,20,30,40,50,45,60,70,65,80]
    })

    fig = px.area(
        df,
        x='Date',
        y='Users',
        title="User Growth"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# DASHBOARD 7
# -----------------------------------

elif page == "Dashboard 7":

    st.title("📌 KPI Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric("Active Users", "12,450")
    c2.metric("New Customers", "1,250")
    c3.metric("Revenue", "₹8,75,000")

# -----------------------------------
# DASHBOARD 8
# -----------------------------------

elif page == "Dashboard 8":

    st.title("🌸 Iris Scatter Dashboard")

    df = px.data.iris()

    fig = px.scatter(
        df,
        x='sepal_width',
        y='sepal_length',
        color='species',
        title="Iris Dataset Scatter Plot"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# DASHBOARD 9
# -----------------------------------

elif page == "Dashboard 9":

    st.title("🏆 Team Performance Dashboard")

    df = pd.DataFrame({
        'Team': ['A', 'B', 'C'],
        'Score': [80, 90, 75]
    })

    fig = px.bar(
        df,
        x='Team',
        y='Score',
        title="Team Scores"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# DASHBOARD 10
# -----------------------------------

elif page == "Dashboard 10":

    st.title("📌 Dashboard 10")

    st.success("This is Dashboard 10")

# -----------------------------------
# DASHBOARD 11
# -----------------------------------

elif page == "Dashboard 11":

    st.title("📌 Dashboard 11")

    st.info("This is Dashboard 11")

# -----------------------------------
# DASHBOARD 12
# -----------------------------------

elif page == "Dashboard 12":

    st.title("📌 Dashboard 12")

    st.warning("This is Dashboard 12")


# -----------------------------------
# FOOTER
# -----------------------------------

st.sidebar.markdown("---")
st.sidebar.write("Made with ❤️ using Streamlit")
