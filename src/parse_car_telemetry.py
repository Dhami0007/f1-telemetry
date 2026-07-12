from pathlib import Path
import struct
import csv

RAW_DIR = Path("data/raw")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PACKET_TYPES = {
    6: "Car Telemetry"
}

HEADER_FORMAT = "<HBBBBBQfIIBB"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

CAR_TELEMETRY_FORMAT = "<HfffBbHBBH4H4B4BH4f4B"
CAR_TELEMETRY_SIZE = struct.calcsize(CAR_TELEMETRY_FORMAT)

TOTAL_CARS = 22

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

def decode_car_telemetry(data, car_index):
    offset = HEADER_SIZE + car_index * CAR_TELEMETRY_SIZE
    values = struct.unpack_from(CAR_TELEMETRY_FORMAT, data, offset)

    return {
        "speed_kph": values[0],
        "throttle": values[1],
        "steer": values[2],
        "brake": values[3],
        "clutch": values[4],
        "gear": values[5],
        "engine_rpm": values[6],
        "drs": values[7],
        "rev_lights_percent": values[8],
        "rev_lights_bit_value": values[9],

        "brake_temp_rl": values[10],
        "brake_temp_rr": values[11],
        "brake_temp_fl": values[12],
        "brake_temp_fr": values[13],

        "tyre_surface_temp_rl": values[14],
        "tyre_surface_temp_rr": values[15],
        "tyre_surface_temp_fl": values[16],
        "tyre_surface_temp_fr": values[17],

        "tyre_inner_temp_rl": values[18],
        "tyre_inner_temp_rr": values[19],
        "tyre_inner_temp_fl": values[20],
        "tyre_inner_temp_fr": values[21],

        "engine_temp": values[22],

        "tyre_pressure_rl": values[23],
        "tyre_pressure_rr": values[24],
        "tyre_pressure_fl": values[25],
        "tyre_pressure_fr": values[26],

        "surface_type_rl": values[27],
        "surface_type_rr": values[28],
        "surface_type_fl": values[29],
        "surface_type_fr": values[30]
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

            if header["packet_id"] != 6:
                continue
            
            player_index = header["player_car_index"]

            telemetry = decode_car_telemetry(data, player_index)

            rows.append({
                "timestamp": row["timestamp"],
                "session_time": header["session_time"],
                "frame_identifier": header["frame_identifier"],
                "player_car_index": player_index,
                **telemetry
            })
        
    if not rows:
        print("No Car Telemetry packets found")
        return
    
    output_file = OUTPUT_DIR / "player_car_telemetry.csv"

    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    
    print(f"Decoded {len(rows)} player telemetry rows")
    print(f"Saved to {output_file}")

main()