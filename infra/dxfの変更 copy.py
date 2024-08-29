import os
import ezdxf

# DXFファイルを読み込む
doc = ezdxf.readfile(R'C:\Users\dobokuka4\Desktop\CAD変更一時保存.dxf')
# モデルスペースを取得
msp = doc.modelspace()

def entity_extension(mtext, neighbor):
    # MTextの挿入点
    mtext_insertion = mtext.dxf.insert
    # 特定のプロパティ(Defpoints)で描かれた文字の挿入点
    neighbor_insertion = neighbor.dxf.insert
    #テキストの行数を求める
    text = mtext.plain_text()
    text_lines = text.split("\n") if len(text) > 0 else []
    # 改行で区切ったリスト数→行数
    text_lines_count = len(text_lines)

    # Defpointsを範囲内とするX座標範囲
    x_start = mtext_insertion[0]  # X開始位置
    x_end  = mtext_insertion[0] + mtext.dxf.width # X終了位置= 開始位置＋幅
    y_start = mtext_insertion[1] + mtext.dxf.char_height # Y開始位置
    y_end  = mtext_insertion[1] - mtext.dxf.char_height * (text_lines_count + 1) # 文字の高さ×(行数+1)
    print("～～ DXF文字情報 ～～")
    print(f"mtextテキスト:{mtext.dxf.text}\nDxfテキスト:{neighbor.dxf.text}")
    print(f"mtext挿入点:{mtext_insertion}\n　Def挿入点:{neighbor_insertion}\n　行数:{text_lines_count}")
    print(f"mtext文字幅:{mtext.dxf.width}\n　mtext文字高:{mtext.dxf.height}\n　mtext1行当たりの文字高:{mtext.dxf.char_height}")
    print(f"X座標の取得範囲:{x_start}～{x_end}\nY座標の取得範囲:{y_start}～:{y_end}")
    print("～～ DXF文字情報 ～～")
    
    return False