import pandas as pd

# Paths to your files
uid_file = "http_connections.csv"           # CSV containing a column named 'uid'
conn_file = "/home/takondwa/Desktop/focus/combined_logs/all_conn.log"
output_file = "filtered_conn.csv"           # CSV output

# Read UID list
uids = pd.read_csv(uid_file)['uid'].astype(str).tolist()

# Prepare lists to store extracted rows
records = []

# Read the conn.log file
with open(conn_file, "r") as f:
    for line in f:
        if line.startswith("#fields"):
            # Extract Zeek headers
            headers = line.strip().split("\t")[1:]
        elif line.startswith("#"):
            continue
        else:
            parts = line.strip().split("\t")
            if len(parts) == len(headers):     # Ensure line matches header length
                row = dict(zip(headers, parts))
                if row.get("uid") in uids:
                    records.append(row)

# Convert to DataFrame and save as CSV
df = pd.DataFrame(records)
df.to_csv(output_file, index=False)

print("Done. Saved:", output_file)
