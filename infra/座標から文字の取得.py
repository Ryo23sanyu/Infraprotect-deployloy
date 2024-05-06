import os
import ezdxf

# DXFファイルを読み込む
doc = ezdxf.readfile(R'C:\work\django\myproject\myvenv\Infraproject\uploads\121_損傷橋.dxf')

# モデルスペースを取得
msp = doc.modelspace()

# 全ての座標を取得
x = 543427.3505810621
y = 229268.8593029478

# 編集する座標
coords = [
    (543427.3505810621, 229268.8593029478),
    #(543666.8474364146, 228932.0443462149)
]

# 座標の一致を確認するための許容誤差（適宜調整してください）
epsilon = 0.001

# 座標に一致するTEXTまたはMTEXTを探索
for entity in msp: # モデルスペースの中のentityをループ処理
    if entity.dxftype() in {'TEXT', 'MTEXT', 'Defpoints'}: # entityが['TEXT', 'MTEXT', 'Defpoints']の場合
        # エンティティの位置を取得
        x, y, _ = entity.dxf.insert
        
        # 指定された座標と一致するかどうか確認
        for cx, cy in coords:
            if abs(x - cx) < epsilon and abs(y - cy) < epsilon:
                # 座標が一致するエンティティの内容を表示
                print(f"一致した座標: ({x}, {y}), テキスト内容: {entity.text}")
                
                new_text = "主桁0000" # 更新するテキスト
                entity.dxf.text = new_text # 古いテキストを新しいテキストに置き換え
                print(entity.dxf.text)
                
                # デスクトップのパスを取得（Windowsの例）
                desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                # デスクトップのパスを取得（MacOS/Linuxの例）
                # desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
                
                # 更新されたDXFファイルをデスクトップに保存
                doc.saveas(os.path.join(desktop_path, "更新.dxf"))

                break  # 終了