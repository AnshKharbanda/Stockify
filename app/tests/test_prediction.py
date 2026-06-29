from app.data.fetcher import test
from app.data.preprocessing import testdata
from app.models.prediction import predict_stock
from app.analysis.visualization import plot_forecast

import matplotlib.pyplot as plt

# Fetch historical data
historical_df = test()

# Preprocess data
historical_df = testdata(historical_df)

# Generate forecast
forecast_df = predict_stock(historical_df)

# Plot
fig = plot_forecast(
    historical_df=historical_df,
    forecast_df=forecast_df,
)

plt.show()

print(forecast_df.head())

print(forecast_df.tail())