import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.collections import LineCollection

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

def trial_line_collection(data):

    points = list()
    segment_speeds = list()
    for index,row in data.iterrows():
        if row["current_lap_num"] == 4:
            points.append((row["world_pos_X"], row["world_pos_Z"]))
            segment_speeds.append(row["speed_kph"])

    # grid spec
    fig = plt.figure()
    gs = fig.add_gridspec(2,6)

    # line collections
    segments = list()

    # creating line segments
    n = len(points)
    i = 0
    while i < n-1:
        segments.append([points[i], points[i+1]])
        i += 1
    segments.append([points[-1], points[0]])

    # LC0
    ax0 = plt.subplot(gs[:, 0])
    line_seg = LineCollection(segments, linestyle = 'solid', cmap = "viridis", linewidth = 3)
    line_seg.set_array(segment_speeds)
    ax0.add_collection(line_seg)
    ax0.autoscale()
    ax0.set_aspect("equal")

    # LC1
    ax1 = plt.subplot(gs[:, 1])
    line_seg = LineCollection(segments, linestyle = 'solid', cmap = "plasma", linewidth = 3)
    line_seg.set_array(segment_speeds)
    ax1.add_collection(line_seg)
    ax1.autoscale()
    ax1.set_aspect("equal")

    # LC2
    ax2 = plt.subplot(gs[:, 2])
    line_seg = LineCollection(segments, linestyle = 'solid', cmap = "inferno", linewidth = 3)
    line_seg.set_array(segment_speeds)
    ax2.add_collection(line_seg)
    ax2.autoscale()
    ax2.set_aspect("equal")

    # LC3
    ax3 = plt.subplot(gs[:, 3])
    line_seg = LineCollection(segments, linestyle = 'solid', cmap = "magma", linewidth = 3)
    line_seg.set_array(segment_speeds)
    ax3.add_collection(line_seg)
    ax3.autoscale()
    ax3.set_aspect("equal")

    # LC4
    ax4 = plt.subplot(gs[:, 4])
    line_seg = LineCollection(segments, linestyle = 'solid', cmap = "cividis", linewidth = 3)
    line_seg.set_array(segment_speeds)
    ax4.add_collection(line_seg)
    ax4.autoscale()
    ax4.set_aspect("equal")

    # LC5
    ax5 = plt.subplot(gs[:, 5])
    line_seg = LineCollection(segments, linestyle = 'solid', cmap = "turbo", linewidth = 3)
    line_seg.set_array(segment_speeds)
    ax5.add_collection(line_seg)
    ax5.autoscale()
    ax5.set_aspect("equal")

    plt.show()

def make_heatmap(data):

    # fetching points and segment speeds
    points = list()
    segment_speeds = list()
    segment_throttle = list()
    segment_brake = list()
    for index,row in data.iterrows():
        if row["current_lap_num"] == 4:
            points.append((row["world_pos_X"], row["world_pos_Z"]))
            segment_speeds.append(row["speed_kph"])
            segment_throttle.append(row["throttle"])
            segment_brake.append(row["brake"])

    # line collections
    segments = list()

    # creating line segments
    n = len(points)
    i = 0
    while i < n-1:
        segments.append([points[i], points[i+1]])
        i += 1
    segments.append([points[-1], points[0]])

    # making plot

    # Speed Heatmap
    fig1, ax1 = plt.subplots(figsize=(4,6))
    line_seg1 = LineCollection(segments, linestyle = 'solid', cmap = "turbo", linewidth = 3)
    line_seg1.set_array(segment_speeds)
    fig1.colorbar(line_seg1, ax=ax1)
    ax1.set_title("Speed heatmap")
    ax1.add_collection(line_seg1)
    ax1.autoscale()
    ax1.axis("off")
    ax1.set_aspect("equal")

    # Throttle map
    fig2, ax2 = plt.subplots(figsize=(4,6))
    line_seg2 = LineCollection(segments, linestyle = 'solid', cmap = "turbo", linewidth = 3)
    line_seg2.set_array(segment_throttle)
    fig2.colorbar(line_seg2, ax=ax2)
    ax2.set_title("Throttle heatmap")
    ax2.add_collection(line_seg2)
    ax2.autoscale()
    ax2.axis("off")
    ax2.set_aspect("equal")

    # Braking Map
    fig3, ax3 = plt.subplots(figsize=(4,6))
    line_seg3 = LineCollection(segments, linestyle = 'solid', cmap = "turbo", linewidth = 3)
    line_seg3.set_array(segment_brake)
    fig3.colorbar(line_seg3, ax=ax3)
    ax3.set_title("Braking heatmap")
    ax3.add_collection(line_seg3)
    ax3.autoscale()
    ax3.axis("off")
    ax3.set_aspect("equal")

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