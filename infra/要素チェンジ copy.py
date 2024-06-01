sub_related_damages = ['支承本体 Bh0101:①腐食(小小)-b,⑤防食機能の劣化(分類1)-e', '沓座モルタル Bm0101:⑦剥離・鉄筋露出-c,⑰その他(分類6:穴ぼこ)-e,⑤防食機能の劣化(分類1)-e']   

# 処理後のリストを格納するための新しいリスト
second_related_damages = []

# リスト内の各要素をループする
for i, damage in enumerate(sub_related_damages):
    # コロンの位置を取得
    colon_index = damage.find(":")
    
    if colon_index != -1:
        if i == 0:
            # 1番目の要素の場合
            parts = damage.split(',')
            
            if len(parts) > 1:
                first_damage = parts[0].split(':')[0]
                after_damage = ':' + parts[1].strip()
                create_damage = first_damage + after_damage
                second_related_damages.append(create_damage)
                print(f"second_related_damages：{second_related_damages}")

        else:
            # 2つ目以降の要素の場合
            parts = damage.split(',')
            second_related_damages.append(damage)
            print(f"second_related_damages：{second_related_damages}")