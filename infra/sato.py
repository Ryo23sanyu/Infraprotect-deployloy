from ezdxf.entities import Text
import ezdxf
from ezdxf.entities.mtext import MText
import pandas as pd

def extract_text_below(entities, target_text):
    below_entities = []
    
    for entity in entities:
        if isinstance(entity, Text):
            if target_text in entity.dxf.text:
                x, y, _ = entity.dxf.insert
                below_entities.extend(get_entities_below(entities, x, y))
    
    return below_entities

def get_entities_below(entities, x, y):
    below_entities = []
    
    for entity in entities:
        if isinstance(entity, Text):
            ex, ey, _ = entity.dxf.insert
            if ey < y:
                below_entities.append(entity)
    
    return below_entities


doc = ezdxf.readfile(R'C:\work\django\myproject\myvenv\Infraproject\uploads\12_細握橋.dxf')
msp = doc.modelspace()
entities = list(msp)

target_text = "損傷図"

# 特定の文字を含むテキストエンティティを検索
target_entities = [entity for entity in entities if isinstance(entity, MText) and target_text in entity.dxf.text]

# 特定の文字の位置の下にあるエンティティを抽出
below_entities = extract_text_below(entities, target_text)

# 抽出結果を表示
# print("特定の文字の位置の下にあるエンティティ:")
for entity in below_entities:
    print(f"MText: {entity.dxf.text}, X: {entity.dxf.insert[0]}, Y: {entity.dxf.insert[1]}")