import cv2
import numpy as np
import serial
import time
import threading
from playsound import playsound  # ✅ thư viện phát âm thanh

# ⚙️ Kết nối Arduino
arduino = serial.Serial('COM4', 9600)
time.sleep(2)

# 🎥 Mở webcam
cap = cv2.VideoCapture(0)

last_color = "none"
last_send_time = 0

def detect_color(roi):
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Dải màu HSV
    green_lower = np.array([35, 80, 80])
    green_upper = np.array([85, 255, 255])

    blue_lower = np.array([90, 80, 80])
    blue_upper = np.array([130, 255, 255])

    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([35, 255, 255])

    mask_green = cv2.inRange(hsv, green_lower, green_upper)
    mask_blue = cv2.inRange(hsv, blue_lower, blue_upper)
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)

    green_count = np.sum(mask_green)
    blue_count = np.sum(mask_blue)
    yellow_count = np.sum(mask_yellow)

    max_color = max(green_count, blue_count, yellow_count)
    if max_color < 5000:
        return "none"

    if max_color == green_count:
        return "green"
    elif max_color == blue_count:
        return "blue"
    elif max_color == yellow_count:
        return "yellow"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    roi_size = 100
    x1, y1 = w//2 - roi_size//2, h//2 - roi_size//2
    x2, y2 = x1 + roi_size, y1 + roi_size
    roi = frame[y1:y2, x1:x2]

    color = detect_color(roi)

    # Chỉ gửi khi màu thay đổi + trễ ít nhất 0.7s
    if color != last_color and color != "none" and (time.time() - last_send_time) > 0.7:
        if color == "green":
            arduino.write(b'G')
        elif color == "blue":
            arduino.write(b'B')
        elif color == "yellow":
            arduino.write(b'Y')

        print(f"Sent to Arduino: {color}")
        last_color = color
        last_send_time = time.time()
        threading.Thread(target=playsound, args=("sub_machine_gun_laser.mp3",), daemon=True).start()



    # Vẽ khung ROI
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
    cv2.putText(frame, f"Detected: {color}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Color Sorting Simulation", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
