import glob

name_item = ['NON-a', '9月7日 佐藤404', '9月7日 佐藤537', '9月8日 佐藤117,9月8日 佐藤253']

photo_paths = []

for target_file in name_item:
    if "," in target_file:
        dis_items = target_file.split(',')
        sub_dis_items = ['infra/static/infra/img/' + dis_item.strip() + ".jpg" for dis_item in dis_items]
        photo_paths.append(sub_dis_items)
    else:
        photo_paths.append(['infra/static/infra/img/' + target_file + '.jpg'])

print(photo_paths)