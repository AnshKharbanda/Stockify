import streamlit as st


def company_overview(company: dict):
    """
    Display company overview.
    """

    st.subheader("🏢 Company Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Company",
        company.get("company_name", "--"),
    )

    c2.metric(
        "Sector",
        company.get("sector", "--"),
    )

    c3.metric(
        "Industry",
        company.get("industry", "--"),
    )

    c4, c5, c6 = st.columns(3)

    c4.metric(
        "Market Cap",
        f"${company.get('market_cap', 0):,}"
        if company.get("market_cap")
        else "--",
    )

    c5.metric(
        "Employees",
        f"{company.get('employees', 0):,}"
        if company.get("employees")
        else "--",
    )

    c6.metric(
        "Exchange",
        company.get("exchange", "--"),
    )

    st.markdown(f"**Country:** {company.get('country', '--')}")
    st.markdown(f"**Currency:** {company.get('currency', '--')}")

    website = company.get("website")

    if website:
        st.markdown(f"**Website:** {website}")

    st.markdown("---")

    st.subheader("📖 Company Summary")

    st.write(company.get("summary", "No summary available."))


def technical_cards(technicals: dict):
    """
    Display latest technical indicators.
    """

    st.subheader("📊 Technical Indicators")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "RSI",
        round(technicals.get("RSI", 0), 2),
    )

    c2.metric(
        "MACD",
        round(technicals.get("MACD", 0), 2),
    )

    c3.metric(
        "SMA 20",
        round(technicals.get("SMA_20", 0), 2),
    )

    c4.metric(
        "EMA 20",
        round(technicals.get("EMA_20", 0), 2),
    )

    c5.metric(
        "MACD Signal",
        round(technicals.get("MACD_Signal", 0), 2),
    )


def report_section(report: str):
    """
    Display AI generated report.
    """

    st.subheader("🤖 AI Stock Analysis Report")

    if not report:
        st.warning(
            "AI Report is currently unavailable."
        )
        return

    st.markdown(report)