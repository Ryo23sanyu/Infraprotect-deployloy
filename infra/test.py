import glob  # globモジュールをインポート

sub_dis_items = ['infra/static/infra/img/9月7日\u3000佐藤*/*396.jpg', 'infra/static/infra/img/佐藤*/*412.jpg']

photo_paths = []  # photo_pathsリストを初期化
# photo_pathsリストにマッチしたファイルのパスを追加
for item in sub_dis_items:
    sub_photo_paths = glob.glob(item)
    photo_paths.extend(sub_photo_paths)

# photo_pathsの内容を出力して確認
print(photo_paths)