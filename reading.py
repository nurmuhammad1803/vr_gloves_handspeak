import serial
import csv
import os
import threading

bluetooth_port = "COM17"
baud_rate = 9600
ser = serial.Serial(bluetooth_port, baud_rate)

db_file = "gesture_database.csv"

headers = ["Flex1", "Flex2", "Flex3", "Flex4", "Flex5", "Flex6", "Flex7", "Flex8", "Flex9", "Flex10",
           "GyroR_X", "GyroR_Y", "GyroR_Z", "AccR_X", "AccR_Y", "AccR_Z",
           "GyroL_X", "GyroL_Y", "GyroL_Z", "AccL_X", "AccL_Y", "AccL_Z", "Label"]

if not os.path.exists(db_file):
    with open(db_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)

latest_values = []

def save_sign(values):
    label = input("\n✍️ Ishora nomini kiriting: ")
    with open(db_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(values + [label])
    print(f"✅ '{label}' ishorasi saqlandi!\n")

def read_sensor():
    global latest_values
    while True:
        if ser.in_waiting:
            data = ser.readline().decode().strip()
            parts = data.split(',')
            if len(parts) == 22:
                try:
                    latest_values = list(map(float, parts))
                    print(f"📡 Qabul qilindi: {latest_values}", end='\r')
                except ValueError:
                    print("⚠️ Xatolik: Raqam formatida emas!")
            else:
                print(f"⚠️ Noto‘g‘ri uzunlikdagi ma’lumot: {len(parts)} element")

sensor_thread = threading.Thread(target=read_sensor, daemon=True)
sensor_thread.start()

def main():
    print("--- 🖐 HANDSPEAK yozish rejimida ishlamoqda ---")
    print("Ishorani saqlash uchun ENTER bosing...")
    try:
        while True:
            input()
            if latest_values:
                save_sign(latest_values)
    except KeyboardInterrupt:
        print("\n❌ Dastur to‘xtatildi.")
        ser.close()

if __name__ == "__main__":
    main()
