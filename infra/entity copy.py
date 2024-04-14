import ezdxf
from ezdxf.entities.mtext import MText
import pandas as pd

def extract_text(filename):# 旗揚げ(MText)と写真番号(Def)を抽出する関数
    doc = ezdxf.readfile(filename)
    msp = doc.modelspace()
    
    extracted_text = []
    for entity in msp:
        if entity.dxftype() == 'MTEXT':
            if entity.dxf.layer != 'Defpoints':
            # MTextのテキストを抽出する
                text = entity.plain_text()
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
                        #extracted_text.append(neighbor_text)
                            break # 文字列が見つかったらbreakにょりforループを終了する
                    if  len(related_text) > 0: #related_textに文字列がある＝Defpointsレイヤから見つかった場合
                        cad_data.append(related_text) # 見つかった文字列を追加する
                #最後にまとめてcad_dataをextracted_textに追加する
                    extracted_text.append(cad_data)
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

def extract_entities_below(entities, target_text):# 文字の座標を取得する関数
    below_entities = []
    # 特定の文字を含むエンティティを検索
    for entity in entities:
        if isinstance(entity, MText) and target_text in entity.dxf.text:
            x, y, _ = entity.dxf.insert
            # 指定された文字よりも座標が上のエンティティを抽出
            for below_entity in entities:
                if isinstance(below_entity, MText):
                    bx, by, _ = below_entity.dxf.insert
                    if by < y and bx >= x:# bx < x:にすると番号図を抽出
                        below_entities.append(below_entity)
    return below_entities

doc = ezdxf.readfile(R'C:\work\django\myproject\myvenv\Infraproject\uploads\121_損傷橋.dxf')
msp = doc.modelspace()
entities = list(msp)

# AutoCADファイル名を指定してテキストを抽出する
filename = R'C:\work\django\myproject\myvenv\Infraproject\uploads\121_損傷橋.dxf'
extracted_text = extract_text(filename)
doc = ezdxf.readfile(filename)
msp = doc.modelspace()
    
target_text = "損傷図"

# 特定の文字の位置の下にあるエンティティを抽出
below_entities = extract_entities_below(entities, target_text)

# 抽出結果を表示
# print("特定の文字の位置の下にあるエンティティ:")
for entity in below_entities:
    print(f"Text: {entity.dxf.text}, X: {entity.dxf.insert[0]}, Y: {entity.dxf.insert[1]}")