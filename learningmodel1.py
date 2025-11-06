from ultralytics import YOLO

# ベースとするモデル
model = YOLO('yolo11n.pt')

# M1 macのGPUを使ってモデルを学習
results = model.train(
    data="C:\c\code\Thesis.v31i.yolov11\data.yaml",
    epochs=9,
    imgsz=640,
    device='mps'
)