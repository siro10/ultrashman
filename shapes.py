import cv2
# 画像の読み込み
img = cv2.imread(r"C:\c\code\git_zemi\result.jpg")# 任意の画像ファイル
# グレースケールに変換
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 二値化
ret, thresh = cv2.threshold(gray, 127, 255, 0)
# 輪郭検出
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# 輪郭を描画
cv2.drawContours(img, contours, -1, (0,255,0), 3)
# 結果を表示
cv2.imshow('gray', gray)
cv2.imshow('result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()