import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.linear_model import LinearRegression
import numpy as np

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Supplement Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==================================
# TITLE
# ==================================

st.title("📊 Supplement Sales Intelligence Dashboard")

st.markdown(
    "Upload a sales CSV file to analyze revenue, products, customers, states and future sales trends."
)

# ==================================
# FILE UPLOAD
# ==================================

uploaded_file = st.file_uploader(
    "Upload Sales CSV",
    type=["csv"]
)

# ==================================
# MAIN APP
# ==================================

if uploaded_file is not None:

    # ==========================
    # LOAD DATA
    # ==========================

    df = pd.read_csv(uploaded_file)

    df["Order_Date"] = pd.to_datetime(
        df["Order_Date"]
    )

    st.success("✅ File uploaded successfully!")

    # ==========================
    # FILTER OPTIONS
    # ==========================

    all_states = sorted(
        df["State"].dropna().unique()
    )

    all_products = sorted(
        df["Product_Name"].dropna().unique()
    )

    all_channels = sorted(
        df["Channel"].dropna().unique()
    )

    # ==========================
    # SESSION STATE
    # ==========================

    if "states" not in st.session_state:
        st.session_state.states = all_states

    if "products" not in st.session_state:
        st.session_state.products = all_products

    if "channels" not in st.session_state:
        st.session_state.channels = all_channels

    # ==========================
    # SIDEBAR
    # ==========================

    st.sidebar.header("🔎 Filters")

    # ---------- STATES ----------

    st.sidebar.subheader("State")

    col1, col2 = st.sidebar.columns(2)

    if col1.button("All States"):
        st.session_state.states = all_states

    if col2.button("Clear"):
        st.session_state.states = []

    selected_states = st.sidebar.multiselect(
        "Choose States",
        options=all_states,
        key="states"
    )

    # ---------- PRODUCTS ----------

    st.sidebar.subheader("Product")

    col3, col4 = st.sidebar.columns(2)

    if col3.button("All Products"):
        st.session_state.products = all_products

    if col4.button("Clear Product"):
        st.session_state.products = []

    selected_products = st.sidebar.multiselect(
        "Choose Products",
        options=all_products,
        key="products"
    )

    # ---------- CHANNEL ----------

    st.sidebar.subheader("Channel")

    col5, col6 = st.sidebar.columns(2)

    if col5.button("All Channels"):
        st.session_state.channels = all_channels

    if col6.button("Clear Channel"):
        st.session_state.channels = []

    selected_channels = st.sidebar.multiselect(
        "Choose Channels",
        options=all_channels,
        key="channels"
    )

    # ==========================
    # APPLY FILTERS
    # ==========================

    filtered_df = df[
        (df["State"].isin(selected_states))
        &
        (df["Product_Name"].isin(selected_products))
        &
        (df["Channel"].isin(selected_channels))
    ]

    if filtered_df.empty:
        st.warning(
            "⚠️ No data available for selected filters."
        )
        st.stop()

    # ==========================
    # KPI CALCULATIONS
    # ==========================

    total_revenue = filtered_df["Revenue"].sum()

    total_orders = filtered_df["Order_ID"].nunique()

    total_customers = filtered_df["Customer_ID"].nunique()

    average_order_value = (
        total_revenue / total_orders
    )

    repeat_percentage = (
        (
            filtered_df["Customer_Type"]
            == "Repeat"
        ).sum()
        /
        len(filtered_df)
    ) * 100

    # ==========================
    # KPI CARDS
    # ==========================

    st.subheader(
        "📌 Key Performance Indicators"
    )

    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric(
        "Revenue",
        f"₹{total_revenue:,.0f}"
    )

    k2.metric(
        "Orders",
        f"{total_orders:,}"
    )

    k3.metric(
        "AOV",
        f"₹{average_order_value:,.2f}"
    )

    k4.metric(
        "Customers",
        f"{total_customers:,}"
    )

    k5.metric(
        "Repeat %",
        f"{repeat_percentage:.2f}%"
    )

    st.divider()

    # ==========================
    # DATA PREPARATION
    # ==========================

    monthly_revenue = (
        filtered_df.groupby(
            pd.Grouper(
                key="Order_Date",
                freq="ME"
            )
        )["Revenue"]
        .sum()
        .reset_index()
    )

    product_revenue = (
        filtered_df.groupby(
            "Product_Name"
        )["Revenue"]
        .sum()
        .reset_index()
        .sort_values(
            by="Revenue",
            ascending=False
        )
    )

    state_revenue = (
        filtered_df.groupby(
            "State"
        )["Revenue"]
        .sum()
        .reset_index()
        .sort_values(
            by="Revenue",
            ascending=False
        )
    )

    customer_revenue = (
        filtered_df.groupby(
            "Customer_Type"
        )["Revenue"]
        .sum()
        .reset_index()
    )

    # ==========================
    # CHART ROW 1
    # ==========================

    left, right = st.columns(2)

    with left:

        st.subheader(
            "📈 Monthly Revenue Trend"
        )

        fig_line = px.line(
            monthly_revenue,
            x="Order_Date",
            y="Revenue",
            markers=True
        )

        st.plotly_chart(
            fig_line,
            use_container_width=True
        )

    with right:

        st.subheader(
            "📊 Revenue by Product"
        )

        fig_bar = px.bar(
            product_revenue,
            x="Revenue",
            y="Product_Name",
            orientation="h"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

    # ==========================
    # CHART ROW 2
    # ==========================

    left2, right2 = st.columns(2)

    with left2:

        st.subheader(
            "🌍 Revenue by State"
        )

        fig_state = px.bar(
            state_revenue,
            x="Revenue",
            y="State",
            orientation="h"
        )

        st.plotly_chart(
            fig_state,
            use_container_width=True
        )

    with right2:

        st.subheader(
            "👥 Revenue by Customer Type"
        )

        fig_donut = px.pie(
            customer_revenue,
            names="Customer_Type",
            values="Revenue",
            hole=0.5
        )

        st.plotly_chart(
            fig_donut,
            use_container_width=True
        )

    st.divider()

    # ==========================
    # SALES FORECASTING
    # ==========================

    st.subheader(
        "📈 Sales Forecast (Next 3 Months)"
    )

    forecast_data = (
        filtered_df.groupby(
            pd.Grouper(
                key="Order_Date",
                freq="ME"
            )
        )["Revenue"]
        .sum()
        .reset_index()
    )

    forecast_data["Month_Index"] = range(
        len(forecast_data)
    )

    X = forecast_data[
        ["Month_Index"]
    ]

    y = forecast_data["Revenue"]

    model = LinearRegression()

    model.fit(X, y)

    future_months = 3

    future_index = np.arange(
        len(forecast_data),
        len(forecast_data)
        + future_months
    ).reshape(-1, 1)

    future_predictions = model.predict(
        future_index
    )

    future_dates = pd.date_range(
        start=forecast_data[
            "Order_Date"
        ].max(),
        periods=future_months + 1,
        freq="ME"
    )[1:]

    forecast_future = pd.DataFrame(
        {
            "Order_Date": future_dates,
            "Predicted_Revenue":
            future_predictions
        }
    )

    historical = forecast_data.copy()

    historical["Type"] = "Historical"

    forecast_plot = forecast_future.rename(
        columns={
            "Predicted_Revenue":
            "Revenue"
        }
    )

    forecast_plot["Type"] = "Forecast"

    combined = pd.concat(
        [
            historical[
                [
                    "Order_Date",
                    "Revenue",
                    "Type"
                ]
            ],
            forecast_plot[
                [
                    "Order_Date",
                    "Revenue",
                    "Type"
                ]
            ]
        ]
    )

    fig_forecast = px.line(
        combined,
        x="Order_Date",
        y="Revenue",
        color="Type",
        markers=True,
        title="Historical Revenue vs Forecast"
    )

    st.plotly_chart(
        fig_forecast,
        use_container_width=True
    )

    st.dataframe(
        forecast_future,
        use_container_width=True
    )

    st.divider()

    # ==========================
    # DATA PREVIEW
    # ==========================

    st.subheader("📋 Data Preview")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

else:

    st.info(
        "👆 Upload a CSV file to start analysis."
    )