import cv2
import sys
import numpy as np
from ultralytics import YOLO
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import RPi.GPIO as GPIO
import time


# Initialize the model (using a pre-trained YOLOv8 model)
model = YOLO(r'/home/taku/ドキュメント/zemi/zemi_code/best11.pt')


# モーター制御用ピン
IN1 = 27
IN2 = 22

# SG90のピン設定
SERVO_PIN = 17  # SG90-1

MIN_DEGREE = -90       # 000 : -90degree
MAX_DEGREE = 90        # 180 : +90degree

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


# 背景差分版
def capture(cap):
    ret,frame = cap.read()
    return cv2.resize(frame, (320, 240))
 
def mark(mask, frame):
        ref = 0
        # 動いているエリアの面積を計算してちょうどいい検出結果を抽出する
        thresh = cv2.threshold(mask, 3, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        max_area = 0
        areaf = 0
        if (contours):
            target = contours[0]
        for cnt in contours:
             #輪郭の面積を求めてくれるcontourArea
            area = cv2.contourArea(cnt)
            if max_area < area and area < 10000 and area > 800:
                max_area = area
                target = cnt
            # 動いているエリアのうちそこそこの大きさのものがあればそれを矩形で表示する
            if (max_area <= 800):
                areaf = frame
            else:
                # 諸般の事情で矩形検出とした。
                x,y,w,h = cv2.boundingRect(target)
                areaf = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                ref = 1
 
        return ref, areaf
def stop_motor_and_servo(servo):
    # モーター停止
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    # サーボをニュートラル位置に戻す
    if servo:
        servo.angle = 0
        sleep(1.0)
    print("モーターとサーボを停止しました。")

def move_motor(servo,rotation_time):
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


def main():
    has_dropped = False
    i = 0      # カウント変数
    # カメラのキャプチャ
    cap = cv2.VideoCapture(0)
    if cap.isOpened() is False:
        print("can not open camera")
        sys.exit()
 
    cap.set(cv2.CAP_PROP_FPS, 10)
    
    # 最初のフレームを背景画像に設定
    bg = capture(cap)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    #fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()に変えて試してほしい。 
    #重かったらfgbg = cv2.bgsegm.createBackgroundSubtractorCNT()で。

    # グレースケール変換
    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY) 
    ref = 0
    skip_count = 0
    while(cap.isOpened()):
        # フレームの取得
        frame = capture(cap)
 
        # グレースケール変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mask = fgbg.apply(gray)
        cv2.imshow("mask", mask)
        if( skip_count == 0 ):
            ref, areaframe = mark(mask, frame)

#-------------------------------------------------#
            #refが1のときは動いた判定なので
            #if(ref == 1):
                #ゴミが乗った後の動作
                #       |
                #       |
                #       |

            #という感じでお願いします
            if not has_dropped:   
                if(ref == 1):
                    
                    while True:                     
                        ret, frame = cap.read()
                        if not ret:
                            break

                        results = model(frame)
                        boxes = results[0].boxes
                        class_ids = boxes.cls
                        confidences = boxes.conf
                        class_names = results[0].names
                        detected = False
                        for class_id, confidence in zip(class_ids, confidences):
                            if confidence > 0.7:
                                object_name = class_names[int(class_id)]

                                if object_name == 'can':
                                    print("Can detected! Activating action for can...")
                                    rotation_time = 3
                                    move_motor(servo, rotation_time)
                                    has_dropped = True
                                    ref = 0
                                    detected = True
                                    break
                                elif object_name == 'plastic bottle':
                                    print("Plastic bottle detected! Activating action for plastic bottle...")
                                    rotation_time = 8
                                    move_motor(servo, rotation_time)
                                    has_dropped = True
                                    ref = 0
                                    detected = True
                                    break

                        if not detected:
                            print("No target object detected. Activating action for burnable garbage...")
                            rotation_time = 5
                            move_motor(servo, rotation_time)
                            has_dropped = True
                            ref = 0

                        if has_dropped:
                            break

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                                   
            
            else:
                if ref == 0:
                    has_dropped = False
#-------------------------------------------------#

            # フレームとマスク画像を表示
            cv2.imshow("areaframe", areaframe)
        skip_count = (skip_count + 1) % 30
        
        i += 1    # カウントを1増やす
        if (ref):
           i = 0
           ref = 0
 
        # 背景画像の更新（一定間隔）
        if(i > 1000):
            bg = capture(cap)
            bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY) 
            i = 0 # カウント変数の初期化
 
        # qキーが押されたら途中終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
 
    stop_motor_and_servo(servo)
    GPIO.cleanup()
    print("GPIOをクリーンアップしました。")
    cap.release()
    cv2.destroyAllWindows()
 
if __name__ == '__main__':
    main()