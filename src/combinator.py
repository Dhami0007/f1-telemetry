# This will use parse_car_telemetry.py & lap_data.py to combine the file
# based on frame identifier so we will have a better understanding of data altogether

# importing files
import parse_car_telemetry
import lap_data
import motion_data
import session_data
import pandas as pd
from pathlib import Path

# helpers
DATA_DIR = Path("data/processed")
LAP_DATA_FILENAME = "lap_data.csv"
CAR_TELE_FILENAME = "player_car_telemetry.csv"
MOTION_DATA_FILENAME = "motion_data.csv"
SESSION_DATA_FILENAME = "session.csv"

LAP_DATA_COLS = ["timestamp", "session_time", "frame_identifier", "player_car_index", "last_lap_time", 
                   "current_lap_time", "sector_1_time_ms", "sector_1_time_min", "sector_2_time_ms", 
                   "sector_2_time_min", "delta_car_ahead_ms", "delta_car_ahead_min", "delta_race_leader_ms", 
                   "delta_race_leader_min", "lap_distance", "total_distance", "speed_trap_fastest_speed", "speed_trap_fastest_lap", "current_lap_num"]

CAR_TELE_DATA_COLS = ["frame_identifier", "player_car_index", "speed_kph", "throttle", "steer", "brake", "clutch", "gear", "engine_rpm", 
                      "drs", "rev_lights_percent", "rev_lights_bit_value", "brake_temp_rl", "brake_temp_rr", "brake_temp_fl", "brake_temp_fr"]

MOTION_DATA_COLS = ["frame_identifier", "player_car_index", "world_pos_X", "world_pos_Y", "world_pos_Z", "world_velo_X", "world_velo_Y", "world_velo_Z"]

SESSION_DATA_COLS = ["frame_identifier", "track_name"]

def main():
    lap_data_df = pd.read_csv(DATA_DIR / LAP_DATA_FILENAME)[LAP_DATA_COLS]
    car_tele_df = pd.read_csv(DATA_DIR / CAR_TELE_FILENAME)[CAR_TELE_DATA_COLS]
    motion_data_df = pd.read_csv(DATA_DIR / MOTION_DATA_FILENAME)[MOTION_DATA_COLS]
    session_data_df = pd.read_csv(DATA_DIR / SESSION_DATA_FILENAME)[SESSION_DATA_COLS]

    tl_df = pd.merge(lap_data_df, car_tele_df, on="frame_identifier")   # telemetry & lap data
    tlm_df = pd.merge(tl_df, motion_data_df, on="frame_identifier")     # telemetry & lap data & motion
    tlms_df = pd.merge(tlm_df, session_data_df, on="frame_identifier")  # telemetry & lap data & motion & session                   

    print(f"it has {len(tlms_df.columns)} columns")

    tlms_df.to_csv(DATA_DIR / "combined_data.csv", index=False)

main()