import pandas as pd
import streamlit as st

from api import (
    search_stock,
    get_company,
    get_history,
    get_complete_analysis,
    get_report,
)

from components import (
    company_overview,
    technical_cards,
    report_section,
)

from charts import (
    plot_history,
    plot_technicals,
    plot_prediction,
    plot_anomalies,
)


# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Stockify",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None

if "selected_ticker" not in st.session_state:
    st.session_state.selected_ticker = None

if "selected_company" not in st.session_state:
    st.session_state.selected_company = None


# ---------------------------------------------------
# Sidebar
# ---------------------------------------------------

with st.sidebar:

    st.title("📈 Stockify")

    st.markdown(
        """
AI Powered Stock Analysis Platform
"""
    )

    st.divider()

    st.markdown("### Features")

    st.markdown(
        """
- Company Overview
- Technical Indicators
- Historical Charts
- Price Forecast
- Anomaly Detection
- AI Generated Report
"""
    )

    st.divider()

    if st.button(
        "🗑 Clear Analysis",
        use_container_width=True,
    ):

        st.session_state.analysis_data = None
        st.session_state.selected_ticker = None
        st.session_state.selected_company = None

        st.rerun()


# ---------------------------------------------------
# Main Header
# ---------------------------------------------------

st.title("📈 Stockify")

st.caption(
    "Analyze stocks using Machine Learning and AI."
)

st.divider()


# ---------------------------------------------------
# Search Section
# ---------------------------------------------------

st.subheader("Search Stock")

query = st.text_input(
    "Company Name",
    placeholder="Apple, Tesla, Reliance...",
)

ticker = None

if query:

    try:

        search_results = search_stock(query)

        if search_results:

            options = {
                f"{stock['ticker']} - {stock['name']}": stock["ticker"]
                for stock in search_results
            }

            selected_company = st.selectbox(
                "Select Company",
                list(options.keys()),
            )

            ticker = options[selected_company]

            st.session_state.selected_ticker = ticker
            st.session_state.selected_company = selected_company

        else:

            st.warning(
                "No matching companies found."
            )

    except Exception as e:

        st.error(str(e))


# ---------------------------------------------------
# Analyze Button
# ---------------------------------------------------

analyze_clicked = False

if st.session_state.selected_ticker:

    left, right = st.columns([1, 4])

    with left:

        analyze_clicked = st.button(
            "Analyze",
            type="primary",
            use_container_width=True,
        )

    with right:

        st.success(
            f"Selected: {st.session_state.selected_company}"
        )
        
# ---------------------------------------------------
# Fetch Analysis
# ---------------------------------------------------

if analyze_clicked:

    with st.spinner("Fetching stock data and generating analysis..."):

        try:

            company = get_company(
                st.session_state.selected_ticker
            )

            history = get_history(
                st.session_state.selected_ticker
            )

            analysis = get_complete_analysis(
                st.session_state.selected_ticker
            )

            try:

                report = get_report(
                    st.session_state.selected_ticker
                )

            except Exception:

                report = None

            st.session_state.analysis_data = {

                "company": company,

                "history": history,

                "technicals": analysis["technicals"],

                "anomalies": analysis["anomalies"],

                "forecast": analysis["forecast"],

                "report": report,
            }

            st.success("Analysis completed successfully!")

        except Exception as e:

            st.error(str(e))


# ---------------------------------------------------
# Display Analysis
# ---------------------------------------------------

