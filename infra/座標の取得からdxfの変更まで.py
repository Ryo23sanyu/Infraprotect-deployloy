import os
import ezdxf

# DXFファイルを読み込む
doc = ezdxf.readfile(R'C:\work\django\myproject\myvenv\Infraproject\uploads\121_損傷橋.dxf')
# モデルスペースを取得
msp = doc.modelspace()

# 全ての座標を取得
def extract_text(filename):# 旗揚げ(MText)と写真番号(Def)を抽出する関数
    doc = ezdxf.readfile(filename)
    msp = doc.modelspace()
    extracted_text = []
    for entity in msp:
        if entity.dxftype() == 'MTEXT': # MTEXTかつ
            if entity.dxf.layer != 'Defpoints': # Defpoints以外の場合
            # MTextのテキストを抽出する
                text = entity.plain_text()
                x, y, _ = entity.dxf.insert
                cad_data = text.split("\n") if len(text) > 0 else [] # .split():\nの箇所で配列に分配
                if len(cad_data) > 0 and not text.startswith("※") and not any(keyword in text for keyword in ["×", ".", "損傷図"]):
            # 改行を含むかどうかをチェックする(and "\n" in cad):# 特定の文字列で始まるかどうかをチェックする: # 特定の文字を含むかどうかをチェックする
                    related_text = "" # 見つけたMTextと関連するDefpointsレイヤの文字列を代入する変数
            # MTextの下、もしくは右に特定のプロパティ(Defpoints)で描かれた文字を探す
                    for neighbor in msp.query('MTEXT[layer=="Defpoints"]'): # DefpointsレイヤーのMTextを抽出
                    # MTextの挿入位置と特定のプロパティで描かれた文字の位置を比較する
                        if entity_extension(entity, neighbor):
                        # 特定のプロパティ(Defpoints)で描かれた文字のテキストを抽出する
                            related_text = neighbor.plain_text()
                            x, y, _ = neighbor.dxf.insert
                        #extracted_text.append(neighbor_text)
                            break # 文字列が見つかったらbreakにょりforループを終了する
                    if  len(related_text) > 0: #related_textに文字列がある＝Defpointsレイヤから見つかった場合
                        #cad_data.append(related_text[:] + str(x) + "," + str(y))
                        cad_data.append(related_text[:]) # cad_dataに「部材名～使用写真」までを追加
                        cad_data.append([str(x), str(y)]) # 続いてcad_dataに「MTEXT」のX,Y座標を追加
                        #cad_data.append(str(x))
                        #cad_data.append(str(y))
                    #最後にまとめてcad_dataをextracted_textに追加する
                    extracted_text.append(cad_data[:] + [[str(x), str(y)]]) # extracted_textに「MTEXTとその座標」およびdefのX,Y座標を追加
    return extracted_text

def entity_extension(mtext, neighbor):# 旗揚げ(MText)と写真番号(Def)を紐付ける関数
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
    # MTextの下、もしくは右に特定のプロパティで描かれた文字が存在するかどうかを判定する(座標：右が大きく、上が大きい)
    if (
        neighbor_insertion[0] >= x_start and neighbor_insertion[0] <= x_end
    ):
        if ( #y_endの方が下部のため、y_end <= neighbor.y <= y_startとする
            neighbor_insertion[1] >= y_end and neighbor_insertion[1] <= y_start
        ):
            return True
    return False

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