#----------------------------------------------------------------------------------#
#Python3.11.9
#author:Isogai_Hiroto
#date:2025/01/15
#Webカメラからを取得した画像(jpg/png)を用いたYOLOによる画像認識
#データセットはroboflowに公開しているものを用いた。
#動作の概要を以下に示す。
    #1.タッチセンサが反応したら、カメラから画像を1回読み取る。
    #2.反応して何もなかった場合、燃やすごみとして判断する。
    #3.画像中からカン・ペットボトルを読み取る。
    #4.リストになかったら燃やすごみとして処理する。
    #5.複数個あった場合は分別を使用者に勧めるために動作せず、音声出力を行う(予定)。
    #6.モータの動作については別関数で処理する。
    #7.全体の処理が終了したら、ファイルに最後の画像と処理済みの画像を保存。
#----------------------------------------------------------------------------------#
from ultralytics import YOLO
import cv2
import time
import os
import shutil
#import RPi.GPIO as GPIO
#自作関数
import voice

#データセットの定義(パスは適宜指定)
model = YOLO(r'C:\c\code\git_zemi\runs\detect\train_1218\weights\best.pt')

#GPIO.setmode(GPIO.BCM)
#GPIO18を入力端子設定(18想定で作成)
#GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
image_path = "result.jpg"
# Webカメラの起動
cap = cv2.VideoCapture(0)

#ここでセンサが反応したら作動
if not cap.isOpened():
    print("カメラを開くことができませんでした")
    exit()

print("Start Program")
while True:
    ret, frame = cap.read()
    if not ret:
        print("フレームを取得できませんでした")
        break
    cv2.imshow('Webcam', frame)
    key = cv2.waitKey(1) & 0xFF
    #sw_status = GPIO.input(18)    #ボタンの状態を保存。
    #time.sleep(0.1)    #0・1秒停止
    #if not(GPIO.input(18) == sw_status):    #もしもボタンに動きがあれば
            #if(GPIO.input(18) == 0):    #ボタンが押されているならば
    if key == ord('q'):
        #パスは適宜指定
        if os.path.exists(r'C:\c\code\git_zemi\runs\detect\predict\result.jpg'):
            os.remove(r'C:\c\code\git_zemi\runs\detect\predict\result.jpg')
        cv2.imwrite(image_path, frame)
        time.sleep(1)

        #結果の出力
        results = model.predict(source=image_path, save=True, conf = 0.35)

        #結果の詳細(画像サイズ、分析結果)を出力
        for result in results:
            #認識されたものがなければ燃えるゴミ
            if (len(result.boxes.conf) == 0):
                print("other")#ここに燃えるゴミのときのモータの動作を入れる。
                break

            i = 1
            num = len(result.boxes.conf)

            # Detection
            print('---boxes.xyxy---')
            print(result.boxes.xyxy)   # box with xyxy format, (N, 4)
            print('---boxes.xywh---')
            print(result.boxes.xywh)   # box with xywh format, (N, 4)
            print('---boxes.xyxyn---')
            print(result.boxes.xyxyn)  # box with xyxy format but normalized, (N, 4)
            print('---boxes.xywhn---')
            print(result.boxes.xywhn)  # box with xywh format but normalized, (N, 4)
            print('---boxes.conf---')
            print(result.boxes.conf)   # confidence score, (N, 1)
            print('---boxes.cls---')
            print(result.boxes.cls)    # cls, (N, 1)

            print(result.names)

            #処理された数を読み取り、1であればそれがなにかによって処理を変える
            if(i == num):
                match result.boxes.cls[0]:
                    case 1:
                        print('can')#ここにカンのときのモータの動作を入れる。
                        break
                    case 2:
                        print('pet')#ここにペットボトルのときのモータの動作を入れる。
                        break
                    case 8:
                        print('pet')#ここにペットボトルのときのモータの動作を入れる。
                        break
                    case _:
                        print('other')#ここに燃えるゴミのときのモータの動作を入れる。
                        break
            elif(i < num):
                voice.play("分別してください。")
                break
        else:
            continue
        break

#ファイルの移動(パスは適宜指定)
new_path = shutil.move(r'C:\c\code\git_zemi\result.jpg', r'C:\c\code\git_zemi\runs\detect\predict')
#print(new_path)

#最後の写真を判定し保存(パスは適宜指定)
results = model.predict(r'C:\c\code\git_zemi\runs\detect\predict', project = "runs/detect/predict", name = "2024_1219jikken",save=True, show_labels = True, show_conf = True,conf=0.35)