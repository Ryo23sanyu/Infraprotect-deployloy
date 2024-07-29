names_1 = ['名前1'] # len = 1
parts_1 = ['変状1'] # len = 1

names_2 = ['名前1'] # len = 1
parts_2 = ['変状1', '変状2'] # len = 2

names_3 = ['名前1', '名前2'] # len = 2
parts_3 = ['変状1'] # len = 1

names_4 = ['名前1', '名前2'] # len = 2
parts_4 = ['変状1', '変状2'] # len = 2

names_5 = [['名前1'], ['名前2']] # len = 2 (多重リスト)
parts_5 = [['変状1', '変状2'], ['変状3']] # len = 2 (多重リスト)

# 使用するデータセット
names = names_5
parts = parts_5

name_length = len(names)
part_length = len(parts)
print(f"name_length: {name_length}")
print(f"part_length: {part_length}")

def is_nested_list(lst):
    return any(isinstance(i, list) for i in lst)

if name_length == 1:
    for single_part in parts:
        name = names[0]
        part = single_part
        print(f"name: {name}")
        print(f"part: {part}")
        print(f"result: ({name}, {part})")
elif name_length >= 2:
    if is_nested_list(names):  # names が多重リストの場合
        for i in range(name_length):
            for name in names[i]:
                for part in parts[i]:
                    print(f"name: {name}")
                    print(f"part: {part}")
                    print(f"result: ({name}, {part})")
    else:
        if part_length == 1:
            # names が2つ以上で parts が1つの場合
            for single_name in names:
                name = single_name
                part = parts[0]
                print(f"name: {name}")
                print(f"part: {part}")
                print(f"result: ({name}, {part})")
        elif part_length >= 2:
            # names が2つ以上で parts が2つ以上の場合
            for name in names:
                for part in parts:
                    print(f"name: {name}")
                    print(f"part: {part}")
                    print(f"result: ({name}, {part})")
