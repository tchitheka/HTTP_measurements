import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Load CSV (domain,timestamp)
# -----------------------------
df = pd.read_csv("suspicious_domains_timestamps.csv")

# Convert UNIX timestamp → datetime
df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")

# Extract date only
df["date"] = df["datetime"].dt.date

# -----------------------------
# Aggregate ALL domains per day
# -----------------------------
daily_total = (
    df.groupby("date")
    .size()
    .reset_index(name="total_connections")
)

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(14, 7))
plt.plot(daily_total["date"], daily_total["total_connections"])

plt.title("Daily Number of Connections to All Malicious Domains")
plt.xlabel("Date")
plt.ylabel("Total Connections")
plt.grid(True)
plt.tight_layout()

plt.show()
