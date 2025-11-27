import pandas as pd
import matplotlib.pyplot as plt

# Load CSV (adjust separator if needed)
df = pd.read_csv("filtered_http_conn.csv")

# Convert Zeek timestamp to date
df['date'] = pd.to_datetime(df['ts'], unit='s').dt.date

# Group per day
daily = df.groupby('date')[['orig_bytes', 'resp_bytes']].sum()

# Convert bytes → megabytes (MiB)
daily_mb = daily / (1024 * 1024)
daily_mb.columns = ['outgoing_MB', 'incoming_MB']

# Plot stacked bar chart
plt.figure(figsize=(10, 6))
plt.bar(daily_mb.index, daily_mb['outgoing_MB'], label='Outgoing (MB)')
plt.bar(daily_mb.index, daily_mb['incoming_MB'], 
        bottom=daily_mb['outgoing_MB'], label='Incoming (MB)')

plt.title("Daily HTTP Traffic (Payload)")
plt.xlabel("Date")
plt.ylabel("Megabytes (MB)")
plt.xticks(rotation=45)

plt.legend()
plt.tight_layout()
plt.show()
