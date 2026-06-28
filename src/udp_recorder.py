import socket
from pathlib import Path
import time
import csv

UDP_IP = "0.0.0.0"
UDP_PORT = 20777

OUTPUT_DIR = Path("data/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

timestamp = time.strftime("%Y%m%d_%H%M%S")
output_file = OUTPUT_DIR / f"raw_udp_packets_{timestamp}.csv"

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    print(f"Listening for F1 25 UDP packets on port {UDP_PORT}...")
    print(f"Press CTRL+C to stop recording.")

    packet_count = 0

    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp","packet_size","packet_hex"])

        try:
            while True:
                data, address = sock.recvfrom(4096)
                packet_count += 1

                writer.writerow([
                    time.time(),
                    len(data),
                    data.hex()
                ])

                if packet_count % 100 == 0:
                    print(f"Recorded {packet_count} packets...")
        
        except KeyboardInterrupt:
            print("\nRecording stopped!")
            print(f"Saved raw packets to: {output_file}")

main()