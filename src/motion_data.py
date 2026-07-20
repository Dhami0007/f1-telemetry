import struct
from pathlib import Path
import csv

RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PACKET_TYPES = {
    0: "Motion"
}

HEADER_FORMAT = "<HBBBBBQfIIBB"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

MOTION_DATA_FORMAT = "<ffffffhhhhhhhhhfff"
MOTION_DATA_SIZE = struct.calcsize(MOTION_DATA_FORMAT)

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

def decode_motion_data(data, car_index):
    offset = HEADER_SIZE + car_index * MOTION_DATA_SIZE

    required_size = offset + MOTION_DATA_SIZE

    if len(data) < required_size:
        raise ValueError(
            f"Packet too short. Need {required_size} bytes, got {len(data)}."
        )

    values = struct.unpack_from(MOTION_DATA_FORMAT, data, offset)

    return {
        "world_pos_X": values[0],
        "world_pos_Y": values[1],
        "world_pos_Z": values[2],

        "world_velo_X": values[3],
        "world_velo_Y": values[4],
        "world_velo_Z": values[5],

        "world_fwd_dir_X": values[6],
        "world_fwd_dir_Y": values[7],
        "world_fwd_dir_Z": values[8],

        "world_rgt_dir_X": values[9],
        "world_rgt_dir_Y": values[10],
        "world_rgt_dir_Z": values[11],

        "gforce_lat": values[12],
        "gforce_long": values[13],
        "gforce_vert": values[14],

        "yaw": values[15],
        "pitch": values[16],
        "roll": values[17]
    }

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

            if header["packet_id"] != 0:
                continue
            
            player_index = header["player_car_index"]

            motion_data = decode_motion_data(data, player_index)

            rows.append({
                "timestamp": row["timestamp"],
                "session_time": header["session_time"],
                "frame_identifier": header["frame_identifier"],
                "player_car_index": player_index,
                **motion_data
            })
    
    if not rows:
        print("No Lap Data packets found")
        return
    
    output_file = OUTPUT_DIR / "motion_data.csv"

    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Decoded {len(rows)} motion data rows")
    print(f"Saved to {output_file}")

main()