if st.session_state.analysis_data:

    data = st.session_state.analysis_data

    company = data["company"]

    history_df = pd.DataFrame(
        data["history"]
    )

    technical_df = pd.DataFrame(
        data["technicals"]
    )

    anomaly_df = pd.DataFrame(
        data["anomalies"]
    )

    forecast_df = pd.DataFrame(
        data["forecast"]
    )

    latest_technical = (
        technical_df.iloc[-1]
        .to_dict()
    )


    # -----------------------------------------------
    # Company Overview
    # -----------------------------------------------

    company_overview(company)

    st.divider()


    # -----------------------------------------------
    # Technical Cards
    # -----------------------------------------------

    technical_cards(
        latest_technical
    )

    st.divider()


    # -----------------------------------------------
    # Quick Statistics
    # -----------------------------------------------

    st.subheader("📌 Quick Statistics")

    c1, c2, c3, c4 = st.columns(4)

    latest_price = round(
        history_df["Close"].iloc[-1],
        2,
    )

    first_price = round(
        history_df["Close"].iloc[0],
        2,
    )

    total_return = (
        (
            latest_price
            - first_price
        )
        / first_price
    ) * 100

    anomaly_count = len(
        anomaly_df[
            anomaly_df["Anomaly"] == -1
        ]
    )

    predicted_price = round(
        forecast_df[
            "Predicted_Close"
        ].iloc[-1],
        2,
    )

    c1.metric(
        "Latest Close",
        f"${latest_price}",
    )

    c2.metric(
        "5Y Return",
        f"{total_return:.2f} %",
    )

    c3.metric(
        "Anomalies",
        anomaly_count,
    )

    c4.metric(
        "Forecast Price",
        f"${predicted_price}",
    )

    st.divider()


    # -----------------------------------------------
    # Analysis Tabs
    # -----------------------------------------------

    tab_history, tab_technical, tab_prediction, tab_anomaly, tab_report = st.tabs(
        [
            "📈 Historical",
            "📊 Technical",
            "🔮 Forecast",
            "🚨 Anomalies",
            "🤖 AI Report",
        ]
    )
    
    # ---------------------------------------------------
    # Historical Chart
    # ---------------------------------------------------

    with tab_history:

        st.subheader("📈 Historical Stock Price")

        st.plotly_chart(
            plot_history(history_df),
            use_container_width=True,
        )

        st.caption(
            "Historical closing prices for the selected stock."
        )

    # ---------------------------------------------------
    # Technical Analysis
    # ---------------------------------------------------

    with tab_technical:

        st.subheader("📊 Technical Indicators")

        st.plotly_chart(
            plot_technicals(technical_df),
            use_container_width=True,
        )

        st.markdown("### Latest Indicator Values")

        latest = technical_df.iloc[-1]

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "RSI",
            f"{latest['RSI']:.2f}",
        )

        c2.metric(
            "MACD",
            f"{latest['MACD']:.2f}",
        )

        c3.metric(
            "MACD Signal",
            f"{latest['MACD_Signal']:.2f}",
        )

        st.info(
            "RSI > 70 generally indicates overbought conditions, "
            "while RSI < 30 may indicate oversold conditions."
        )

    # ---------------------------------------------------
    # Forecast
    # ---------------------------------------------------

    with tab_prediction:

        st.subheader("🔮 Price Forecast")

        st.plotly_chart(
            plot_prediction(
                history_df,
                forecast_df,
            ),
            use_container_width=True,
        )

        predicted_price = forecast_df[
            "Predicted_Close"
        ].iloc[-1]

        current_price = history_df[
            "Close"
        ].iloc[-1]

        expected_return = (
            (
                predicted_price
                - current_price
            )
            / current_price
        ) * 100

        c1, c2 = st.columns(2)

        c1.metric(
            "Current Price",
            f"${current_price:.2f}",
        )

        c2.metric(
            "Predicted Price",
            f"${predicted_price:.2f}",
            delta=f"{expected_return:.2f}%",
        )

    # ---------------------------------------------------
    # Anomaly Detection
    # ---------------------------------------------------

    with tab_anomaly:

        st.subheader("🚨 Market Anomalies")

        st.plotly_chart(
            plot_anomalies(anomaly_df),
            use_container_width=True,
        )

        anomalies = anomaly_df[
            anomaly_df["Anomaly"] == -1
        ]

        st.markdown("### Detected Anomalies")

        if anomalies.empty:

            st.success(
                "No significant anomalies detected."
            )

        else:

            st.dataframe(
                anomalies[
                    [
                        "Date",
                        "Close",
                        "Anomaly_Score",
                    ]
                ],
                use_container_width=True,
            )

    # ---------------------------------------------------
    # AI Report
    # ---------------------------------------------------

    with tab_report:

        st.subheader("🤖 AI Stock Report")

        if data["report"]:

            report_section(
                data["report"]["report"]
            )

        else:

            st.warning(
                """
AI Report is currently unavailable.

Possible reasons:

- OpenAI API key is not configured.
- API quota has been exhausted.
- The LLM service is temporarily unavailable.
                """
            )

    # ---------------------------------------------------
    # Footer
    # ---------------------------------------------------

    st.divider()

    st.caption(
        "Stockify V1 • FastAPI • Streamlit • Plotly • Scikit-Learn • OpenAI"
    )