import serial
import csv
import os

bluetooth_port = "COM17"
baud_rate = 9600
ser = serial.Serial(bluetooth_port, baud_rate)

db_file = "gesture_database.csv"

gesture_db = []

if os.path.exists(db_file):
    with open(db_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            values = list(map(float, row[:-1]))
            label = row[-1]
            gesture_db.append((values, label))

def recognize_gesture(sensor_values):
    flex_tolerance = 10  # for flex sensors
    motion_tolerance = 0.5  # for gyro/accel

    for stored_values, label in gesture_db:
        match = True
        for i in range(len(sensor_values)):
            tol = flex_tolerance if i < 10 else motion_tolerance
            if abs(sensor_values[i] - stored_values[i]) > tol:
                match = False
                break
        if match:
            return label
    return None

def main():
    print("--- 🧠 HANDSPEAK tarjima rejimida ishlamoqda ---")
    last_recognized = None

    try:
        while True:
            if ser.in_waiting:
                data = ser.readline().decode().strip()
                parts = data.split(',')
                if len(parts) == 22:
                    try:
                        sensor_values = list(map(float, parts))
                        recognized_label = recognize_gesture(sensor_values)

                        if recognized_label and recognized_label != last_recognized:
                            print(f"\n✅ Taniqdi: {recognized_label}")
                            last_recognized = recognized_label
                        elif recognized_label is None:
                            last_recognized = None
                    except ValueError:
                        print("⚠️ Format xatosi!")
                else:
                    print(f"⚠️ Noto‘g‘ri uzunlikdagi ma’lumot: {len(parts)}")
    except KeyboardInterrupt:
        print("\n❌ Dastur yopildi.")
        ser.close()

if __name__ == "__main__":
    main()
