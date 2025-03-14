import serial
import csv
import os
import threading

bluetooth_port = "COM17" 
baud_rate = 9600
ser = serial.Serial(bluetooth_port, baud_rate)

db_file = "gesture_database.csv"

if not os.path.exists(db_file):
    with open(db_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Thumb", "Index1", "Index2", "Middle1", "Middle2", "Label"])

def save_sign(values):
    label = input("\nIshora nomini kiriting ")  
    with open(db_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(values + [label])
    print(f"✅'{label}' ishorasi saqlandi!\n")

def read_sensor():
    while True:
        if ser.in_waiting:
            data = ser.readline().decode().strip()
            if data:
                global latest_values
                latest_values = list(map(int, data.split(',')))
                print(f"Flex qiymatlari: {latest_values}", end='\r')  # Overwrites the same line

latest_values = []
sensor_thread = threading.Thread(target=read_sensor, daemon=True)
sensor_thread.start()

def main():
    print("--- HANDSPEAK yozish rejimida ishlamoqda ---")
    print("Ishorani saqlash uchun ENTER'ni bosing")
    try:
        while True:
            input()
            if latest_values:
                save_sign(latest_values)
    except KeyboardInterrupt:
        print("\nDastur yopildi")
        ser.close()

if __name__ == "__main__":
    main()
