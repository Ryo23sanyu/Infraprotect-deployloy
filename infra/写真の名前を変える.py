import os

# フォルダパス
folder_path = r'C:\work\django\myproject\program\Infraproject\前回写真'

# ファイル名変更のマッピング
photo_name_dict = {
    (9, 4): 1, (9, 24): 2, (9, 44): '前回写真-3', (23, 4): 3, 
    (23, 24): 4, (23, 44): 5, (46, 4): 6, (46, 24): 7, (46, 44): 8, 
    (60, 4): 9, (60, 24): 10, (60, 44): 11, (83, 4): 12, (83, 24): 13, 
    (83, 44): 14, (97, 4): 15, (97, 24): 16, (97, 44): 17, (120, 4): 18, 
    (120, 24): 19, (120, 44): 20, (134, 4): 21, (134, 24): 22, (134, 44): 23
}

# 辞書の値をリストにして順番に取得
new_names = list(photo_name_dict.values())
print(new_names) # [1, 2, '前回写真-3', 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
# フォルダ内のファイルをリストする
files = os.listdir(folder_path)
files = [f for f in files if f.startswith('photo_') and f.endswith('.jpg')]

# 古い名前に基づき写真ファイルを順番にソート
files.sort(key=lambda x: (int(x.split('_')[1]), int(x.split('_')[2].split('.')[0])))
# ['photo_12_4.jpg', 'photo_12_24.jpg', 'photo_12_44.jpg', 'photo_26_4.jpg', 'photo_26_24.jpg', 'photo_26_44.jpg', 'photo_49_4.jpg', 'photo_49_24.jpg', 'photo_49_44.jpg', 'photo_63_4.jpg', 'photo_63_24.jpg', 'photo_63_44.jpg', 'photo_86_4.jpg', 'photo_86_24.jpg', 'photo_86_44.jpg', 'photo_100_4.jpg', 'photo_100_24.jpg', 'photo_100_44.jpg', 'photo_123_4.jpg', 'photo_123_24.jpg', 'photo_123_44.jpg', 'photo_137_4.jpg', 'photo_137_24.jpg', 'photo_137_44.jpg']
print(files)

# インデックスを初期化
index = 0

for file_name in files:
    # 'photo_' で始まり、'.jpg' で終わるファイルのみを対象にする
    if file_name.startswith('photo_') and file_name.endswith('.jpg'):
        full_path = os.path.join(folder_path, file_name)
        
        try:
            # 新しい名前を取得しインデックスを更新
            new_name = f"{new_names[index]}.jpg"
            new_full_path = os.path.join(folder_path, new_name)
            
            os.rename(full_path, new_full_path)
            print(f"Renamed {full_path} to {new_full_path}")
            
            # インデックスを次に進める
            index += 1

        except Exception as e:
            print(f"Error processing file {file_name}: {e}")

        # もしファイル数が辞書の名前数を超えるならばループを抜ける
        if index >= len(new_names):
            break
