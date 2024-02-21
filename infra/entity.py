import ezdxf
from ezdxf.entities.mtext import MText
import pandas as pd

def extract_entities_below(entities, target_text):
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


doc = ezdxf.readfile(R'C:\work\django\myproject\myvenv\Infraproject\uploads\12_細握橋.dxf')
msp = doc.modelspace()
entities = list(msp)

target_text = "損傷図"

# 特定の文字の位置の下にあるエンティティを抽出
below_entities = extract_entities_below(entities, target_text)

# 抽出結果を表示
# print("特定の文字の位置の下にあるエンティティ:")
for entity in below_entities:
    print(f"Text: {entity.dxf.text}, X: {entity.dxf.insert[0]}, Y: {entity.dxf.insert[1]}")