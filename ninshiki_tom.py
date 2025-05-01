from ultralytics import YOLO
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import RPi.GPIO as GPIO
import sys
import cv2
import time

# Initialize the model (using a pre-trained YOLOv8 model)
model = YOLO(r'/home/taku/ドキュメント/zemi/zemi_code/best11.pt')
# Capture video from the camera
cap = cv2.VideoCapture(0)


# モーター制御用ピン
IN1 = 27
IN2 = 22
# SG90のピン設定
SERVO_PIN = 17  # SG90-1

MIN_DEGREE = -90       # 000 : -90degree
MAX_DEGREE = 90       # 180 : +90degree

# GPIO初期化
GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# 初期化
factory = PiGPIOFactory()
# min_pulse_width, max_pulse_width, frame_width =>SG90仕様
servo = AngularServo(SERVO_PIN, min_angle=MIN_DEGREE, max_angle=MAX_DEGREE, 
                    min_pulse_width=1/1000, max_pulse_width=2/1000, frame_width=1/50,
                    pin_factory=factory)

def stop_motor_and_servo(servo):
    # モーター停止
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    # サーボをニュートラル位置に戻す
    if servo:
        servo.angle = 0
        sleep(1.0)
    print("モーターとサーボを停止しました。")

def move_motor(servo):
    # モーターを正転させる
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    sleep(rotation_time)

    # モーター停止
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    sleep(2)  # 停止後の待機時間
    
    servo.angle = 40  
    sleep(2.0)
    servo.angle = 0
    sleep(2.0)
    
    # モーターを逆転させる
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    sleep(rotation_time)

    # モーター停止
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)


try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        boxes = results[0].boxes
        class_ids = boxes.cls
        confidences = boxes.conf
        class_names = results[0].names

        for class_id, confidence in zip(class_ids, confidences):
            if confidence > 0.5:
                object_name = class_names[int(class_id)]

                if object_name == 'can':
                    print("Can detected! Activating action for can...")
                    rotation_time = 10
                    move_motor(servo)

                elif object_name == 'plastic bottle':
                    print("Plastic bottle detected! Activating action for plastic bottle...")
                    rotation_time = 20
                    move_motor(servo)

        cv2.imshow("Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("強制終了やで")

finally:
    stop_motor_and_servo(servo)
    GPIO.cleanup()
    print("GPIOをクリーンアップしました。")
    cap.release()
    cv2.destroyAllWindows()





