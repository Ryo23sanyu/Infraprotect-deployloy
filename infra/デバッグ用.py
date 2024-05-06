# <<全景写真アップロード>>
import os
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from infra.forms import UploadForm


save_path = r"C:\work\django\myproject\myvenv\Infraproject\infra\static\infra\img"
def display_photo(request):
    print("リクエストメソッド:", request.method)  # リクエストのメソッドを表示
    if request.method == 'POST': # HTTPリクエストがPOSTメソッド(フォームの送信など)であれば、以下のコードを実行
        form = UploadForm(request.POST, request.FILES) # UploadFormを使用して、送信されたデータ(request.POST)とファイル(request.FILES)を取得
        print("フォームが有効か？:", form.is_valid())  # フォームの有効性を表示
        if form.is_valid(): # formのis_valid()メソッドを呼び出して、フォームのバリデーション(検証)を実行
    # フォームが有効な場合は、選択された写真を特定のフォルダに保存します
            # print("フォームが有効")
            photo = form.cleaned_data['photo'] # バリデーションを通過したデータから、'photo'キーに対応するデータを取得しphoto変数に格納
            print("アップロードされた写真の名前:", photo.name)  # アップロードされた写真の名前を表示
            file_name = photo.name  # アップロードされたファイルの名前をfile_name変数に格納
            file_path = os.path.join(save_path, file_name)
            #設定された保存パス（save_path）とファイル名（file_name）を組み合わせ、フルパスをfile_path変数に格納

            with open(file_path, 'wb') as f: # file_pathで指定されたパスにファイルをバイナリ書き込みモード('wb')で開く
                for chunk in photo.chunks(): # アップロードされたファイル(photo)をchunks()メソッドを使用して分割し、ループ処理を行う
                    f.write(chunk) # 各チャンクを開かれたファイル(f)に書き込む
        else:
            print("フォームエラー:", form.errors)  # フォームのエラーを表示
        # フォームが有効・無効 共通
            print(form.errors)  # コンソールにエラーメッセージを出力
            return HttpResponseBadRequest('添付ファイルが見つかりませんでした。 エラー: {}'.format(form.errors))
            #return HttpResponseBadRequest('添付ファイルが見つかりませんでした。')
    else:
        form = UploadForm() # Forms.pyの「UploadForm」を呼び出し
    return render(request, 'upload_photo.html', {'form': form})