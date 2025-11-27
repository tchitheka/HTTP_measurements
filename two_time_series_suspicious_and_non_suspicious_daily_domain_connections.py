import pandas as pd
import matplotlib.pyplot as plt

# ============================================
# 1. Load suspicious timestamps
# ============================================
df_bad = pd.read_csv("suspicious_domains_timestamps.csv")

df_bad["datetime"] = pd.to_datetime(df_bad["timestamp"], unit="s")
df_bad["date"] = df_bad["datetime"].dt.date

daily_bad = (
    df_bad.groupby("date")
    .size()
    .reset_index(name="suspicious_connections")
)

# ============================================
# 2. Load non-suspicious timestamps
# ============================================
df_good = pd.read_csv("non_suspicious_timestamps.csv")

df_good["datetime"] = pd.to_datetime(df_good["timestamp"], unit="s")
df_good["date"] = df_good["datetime"].dt.date

daily_good = (
    df_good.groupby("date")
    .size()
    .reset_index(name="non_suspicious_connections")
)

# ============================================
# 3. Merge for plotting
# ============================================
df_plot = pd.merge(
    daily_bad,
    daily_good,
    on="date",
    how="outer"
).sort_values("date")

df_plot = df_plot.fillna(0)

# ============================================
# 4. Normalize to 0–1
# ============================================
df_plot["norm_suspicious"] = (
    df_plot["suspicious_connections"] / df_plot["suspicious_connections"].max()
)

df_plot["norm_non_suspicious"] = (
    df_plot["non_suspicious_connections"] / df_plot["non_suspicious_connections"].max()
)

# ============================================
# 5. Plot normalized curves
# ============================================
plt.figure(figsize=(15, 7))

plt.plot(
    df_plot["date"],
    df_plot["norm_suspicious"],
    label="Suspicious lookups",
    linewidth=2
)

plt.plot(
    df_plot["date"],
    df_plot["norm_non_suspicious"],
    label="Non-Suspicious lookups",
    linewidth=2
)

plt.title("Daily DNS lookups ")
plt.xlabel("Date")
plt.ylabel("Normalized Scale (0–1)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
