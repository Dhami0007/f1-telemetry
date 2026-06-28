from pathlib import Path
import struct
from collections import Counter
import csv

RAW_DIR = Path("data/raw")

# Packet types and header breakdown as per F1 2025 guidelines for telemetry export
# https://forums.ea.com/blog/f1-games-game-info-hub-en/ea-sports%E2%84%A2-f1%C2%AE25-2026-season-pack-udp-specification/12187347

PACKET_TYPES = {
    0: "Motion",
    1: "Session",
    2: "Lap Data",
    3: "Event",
    4: "Participants",
    5: "Car Setups",
    6: "Car Telemetry",  # What we are mainly interested in
    7: "Car Status",
    8: "Final Classification",
    9: "Lobby Info",
    10: "Car Damage",
    11: "Session History",
    12: "Tyre Sets",
    13: "Motion Ex",
    14: "Time Trial",
    15: "Lap Positions",
    16: "Car Telemetry 2"
}

HEADER_FORMAT = "<HBBBBBQfIIBB"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

def decode_header(packet_hex):
    data = bytes.fromhex(packet_hex)
    values = struct.unpack_from(HEADER_FORMAT, data, 0)

    return{
        "packet_format": values[0],
        "game_year": values[1],
        "game_major_version": values[2],
        "game_minor_version": values[3],
        "packet_version": values[4],
        "packet_id": values[5],
        "session_uid": values[6],
        "session_time": values[7],
        "frame_identifier": values[8],
        "overall_frame_identifier": values[9],
        "player_car_index": values[10],
        "secondary_player_car_index": values[11],
        "packet_size": len(data)
    }

def main():
    csv_files = sorted(RAW_DIR.glob("raw_udp_packets_*.csv"))

    if not csv_files:
        print("No raw UDP CSV files found in data/raw")
        return
    
    latest_file = csv_files[-1]
    print(f"Reading: {latest_file}")

    decoded_rows = list()
    packet_counter = Counter()

    with open(latest_file, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            header = decode_header(row["packet_hex"])
            packet_id = header["packet_id"]

            header["timestamp"] = row["timestamp"]
            header["packet_name"] = PACKET_TYPES.get(packet_id, "Unknown")

            decoded_rows.append(header)
            packet_counter[packet_id] += 1
    
    output_file = Path("data/processed/packet_headers.csv")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames = decoded_rows[0].keys())
        writer.writeheader()
        writer.writerows(decoded_rows)

    print("\nPacket counts:")

    for packet_id, count in sorted(packet_counter.items()):
        print(f"{packet_id}: {PACKET_TYPES.get(packet_id, 'Unknown')} = {count}")

    print(f"\nSaved decoded headers to: {output_file}")

main()