import struct
from pathlib import Path
import csv

RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PACKET_TYPES = {
    2: "Lap Data"
}

HEADER_FORMAT = "<HBBBBBQfIIBB"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

LAP_DATA_FORMAT = "<IIHBHBHBHBfffBBBBBBBBBBBBBBBHHBfB"
LAP_DATA_SIZE = struct.calcsize(LAP_DATA_FORMAT)

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

def decode_lap_data(data, car_index):
    offset = HEADER_SIZE + car_index * LAP_DATA_SIZE

    required_size = offset + LAP_DATA_SIZE

    if len(data) < required_size:
        raise ValueError(
            f"Packet too short. Need {required_size} bytes, got {len(data)}."
        )

    values = struct.unpack_from(LAP_DATA_FORMAT, data, offset)

    return {
        "last_lap_time": values[0],
        "current_lap_time": values[1],

        "sector_1_time_ms": values[2],
        "sector_1_time_min": values[3],
        "sector_2_time_ms": values[4],
        "sector_2_time_min": values[5],

        "delta_car_ahead_ms": values[6],
        "delta_car_ahead_min": values[7],
        "delta_race_leader_ms": values[8],
        "delta_race_leader_min": values[9],

        "lap_distance": values[10],
        "total_distance":values[11],

        "delta_safety_car": values[12],

        "car_position": values[13],
        "current_lap_num": values[14],
        
        "pit_status": values[15],
        "pit_stops_count": values[16],

        "sector": values[17],

        "current_lap_invalid": values[18],
        "penalties": values[19],
        "total_warnings": values[20],
        "corner_cutting_warnings": values[21],
        "unserved_drive_thru_pens_count": values[22],
        "unserved_stop_go_pens_count": values[23],
        
        "grid_pos": values[24],
        "driver_status":  values[25],
        "result_status": values[26],

        "pitlane_timer_active": values[27],
        "pitlane_time_in_lane_ms": values[28],
        "pitstop_timer_ms": values[29],
        "pitstop_should_serve_pen": values[30],
        
        "speed_trap_fastest_speed": values[31],
        "speed_trap_fastest_lap": values[32]
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

            if header["packet_id"] != 2:
                continue
            
            player_index = header["player_car_index"]

            lap_data = decode_lap_data(data, player_index)

            rows.append({
                "timestamp": row["timestamp"],
                "session_time": header["session_time"],
                "frame_identifier": header["frame_identifier"],
                "player_car_index": player_index,
                **lap_data
            })
    
    if not rows:
        print("No Lap Data packets found")
        return
    
    output_file = OUTPUT_DIR / "lap_data.csv"

    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Decoded {len(rows)} lap data rows")
    print(f"Saved to {output_file}")

main()