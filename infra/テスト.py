import re
from markupsafe import Markup

combined_list = [{'first': Markup('横桁 Cr0803'), 'second': ['⑦剥離・鉄筋露出-d']}, {'first': Markup('主桁 Mg0901'), 'second': ['異物混入']}, {'first': Markup('横桁 Cr0201,0301,0402,</br>0403,0602,0604,</br>0704'), 'second': ['⑦剥離・鉄筋露出-d']}, {'first': Markup('床版 Ds0201,0203'), 'second': ['⑦剥離・鉄筋露出-d']}, {'first': Markup('排水管 Dp0201,0202'), 'second': ['①腐食(小大)-c']}, {'first': Markup('横桁 Cr0801'), 'second': ['⑦剥離・鉄筋露出-d']}, {'first': Markup('排水管 Dp0101'), 'second': ['①腐食(大大)-e']}, {'first': Markup('横桁 Cr0802'), 'second': ['⑦剥離・鉄筋露出-d']}, {'first': Markup('床版 Ds0803'), 'second': ['⑦剥離・鉄筋露出-d']}, {'first': Markup('横桁 Cr0503'), 'second': ['⑦剥離・鉄筋露出-d', '施工不良']}, {'first': Markup('横桁 Cr0401'), 'second': ['⑦剥離・鉄筋露出-e']}, {'first': Markup('床版 Ds0101'), 'second': ['⑦剥離・鉄筋露出-d']}, {'first': Markup('横桁 Cr0102'), 'second': ['施工不良']}, {'first': Markup('横桁 Cr0103'), 'second': ['⑦剥離・鉄筋露出-e']}, {'first': Markup('排水管 Dp0102'), 'second': ['①腐食(小大)-c']}, {'first': Markup('横桁 Cr0304'), 'second': ['⑦剥離・鉄筋露出-e']}, {'first': Markup('横桁 Cr0204'), 'second': ['⑦剥離・鉄筋露出-e']}, {'first': Markup('横桁 Cr0101'), 'second': ['施工不良']}, {'first': Markup('主桁 Mg0901'), 'second': ['⑦剥離・鉄筋露出-c']}, {'first': Markup('地覆 Fg0201'), 'second': ['⑫うき-e']}, {'first': Markup('橋台[胸壁] Ap0102,</br>橋台[竪壁] Ac0102,</br>伸縮装 置 Ej0102'), 'second': ['⑳漏水・滞水-e']}, {'first': Markup('橋台[胸壁] Ap0101,</br>橋台[竪壁] Ac0101,</br>伸縮装置 Ej0101'), 'second': ['⑳漏水・滞水-e']}, {'first': Markup('排水ます Dr0101'), 'second': ['埋没']}, {'first': Markup('防護柵 Gf0101'), 'second': ['⑦剥離・鉄筋露出-d']}, {'first': Markup('防護柵 Gf0101'), 'second': ['⑦剥離・鉄筋露出-c']}, {'first': Markup('防護柵 Gf0101'), 'second': ['⑦剥離・鉄筋露出-d']}, {'first': Markup('舗装 Pm0101'), 'second': ['㉔土砂詰ま り-e']}, {'first': Markup('防護柵 Gf0201'), 'second': ['⑦剥離・鉄筋露出-c']}, {'first': Markup('舗装 Pm0201'), 'second': ['㉔土砂詰まり-e']}, {'first': Markup('舗装 Pm0201'), 'second': ['⑮舗装の異常-e']}, {'first': Markup('舗装 Pm0201'), 'second': ['⑮舗装の異常-e']}, {'first': Markup('舗装 Pm0101,0201'), 'second': ['⑮舗装の異常-e']}, {'first': Markup('支承本体 Bh0102,</br>沓座モルタル Bm0102'), 'second': None}, {'first': Markup('PC定着部 Cn1203'), 'second': None}, {'first': Markup('排水ます Dr0102,0201,0202'), 'second': ['埋没']}]

for item in combined_list:
    # Markupオブジェクトを文字列に変換してから</br>タグを除去
    clean_text = str(item['first']).replace("</br>", "")
    
    if "," in clean_text:
        pattern = ',(\d|,)*(?=\s|$)' # 「,」の後に(「数字」か「,」)の場合
        # 条件に一致するかチェック
        if re.search(pattern, clean_text):
          print(clean_text.split(" ")[0])
        else:
          sub_pattern = r'[A-Za-z0-9/ /]'
          # 置換処理を行い、日本語のみ抽出
          result = re.sub(sub_pattern, '', clean_text)
          print(result)# 数字、アルファベット、コンマを削除
    else:
        print(clean_text.split(" ")[0])