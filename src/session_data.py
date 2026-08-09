import struct
from pathlib import Path
import csv

RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

TRACK_IDS = {
    0: "Melbourne",
    2: "Shanghai",
    3: "Sakhir (Bahrain)",
    4: "Catalunya",
    5: "Monaco",
    6: "Montreal",
    7: "Silverstone",
    9: "Hungaroring",
    10: "Spa",
    11: "Monza",
    12: "Singapore",
    13: "Suzuka",
    14: "Abu Dhabi",
    15: "Texas",
    16: "Brazil",
    17: "Austria",
    19: "Mexico",
    20: "Baku (Azerbaijan)",
    26: "Zandvoort",
    27: "Imola",
    29: "Jeddah",
    30: "Miami",
    31: "Las Vegas",
    32: "Losail",
    39: "Silverstone (Reverse)",
    40: "Austria (Reverse)",
    41: "Zandvoort (Reverse)",
    42: "Madrid"
}

PACKET_TYPES = {
    1: "Session"
}

HEADER_FORMAT = "<HBBBBBQfIIBB"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

TARGET_FORMAT = "<BbbBHBb"
TARGET_FORMAT_SIZE = struct.calcsize(TARGET_FORMAT)

# This function is same in decode_packet_header.py file
def decode_header(data):
    values = struct.unpack_from(HEADER_FORMAT, data, 0)

    return {
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
    }

def decode_session_data(data):
    offset = HEADER_SIZE

    required_size = offset + TARGET_FORMAT_SIZE

    if len(data) < required_size:
        raise ValueError(
            f"Packet too short. Need {required_size} bytes, got {len(data)}."
        )

    values = struct.unpack_from(TARGET_FORMAT, data, offset)

    track_id = values[-1]
    track_name = TRACK_IDS[track_id]

    return track_name.upper() + "GRAND PRIX"

def main():
    csv_files = sorted(RAW_DIR.glob("raw_udp_packets_*.csv"))

    if not csv_files:
        print("No raw UDP CSV files found in data/raw")
        return
    
    latest_file = csv_files[-1]
    print(f"Reading: {latest_file}")

    rows = list()
    
    with open(latest_file, newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            data = bytes.fromhex(row["packet_hex"])
            header = decode_header(data)

            if header["packet_id"] != 1:
                continue
            
            player_index = header["player_car_index"]

            track_name = decode_session_data(data)

            rows.append({
                "timestamp": row["timestamp"],
                "session_time": header["session_time"],
                "frame_identifier": header["frame_identifier"],
                "player_car_index": player_index,
                "track_name": track_name
            })
    
    if not rows:
        print("No Lap Data packets found")
        return
    
    output_file = OUTPUT_DIR / "session.csv"

    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Decoded {len(rows)} session data rows")
    print(f"Saved to {output_file}")

main()