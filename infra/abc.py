# last_item_replaced リストを宣言
import glob

last_item = ['NON-a', '9月7日 S404(前-1)', '9月7日 S537', '9月8日 S117(前-3),9月8日 S253']

last_item_replaced = []
for item in last_item: # last_itemの全レコードに対してループ処理を行う
    # last_itemの１要素に対してS→佐藤の置換を行った結果をlast_item_replacedに追加
    last_item_replaced.append(item.replace("S", "佐藤").replace(" ", "　"))

# picture_table リストを宣言
picture_table = []
for picture in last_item_replaced:  # last_item_replacedの全レコードに対してループ処理を行う
    # glob()を実行した結果をpicture_tableに追加
    target_file = picture + '.jpg'
    photo_paths = glob.glob('infra/static/infra/img/' + target_file)
    picture_table.append(''.join(photo_paths).replace('infra/static/', '', 1))

# i番目のpicture_tableをitemの値として代入
item = {'last': picture_table}

print(item)