# 行の開始地点と増加するステップを定義
import math


partsname_and_number_row = 10 # 部材名・要素番号
damagename_and_lank_row = 11 # 損傷の種類・損傷程度
picture_start_row = 13 # 損傷写真
lasttime_lank_row = 15 # 前回損傷程度
damage_memo_row = 17 # 損傷メモ
step = 14
output_data = 74#len(output_data) * 3  # データ数に3列分を掛けています
num_positions = math.ceil(output_data/3)
# 関連する列を定義
picture_columns = ["E", "AE", "BE"] # 写真列
left_columns = ["I", "AI", "BI"] # 左列
right_columns = ["R", "AR", "BR"] # 右列
bottom_columns = ["T", "AT", "BT"] # 前回程度+メモ

# セル位置のリストを生成
join_partsname_cell = [f"{col}{partsname_and_number_row + i * step}" for i in range(num_positions) for col in left_columns] # 部材名
join_number_cell = [f"{col}{partsname_and_number_row + i * step}"    for i in range(num_positions) for col in right_columns] # 要素番号
join_damagename_cell = [f"{col}{damagename_and_lank_row + i * step}" for i in range(num_positions) for col in left_columns] # 損傷の種類
join_lank_cell = [f"{col}{damagename_and_lank_row + i * step}"       for i in range(num_positions) for col in right_columns] # 損損傷程度
join_picture_cell = [f"{col}{picture_start_row + i * step}"          for i in range(num_positions) for col in picture_columns] # 損傷写真
join_lasttime_lank_cell = [f"{col}{lasttime_lank_row + i * step}"    for i in range(num_positions) for col in bottom_columns] # 前回損傷程度
join_damage_memo_cell = [f"{col}{damage_memo_row + i * step}"        for i in range(num_positions) for col in bottom_columns] # 損傷メモ

print(f"join_partsname_cell:{join_partsname_cell}")
print(f"join_number_cell:{join_number_cell}")
print(f"join_damagename_cell:{join_damagename_cell}")
print(f"join_lank_cell:{join_lank_cell}")
print(f"join_picture_cell:{join_picture_cell}")
print(f"join_lasttime_lank_cell:{join_lasttime_lank_cell}")
print(f"join_damage_memo_cell:{join_damage_memo_cell}")
print(len(join_damage_memo_cell))