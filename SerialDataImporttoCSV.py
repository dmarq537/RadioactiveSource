# -*- coding: utf-8 -*-
"""
Serial Logger (last 4 whitespace-separated columns, no timestamp column)
- Creates a unique CSV file per run with date-time in the filename.
- Writes: Entry, Col2, Col3, Col4, Col5
- Skips lines with fewer than 5 columns.
"""

import csv
import time
from datetime import datetime
from pathlib import Path

import serial

# ---------------------------
# User configuration
# ---------------------------
SERIAL_PORT = 'COM3'       # Set to your device's COM port
BAUD_RATE = 9600           # Match your device's baud rate
LOG_INTERVAL_SECONDS = 1   # Time between reads (seconds)
OUTPUT_DIR = Path("logs")  # Directory to store CSV files

# ---------------------------
# Helper: build a unique filename with date-time stamp
# Example: logs/serial_last4_2025-10-06_15-18-42.csv
# ---------------------------
def make_output_path(base_dir: Path) -> Path:
    base_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return base_dir / f"serial_last4_{stamp}.csv"

# ---------------------------
# Core logger
# - Opens serial port with timeout
# - Parses each line by whitespace
# - Logs only the last 4 columns (i.e., skips the first)
# - Adds an incrementing Entry counter
# ---------------------------
def log_serial_last4_no_timestamp(port: str, baud: int, interval_s: float, out_dir: Path) -> None:
    csv_path = make_output_path(out_dir)
    ser = None
    entry_count = 1

    try:
        # Open serial port with a small timeout so readline() returns periodically
        ser = serial.Serial(port, baud, timeout=1)
        print(f"Connected to {port} @ {baud} baud")
        print(f"Writing to: {csv_path}")

        with csv_path.open('w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Header (no timestamp column)
            writer.writerow(['Entry', 'Col2', 'Col3', 'Col4', 'Col5'])

            while True:
                # Read a line, decode bytes -> str, strip trailing newline/whitespace
                raw_line = ser.readline().decode(errors='ignore').strip()

                if raw_line:
                    # Split by any amount of whitespace (fits Arduino's spaced columns)
                    cols = raw_line.split()

                    # Expect at least 5 columns; skip malformed lines silently
                    if len(cols) >= 5:
                        # Skip the first column; take the next four
                        last_four = cols[1:5]
                        writer.writerow([entry_count] + last_four)
                        f.flush()  # ensure data is written to disk promptly
                        print(f"[{entry_count}] {last_four}")
                        entry_count += 1

                time.sleep(interval_s)

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("Stopped by user (Ctrl+C).")
    finally:
        if ser is not None and ser.is_open:
            ser.close()
            print("Serial port closed.")

# ---------------------------
# Entrypoint
# ---------------------------
if __name__ == "__main__":
    log_serial_last4_no_timestamp(
        port=SERIAL_PORT,
        baud=BAUD_RATE,
        interval_s=LOG_INTERVAL_SECONDS,
        out_dir=OUTPUT_DIR,
    )
