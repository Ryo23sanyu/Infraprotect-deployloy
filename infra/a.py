save_path = r"C:\work\django\myproject\myvenv\Infraproject\infra\static\infra\img"
files_jpg = save_path + "\*.jpg"
files_png = save_path + "\*.png"
files = files_jpg + files_png  # 2つのリストを結合する。
# ページに表示する際、"infra/static/" を削除する。
image_files = []
for file in files:
    image_files.append( file.replace("infra/static/", "") )
    
print(image_files)