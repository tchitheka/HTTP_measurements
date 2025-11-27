#!/bin/bash
#
# Combine Zeek logs from multiple PCAPs using Dockerized Zeek
# Keeps only the first header for each log type, removes repeated headers.
#

PCAP_DIR="."
OUTPUT_DIR="$PCAP_DIR/combined_logs"
mkdir -p "$OUTPUT_DIR"

ALL_SSL="$OUTPUT_DIR/all_ssl.log"
ALL_QUIC="$OUTPUT_DIR/all_quic.log"
ALL_PE="$OUTPUT_DIR/all_pe.log"

# Initialize output logs
> "$ALL_SSL"
> "$ALL_QUIC"
> "$ALL_PE"

echo "📦 Starting Zeek processing for PCAPs in: $PCAP_DIR"
echo "-----------------------------------------------------------"

first_ssl=true
first_quic=true
first_pe=true

for pcap in "$PCAP_DIR"/*.pcap; do
    [ -e "$pcap" ] || { echo "No .pcap files found."; exit 1; }

    echo "▶️ Processing: $(basename "$pcap")"

    docker run --rm -v "$(pwd)":/pcaps -w /pcaps zeek/zeek \
        zeek -r "$(basename "$pcap")" >/dev/null 2>&1

    # === Generic merge function ===
    merge_log() {
        local log_file=$1
        local output_file=$2
        local first_flag=$3

        if [ -f "$log_file" ]; then
            echo "  → Merging $log_file"
            if $first_flag; then
                cat "$log_file" >> "$output_file"
                eval "$3=false"
            else
                grep -v '^#' "$log_file" >> "$output_file"
            fi
        fi
    }

    # Merge only these logs
    merge_log "ssl.log" "$ALL_SSL" first_ssl
    merge_log "quic.log" "$ALL_QUIC" first_quic
    merge_log "pe.log" "$ALL_PE" first_pe

    # Clean temporary Zeek logs
    rm -f *.log *.json *.bro >/dev/null 2>&1

    echo "✅ Done with: $(basename "$pcap")"
    echo "-----------------------------------------------------------"
done

echo "🎉 All PCAPs processed successfully!"
echo "Combined logs saved in: $OUTPUT_DIR"
echo "  - $ALL_SSL"
echo "  - $ALL_QUIC"
echo "  - $ALL_PE"
