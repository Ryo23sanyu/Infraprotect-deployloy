import re

result = [{'join': [{'first': ['排水管 Dp0101'], 'second': ['㉓変形・欠損-c', '①腐食(小大)-c', '①腐食(大大)-e', '⑤防食機能の劣化(分類1)-e']}]}]

#優先順位の指定
order_number = {"None": 0, "①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5, "⑥": 6, "⑦": 7, "⑧": 8, "⑨": 9, "⑩": 10, "⑪": 11, "⑫": 12, "⑬": 13, "⑭": 14, "⑮": 15, "⑯": 16, "⑰": 17, "⑱": 18, "⑲": 19, "⑳": 20, "㉑": 21, "㉒": 22, "㉓": 23, "㉔": 24, "㉕": 25, "㉖": 26}
order_lank = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}

# <<◆ リストの並び替え ◆>>
def sort_second_list(second_list):
    def extract_key(value):
        match = re.match(r"([①-⑳㉑-㉖])[^-]*-([a-e])", value)
        if match:
            number, rank = match.groups()
            number_key = order_number.get(number, float('inf'))
            rank_key = order_lank.get(rank, float('inf'))
            return number_key, rank_key
        else:
            return float('inf'), float('inf')

    return sorted(second_list, key=extract_key)

# <<◆ リストの並び替え ◆>>
for item in result:
    item['join'][0]['second'] = sort_second_list(item['join'][0]['second'])

print("Sorted items:")
print(result)