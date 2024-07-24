new_serial_number = "0101~0205"

one = new_serial_number.find("~")

start_number = new_serial_number[:one]
end_number = new_serial_number[one+1:]

# 最初の2桁と最後の2桁を取得
start_prefix = start_number[:2]
start_suffix = start_number[2:]
end_prefix = end_number[:2]
end_suffix = end_number[2:]

first_elements = []
# 決められた範囲内の番号を一つずつ追加
for prefix in range(int(start_prefix), int(end_prefix)+1):
    for suffix in range(int(start_suffix), int(end_suffix)+1):
        number_items = "{:02d}{:02d}".format(prefix, suffix)
        first_elements.append(number_items)
print(first_elements)