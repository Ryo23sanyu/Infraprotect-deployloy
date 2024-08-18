import os
import ezdxf

# DXFファイルを読み込む
doc = ezdxf.readfile(R'C:\work\django\myproject\myvenv\Infraproject\uploads\121_損傷橋.dxf')
# モデルスペースを取得
msp = doc.modelspace()

coords = [
    (543427.3505810621, 229268.8593029478), # 修正する座標を指定
]

# 座標の一致を確認するための許容誤差
epsilon = 0.001

# 座標に一致するTEXTまたはMTEXTを探索
for entity in msp: # モデルスペースの中のentityをループ処理
    if entity.dxftype() in {'TEXT', 'MTEXT', 'Defpoints'}: # entityが['TEXT', 'MTEXT', 'Defpoints']の場合
        # エンティティの位置を取得
        x, y, _ = entity.dxf.insert
        
        # 指定された座標と一致するかどうか確認
        for cx, cy in coords:
            if abs(x - cx) < epsilon and abs(y - cy) < epsilon:
                
                # 更新するテキスト(固定値)
                new_text = "主桁0000" # 更新するテキスト
                entity.dxf.text = new_text # 古いテキストを新しいテキストに置き換え
                
                # デスクトップのパスを取得（Windowsの例）
                desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
                # デスクトップのパスを取得（MacOS/Linuxの例）
                # desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
                
                # 更新されたDXFファイルをデスクトップに保存
                doc.saveas(os.path.join(desktop_path, "さいど更新.dxf"))

                break  # 終了