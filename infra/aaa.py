### インポート
import tkinter
import tkinter.filedialog
from PIL import Image, ImageTk

### 定数
WIDTH  = 640        # 幅
HEIGHT = 400        # 高さ
ROW_SIZE = 3        # 1行に表示する写真の枚数

### 関数
def select_photos():
    ### ファイルダイアログ
    names = tkinter.filedialog.askopenfilenames(title="ファイル選択", initialdir="C:/", filetypes=[("Image File","*.jpg")])

    ### 画像ロードとリサイズ
    images = []
    for name in names:
        img = Image.open(name)
        img = img.resize((WIDTH, HEIGHT))
        images.append(ImageTk.PhotoImage(img))

    ### 選択した写真を横3枚×縦に表示
    row = 0
    col = 0
    for image in images:
        canvas.create_image(col * WIDTH, row * HEIGHT, anchor='nw', image=image)
        col += 1
        if col == ROW_SIZE:
            col = 0
            row += 1

### メイン画面作成
main = tkinter.Tk()

### 画面サイズ設定
main.geometry("640x440")

### ボタン作成・配置
button = tkinter.Button(main, text="ファイル選択", command=select_photos)
button.pack()

### キャンバス作成・配置
canvas = tkinter.Canvas(main, width=WIDTH * ROW_SIZE, height=HEIGHT)
canvas.pack()

### イベントループ
main.mainloop()