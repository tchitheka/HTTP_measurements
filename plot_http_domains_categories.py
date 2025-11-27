import pandas as pd
import matplotlib.pyplot as plt

# Load CSV file
df = pd.read_csv("categorized_domains.csv")

# Count categories and sort from highest to lowest
category_counts = df["Category"].value_counts().head(25).sort_values(ascending=True)

# Plot horizontal bar chart
plt.figure(figsize=(10, 8))
category_counts.plot(kind="barh")

plt.title("Top 25 Domain Categories")
plt.xlabel("Number of Domains")
plt.ylabel("Category")

plt.tight_layout()
plt.show()
