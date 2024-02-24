import ezdxf

def extract_text(filename, layer_name):
    doc = ezdxf.readfile(filename)
    msp = doc.modelspace()
    
    texts = []
    for entity in msp:
        if entity.dxftype() == 'MTEXT' and entity.dxf.layer == layer_name:
            texts.append(entity.get_text())
    
    return texts

# ファイル名と画層名を指定して文字を抽出する
filename = R'C:\work\django\myproject\myvenv\Infraproject\uploads\12_損傷橋.dxf'
layer_name = '枠'
extracted_texts = extract_text(filename, layer_name)

# 抽出された文字を表示する
for text in extracted_texts:
    print(text)