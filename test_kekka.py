import cv2
import numpy as np

#「背景」となる画像の取り込み（グレースケール）
# もともとが白黒の画像ですが、色数が多い場合は2色の色味に変更しないと計算がしづらくなります。
# 任意の画像ファイル
img_diff = cv2.imread(r"C:\c\code\git_zemi\result.jpg", cv2.IMREAD_GRAYSCALE)

#白色のピクセル数の算出
whitePixels = np.count_nonzero(img_diff)

#黒色のピクセル数の算出
blackPixels = img_diff.size - whitePixels

#白色の部分が全体のどれくらいの割合を占めているのかを算出
print( whitePixels / img_diff.size * 100)