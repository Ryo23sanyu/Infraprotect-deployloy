
### インポート
import os
import tkinter
import tkinter.filedialog
from PIL import Image, ImageTk

### 定数
WIN_WIDTH = 640 # Window：幅
WIN_HEIGHT = 780 # Window ： 高さ
WIN_MARGIN = 20  # Windowとキャンパスのマージン

WIDTH  = 200        # 画像：幅
HEIGHT = 150       # 画像：高さ
ROW_SIZE = 3        # 1行に表示する写真の枚数

CANVAS_WIDTH = WIDTH * ROW_SIZE - WIN_MARGIN
CANVAS_HEIGHT = WIN_HEIGHT - WIN_MARGIN

images = {}

### 関数
def func():
    
    # ファイルダイアログ
    names = tkinter.filedialog.askopenfilenames(title="ファイル選択", initialdir=os.getcwd(), filetypes=[("Image File","*.jpg")])
    
    # 画像ロード
    for name in names:
        img = Image.open(name)
        img = img.resize((WIDTH, HEIGHT))
        image = ImageTk.PhotoImage(img)
    
        images[name] = image
    
    # ## 表示済み画像の消去(一覧を変更する機能を追加した場合有効化)
    # for name in images.keys():
    #     canvas.delete(name)
    ### 選択した写真を横3枚×縦に表示
    row = 0
    col = 0
    for name, image in images.items():
        canvas.create_image(col * WIDTH, row * HEIGHT, anchor='nw', image=image, tag=name)
        col += 1
        if col == ROW_SIZE:
            col = 0
            row += 1    
    
### メイン画面作成
main = tkinter.Tk()

### 画面サイズ設定
main.geometry(str(WIN_WIDTH) + "x" + str(WIN_HEIGHT))

### ボタン作成・配置
button = tkinter.Button(main, text="ファイル選択", command=func)
button.pack()

### キャンバス作成・配置
canvas = tkinter.Canvas(main, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvas.pack()

### イベントループ
main.mainloop()




