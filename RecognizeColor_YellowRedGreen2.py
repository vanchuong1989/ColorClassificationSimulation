import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w, _ = frame.shape
    x1, y1 = w // 2 - 50, h // 2 - 50
    x2, y2 = w // 2 + 50, h // 2 + 50
    roi = frame[y1:y2, x1:x2]

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    avg_hsv = np.mean(hsv.reshape(-1, 3), axis=0)
    h_val, s_val, v_val = avg_hsv

    color = "UNKNOWN"

    # --- RED (mở rộng vùng nhận diện và giới hạn S để tránh trắng phản sáng) ---
    if ((0 <= h_val <= 15) or (160 <= h_val <= 180)) and s_val > 70 and v_val > 60:
        color = "RED"
    # --- YELLOW ---
    elif 15 < h_val <= 45 and s_val > 80 and v_val > 70:
        color = "YELLOW"
    # --- GREEN ---
    elif 45 < h_val <= 85 and s_val > 70 and v_val > 60:
        color = "GREEN"

    # --- Hiển thị ---
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
    cv2.putText(frame, f"Color: {color}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(frame, f"H:{int(h_val)} S:{int(s_val)} V:{int(v_val)}",
                (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

    cv2.imshow("Color Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
