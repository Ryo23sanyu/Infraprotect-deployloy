import re

# 例としての定義、実際にはお持ちのデータを使用してください
first_part_extracted = ["パート1", "パート2"]
second_items = [["①アイテム1", "⑤アイテム2", "⑰その他(分類6:ほし)-e"], ["①アイテム3", "⑤アイテム4", "⑰何か(分類7:うみ)-e"]]
replacement_patterns = {"①": "A", "⑤": "B"}  # replacement_patternsの例

# first_part_extractedとsecond_itemsを同時にループ
for first_part, sublist in zip(first_part_extracted, second_items):
    if any(item.startswith('①') for item in sublist):
        sublist[:] = [item for item in sublist if not item.startswith('⑤')]
    
    new_sublist = []
    for item in sublist:
        if item.startswith('⑰'):
            match = re.search(r':(.*?)(?=\)-e)', item)
            if match:
                new_sublist.append(match.group(1))
            else:
                new_sublist.append(item)
        else:
            new_sublist.append(item)
            
    sublist[:] = new_sublist
    second_replaced = "、".join(replacement_patterns.get(char, char) for char in sublist)
    
    # first_partとsecond_replacedが対応するように出力
    print(first_part + "に" + second_replaced + "が見られる。")
