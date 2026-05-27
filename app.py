import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI CSV Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #2D3748;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: white;
}

.metric-card {
    background-color: #1E1E1E;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid #2D3748;
}

.metric-value {
    font-size: 34px;
    font-weight: bold;
    color: #60A5FA;
}

.metric-label {
    color: #A1A1AA;
    font-size: 16px;
}

.insight-box {
    background-color: #111827;
    padding: 18px;
    border-radius: 12px;
    border-left: 5px solid #3B82F6;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #

st.title("📊 AI Powered CSV Intelligence Dashboard")

st.markdown("""
### Upload any CSV file and instantly generate:
- Smart KPIs
- Interactive Charts
- Correlation Analysis
- Dataset Insights
- Auto Visualizations
- Business Intelligence Reports
""")

st.divider()

# ---------------- FILE UPLOADER ---------------- #

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# ---------------- IF FILE UPLOADED ---------------- #

if uploaded_file is not None:

    try:

        df = pd.read_csv(uploaded_file)

        st.success("CSV File Uploaded Successfully ✅")

        # ---------------- CLEAN DATA ---------------- #

        df = df.drop_duplicates()

        # ---------------- COLUMN TYPES ---------------- #

        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

        categorical_cols = df.select_dtypes(include='object').columns.tolist()

        # ---------------- SIDEBAR ---------------- #

        st.sidebar.title("🔍 Smart Filters")

        filtered_df = df.copy()

        for col in categorical_cols:

            unique_values = df[col].dropna().unique().tolist()

            if 2 <= len(unique_values) <= 20:

                selected = st.sidebar.multiselect(
                    col,
                    unique_values,
                    default=unique_values
                )

                filtered_df = filtered_df[
                    filtered_df[col].isin(selected)
                ]

        # ---------------- KPI SECTION ---------------- #

        st.subheader("📈 Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{filtered_df.shape[0]}</div>
                <div class="metric-label">Rows</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{filtered_df.shape[1]}</div>
                <div class="metric-label">Columns</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(numeric_cols)}</div>
                <div class="metric-label">Numeric Features</div>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            missing = int(filtered_df.isnull().sum().sum())

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{missing}</div>
                <div class="metric-label">Missing Values</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # ---------------- SMART INSIGHTS ---------------- #

        st.subheader("🧠 AI Generated Insights")

        insight_col1, insight_col2 = st.columns(2)

        with insight_col1:

            if len(categorical_cols) > 0:

                top_cat_col = categorical_cols[0]

                top_value = filtered_df[top_cat_col].mode()[0]

                st.markdown(f"""
                <div class="insight-box">
                🔥 Most frequent value in <b>{top_cat_col}</b> is
                <b>{top_value}</b>
                </div>
                """, unsafe_allow_html=True)

            if len(numeric_cols) > 0:

                top_numeric = filtered_df[numeric_cols].sum().idxmax()

                st.markdown(f"""
                <div class="insight-box">
                📊 Highest overall numeric activity found in
                <b>{top_numeric}</b>
                </div>
                """, unsafe_allow_html=True)

        with insight_col2:

            st.markdown(f"""
            <div class="insight-box">
            ✅ Dataset contains
            <b>{filtered_df.shape[0]}</b> records and
            <b>{filtered_df.shape[1]}</b> features
            </div>
            """, unsafe_allow_html=True)

            health_score = max(
                0,
                100 - (missing / (filtered_df.shape[0] * filtered_df.shape[1]) * 100)
            )

            st.markdown(f"""
            <div class="insight-box">
            🚀 Dataset Health Score:
            <b>{health_score:.2f}%</b>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # ---------------- AUTO CHARTS ---------------- #

        st.subheader("📊 Smart Visual Analytics")

        chart_col1, chart_col2 = st.columns(2)

        # ---------------- LEFT CHART ---------------- #

        with chart_col1:

            if len(numeric_cols) > 0:

                best_numeric = numeric_cols[0]

                fig = px.histogram(
                    filtered_df,
                    x=best_numeric,
                    nbins=30,
                    title=f"Distribution of {best_numeric}",
                    template="plotly_dark",
                    color_discrete_sequence=["#60A5FA"]
                )

                fig.update_layout(
                    paper_bgcolor="#0E1117",
                    plot_bgcolor="#0E1117"
                )

                st.plotly_chart(fig, use_container_width=True)

        # ---------------- RIGHT CHART ---------------- #

        with chart_col2:

            if len(categorical_cols) > 0:

                best_cat = categorical_cols[0]

                cat_df = filtered_df[best_cat].value_counts().head(10)

                fig = px.bar(
                    x=cat_df.index,
                    y=cat_df.values,
                    title=f"Top Categories in {best_cat}",
                    template="plotly_dark",
                    color=cat_df.values,
                    color_continuous_scale="Blues"
                )

                fig.update_layout(
                    xaxis_title=best_cat,
                    yaxis_title="Count",
                    paper_bgcolor="#0E1117",
                    plot_bgcolor="#0E1117"
                )

                st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # ---------------- CORRELATION HEATMAP ---------------- #

        if len(numeric_cols) >= 2:

            st.subheader("🔥 Correlation Heatmap")

            corr = filtered_df[numeric_cols].corr()

            fig = px.imshow(
                corr,
                text_auto=True,
                color_continuous_scale="Blues",
                aspect="auto"
            )

            fig.update_layout(
                paper_bgcolor="#0E1117",
                plot_bgcolor="#0E1117"
            )

            st.plotly_chart(fig, use_container_width=True)

            st.divider()

        # ---------------- PIE + SCATTER ---------------- #

        chart_col3, chart_col4 = st.columns(2)

        with chart_col3:

            if len(categorical_cols) > 0:

                pie_col = categorical_cols[0]

                pie_data = filtered_df[pie_col].value_counts().head(5)

                fig = px.pie(
                    values=pie_data.values,
                    names=pie_data.index,
                    title=f"{pie_col} Distribution",
                    template="plotly_dark"
                )

                fig.update_layout(
                    paper_bgcolor="#0E1117",
                    plot_bgcolor="#0E1117"
                )

                st.plotly_chart(fig, use_container_width=True)

        with chart_col4:

            if len(numeric_cols) >= 2:

                fig = px.scatter(
                    filtered_df,
                    x=numeric_cols[0],
                    y=numeric_cols[1],
                    template="plotly_dark",
                    title=f"{numeric_cols[0]} vs {numeric_cols[1]}",
                    color=numeric_cols[1]
                )

                fig.update_layout(
                    paper_bgcolor="#0E1117",
                    plot_bgcolor="#0E1117"
                )

                st.plotly_chart(fig, use_container_width=True)

        st.divider()

        # ---------------- DATA PREVIEW ---------------- #

        with st.expander("📄 View Dataset Preview"):

            st.dataframe(
                filtered_df.head(20),
                use_container_width=True
            )

        # ---------------- STATISTICAL SUMMARY ---------------- #

        with st.expander("📑 Statistical Summary"):

            if len(numeric_cols) > 0:

                st.dataframe(
                    filtered_df[numeric_cols].describe(),
                    use_container_width=True
                )

        # ---------------- DOWNLOAD BUTTON ---------------- #

        st.subheader("⬇ Download Filtered Dataset")

        csv = filtered_df.to_csv(index=False).encode('utf-8')

        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="filtered_dataset.csv",
            mime="text/csv"
        )

    except Exception as e:

        st.error("Error Processing CSV File ❌")

        st.code(str(e))

# ---------------- NO FILE ---------------- #

else:

    st.info("👆 Upload any CSV file to begin intelligent analysis.")