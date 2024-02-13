start = "0101"
end = "0206"

# 最初の2桁と最後の2桁を取得
start_prefix = start[:2]
start_suffix = start[2:]
end_prefix = end[:2]
end_suffix = end[2:]

# 抽出した数字を表示
for prefix in range(int(start_prefix), int(end_prefix)+1):
    for suffix in range(int(start_suffix), int(end_suffix)+1):
        print("{:02d}{:02d}".format(prefix, suffix))

text = "Sample00\n①\n②\n③\n写真-1"
lines = text.split('\n')

result = []
for i in range(len(lines)):
    if lines[i] == "写真-1":
        result.append(lines[i-1] + ', ' + lines[i])
    else:
        result.append(lines[i])

output = '\n'.join(result)
print(lines)