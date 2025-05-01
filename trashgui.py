#----------------------------------------------------------------------------------#
#Python3.11.9
#author:Isogai_Hiroto
#date:2025/04/24
#ユーザー画面と、本プロジェクトのハブプログラム
#動作の概要を以下に示す。
    #1.tkinterによる入力画面の出力
    #2.確定ボタンを押し、ninshiki.pyへ値を送信
    #3.必要事項が記されていない場合は、やり直しを要求する。
#このコードはハブである
#☆trashgui.py
#   -zemimota_tom.py
#   -ninshiki.py
#----------------------------------------------------------------------------------#

import tkinter as tk
import tkinter.font as tkfont
from PIL import Image, ImageTk
from tkinter import messagebox
import ninshiki

def on_register():
    # 各エントリーフィールドから値を取得
    moeru = state_checkbox1.get()
    pet = state_checkbox2.get()
    bin = state_checkbox3.get()
    can = state_checkbox4.get()
    trash1 = trash_var1.get()
    trash2 = trash_var2.get()
    trash3 = trash_var3.get()
    trash4 = trash_var4.get()

    if (moeru == pet == bin == can == 0):
        messagebox.showwarning("警告", "すべてのフィール(ドを入力してください。")
        return()

    # 全てのフィールドが入力されているか確認
    if (trash1 == trash2 == trash3 == trash4 == 0):
        messagebox.showwarning("警告", "すべてのフィールドを入力してください。")
        return()

    if ((trash1 == trash2) or (trash2 == trash3) or (trash3 == trash4) or (trash4 == trash1)):
        messagebox.showwarning("警告", "すべて違う場所にしてください。")
        return()

    messagebox.showinfo("情報", "情報が登録されました。")
    ninshiki.ninshiki(moeru, pet, bin, can, trash1, trash2, trash3, trash4)
    return()

def bunbetu():
    messagebox.showwarning("警告", "分別してください。")
    return


root = tk.Tk()
root.title("ユーザ画面")

#Font
font_main = tkfont.Font(
    family = "Arial Black",
    size = 24,
    weight = "bold",
    slant = "roman",
    underline = False,
    overstrike = False,
)

font_sub = tkfont.Font(
    family = "Arial Black",
    size = 16,
    weight = "normal",
    slant = "roman",
    underline = False,
    overstrike = False,
)

font_semisub = tkfont.Font(
    family = "Arial Black",
    size = 11,
    weight = "normal",
    slant = "roman",
    underline = False,
    overstrike = False,
)

#head
label1 = tk.Label(root, text = "ウルトラッシュマンユーザ画面", font = font_main, anchor = tk.CENTER)
label1.grid(row = 0, column= 0, columnspan=5)

#choice trash
label2 = tk.Label(root, text = "ゴミの種類を選んでください(複数選択可)", font = font_sub)
label2.grid(row = 1, column= 0, columnspan=5)

#variable for checkbox
state_checkbox1 = tk.BooleanVar()
state_checkbox2 = tk.BooleanVar()
state_checkbox3 = tk.BooleanVar()
state_checkbox4 = tk.BooleanVar()

checkbox1 = tk.Checkbutton(root, text = "燃やすごみ", variable=state_checkbox1)
checkbox1.grid(row = 2, column= 0, sticky="s")

checkbox2 = tk.Checkbutton(root, text = "ペットボトル", variable=state_checkbox2)
checkbox2.grid(row = 2, column= 1, sticky="s")

checkbox3 = tk.Checkbutton(root, text = "ビン", variable=state_checkbox3)
checkbox3.grid(row = 2, column= 2, sticky="s")

checkbox4 = tk.Checkbutton(root, text = "カン", variable=state_checkbox4)
checkbox4.grid(row = 2, column= 3, sticky="s")

#choice trash places
label3 = tk.Label(root, text = "下の画像を参考にゴミ箱の配置を決めてください", font = font_sub)
label3.grid(row = 3, column= 0, columnspan=5)

image = Image.open("/c/5I 専門教科授業資料/ウルトラッシュマンgu1i.png")
photo = ImageTk.PhotoImage(image)
label4 = tk.Label(root, image=photo)
label4.grid(row=4, column=1, columnspan=3)

