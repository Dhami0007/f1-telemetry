import matplotlib.pyplot as plt
import pandas as pd
import os

def fetch_data(file):
    df = pd.read_csv(file)
    return df
    
def make_plot(data):
    data.plot(x="session_time", y="speed_kph")

    data.plot(x="session_time", y="throttle")
   
    data.plot(x="session_time", y="brake")
    plt.show()

def main():
    car_tele_file = "./data/processed/player_car_telemetry.csv"
    car_tele_df = fetch_data(car_tele_file)
    
    make_plot(car_tele_df)

main()