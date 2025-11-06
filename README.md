# ultrashman

## 概要

- 情報工学ゼミ2024，オープンキャンパス2025にて展示した作品。
- 研究室:安藤研究室
- ゴミを種類を自動判別して捨ててくれるシステム。

## コードの説明
- **Background Subtraction.py**
  - 背景差分プログラム
  - 現在の画像と少し前の画像を比較することで，カメラ画像中のどこが変化したか読み取る。
  - ゴミが台に載ったことを認識するために利用した。
  - 今後タッチセンサ等に置き換わるときには必要ない。

- **Color recognition.py**
  - 色認識プログラム
  - 画像中の 〇 色の面積が一番広い所を探す。
  - ゴミ箱の位置を読み取るために利用した。
  - 誤作動しないないよう，色認識しない場所にはマスク処理。
  - 認識可能な色は，赤・青・黄の３種類。

  - **動作ex.(赤色を認識するパターン)**
    - RGB -> HSV変換。
    - 各画像処理を行い赤色を抽出。
    - 一番赤色の面積が広い所を計算。
    - その面積の重点を返す。

- **Detection of changes.py**
  - 静止画像による背景差分プログラム
  - **Background Subtraction.py** のプロトタイプ
 
- **camera_test(realtime).py**
  - Webカメラによるリアルタイム認識プログラム
  - 適切なデータセットを選び，Webカメラを用いて，リアルタイムでゴミの種類を検知する。

- **learningmodel1.py** & **learningmodel11.py**
  - 認識モデル作成用プログラム
  - roboflowから公開ラベル付きデータセットを選び，Gitファイルで自分のPCにダウンロード。
  - Gitファイル中の[args.yaml]ファイルを挿入し，推論することができる。
  - epoch数が多ければ多いほど正確なモデルができるが，時間がかかる可能性があるため適切なepoch・imgszにする。

- **ninshiki_ouyou.py**
  - Webカメラによるリアルタイム認識プログラム
  - 認識結果が配列で管理されているため，Mainプログラムに挿入しやすい形になっている。
  - ターミナルの出力を見ることで何が認識できたか，逆に何を認識することが出来なかったか，一目でわかる。

- **ninshiki_picture&video.py**
  - 静止画像・動画用認識プログラム
  - resultの内容を変えれば，静止画像・動画の認識をすることができる。

- **ninshiki_tom.py**
  - **ninshiki_ouyou.py**にモータ動作を組み合わせたもの

- **shapes.py**
  - 画像中の特徴的な形の輪郭のみ読み取るプログラム
  - どこで使ったかはあまり把握していないが，物体の輪郭を読み取り面積を求めるときなどに使えばよい。

- **test_kekka.py**
  - 変化量が全体のどの程度占めているか求めるプログラム。
  - 背景差分プログラム系のプロトタイプ

- **zemimota_tom.py**
  - サーボモータ・マブチモータ用プログラム

- **ultrashman_ReRe.py** or **ultrashman_gomibakobunbetsu.py**
  - <u>**正規プログラム**</u>
  - とりあえず前者が完成形プログラムなので，筐体の様相を整えたら，このプログラムを動かしてください。

*基本的に正規プログラム以外は単体動作確認済み*

## データセットについて
- ここにおいてある[best11.pt]を使ってください。
- もし他のもやってみたいのであればroboflowから探してみてください。その際，YoloのバージョンについてはYolov11 or Yolov8でお願いします(以上2つでしか動作確認をしていないため)。

## 今後の展望
- タッチセンサにすれば処理が軽くなるかもしれない
  ->  **zemimota_tom.py**に処理を加えることで可能
- ゴミの認識が完璧でない
  -> 一から作れば正確なデータセットができる。Roboflowで自作データセットの作成が可能。方法は参考URLから。

## 参考ＵＲＬ
- <https://www.hinomaruc.com/displaying-results-of-object-detection-with-yolov8/>, YOLOv8による物体検知の結果を表示してみる
- <https://qiita.com/daifuku10/items/50cb5cd9740e07fde591>, Python で物体認識AIのYOLOv8を試してみた！〜応用編〜
- <https://ai-wonderland.com/entry/yolov8webcamera>, 【YOLOv8】WindowsでWEBカメラからリアルタイム物体検出
- <https://qiita.com/Mikeinu/items/530bdb2ddeeedc32eb58>, 【Python】最新物体検知AI YOLOv8のPythonライブラリ ultralytics がすごすぎる！
- <https://universe.roboflow.com/>, Roboflowホームページ
- <https://python.joho.info/opencv-tutorial/>, PythonとOpenCVで画像処理プログラミング超入門
- <https://burgerdog.hatenablog.com/entry/opencvpi>, 背景差分による物体検知
- <https://docs.roboflow.com/roboflow/roboflow-jp/universe/roboflow-universe-toha>, Roboflow Universe とは？ 
