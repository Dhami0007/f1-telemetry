# This will use parse_car_telemetry.py & lap_data.py to combine the file
# based on frame identifier so we will have a better understanding of data altogether

# importing files
import parse_car_telemetry
import lap_data
import pandas as pd
from pathlib import Path

# helpers
DATA_DIR = Path("data/processed")
LAP_DATA_FILENAME = "lap_data.csv"
CAR_TELE_FILENAME = "player_car_telemetry.csv"

def main():
    # creating the files
    parse_car_telemetry.main()
    lap_data.main()

    lap_data_df = pd.read_csv(DATA_DIR / LAP_DATA_FILENAME)
    car_tele_df = pd.read_csv(DATA_DIR / CAR_TELE_FILENAME)

    tele_lap_df = pd.merge(lap_data_df, car_tele_df, on="frame_identifier")
    print(tele_lap_df.head())
    print(f"it has {len(tele_lap_df.columns)} columns")

main()