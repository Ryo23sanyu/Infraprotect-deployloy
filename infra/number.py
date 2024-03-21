from django.http import HttpResponse# 追加
def sample_view(request):# 追加
    start = "0101"
    end = "0206"

# 最初の2桁と最後の2桁を取得
    start_prefix = start[:2]
    start_suffix = start[2:]
    end_prefix = end[:2]
    end_suffix = end[2:]

# 抽出した数字を表示
    result = ""# 追加
    for prefix in range(int(start_prefix), int(end_prefix)+1):
        for suffix in range(int(start_suffix), int(end_suffix)+1):
            result += "{:02d}{:02d}".format(prefix, suffix)
        
    return HttpResponse(result)# 追加

mention = ["横桁 Cr0201,0301,0402 ⑦-d", "排管 Dp0201,0202 ①-c,⑤-e"]

result_items = []
for item in mention:
    item = item.replace("　", " ") # 全角スペースを半角スペースに変換
    middle_items = []
    if " " in item: # スペースがある場合は分割する
        sub_item = item.split(' ')
        for sub in sub_item:
            if "," in sub: # コンマが含まれる場合は分割する
                comma = sub.split(",")
                middle_items.extend(comma) # 分割した要素を追加する
            else:
                middle_items.append(sub)
    else:
        middle_items.append(item)
    
    result_items.append(middle_items)

print(result_items)



mention = ["主桁 Mg0101～0402 ⑦-d"]

result_items = []
for item in mention:
    item = item.replace("　", " ") # 全角スペースを半角スペースに変換
    middle_items = []
    if " " in item: # スペースがある場合は分割する
        sub_item = item.split(' ')
        for sub in sub_item:
            if "～" in sub:
                for i in range(len(sub)):#itemの文字数をiに代入
                    if "A" <= sub[i].upper() <= "Z" and i < len(sub) - 1 and sub[i+1].isnumeric():
                        start = sub[sub[i]+1:sub.find("～")]
                        end = sub[sub.find("～")+1:] # ハイフン以降の文字を取得するためにインデックスを修正します
                
                # 最初の2桁と最後の2桁を取得
                start_prefix = start[:2]
                start_suffix = start[2:]
                end_prefix = end[:2]
                end_suffix = end[2:]
                
                result = ""# 追加
                for prefix in range(int(start_prefix), int(end_prefix)+1):
                    for suffix in range(int(start_suffix), int(end_suffix)+1):
                        result += "{:02d}{:02d}".format(prefix, suffix)

                result_items.append(result) # '&'から'+'に修正します
            else:
                result_items.append(sub) # ハイフンが含まれない場合はそのまま追加します
    else:
        result_items.append(item) # スペースが含まれない場合もそのまま追加します

print(result_items)