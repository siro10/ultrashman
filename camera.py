#----------------------------------------------------#
#camera関数
    #.takepicture : 画像を取得しpicture_result下に保存する
#----------------------------------------------------#
import cv2

#保存画像ファイル名
image_path = "C:\c\code\git_zemi\picure_result\result.jpg"
# Webカメラの起動
cap = cv2.VideoCapture(1)

def takepicture():
    ret, frame = cap.read()
    if not ret:
        return -1
    #画像保存
    cv2.imwrite(image_path, frame)

#cap.release()