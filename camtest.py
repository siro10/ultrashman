import cv2

counter = 1
cap = cv2.VideoCapture(2)

if not cap.isOpened():
    print("カメラを開くことができませんでした")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("フレームを取得できませんでした")
        break

    cv2.imshow('Webcam', frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('s'):
        filename = f"image{counter:03d}.jpg"
        cv2.imwrite(filename, frame)
        print(f"画像を保存しました: {filename}")
        counter += 1

    if key == 27:  # ESCキーを押したらループを抜ける
        break

cap.release()
cv2.destroyAllWindows()