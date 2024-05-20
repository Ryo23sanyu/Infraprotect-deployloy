list = [(518650.2476225982, 209726.0102280809, 0.0, 0.0, 0.0), (560700.2476225981, 209726.0102280809, 0.0, 0.0, 0.0), (560700.2476225981, 239426.0102280809, 0.0, 0.0, 0.0), (518650.2476225982, 239426.0102280809, 0.0, 0.0, 0.0)]
# 時計回りで座標が表示

left_top_point = list[0][0] # 左上の座標
right_top_point = list[1][0] # 右上の座標
right_bottom_point = list[2][0] # 右下の座標
left_bottom_point = list[3][0] # 左下の座標

print(max(left_top_point,right_top_point,left_bottom_point,right_bottom_point)) # X座標の最大値
print(min(left_top_point,right_top_point,left_bottom_point,right_bottom_point)) # X座標の最小値