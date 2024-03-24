import glob

name_item =  ['NON-a', '9月7日 佐藤*/*404', '9月7日 佐藤*/*537', '9月8日 佐藤*/*117,9月8日 佐藤*/*253']

target_file = name_item

for many_text in target_file:
    if "," in many_text:
        dis_items = many_text.split(',') # 「9月8日 S*/*117」,「9月8日 S*/*253」
        sub_dis_items = ['infra/static/infra/img/' + item + ".jpg" for item in dis_items]
        # ['infra/static/infra/img/9月8日 佐藤*/*117.jpg', 'infra/static/infra/img/9月8日 佐藤*/*253.jpg']
        for item in sub_dis_items:
            sub_photo_paths = glob.glob(item)
        
        join_dis_items = ",".join(sub_photo_paths)
        # infra/static/infra/img/9月8日 佐藤*/*117.jpg,infra/static/infra/img/9月8日 佐藤*/*253.jpg
        photo_paths = join_dis_items.replace("S", "佐藤").replace(" ", "　")
        
        print(photo_paths)