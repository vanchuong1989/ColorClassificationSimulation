#include <Servo.h>

Servo sorterServo;   // servo chính điều khiển cánh tay đẩy
char colorCode;      // ký tự nhận được từ Python

// Góc cho từng màu
int posGreen = 45;   // trái
int posYellow = 90;  // giữa
int posBlue = 135;   // phải

void setup() {
  Serial.begin(9600);
  sorterServo.attach(12);  // ⚠️ Servo nối chân D9 của Arduino
  sorterServo.write(posYellow); // khởi động ở vị trí giữa
}

void loop() {
  if (Serial.available() > 0) {
    colorCode = Serial.read();

    if (colorCode == 'G') {
      sorterServo.write(posGreen);
      Serial.println("Detected: Green");
    }
    else if (colorCode == 'Y') {
      sorterServo.write(posYellow);
      Serial.println("Detected: Yellow");
    }
    else if (colorCode == 'B') {
      sorterServo.write(posBlue);
      Serial.println("Detected: Blue");
    }

    delay(800);  // giữ vị trí 0.8s để servo xoay xong
    sorterServo.write(posYellow); // trở lại vị trí giữa sẵn sàng
  }
}
