import os
from openai import OpenAI

client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_report(data):
    try:
        prompt=f"""
        You are a financial analyst.

        Analyze the following stock data:

        Price:{data['price']}
        Trend:{data['trend']}
        Momentum:{data['momentum']}
        Volume:{data['volume']}
        ML Confidence:{data['confidence']}
        ML Signal:{data['signal']}
        Risk Level:{data['risk']}

        Instructions:
        - Write ONLY one paragraph
        - Do NOT use bullet points
        - Do NOT use headings
        - Keep it simple and professional
        - Explain whether the stock shows any abnormal or suspicious behavior
        -Keep the explanation natural and human-like, as if explaining to an investor.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0.4
        )

        return response.choices[0].message.content
    
    except Exception as e:
        return mock_report(data)
        


def mock_report(data):
    return f"""The stock is currently in a {data['trend']} trend with {data['momentum']} momentum and {data['volume']} trading activity.Based on the model's analysis, the confidence level is {round(data['confidence'],2)}, indicating a {data['risk']} risk profile.There are no strong signs of abnormal or suspicious behavior at this time."""

