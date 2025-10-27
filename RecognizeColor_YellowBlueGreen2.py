import cv2
import numpy as np
import serial
import time

# ⚙️ Kết nối với Arduino
arduino = serial.Serial('COM4', 9600)  # ⚠️ Thay COM3 bằng cổng Arduino thực tế
time.sleep(2)  # đợi Arduino khởi động

# 🎥 Mở webcam
cap = cv2.VideoCapture(0)

def detect_color(roi):
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # 🟢 Xanh lá
    green_lower = np.array([35, 80, 80])
    green_upper = np.array([85, 255, 255])

    # 🔵 Xanh dương
    blue_lower = np.array([90, 80, 80])
    blue_upper = np.array([130, 255, 255])

    # 🟡 Vàng
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([35, 255, 255])

    # Tạo mask cho từng màu
    mask_green = cv2.inRange(hsv, green_lower, green_upper)
    mask_blue = cv2.inRange(hsv, blue_lower, blue_upper)
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)

    # Tính tổng số pixel cho từng màu
    green_count = np.sum(mask_green)
    blue_count = np.sum(mask_blue)
    yellow_count = np.sum(mask_yellow)

    # Xác định màu chiếm ưu thế
    max_color = max(green_count, blue_count, yellow_count)

    if max_color < 5000:  # ngưỡng lọc nhiễu
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

    # Lấy kích thước khung hình
    h, w, _ = frame.shape

    # Xác định vùng trung tâm để phân tích (ROI)
    roi_size = 100
    x1 = w//2 - roi_size//2
    y1 = h//2 - roi_size//2
    x2 = x1 + roi_size
    y2 = y1 + roi_size

    # Cắt vùng ROI
    roi = frame[y1:y2, x1:x2]

    # Nhận diện màu trong ROI
    color = detect_color(roi)

    # Vẽ khung ROI trên video
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
    cv2.putText(frame, f"Detected: {color}", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Color Sorting Simulation", frame)

    # Gửi tín hiệu đến Arduino
    if color == "green":
        arduino.write(b'G')
        print("green")

    elif color == "blue":
        arduino.write(b'B')
        print("blue")

    elif color == "yellow":
        arduino.write(b'Y')
        print("yellow")


    # Thoát khi nhấn phím 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()
