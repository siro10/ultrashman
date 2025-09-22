import cv2
import sys
import numpy as np
from ultralytics import YOLO
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep
import RPi.GPIO as GPIO
import time
from gtts import gTTS
import pygame
import os
import math
# Initialize the model (using a pre-trained YOLOv8 model)
model = YOLO(r'/home/taku/ドキュメント/zemi/zemi_code/best11.pt')

# モーター制御用ピン
IN1 = 27
IN2 = 22

# SG90のピン設定
SERVO_PIN = 17  # SG90-1

MIN_DEGREE = -180       # 000 : -90degree
MAX_DEGREE = 180        # 180 : +90degree


REDLOW_COLOR1 = np.array([0, 150, 150])
REDHIGH_COLOR1 = np.array([20, 255, 255])
REDLOW_COLOR2 = np.array([150, 150, 150])
REDHIGH_COLOR2 = np.array([179, 255, 255])

BLUELOW_COLOR = np.array([100, 150, 150])
BLUEHIGH_COLOR = np.array([130, 255, 255])

YELLOWLOW_COLOR = np.array([20, 150, 150])
YELLOWHIGH_COLOR = np.array([30, 255, 255])

IMAGETRIPLITION_X = 4032//3 #画像の3分割点(x座標)
IMAGETRIPLITION_Y = 3024//3 #画像の3分割点(y座標)


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

def notify_label(label_text):
    tts = gTTS(text=f"{label_text}が見つかりました", lang='ja')
    tts.save("label_notify.mp3")
    
    pygame.mixer.init()
    pygame.mixer.music.load("label_notify.mp3")
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        continue

    os.remove("label_notify.mp3") 

def stop_motor_and_servo(servo):
    # モーター停止
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    # サーボをニュートラル位置に戻す
    if servo:
        servo.angle = 0
        sleep(1.0)
    print("モーターとサーボを停止しました。")

def move_motor(servo,angle):
    if angle = -1:
        return
    
    # モーターを正転させる
    servo.angle = angle
    sleep(3)
    
    
    GPIO.output(IN1,GPIO.HIGH)
    GPIO.output(IN1,GPIO.LOW)
    sleep(2)
    
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN1,GPIO.LOW)
    sleep(2)
    
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN1,GPIO.HIGH)
    sleep(2)
    
    GPIO.output(IN1,GPIO.LOW)
    GPIO.output(IN1,GPIO.LOW)

    
    # モーターを逆転させる
    servo.angle = 0  
    sleep(2)

    # モーター停止


def detect_target(frame, num):
    img = frame.copy()  
    #img = cv2.imread(frame)
    x_img = img.shape[0]
    y_img = img.shape[1]
    x_img_mask = 4032
    y_img_mask = IMAGETRIPLITION_Y
    x_start = 0
    y_start = IMAGETRIPLITION_Y*2
    img[y_start:y_start+y_img_mask, x_start:x_start+x_img_mask] = 0
    cv2.imwrite("mask_img.jpg", img)

    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)  # Convert RGB to YUV
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))  # Create CLAHE object
    img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0])  # Apply histogram equalization to luminance channel
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)  # Convert YUV back to RGB

    img_blur = cv2.blur(img, (15, 15))  # Apply smoothing filter

    hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)  # Convert BGR to HSV

    bin_img1 = cv2.inRange(hsv, REDLOW_COLOR1, REDHIGH_COLOR1)  # Create masks
    bin_img2 = cv2.inRange(hsv, REDLOW_COLOR2, REDHIGH_COLOR2)
    bin_img3 = cv2.inRange(hsv, BLUELOW_COLOR, BLUEHIGH_COLOR)
    bin_img4 = cv2.inRange(hsv, YELLOWLOW_COLOR, YELLOWHIGH_COLOR)
    redmask = bin_img1 + bin_img2  # Combine masks if needed
    bluemask = bin_img3
    yellowmask = bin_img4

    # Select mask based on object type (other=red, can=blue, bottle=yellow)
    match num:
        case 1:
            masked_img = cv2.bitwise_and(img_blur, img_blur, mask= bluemask)  # Extract specific color from original image
        case 2:
            masked_img = cv2.bitwise_and(img_blur, img_blur, mask= yellowmask)
        case _:
            masked_img = cv2.bitwise_and(img_blur, img_blur, mask= redmask)

    out_img = masked_img
    
    match num:
        case 1:
            num_labels, label_img, stats, centroids = cv2.connectedComponentsWithStats(bluemask) # 連結成分でラベリングする
        case 2:
            num_labels, label_img, stats, centroids = cv2.connectedComponentsWithStats(yellowmask) # 連結成分でラベリングする
        case _:
            num_labels, label_img, stats, centroids = cv2.connectedComponentsWithStats(redmask) # 連結成分でラベリングする
    
    #num_labels, label_img, stats, centroids = cv2.connectedComponentsWithStats(redmask)  # Label connected components
    num_labels = num_labels - 1  # Remove background label
    stats = np.delete(stats, 0, 0)
    centroids = np.delete(centroids, 0, 0)

    if num_labels >= 1:  # If labels exist
        max_index = np.argmax(stats[:, 4])  # Get index of largest area
        x = stats[max_index][0]
        y = stats[max_index][1]
        w = stats[max_index][2]
        h = stats[max_index][3]
        s = stats[max_index][4]
        mx = int(centroids[max_index][0])  # X coordinate of centroid
        my = int(centroids[max_index][1])  # Y coordinate of centroid
        cv2.rectangle(out_img, (x, y), (x+w, y+h), (255, 0, 255))  # Draw bounding box
        cv2.putText(out_img, "%d,%d"%(mx, my), (x-15, y+h+15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))  # Display centroid
        cv2.putText(out_img, "%d"%(s), (x, y+h+30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))  # Display area
        print(mx, my)
        print(x_img, y_img)

        cv2.imwrite("out_img.jpg", out_img)  # Save output image

        #回転する方向を指定(+135, +175(180はカメラ台に激突する), -135), (初期位置をカメラ台方向と仮定)
        if mx >= 0 and mx <= IMAGETRIPLITION_X:
            return 135
        elif mx >= IMAGETRIPLITION_X and mx <= IMAGETRIPLITION_X*2:
            return 175
        else:
            return -135
    else:
        print("Target not found!!")
        return -1




def main():
    has_dropped = False
    i = 0      # カウント変数
    # カメラのキャプチャ
    cap = cv2.VideoCapture(0)
    if cap.isOpened() is False:
        print("can not open camera")
        sys.exit()
 
    cap.set(cv2.CAP_PROP_FPS, 10)
    stop_motor_and_servo(servo)
    
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
                                    
                                    notify_label("缶")
                                    angle= detect_target(frame,1)
                                    move_motor(servo, angle)
                                    has_dropped = True
                                    ref = 0
                                    detected = True
                                    break
                                elif object_name == 'plastic bottle':
                                    print("Plastic bottle detected! Activating action for plastic bottle...")
                                    notify_label("ペットボトル")
                                    angle = detect_target(frame,2)
                                    move_motor(servo, angle)
                                    has_dropped = True
                                    ref = 0
                                    detected = True
                                    break

                        if not detected:
                            print("No target object detected. Activating action for burnable garbage...")
                            notify_label("燃えるゴミ")
                            angle = detect_target(frame,0)
                            move_motor(servo, angle)
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