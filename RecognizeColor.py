import cv2
import serial
import time
import numpy as np

# 🔌 Cập nhật cổng COM phù hợp (ví dụ: "COM3" hoặc "/dev/ttyUSB0")
arduino = serial.Serial(port='COM4', baudrate=9600, timeout=1)
#arduino = serial.Serial()
time.sleep(2)

def detect_color(frame):
    # Giảm kích thước ảnh để xử lý nhanh hơn
    resized = cv2.resize(frame, (200, 200))
    # Lấy vùng trung tâm
    h, w, _ = resized.shape
    cx, cy = w // 2, h // 2
    center_color = resized[cy, cx]

    # Lấy giá trị RGB trung tâm
    b, g, r = center_color
    color = "UNKNOWN"

    if r > 120 and r > g + 40 and r > b + 40:
        color = "RED"
    elif g > 120 and g > r + 40 and g > b + 40:
        color = "GREEN"
    elif r > 120 and g > 120 and b < 80:
        color = "YELLOW"

    return color, (r, g, b)

cap = cv2.VideoCapture(0)
prev_color = ""

while True:
    ret, frame = cap.read()
    if not ret:
        break

    color, (r, g, b) = detect_color(frame)
    cv2.putText(frame, f"{color}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
    cv2.rectangle(frame, (150,100), (470,380), (0,255,0), 2)
    cv2.imshow("Color Detection", frame)

    if color != prev_color and color != "UNKNOWN":
        print("Detected:", color)
        arduino.write((color + "\n").encode())
        prev_color = color
        time.sleep(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
arduino.close()
cv2.destroyAllWindows()
