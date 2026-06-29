from app.analysis.visualization import plot_anomalies
from app.data.fetcher import test
from app.data.preprocessing import testdata
from app.models.anomaly import detect_anomalies

import matplotlib.pyplot as plt

data=test()

prepared_data=testdata(data)

anomalies=detect_anomalies(prepared_data)

anomaly_days = anomalies[anomalies["Anomaly"] == -1]

print(f"Total Trading Days : {len(anomalies)}")
print(f"Anomalies Detected : {len(anomaly_days)}")
print(
    f"Percentage         : {100 * len(anomaly_days) / len(anomalies):.2f}%"
)

fig=plot_anomalies(anomalies)

plt.show()

print(
    anomaly_days[
        ["Date", "Close", "Anomaly_Score"]
    ]
)