#1
label5 = tk.Label(root, text = "⓵のゴミ箱の配置を決めてください", font = font_semisub)
label5.grid(row = 5, column= 0, columnspan=5)

trash_var1 = tk.StringVar(value=0)
trash_var1.set(None)
radio_11 = tk.Radiobutton(root, text="燃やすごみ", variable=trash_var1, value = 1)
radio_11.grid(row=6, column=0)
radio_12 = tk.Radiobutton(root, text="ペットボトル", variable=trash_var1, value = 2)
radio_12.grid(row=6, column=1)
radio_13 = tk.Radiobutton(root, text="ビン", variable=trash_var1, value = 3)
radio_13.grid(row=6, column=2)
radio_14 = tk.Radiobutton(root, text="カン", variable=trash_var1, value = 4)
radio_14.grid(row=6, column=3)
radio_15 = tk.Radiobutton(root, text="なし", variable=trash_var1, value = 99)
radio_15.grid(row=6, column=4)

#2
label6 = tk.Label(root, text = "⓶のゴミ箱の配置を決めてください", font = font_semisub)
label6.grid(row = 7, column= 0, columnspan=5)

trash_var2 = tk.StringVar(value=0)
trash_var2.set(None)
radio_21 = tk.Radiobutton(root, text="燃やすごみ", variable=trash_var2, value = 1)
radio_21.grid(row=8, column=0)
radio_22 = tk.Radiobutton(root, text="ペットボトル", variable=trash_var2, value = 2)
radio_22.grid(row=8, column=1)
radio_23 = tk.Radiobutton(root, text="ビン", variable=trash_var2, value = 3)
radio_23.grid(row=8, column=2)
radio_24 = tk.Radiobutton(root, text="カン", variable=trash_var2, value = 4)
radio_24.grid(row=8, column=3)
radio_25 = tk.Radiobutton(root, text="なし", variable=trash_var2, value = 99)
radio_25.grid(row=8, column=4)

#3
label7 = tk.Label(root, text = "⓷のゴミ箱の配置を決めてください", font = font_semisub)
label7.grid(row = 9, column= 0, columnspan=5)

trash_var3 = tk.StringVar(value=0)
trash_var3.set(None)
radio_31 = tk.Radiobutton(root, text="燃やすごみ", variable=trash_var3, value = 1)
radio_31.grid(row=10, column=0)
radio_32 = tk.Radiobutton(root, text="ペットボトル", variable=trash_var3, value = 2)
radio_32.grid(row=10, column=1)
radio_33 = tk.Radiobutton(root, text="ビン", variable=trash_var3, value = 3)
radio_33.grid(row=10, column=2)
radio_34 = tk.Radiobutton(root, text="カン", variable=trash_var3, value = 4)
radio_34.grid(row=10, column=3)
radio_35 = tk.Radiobutton(root, text="なし", variable=trash_var3, value = 99)
radio_35.grid(row=10, column=4)

#4
label8 = tk.Label(root, text = "⓸のゴミ箱の配置を決めてください", font = font_semisub)
label8.grid(row = 11, column= 0, columnspan=5)

trash_var4 = tk.StringVar(value=0)
trash_var4.set(None)
radio_41 = tk.Radiobutton(root, text="燃やすごみ", variable=trash_var4, value = 1)
radio_41.grid(row=12, column=0)
radio_42 = tk.Radiobutton(root, text="ペットボトル", variable=trash_var4, value = 2)
radio_42.grid(row=12, column=1)
radio_43 = tk.Radiobutton(root, text="ビン", variable=trash_var4, value = 3)
radio_43.grid(row=12, column=2)
radio_44 = tk.Radiobutton(root, text="カン", variable=trash_var4, value = 4)
radio_44.grid(row=12, column=3)
radio_45 = tk.Radiobutton(root, text="なし", variable=trash_var4, value = 99)
radio_45.grid(row=12, column=4)

# 確定ボタンを作成し、クリックイベントをバインド
button_register = tk.Button(root, text="確定", command=on_register)
button_register.grid(row=13, column=1, columnspan=3)

#rootを表示し無限ループ
root.mainloop()