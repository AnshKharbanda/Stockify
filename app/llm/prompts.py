def build_stock_prompt(
    company_info: dict,
    technicals: dict,
    anomalies: list,
    forecast: list,
) -> str:
    """
    Build the prompt for the stock analysis report.
    """

    return f"""
    You are an experienced financial analyst.

    Analyze the following stock data and generate a comprehensive report.

    ==========================
    COMPANY INFORMATION
    ==========================

    {company_info}

    ==========================
    LATEST TECHNICAL INDICATORS
    ==========================

    {technicals}

    ==========================
    ANOMALY DETECTION
    ==========================

    Detected Anomalies:
    {anomalies}

    ==========================
    30-DAY PRICE FORECAST
    ==========================

    {forecast}

    ==========================
    REPORT REQUIREMENTS
    ==========================

    Write a professional stock analysis report with the following sections:

    1. Company Overview
    - Briefly describe the company.
    - Mention its industry and business.

    2. Technical Analysis
    - Analyze RSI, MACD, SMA, EMA and Bollinger Bands.
    - Explain whether the stock appears bullish, bearish or neutral.

    3. Anomaly Analysis
    - Explain the detected anomalies.
    - Discuss whether they may indicate unusual market activity.

    4. Price Forecast
    - Summarize the expected price movement over the next 30 trading days.
    - Mention possible trends.

    5. Risk Analysis
    - Discuss technical and market risks.
    - Mention uncertainty in the prediction.

    6. Investment Outlook
    - Provide a balanced conclusion.
    - State whether the current technical picture appears positive, negative or neutral.
    - Do NOT guarantee future returns.
    - Clearly mention that this analysis is for educational purposes and not financial advice.

    Formatting Requirements:

    - Use Markdown.
    - Use headings.
    - Use bullet points where appropriate.
    - Keep the report professional and easy to understand.
    - Explain technical terms briefly.
    - Do not fabricate information that is not present in the provided data.
    """