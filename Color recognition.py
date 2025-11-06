import cv2
import numpy as np
import math

# 赤色は２つの領域にまたがる
# np.array([色彩, 彩度, 明度])
# 各値は適宜設定する！！
REDLOW_COLOR1 = np.array([0, 150, 150]) # 各最小値を指定
REDHIGH_COLOR1 = np.array([20, 255, 255]) # 各最大値を指定
REDLOW_COLOR2 = np.array([150, 150, 150])
REDHIGH_COLOR2 = np.array([179, 255, 255])

BLUELOW_COLOR = np.array([100, 150, 150]) # 各最小値を指定
BLUEHIGH_COLOR = np.array([130, 255, 255]) # 各最大値を指定

YELLOWLOW_COLOR = np.array([20, 150, 150]) # 各最小値を指定
YELLOWHIGH_COLOR = np.array([30, 255, 255]) # 各最大値を指定

IMAGETRIPLITION_X = 4032//3 #画像の3分割点(x座標)
IMAGETRIPLITION_Y = 3024//3 #画像の3分割点(y座標)

def detect_target(img_name, num):
    img = cv2.imread(img_name) # 画像を読み込む
    x_img = img.shape[0]
    y_img = img.shape[1]
    x_img_mask = 4032
    y_img_mask = IMAGETRIPLITION_Y
    x_start = 0
    y_start = IMAGETRIPLITION_Y*2
    img[y_start:y_start+y_img_mask, x_start:x_start+x_img_mask] = 0
    #マスク画像
    cv2.imwrite("mask_img.jpg", img)

    img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV) # RGB => YUV(YCbCr)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)) # claheオブジェクトを生成
    img_yuv[:,:,0] = clahe.apply(img_yuv[:,:,0]) # 輝度にのみヒストグラム平坦化
    img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR) # YUV => RGB

    img_blur = cv2.blur(img, (15, 15)) # 平滑化フィルタを適用

    hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV) # BGRからHSVに変換

    bin_img1 = cv2.inRange(hsv, REDLOW_COLOR1, REDHIGH_COLOR1) # マスクを作成
    bin_img2 = cv2.inRange(hsv, REDLOW_COLOR2, REDHIGH_COLOR2)
    bin_img3 = cv2.inRange(hsv, BLUELOW_COLOR, BLUEHIGH_COLOR)
    bin_img4 = cv2.inRange(hsv, YELLOWLOW_COLOR, YELLOWHIGH_COLOR)
    redmask = bin_img1 + bin_img2 # 必要ならマスクを足し合わせる
    bluemask = bin_img3
    yellowmask = bin_img4

    #ごみの種類によって変化させる(燃やすごみ=(other, red), カン=(1, blue), ペットボトル-(2, green))
    match num:
        case 1:
            masked_img = cv2.bitwise_and(img_blur, img_blur, mask= bluemask) # 元画像から特定の色を抽出
        case 2:
            masked_img = cv2.bitwise_and(img_blur, img_blur, mask= yellowmask) # 元画像から特定の色を抽出
        case _:
            masked_img = cv2.bitwise_and(img_blur, img_blur, mask= redmask) # 元画像から特定の色を抽出
    #masked_img = cv2.bitwise_and(img_blur, img_blur, mask= yellowmask) # 元画像から特定の色を抽出

    out_img = masked_img
    match num:
        case 1:
            num_labels, label_img, stats, centroids = cv2.connectedComponentsWithStats(bluemask) # 連結成分でラベリングする
        case 2:
            num_labels, label_img, stats, centroids = cv2.connectedComponentsWithStats(yellowmask) # 連結成分でラベリングする
        case _:
            num_labels, label_img, stats, centroids = cv2.connectedComponentsWithStats(redmask) # 連結成分でラベリングする
    #num_labels, label_img, stats, centroids = cv2.connectedComponentsWithStats(redmask) # 連結成分でラベリングする
    # 背景のラベルを削除
    num_labels = num_labels - 1
    stats = np.delete(stats, 0, 0)
    centroids = np.delete(centroids, 0, 0)

    if num_labels >= 1: # ラベルの有無で場合分け
        max_index = np.argmax(stats[:, 4]) # 最大面積のインデックスを取り出す
        # 以下最大面積のラベルについて考える
        x = stats[max_index][0]
        y = stats[max_index][1]
        w = stats[max_index][2]
        h = stats[max_index][3]
        s = stats[max_index][4]
        mx = int(centroids[max_index][0]) # 重心のX座標
        my = int(centroids[max_index][1]) # 重心のY座標
        cv2.rectangle(out_img, (x, y), (x+w, y+h), (255, 0, 255)) # ラベルを四角で囲む
        cv2.putText(out_img, "%d,%d"%(mx, my), (x-15, y+h+15), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0)) # 重心を表示
        cv2.putText(out_img, "%d"%(s), (x, y+h+30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0)) # 面積を表示
        print(mx, my)
        print(x_img, y_img)

        cv2.imwrite("outr_img.jpg", out_img) # 書き出す

        #回転する方向を指定(+135, +175(180はカメラ台に激突する), -135), (初期位置をカメラ台方向と仮定)
        if mx >= 0 and mx <= IMAGETRIPLITION_X:
            return 135
        elif mx >= IMAGETRIPLITION_X and mx <= IMAGETRIPLITION_X*2:
            return 175
        else:
            return -135
    else:
        print("目標物が見当たりません！！")
        return -1

#このプログラムのみで動作させるときのmain文
if __name__ == '__main__':
    detect_target(r'C:\c\code\0925_color_sei.jpg', 10) # 画像ファイル名を入力