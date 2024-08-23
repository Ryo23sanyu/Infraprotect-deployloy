import os
import shutil

if __name__ == "__main__":
    # ローカルファイルリストの取得
    folder_path = 'C:/Users/dobokuka4/Desktop/(件名なし)/案件名/写真' # フォルダパス
    
    # ファイルリストを取得
    try:
        items = os.listdir(folder_path) # フォルダ内のファイルとディレクトリのリスト
        print(items)
    except FileNotFoundError:
        print(f"指定されたパスが見つかりません: {folder_path}")
    except PermissionError:
        print(f"指定されたパスにアクセスする権限がありません: {folder_path}")
        
    # ローカルファイルを別のローカルファイルにコピー
    source_path = '/var/hoge' # コピー元のファイルパス
    destination_path = 'C:/Users/dobokuka4/Desktop/(件名なし)/案件名/写真/hoge.txt' # コピー先のファイルパス

    try:
        # ファイルをコピー
        shutil.copyfile(source_path, destination_path)
        print(f"ファイルをコピーしました: {source_path} -> {destination_path}")
    except FileNotFoundError:
        print(f"指定されたファイルが見つかりません: {source_path}")
    except PermissionError:
        print(f"指定されたファイルにアクセスする権限がありません: {source_path}")
