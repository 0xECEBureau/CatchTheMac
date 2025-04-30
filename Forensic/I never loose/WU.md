```python
#!/usr/bin/env python3
"""
Anomaly detection for Counter-Strike LAN PCAPs.

This script provides two detectors:
  1. Health anomaly detector: finds packets with HP > threshold (default 100).
  2. Cheat event detector: finds packets containing the "SHOOT_ALL" event.

Usage:
  python detect_anomalies.py <pcap_file> [--health] [--events] [--health-threshold N]

If neither --health nor --events is specified, both detectors run.
"""

import re
import argparse
from scapy.all import rdpcap, Raw


def detect_health_anomalies(packets, threshold):
    """
    Scan packets for HP values above the threshold.
    """
    print(f"\n[+] Scanning for health anomalies (HP > {threshold})...")
    count = 0
    for pkt in packets:
        if Raw in pkt:
            try:
                payload = pkt[Raw].load.decode('utf-8', errors='ignore')
            except Exception:
                continue
            m = re.search(r'HP:(\d+)', payload)
            if m and int(m.group(1)) > threshold:
                count += 1
                print(f"  - Anomaly #{count}: {payload} | Packet: {pkt.summary()} | Time: {pkt.time}")
    if count == 0:
        print("  No health anomalies found.")


def detect_cheat_events(packets):
    """
    Scan packets for the cheating event (KILL_ALL).
    """
    print("\n[+] Scanning for cheat events (KILL_ALL)...")
    count = 0
    for pkt in packets:
        if Raw in pkt:
            try:
                payload = pkt[Raw].load.decode('utf-8', errors='ignore')
            except Exception:
                continue
            if 'CMD:KILL_ALL' in payload:
                count += 1
                print(f"  - Cheat Event #{count}: {payload} | Packet: {pkt.summary()} | Time: {pkt.time}")
    if count == 0:
        print("  No cheat events found.")


def main():
    parser = argparse.ArgumentParser(description="Detect anomalies in a CS LAN PCAP.")
    parser.add_argument('pcap_file', help='Path to the PCAP file to analyze')
    parser.add_argument('--health', action='store_true', help='Detect health anomalies (HP > threshold)')
    parser.add_argument('--events', action='store_true', help='Detect cheat event packets (SHOOT_ALL)')
    parser.add_argument('--health-threshold', type=int, default=100,
                        help='Threshold for HP anomalies (default: 100)')
    args = parser.parse_args()

    packets = rdpcap(args.pcap_file)

    # Determine which detectors to run
    run_health = args.health or not (args.health or args.events)
    run_events = args.events or not (args.health or args.events)

    if run_health:
        detect_health_anomalies(packets, args.health_threshold)
    if run_events:
        detect_cheat_events(packets)


if __name__ == '__main__':
    main()
```

`python3 solver.py cs_lan_with_junk_and_events.pcap --health --events`
