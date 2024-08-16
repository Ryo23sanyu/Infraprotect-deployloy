import os

def get_directories(path='~'):
    dir_path = os.path.expanduser(os.path.join(path, 'Desktop')) # デスクトップディレクトリ
    files_dir = [
        f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))
    ]
    return files_dir

def create_article(request):
    directories = get_directories()
    print(f"directories：{directories}")

# デモ関数を呼び出して結果を確認
create_article(None)