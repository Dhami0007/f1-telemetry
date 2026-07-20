# This will use parse_car_telemetry.py & lap_data.py to combine the file
# based on frame identifier so we will have a better understanding of data altogether

# importing files
import parse_car_telemetry
import lap_data
import motion_data
import pandas as pd
from pathlib import Path

# helpers
DATA_DIR = Path("data/processed")
LAP_DATA_FILENAME = "lap_data.csv"
CAR_TELE_FILENAME = "player_car_telemetry.csv"
MOTION_DATA_FILENAME = "motion_data.csv"

def main():
    lap_data_df = pd.read_csv(DATA_DIR / LAP_DATA_FILENAME)
    car_tele_df = pd.read_csv(DATA_DIR / CAR_TELE_FILENAME)
    motion_data_df = pd.read_csv(DATA_DIR / MOTION_DATA_FILENAME)

    tele_lap_df = pd.merge(lap_data_df, car_tele_df, on="frame_identifier")
    tele_lap_motion_df = pd.merge(tele_lap_df, motion_data_df, on="frame_identifier")
    print(f"it has {len(tele_lap_motion_df.columns)} columns")

    tele_lap_motion_df.to_csv(DATA_DIR / "combined_data.csv", index=False)

main()