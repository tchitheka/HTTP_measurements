import csv
import subprocess

domains_file = "suspicious_domains.csv"
ssl_log = "/home/takondwa/Desktop/focus/combined_logs/all_ssl.log"
output_file = "suspicious_domains_timestamps.csv"

results = []

# Load domain names
with open(domains_file) as f:
    reader = csv.DictReader(f)
    domains = [row["domain"].strip() for row in reader]

for domain in domains:
    ssl_cmd = f'grep -i "{domain}" {ssl_log}'
    ssl_output = subprocess.getoutput(ssl_cmd).splitlines()

    for line in ssl_output:
        # timestamp is always the first field
        parts = line.split()
        if len(parts) > 0:
            ts = parts[0]
            results.append([domain, ts])

# Save CSV
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["domain", "timestamp"])
    writer.writerows(results)

print(f"Done! Saved SSL timestamps to {output_file}")
