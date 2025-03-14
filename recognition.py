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
        next(reader) 
        for row in reader:
            values = list(map(int, row[:-1])) 
            label = row[-1]  
            gesture_db.append((values, label))

def recognize_gesture(sensor_values):
    tolerance = 5  
    for stored_values, label in gesture_db:
        if all(abs(sensor_values[i] - stored_values[i]) <= tolerance for i in range(len(sensor_values))):
            return label  
    return None  

def main():
    print("--- HANDSPEAK tarjima rejimida ishlamoqda ---")
    print("Qo'lqopdan ma'lumotlar olinmoqda...")

    last_recognized = None 

    try:
        while True:
            if ser.in_waiting:
                data = ser.readline().decode().strip()
                if data:
                    sensor_values = list(map(int, data.split(',')))
                    recognized_label = recognize_gesture(sensor_values)

                    if recognized_label and recognized_label != last_recognized:
                        print(f"\n✅ Ishora: {recognized_label}")
                        last_recognized = recognized_label 
                    elif recognized_label is None:
                        last_recognized = None  

    except KeyboardInterrupt:
        print("\nDastur yopildi")
        ser.close()

if __name__ == "__main__":
    main()
