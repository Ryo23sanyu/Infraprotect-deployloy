import math

result = 30 / 8
print(result)       # 出力: 3.75

result_floor = math.floor(result)
print(result_floor) # 出力: 3

result_ceil = math.ceil(result)
print(result_ceil) # 出力: 4

i10 = 8
page_plus = math.ceil(i10/6)
print(f"現在、{page_plus}ページ目")

i10 = (page_plus*6)+1
print(f"径間が変わるとしたら{i10}個目")