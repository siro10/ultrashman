from ultralytics import YOLO
import cv2
import time
# モデルを選択(使用するモデル(,ptファイル)を挿入)
#model = YOLO("yolo11s.pt")
model = YOLO(r'C:\c\code\git_zemi\detect\train22\weights\best.pt')
#model = YOLO(r'C:\c\code\git_zemi\detect\train21\weights\best.pt')
#model = YOLO(r'runs\detect\train6\weights\best.pt')

# 検出対象ファイル指定
#results = model("https://ultralytics.com/images/bus.jpg", save=True)

#画像ファイル
results = model(r"C:\c\code\jikken_picture\2024_1219jikken.jpg", save=True)
#動画ファイル
results = model("./images/test2.mp4", save=True)

for i in enumerate(results):
    # Detection
    print('---boxes.xyxy---')
    print(results.boxes.xyxy)   # box with xyxy format, (N, 4)
    print('---boxes.xywh---')
    print(results.boxes.xywh)   # box with xywh format, (N, 4)
    print('---boxes.xyxyn---')
    print(results.boxes.xyxyn)  # box with xyxy format but normalized, (N, 4)
    print('---boxes.xywhn---')
    print(results.boxes.xywhn)  # box with xywh format but normalized, (N, 4)
    print('---boxes.conf---')
    print(results.boxes.conf)   # confidence score, (N, 1)
    print('---boxes.cls---')
    print(results.boxes.cls)    # cls, (N, 1)

    print(results.names)
    time.sleep(10)