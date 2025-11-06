# -*- coding: UTF-8 -*-
import cv2

if __name__ == '__main__':

    # 画像の読み込み
    # 変化前と変化後の画像ファイル
    img_src1 = cv2.imread(r"C:\c\code\git_zemi\20250508_1.jpg", 1)
    img_src2 = cv2.imread(r"C:\c\code\git_zemi\20250508_2.jpg", 1)

    fgbg = cv2.createBackgroundSubtractorMOG2()

    fgmask = fgbg.apply(img_src1)
    fgmask = fgbg.apply(img_src2)

    # 表示
    cv2.imshow('frame',fgmask)

    # 検出画像
    bg_diff_path  = './diff.jpg'
    cv2.imwrite(bg_diff_path,fgmask)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

