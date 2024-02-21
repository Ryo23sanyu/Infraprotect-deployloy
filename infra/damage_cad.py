# @title デフォルトのタイトル テキスト
# C:\work\django\myproject\myvenv\Scripts\python.exe
import json
import ezdxf
from ezdxf.entities.mtext import MText
import pandas as pd

dxf = ezdxf.readfile(R'C:\work\django\myproject\myvenv\Infraproject\uploads\12_細握橋.dxf') # ファイルにアップロードしたdxfファイル名

cad_read = []
found_string = False

for entity in dxf.entities:
    if type(entity) is MText:
        cad =  entity.plain_text()
        cad_data = cad.split("\n") if len(cad) > 0 else []
        # print(cad_data)
        
        if found_string:
            cad_read += cad_data  # cad_dataの各要素をcad_readに追加する

        if len(cad_data) > 0:
            for line in cad_data:
                if line == "損傷図":
                    found_string = True
                    break

print(cad_read)  # 抽出した行を表示する