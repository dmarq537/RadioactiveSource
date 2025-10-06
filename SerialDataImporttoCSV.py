# -*- coding: utf-8 -*-
"""
Serial Logger (Last 4 Cols, No Timestamp )
"""

import serial
import csv
import time

# --- Configuration ---
SERIAL_PORT = 'COM3'       # change to your board's port
BAUD_RATE = 9600          # match your device's baud rate
CSV_FILENAME = 'serial_4_sources.csv'
LOG_INTERVAL_SECONDS = 1

def log_serial_data_to_csv(port, baud_rate, filename):
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f" Connected to {port} @ {baud_rate} baud.")

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Header row: no timestamp
            writer.writerow(['Entry', 'Col2', 'Col3', 'Col4', 'Col5'])

            entry_count = 1
            print(f"Logging to {filename} (last 4 cols, no timestamp). Ctrl+C to stop.")

            while True:
                raw_line = ser.readline().decode(errors='ignore').strip()

                if raw_line:
                    # Split by whitespace
                    cols = raw_line.split()

                    # Take the last 4 columns (skip first)
                    if len(cols) >= 5:
                        last_four = cols[1:5]
                        writer.writerow([entry_count] + last_four)
                        csvfile.flush()
                        print(f"[{entry_count}] {last_four}")
                        entry_count += 1

                time.sleep(LOG_INTERVAL_SECONDS)

    except serial.SerialException as e:
        print(f"Serial error: {e}")
    except KeyboardInterrupt:
        print("\nLogging stopped by user.")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
            print(" Serial port closed.")

if __name__ == "__main__":
    log_serial_data_to_csv(SERIAL_PORT, BAUD_RATE, CSV_FILENAME)
