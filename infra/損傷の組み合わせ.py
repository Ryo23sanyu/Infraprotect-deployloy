names_1 = ['名前1'] # len = 1
parts_1 = ['変状1'] # len = 1

names_2 = ['名前1'] # len = 1
parts_2 = ['変状1', '変状2'] # len = 2

names_3 = ['名前1', '名前2'] # len = 2
parts_3 = ['変状1'] # len = 1

names_4 = ['名前1', '名前2'] # len = 2
parts_4 = ['変状1', '変状2'] # len = 2

names_5 = [['名前1'], ['名前2']] # len = 2
parts_5 = [['変状1', '変状2', '変状3'], ['変状4']] # len = 2

names_6 = [['名前1', '名前2'], ['名前3']] # len = 2
parts_6 = [['変状1', '変状2', '変状3'], ['変状4', '変状5']] # len = 2

# 多重リストかどうかを判定する関数
def is_multi_list(lst):
    return any(isinstance(i, list) for i in lst)
  
names = names_6
damages = parts_6

name_length = len(names)
damage_length = len(damages)
print(f"name_length:{name_length}")
print(f"damage_length:{damage_length}")

if not is_multi_list(names) and not is_multi_list(damages) and name_length == 1: # 部材名が1つの場合
    for single_damage in damages: 
        name = names[0]
        damage = single_damage
        print(f"name:{name}")
        print(f"part:{damage}")
        print(f"result:{name,damage}")
elif not is_multi_list(names) and not is_multi_list(damages) and name_length >= 2: # 部材名が2つ以上の場合
    if damage_length == 1: # かつ損傷名が1つの場合
        for single_name in names:
            name = single_name
            damage = damages[0]
            print(f"name:{name}")
            print(f"part:{damage}")
            print(f"result: ({name}, {damage})")
    elif not is_multi_list(names) and not is_multi_list(damages) and damage_length >= 2: # かつ損傷名が2つ以上の場合
        for name in names:
            for damage in damages:
                print(f"name:{name}")
                print(f"part:{damage}")
                print(f"result: ({name},{damage})")

else: # 多重リストの場合
    for i in range(name_length):
        for name in names[i]:
            for damage in damages[i]:
                print(f"name: {name}")
                print(f"part: {damage}")
                print(f"result: ({name}, {damage})")
print(0)