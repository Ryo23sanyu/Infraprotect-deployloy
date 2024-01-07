# @title デフォルトのタイトル テキスト
import ezdxf
import openpyxl
from ezdxf.entities.mtext import MText
from ezdxf.entities.text import Text

dxf = ezdxf.readfile('5_大久保歩道橋.dxf') # ファイルにアップロードしたdxfファイル名

for entity in dxf.entities:
    if type(entity) is MText: # or type(entity) is Text: MTextとTextが文字列を表す(https://ymt-lab.com/post/2021/ezdxf-read-dxf-file/)
        print( entity.plain_text() ) # GoogleColaboratory上に出力

workbook = openpyxl.Workbook() # 新規ファイルの作成
sheet = workbook.active # アクティブなシートの選択

row = 1  # 出力する行数

for entity in dxf.entities: # 上と同じ
    if type(entity) is MText: # 上と同じ
        text = entity.plain_text() # textに格納
        sheet.cell(row=row, column=1).value = text #sheet.cell():セルの選択、row:行、column:列 → A列を1行ずつ選択
        row += 1 # 一段下げる

workbook.save('歩道橋.xlsx')# 保存するエクセル名