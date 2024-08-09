import serial
import requests
from datetime import datetime
import os

def receive_message():
    port = "/dev/serial0"  # 라즈베리 파이에서 기본 UART 포트
    baudrate = 9600

    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        ser.flushInput()  # 시리얼 버퍼를 초기화
        print(f"Connected to Arduino on {port}")
    except serial.SerialException as e:
        print(f"Could not open serial port {port}: {e}")
        return

    # 폴더가 없으면 생성
    folder_path = "refridge_images"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    try:
        while True:
            if ser.in_waiting > 0:
                try:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    print(f"Received message: {line}")
                    if line == "U":
                        print("Access granted. Door unlocked.")
                    elif line == "L":
                        print("Access granted. Door locked.")
                        try:
                            response = requests.get('http://192.168.50.252:80/capture')
                            if response.status_code == 200:
                                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                                image_filename = os.path.join(folder_path, f'image_{current_time}.jpg')
                                with open(image_filename, 'wb') as f:
                                    f.write(response.content)
                                print(f"Image captured and saved as {image_filename}")
                            else:
                                print(f"Failed to capture image, status code: {response.status_code}")
                        except requests.RequestException as e:
                            print(f"HTTP request failed: {e}")
                except UnicodeDecodeError as e:
                    print(f"Unicode decode error: {e}")
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        ser.close()
        print("Serial connection closed.")

# if __name__ == "__main__":
#     receive_message()
