import os

# dir_path = os.getcwd() # 現在の作業ディレクトリ
# dir_path = os.path.expanduser('~') # ユーザーのホームディレクトリ
dir_path = os.path.expanduser('~/Desktop') # デスクトップディレクトリ

files_dir = [
    f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))
]
print(files_dir)