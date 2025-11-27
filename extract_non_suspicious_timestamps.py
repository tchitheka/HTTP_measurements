import csv

all_ssl_log = "/home/takondwa/Desktop/focus/combined_logs/all_ssl.log"
bad_ts_csv = "suspicious_domains_timestamps.csv"
output_file = "non_suspicious_timestamps.csv"

# Load timestamps that SHOULD be excluded
exclude_timestamps = set()

with open(bad_ts_csv) as f:
    reader = csv.DictReader(f)
    for row in reader:
        exclude_timestamps.add(row["timestamp"].strip())

# Scan all_ssl.log and collect timestamps NOT in exclude list
clean_results = []

with open(all_ssl_log) as f:
    for line in f:
        if not line.startswith("#") and line.strip():
            ts = line.split()[0]
            if ts not in exclude_timestamps:
                clean_results.append(ts)

# Write results
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp"])
    for ts in clean_results:
        writer.writerow([ts])

print(f"Done! Saved non-suspicious timestamps to {output_file}")
