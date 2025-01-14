##
#Python3.11.9
#author:Isogai_Hiroto
#date:2024/12/19
#画像(jpg/png)を用いたYOLOによる画像認識(β版)
#データセットはroboflowに公開しているものを用いた。
#ベータ版の構想を以下に示す。
    #1.タッチセンサが反応したら、カメラから画像を1秒に一回読み取る。(camera関数を作成)
    #2.画像中からカン・ペットボトルを読み取る。
    #3.リストになかったら燃やすごみとして処理する
    #4.モータの動作については別関数で処理する
#----------------------------------------------------------------------------------#
from ultralytics import YOLO
from PIL import Image
import cv2
import time
import RPi.GPIO as GPIO

#自作関数
import ninshiki_camera


#データセットの定義
model = YOLO(r'C:\c\code\runs\detect\train_1218\weights\best.pt')

GPIO.setmode(GPIO.BCM)
#GPIO18を入力端子設定
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#ここでセンサが反応したら作動
while True:
    sw_status = GPIO.input(18)    #ボタンの状態を保存。
    time.sleep(0.1)    #0・1秒停止
    if not(GPIO.input(18) == sw_status):    #もしもボタンに動きがあれば
            if(GPIO.input(18) == 0):    #ボタンが押されているならば
                im1 = ninshiki_camera.takepicture

                #結果の出力
                results = model.predict(source=im1, save=True, conf = 0.5)

                #結果の詳細(画像サイズ、分析結果)を出力
                for result in results:
                    #認識されたものがなければ終了
                    if (len(result.boxes.conf) == 0):
                        break

                    i = 0
                    num = len(result.boxes.conf)

                    #処理された数を読み取り、それがなにかによって処理を変える
                    if(i < num):
                        if(result.boxes.conf[i] > 0.5):
                            match result.boxes.cls[i]:
                                case 1:
                                    print('can')
                                case 2:
                                    print('pet')
                                case 8:
                                    print('pet')
                                case _:
                                    print('other')
                        i += 1
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
                time.sleep(1)

    if cv2.waitKey():
            break