import matplotlib.pyplot as plt
import pandas as pd
import os

def fetch_data(file):
    df = pd.read_csv(file)
    return df
    
def make_tele_plot(data):
    data.plot(x="session_time", y="speed_kph")

    data.plot(x="session_time", y="throttle")
   
    data.plot(x="session_time", y="brake")
    plt.show()

def make_raceline(data):
    plt.figure(figsize=(8,8))

    plt.plot(
        data["world_pos_X"],
        data["world_pos_Z"]
    )

    plt.axis("equal")
    plt.xlabel("World x")
    plt.ylabel("World Z")
    plt.title("Race Line")

    plt.show()

def make_heatmap(data):
    plt.figure(figsize=(8,8))

    plt.scatter(
        data["world_pos_X"],
        data["world_pos_Z"],
        c=data["speed_kph"],
        s=4
    )

    plt.colorbar(label="Speed (km/h)")
    plt.show()

def main():
    car_tele_file = "./data/processed/player_car_telemetry.csv"
    car_tele_df = fetch_data(car_tele_file)
    
    # make_tele_plot(car_tele_df)

    motion_file = "./data/processed/motion_data.csv"
    motion_df = fetch_data(motion_file)

    # make_raceline(motion_df)

    combined_file = "./data/processed/combined_data.csv"
    combined_df = fetch_data(combined_file)

    make_heatmap(combined_df)


main()