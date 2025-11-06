from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO('yolo11n.pt')  # 必要に応じてモデルを変更
    model.train(data='C:\c\code\Ultimate.yolov11\data.yaml', epochs=64, imgsz=640)