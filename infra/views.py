# アプリ内からインポート
from collections import defaultdict
import datetime
from functools import reduce
from io import BytesIO
from itertools import groupby, zip_longest
from operator import attrgetter
import re
import os
import glob
from django.db import IntegrityError
import openpyxl
import tempfile
# サードパーティー製モジュール
import ezdxf
import pandas as pd
import urllib.parse
from markupsafe import Markup
from copy import copy
from itertools import zip_longest
from openpyxl import load_workbook
from openpyxl.drawing.image import Image as OpenpyxlImage
from PIL import Image as PILImage
# django内からインポート
from django.http import FileResponse, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from infraproject import settings
from .models import Approach, Article, DamageComment, DamageList, DamageReport, FullReportData, Infra, PartsName, PartsNumber, Table, LoadGrade, LoadWeight, Photo, Panorama, NameEntry, Regulation, Rulebook, Thirdparty, UnderCondition, Material
from .forms import BridgeCreateForm, BridgeUpdateForm, CensusForm, FileUploadForm, NameEntryForm, PartsNumberForm, TableForm, UploadForm, PhotoUploadForm, NameForm


class ListInfraView(LoginRequiredMixin, ListView):
    template_name = 'infra/infra_list.html'
    model = Infra # 使用するモデル「infra」
    def get_queryset(self, **kwargs):
        # モデル検索のクエリー。Infra.objects.all() と同じ結果で全ての Infra
        queryset = super().get_queryset(**kwargs)
        # パスパラメータpkによりarticleを求める
        # 指定されたpk(idの指定)のデータを取得
# article  = Article.objects.get(id = self.kwargs["pk"])
        # get使用すると、存在しない場合エラーになってしまう
        # 求めたarticleを元にモデル検索のクエリーを絞り込む
        # infra_objectフィルタ－
        #queryset = queryset.filter(article=article)
        queryset = queryset.filter(article = self.kwargs["article_pk"])
        # 絞り込んだクエリーをDjangoに返却し表示データとしてもらう
        return queryset
    def get_context_data(self, **kwargs):
        # HTMLテンプレートでの表示変数として「article_id」を追加。
        # 値はパスパラメータpkの値→取り扱うarticle.idとなる
        kwargs["article_id"] = self.kwargs["article_pk"]
        return super().get_context_data(**kwargs)


class DetailInfraView(LoginRequiredMixin, DetailView):
    template_name = 'infra/infra_detail.html'
    model = Infra
    def get_context_data(self, **kwargs):
        # HTMLテンプレートでの表示変数として「article_id」を追加。
        # 値はパスパラメータpkの値→取り扱うarticle.idとなる
        kwargs["article_id"] = self.kwargs["article_pk"]
        #モデルのTableクラス ↑                    ↑  infraに格納する値は自らのpkの値とする
        return super().get_context_data(**kwargs)
  
class CreateInfraView(LoginRequiredMixin, CreateView):
    template_name = 'infra/infra_create.html' # 対応するhtmlの名前
    model = Infra # models.pyのどのモデルと紐付くか
    # form_class = BridgeCreateForm # forms.pyのどのクラスと紐付くか
    fields = ('title', '径間数', '橋長', '全幅員','橋梁コード', '活荷重', '等級', '適用示方書', '上部構造形式', '下部構造形式', '基礎構造形式', '近接方法', '交通規制', '第三者点検', '海岸線との距離', '路下条件', '交通量', '大型車混入率', '特記事項', 'カテゴリー', 'article')
    success_url = reverse_lazy('detail-infra')

    def form_valid(self, form):
        #ここのobjectはデータベースに登録を行うmodelつまりInfraの１レコードです。
        #formはModelFormと呼ばれるフォームの仕組みで、saveを実行すると関連付いているモデルとして登録を行う動きをします。
        object = form.save(commit=False)
        #ここでのobjectは登録対象のInfraモデル１件です。登録処理を行いPKが払い出された情報がobjectです
        #今回はarticle_id、つまりarticleオブジェクトが無いのでこれをobjectに設定します。
        #articleオブジェクトを検索しobjectに代入する事で登録できます。
# article = Article.objects.get( id = self.kwargs["pk"] )
        # id = 1 のarticleを検索
            # article = Article.objects.get(id = 1 )
        object.案件名 = self.kwargs["article_pk"]
        # titleの項目に「A」を設定
            # article.title = "A"
        #設定したのちsaveを実行し更新します。
        object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('list-infra', kwargs={'article_pk': self.kwargs["article_pk"]})

    #新規作成時、交通規制の全データをコンテキストに含める。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["loadWeights"] = LoadWeight.objects.all()
        context["loadGrades"] = LoadGrade.objects.all()
        context["rulebooks"] = Rulebook.objects.all()
        context["approachs"] = Approach.objects.all()
        context["regulations"] = Regulation.objects.all()
        context["thirdpartys"] = Thirdparty.objects.all()
        context["underconditions"] = UnderCondition.objects.all()
        return context
        
    def keikan_create_view(request, article_pk, pk): # keikan_create_view関数を定義
        if request.method == "POST": # リクエストメソッドがpostの場合
            form = BridgeCreateForm(request.POST) # BridgeCreateFormというフォームクラスのインスタンスを生成
            if form.is_valid(): # formが正常の場合
                keikan_number = form.cleaned_data['径間数'] # form.cleaned_dataから'径間数'キーに対応するデータを取得
                request.session['keikan_number'] = keikan_number # 取得した"径間数"を現在のユーザーセッションに保存
                # print(form.instance.pk)
                return redirect('bridge-table', article_pk, pk) # 「table」という名前のURLにリダイレクト
            else:
                form = BridgeCreateForm() # 新しい空のフォームインスタンスを生成
        return render(request, 'infra/infra_create.html', {'form': form, 'object': Table.objects.filter(id=pk).first()}) # 'infra_create.html'テンプレートをレンダリング
    
    def damage_view(request, article_pk, pk): # damage_view関数を定義
        keikan_number = request.session.get('keikan_number', 1) # request.session.getメソッドを使い、セッションから"径間数"を取得、デフォルト値は1
        keikan_range = list(range(keikan_number)) # 1からkeikan_number（"径間数"）までの連続する整数列を生成
        return render(request, 'bridge_table.html', {'keikan_range': keikan_range, 'object': Table.objects.filter(id=pk).first()}) # 'table.html'テンプレートをレンダリング

class DeleteInfraView(LoginRequiredMixin, DeleteView):
    template_name = 'infra/infra_delete.html'
    model = Infra
    success_url = reverse_lazy('list-infra')
    def get_success_url(self):
        return reverse_lazy('list-infra', kwargs={'article_pk': self.kwargs["article_pk"]})
      
class UpdateInfraView(LoginRequiredMixin, UpdateView):
    template_name = 'infra/infra_update.html'
    model = Infra
    fields = ('title', '径間数', '橋長', '全幅員', 'latitude', 'longitude', '橋梁コード', '活荷重', '等級', '適用示方書', '上部構造形式', '下部構造形式', '基礎構造形式', '近接方法', '交通規制', '第三者点検', '海岸線との距離', '路下条件', '交通量', '大型車混入率', '特記事項', 'カテゴリー', 'article')
    success_url = reverse_lazy('detail-infra')
    def get_success_url(self):
        return reverse_lazy('detail-infra', kwargs={'article_pk': self.kwargs["article_pk"], 'pk': self.kwargs["pk"]})

    #新規作成時、交通規制の全データをコンテキストに含める。
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 編集中のインスタンスに紐づく交通規制のIDをリストとして取得
        # コンテキストに追加
        selected_regulations = self.object.交通規制.values_list('id', flat=True)# 選択状態を保持
        context['selected_regulations'] = list(selected_regulations)# 選択状態を保持
        context["regulations"] = Regulation.objects.all()
        
        selected_loadWeights = self.object.活荷重.values_list('id', flat=True)
        context['selected_loadWeights'] = list(selected_loadWeights)
        context["loadWeights"] = LoadWeight.objects.all()
        
        selected_loadGrades = self.object.等級.values_list('id', flat=True)
        context['selected_loadGrades'] = list(selected_loadGrades)
        context["loadGrades"] = LoadGrade.objects.all()
        
        selected_rulebooks = self.object.適用示方書.values_list('id', flat=True)
        context['selected_rulebooks'] = list(selected_rulebooks)
        context["rulebooks"] = Rulebook.objects.all()
        
        selected_approachs = self.object.近接方法.values_list('id', flat=True)
        context['selected_approachs'] = list(selected_approachs)
        context["approachs"] = Approach.objects.all()
        
        selected_thirdpartys = self.object.第三者点検.values_list('id', flat=True)
        context['selected_thirdpartys'] = list(selected_thirdpartys)
        context["thirdpartys"] = Thirdparty.objects.all()
        
        selected_underconditions = self.object.路下条件.values_list('id', flat=True)
        context['selected_underconditions'] = list(selected_underconditions)
        context["underconditions"] = UnderCondition.objects.all()
        return context

def infra_view(request):
    if request.method == 'POST':
        等級 = request.POST.get('等級', None)
        # load_gradeを使って必要な処理を行う
        # 例えば、選択されたload_gradeに基づいてデータをフィルタリングして表示するなど

    # 通常のビューロジック
    return render(request, 'infra/infra_detail.html')

def index_view(request):
    order_by = request.GET.get('order_by', '案件名')
    object_list = Article.objects.order_by(order_by)
    return render(request, 'infra/index.html', {'object_list': object_list})

class ListArticleView(LoginRequiredMixin, ListView):
    template_name = 'infra/article_list.html'
    model = Article
  
class DetailArticleView(LoginRequiredMixin, DetailView):
    template_name = 'infra/article_detail.html'
    model = Article
    
class CreateArticleView(LoginRequiredMixin, CreateView):
    template_name = 'infra/article_create.html'
    model = Article
    fields = ('案件名', '土木事務所', '対象数', '担当者名', 'その他')
    success_url = reverse_lazy('list-article')
  
class DeleteArticleView(LoginRequiredMixin, DeleteView):
    template_name = 'infra/article_delete.html'
    model = Article
    success_url = reverse_lazy('list-article')
  
class UpdateArticleView(LoginRequiredMixin, UpdateView):
    template_name = 'infra/article_update.html'
    model = Article
    fields = ('案件名', '土木事務所', '対象数', '担当者名', 'その他')
    success_url = reverse_lazy('list-article')

# << ファイルのアップロード・各infraに紐付け >>
def file_upload(request, article_pk, pk):
    if request.method == 'POST':
                #                  ↓  request.POST の中にdxfファイルの名前が入っているだけ。.copy() を実行して編集可能にする。
        copied          = request.POST.copy()

        # ここで Infraのid(pk)を指定する。
        copied["infra"] = pk
        
        # バリデーション
        form = TableForm(copied, request.FILES)
        
        # 既存のオブジェクトに対して新しいファイルを上書きする処理
        if Table.objects.filter(infra=pk).first():
            obj = Table.objects.get(infra=pk)
            form = TableForm(copied, request.FILES, instance=obj)
            
        if form.is_valid():
            form.save()
            return redirect('file_upload_success')
    else:
        form = TableForm()
    return render(request, 'infra/file_upload.html', {'form': form, 'article_pk': article_pk, 'pk': pk})

def file_upload_success(request):
    return render(request, 'infra/file_upload_success.html')
  
def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'infra/photo_list.html', {'photos': photos})

def selected_photos(request):
    selected_photo_ids = request.POST.getlist('selected_photos')
    selected_photos = Photo.objects.filter(id__in=selected_photo_ids)
    return render(request, 'infra/selected_photos.html', {'selected_photos': selected_photos})


def panorama_list(request):
    panoramas = Panorama.objects.all()
    if request.method == 'POST':
        selected_ids = request.POST.getlist('image_list')
        for panorama in panoramas:
            if str(panorama.id) in selected_ids:
                panorama.checked = True
            else:
                panorama.checked = False
            panorama.save()
        return redirect('image_list')  # 再描画のためにリダイレクト
    
    return redirect('image_list')
    #return render(request, 'image_list.html', {'panoramas': panoramas})

def panorama_upload(request):
    if request.method == 'POST':
        image = request.FILES['image']
        checked = request.POST.get('checked', False)
        panorama = Panorama.objects.create(image=image, checked=checked)
        return redirect('photo')
    return render(request, 'panorama_upload.html')

# << センサス調査 >>
def census_view(request):
    form = CensusForm()
    return render(request, 'infra_detail.html', {'form': form})

# << 全景写真の表示 >>
def image_list(request):
    # 特定のディレクトリ内の全てのファイルパスをリストで取得したい場合はglobを使うと良い。
    save_path = str(settings.BASE_DIR) + "\infra\static\infra\img"
    # 「C:\work\django\myproject\program\Infraproject」+「\infra\static\infra\img」と同意
    files_jpg = glob.glob(save_path + "\*.jpg")
    files_png = glob.glob(save_path + "\*.png")
    files = files_jpg + files_png  # 2つのリストを結合する。
    # ページに表示する際、"infra/static/" を削除する。

    web_base_path = "infra/img/"  # ウェブからアクセスする際のベースパス

    image_files = []
    for file_path in files:
        # OSの絶対パスからウェブアクセス可能な相対パスへ変換
        relative_path = file_path.replace(save_path, web_base_path).replace("\\", "/")
        image_files.append(relative_path)
    # テンプレートに画像ファイルの一覧を渡してレンダリングする
    return render(request, 'image_list.html', {'image_files': image_files})

# << 全景写真アップロード >>
save_path = str(settings.BASE_DIR) + "\infra\static\infra\img"
# 「C:\work\django\myproject\program\Infraproject」+「\infra\static\infra\img」と同意
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
            return redirect('image_list')
        else:
            print("フォームエラー:", form.errors)  # フォームのエラーを表示
        # フォームが有効・無効 共通
            print(form.errors)  # コンソールにエラーメッセージを出力
            return HttpResponseBadRequest('添付ファイルが見つかりませんでした。 エラー: {}'.format(form.errors))
            #return HttpResponseBadRequest('添付ファイルが見つかりませんでした。')
    else:
        form = UploadForm() # Forms.pyの「UploadForm」を呼び出し
    return render(request, 'upload_photo.html', {'form': form})

def photo_upload(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = PhotoUploadForm()
    return render(request, 'image_list.html', {'form': form})

# << 全景写真の変更 >>
def change_photo(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # ここで、古い写真の削除や新しい写真の保存処理を行います。
            # 例: image_idを使用して特定のレコードを探し、そのレコードに新しい画像を保存
            image_id = request.POST.get('image_id', None)  # 画像ID取得
            if image_id:
                image_instance = UploadForm.objects.get(id=image_id)
                image_instance.photo = form.cleaned_data['photo']
                image_instance.save()
                return redirect('image_list')
            else:
                # エラー処理
                pass
        else:
            # フォームのバリデーションに失敗したときの処理
            pass
    else:
        form = UploadForm()  # GETリクエストの場合、空のフォームを表示

    return render(request, 'upload_photo.html', {'form': form})

# << 損傷写真帳の作成 >>
def bridge_table(request, article_pk, pk): # idの紐付け infra/bridge_table.htmlに表示
    context = {}
    # プロジェクトのメディアディレクトリからdxfファイルまでの相対パス
    # URL：article/<int:article_pk>/infra/<int:pk>/bridge-table/
    table = Table.objects.filter(id=pk).first()
    #print(f"table_name:{table}") # Table object (17)
    infra_instance = Infra.objects.filter(title = table.infra.title)
    #print(f"table_name:{infra_instance}") # センサス橋
    # オブジェクトディレクトリの相対パスを取得
    if table.dxf:
        encoded_url_path = table.dxf.url
    decoded_url_path = urllib.parse.unquote(encoded_url_path) # URLデコード
    # 絶対パスと合体
    dxf_filename = os.path.join(settings.BASE_DIR, decoded_url_path.lstrip('/'))
    
    context["object"] = table
    # keikan_infra = Infra.objects.filter(id=pk).first() # 271行目と同じ
    context["buttons"] = table.infra.径間数 * " " # Tableクラスのinfraオブジェクトから「径間数」を取り出す
    
    if "search_title_text" in request.GET:
        # request.GET：検索URL（http://127.0.0.1:8000/article/1/infra/bridge_table/?search_title_text=1径間） 
        search_title_text = request.GET["search_title_text"]
        # 検索URL内のsearch_title_textの値（1径間）を取得する
    else:
        search_title_text = "1径間" # 検索URLにsearch_title_textがない場合

    second_search_title_text = "損傷図"
    
    sorted_items = create_picturelist(request, table, dxf_filename, search_title_text, second_search_title_text)

    # << 辞書型として、全径間を1つの多重リストに格納 >>
    max_search_title_text = table.infra.径間数
    database_sorted_items = []  # 結果をまとめるリスト
    
    for search_title_text_with_suffix in range(1, max_search_title_text + 1):
        search_title_text = f"{search_title_text_with_suffix}径間"
        sub_database_sorted_items = create_picturelist(request, table, dxf_filename, search_title_text, second_search_title_text)
        for item in sub_database_sorted_items:
            item['search'] = search_title_text
            database_sorted_items.append(item)
    # print(f"database_sorted_items:{database_sorted_items}")
    """辞書型の多重リストをデータベースに登録"""
    # << ['']を外してフラットにする >>
    def flatten(value):
        def _flatten(nested_list):
            if isinstance(nested_list, list):
                for item in nested_list:
                    yield from _flatten(item)
            else:
                yield nested_list
        
        return ', '.join(_flatten(value))

    # << joinキーを変換 >>
    def join_to_result_string(join):
        result_parts = []
        for item in join:
            parts_name = item['parts_name'][0]
            damage_names = item['damage_name']
            formatted_damage_names = '/'.join(damage_names)
            result_parts.append(f"{parts_name} : {formatted_damage_names}")
        return ', '.join(result_parts)

    # << 写真のキーを変換 >>
    def simple_flatten(value):
        return ', '.join(map(str, value)) if isinstance(value, list) else value
    
    # <<正規表現で4桁以上の番号を取得>>
    def extract_number(text):
        pattern = r'\d{4,}' # 4文字以上の連続する数字
        matches = re.findall(pattern, text)
        return matches
    
    for damage_data in database_sorted_items:
        #print(f"damage_data：{damage_data}")
        # 元の辞書から 'picture_number' の値を取得
        #             　辞書型 ↓           ↓ キーの名前      ↓ 存在しない場合、デフォルト値として空白を返す
        picture_number = damage_data.get('picture_number', '')
        # 正規表現で数字のみを抽出
        if picture_number:
            # 数字のみを抽出
            numbers_only = re.findall(r'\d+', str(picture_number)) # ['2']
            # 数字を結合して整数に変換
            numbers_only = int(''.join(numbers_only)) if numbers_only else None # 2
        else:
            numbers_only = None

        damage_coordinate = damage_data.get('damage_coordinate', [None, None])
        picture_coordinate = damage_data.get('picture_coordinate', [None, None])

        #parts_list = flatten(damage_data.get('parts_name', ''))
        #damage_list = flatten(damage_data.get('damage_name', ''))

        names = damage_data.get('parts_name', '')
        damages = damage_data.get('damage_name', '')
        #print(f"names:{names}")
        #print(f"damages:{damages}")
        
        split_names = []

        for item in names:
            split_items = []
            for split in item:
                if "～" in split:
                    one = split.find("～")
                    start_number = ''.join(extract_number(split[:one])) # 0101
                    end_number = ''.join(extract_number(split[one+1:])) # 0204

                    # 最初の2桁と最後の2桁を取得
                    start_prefix = start_number[:2] # 01
                    start_suffix = start_number[2:] # 01
                    end_prefix = end_number[:2] # 01
                    end_suffix = end_number[2:] # 03
                    
                    part_name = split[:one].replace(start_number, '')
                
                    for prefix in range(int(start_prefix), int(end_prefix)+1):
                        for suffix in range(int(start_suffix), int(end_suffix)+1):
                            number_items = "{:02d}{:02d}".format(prefix, suffix)
                            join_item = part_name + number_items
                            split_items.append(join_item)
                    
                else:
                    split_items.append(split)
            split_names.append(split_items)
        
        join = join_to_result_string(damage_data.get('join', ''))
        this_time_picture = simple_flatten(damage_data.get('this_time_picture', ''))
        last_time_picture = simple_flatten(damage_data.get('last_time_picture', ''))
        textarea_content = damage_data.get('textarea_content', '')
        damage_coordinate_x = damage_coordinate[0] if damage_coordinate else None
        damage_coordinate_y = damage_coordinate[1] if damage_coordinate else None
        picture_coordinate_x = picture_coordinate[0] if picture_coordinate else None
        picture_coordinate_y = picture_coordinate[1] if picture_coordinate else None
        span_number = damage_data.get('search', '')
        
        name_length = len(split_names)
        damage_length = len(damages)
        
        # 多重リストかどうかを判定する関数
        def is_multi_list(lst):
            return any(isinstance(i, list) for i in lst)
        
        def process_names(names):
            """
            与えられたnamesを処理し、適切な部分を返す関数。
            """
            
            parts_left = ["主桁", "PC定着部"]  # 左の数字
            parts_right = ["横桁", "橋台"]     # 右の数字
            parts_zero = ["床版"]              # 00になる場合

            # namesから部品名（parts）と数字を抽出
            space = names.find(" ")
            parts = names[:space]  # 部品名
            number = ''.join(extract_number(names))  # 数字
            parts_join = names.replace(number, '') # 符号部分を取得

            # 必要な部分の数字を抽出するロジック
            split_number = ''

            if parts in parts_zero:
                split_number = '00'
            elif len(number) == 4 or int(number[2:]) >= 100:
                if parts in parts_left:
                    split_number = number[:2]
                elif parts in parts_right:
                    split_number = number[2:]
                else:
                    split_number = '00'
            else:
                if parts in parts_left:
                    split_number = number[:3]
                elif parts in parts_right:
                    split_number = number[3:]
                else:
                    split_number = '00'

            result = parts_join + split_number  # 結果を組み立てる
            return result
            # 共通のフィールドを辞書に格納
        
        if not is_multi_list(split_names) and not is_multi_list(damages) and name_length == 1: # 部材名が1つの場合
            for single_damage in damages: 
                parts_name = names[0]
                damage_name = flatten(single_damage)
                #print(f"parts_name1:{parts_name}")
                #print(f"damage_name1:{damage_name}")
                parts_split = process_names(flatten(parts_name))
                data_fields = {
                    'parts_name': parts_name,
                    'damage_name': damage_name,
                    'parts_split': parts_split,
                    'join': join,
                    'picture_number': numbers_only,
                    'this_time_picture': this_time_picture,
                    'last_time_picture': last_time_picture,
                    'textarea_content': textarea_content,
                    'damage_coordinate_x': damage_coordinate_x,
                    'damage_coordinate_y': damage_coordinate_y,
                    'picture_coordinate_x': picture_coordinate_x,
                    'picture_coordinate_y': picture_coordinate_y,
                    'span_number': span_number,
                    'special_links': '/'.join([str(parts_split), str(damage_name), str(span_number)]),
                    'infra': Infra.objects.get(id=pk)
                }
                report_data_exists = FullReportData.objects.filter(**data_fields).exists()
                if report_data_exists:
                    print("データが存在しています。")
                else:
                    try:
                        damage_obj, created = FullReportData.objects.update_or_create(**data_fields)
                        damage_obj.save()
                    except IntegrityError:
                        print("ユニーク制約に違反していますが、既存のデータを更新しませんでした。")

        elif not is_multi_list(split_names) and not is_multi_list(damages) and name_length >= 2: # 部材名が2つ以上の場合
            if damage_length == 1: # かつ損傷名が1つの場合
                for single_name in split_names:
                    parts_name = single_name
                    damage_name = flatten(damages[0])
                    #print(f"parts_name2:{parts_name}")
                    #print(f"damage_name2:{damage_name}")
                    parts_split = process_names(flatten(parts_name))
                    data_fields = {
                        'parts_name': parts_name,
                        'damage_name': damage_name,
                        'parts_split': parts_split,
                        'join': join,
                        'picture_number': numbers_only,
                        'this_time_picture': this_time_picture,
                        'last_time_picture': last_time_picture,
                        'textarea_content': textarea_content,
                        'damage_coordinate_x': damage_coordinate_x,
                        'damage_coordinate_y': damage_coordinate_y,
                        'picture_coordinate_x': picture_coordinate_x,
                        'picture_coordinate_y': picture_coordinate_y,
                        'span_number': span_number,
                        'special_links': '/'.join([str(parts_split), str(damage_name), str(span_number)]),
                        'infra': Infra.objects.get(id=pk)
                    }
                    report_data_exists = FullReportData.objects.filter(**data_fields).exists()
                    if report_data_exists:
                        print("データが存在しています。")
                    else:
                        try:
                            damage_obj, created = FullReportData.objects.update_or_create(**data_fields)
                            damage_obj.save()
                        except IntegrityError:
                            print("ユニーク制約に違反していますが、既存のデータを更新しませんでした。")

            elif not is_multi_list(split_names) and not is_multi_list(damages) and damage_length >= 2: # かつ損傷名が2つ以上の場合
                for name in split_names:
                    for damage in damages:
                        parts_name = name
                        damage_name = flatten(damage)
                        #print(f"parts_name3:{parts_name}")
                        #print(f"damage_name3:{damage_name}")
                        parts_split = process_names(flatten(parts_name))
                        data_fields = {
                            'parts_name': parts_name,
                            'damage_name': damage_name,
                            'parts_split': parts_split,
                            'join': join,
                            'picture_number': numbers_only,
                            'this_time_picture': this_time_picture,
                            'last_time_picture': last_time_picture,
                            'textarea_content': textarea_content,
                            'damage_coordinate_x': damage_coordinate_x,
                            'damage_coordinate_y': damage_coordinate_y,
                            'picture_coordinate_x': picture_coordinate_x,
                            'picture_coordinate_y': picture_coordinate_y,
                            'span_number': span_number,
                            'special_links': '/'.join([str(parts_split), str(damage_name), str(span_number)]),
                            'infra': Infra.objects.get(id=pk)
                        }
                        report_data_exists = FullReportData.objects.filter(**data_fields).exists()
                        if report_data_exists:
                            print("データが存在しています。")
                        else:
                            try:
                                damage_obj, created = FullReportData.objects.update_or_create(**data_fields)
                                damage_obj.save()
                            except IntegrityError:
                                print("ユニーク制約に違反していますが、既存のデータを更新しませんでした。")

        else: # 多重リストの場合
            for i in range(name_length):
                for name in split_names[i]:
                    for damage in damages[i]:
                        parts_name = name
                        damage_name = flatten(damage)
                        #print(f"parts_name4:{parts_name}")
                        #print(f"damage_name4:{damage_name}")
                        parts_split = process_names(flatten(parts_name))
                        data_fields = {
                            'parts_name': parts_name,
                            'damage_name': damage_name,
                            'parts_split': parts_split,
                            'join': join,
                            'picture_number': numbers_only,
                            'this_time_picture': this_time_picture,
                            'last_time_picture': last_time_picture,
                            'textarea_content': textarea_content,
                            'damage_coordinate_x': damage_coordinate_x,
                            'damage_coordinate_y': damage_coordinate_y,
                            'picture_coordinate_x': picture_coordinate_x,
                            'picture_coordinate_y': picture_coordinate_y,
                            'span_number': span_number,
                            'special_links': '/'.join([str(parts_split), str(damage_name), str(span_number)]),
                            'infra': Infra.objects.get(id=pk)
                        }
                        report_data_exists = FullReportData.objects.filter(**data_fields).exists()
                        if report_data_exists:
                            print("データが存在しています。")
                        else:
                            try:
                                damage_obj, created = FullReportData.objects.update_or_create(**data_fields)
                                damage_obj.save()
                            except IntegrityError:
                                print("ユニーク制約に違反していますが、既存のデータを更新しませんでした。")
    """
        # 共通のdata_fieldsを設定
        data_fields = {
            'parts_name': names, # parts_name,
            'damage_name': damages, # damage_name,
            'parts_split': parts_split,
            'join': join,
            'picture_number': numbers_only,
            'this_time_picture': this_time_picture,
            'last_time_picture': last_time_picture,
            'textarea_content': textarea_content,
            'damage_coordinate_x': damage_coordinate_x,
            'damage_coordinate_y': damage_coordinate_y,
            'picture_coordinate_x': picture_coordinate_x,
            'picture_coordinate_y': picture_coordinate_y,
            'span_number': span_number,
            'special_links': '/'.join([str(parts_split), str(damage_name), str(span_number)]),
            'infra': Infra.objects.get(id=pk)
        }
        report_data_exists = FullReportData.objects.filter(**data_fields).exists()

        if report_data_exists:
            print("データが存在しています。")
        else:
            try:
                damage_obj, created = FullReportData.objects.update_or_create(**data_fields)
                damage_obj.save()
            except IntegrityError:
                print("ユニーク制約に違反していますが、既存のデータを更新しませんでした。")
    """                
    """辞書型の多重リストをデータベースに登録(ここまで)"""
    # path('article/<int:article_pk>/infra/<int:pk>/bridge-table/', views.bridge_table, name='bridge-table')

    #context["damage_table"] = sorted_items
    #return render(request, "infra/bridge_table.html", context)

    # # テンプレートをレンダリング
    # return render(request, 'infra/bridge_table.html', context)
    bridges = FullReportData.objects.filter(infra=pk)
    
    # HTMLにまとめて表示するためのグループ化
    grouped_data = []
    for key, group in groupby(bridges, key=attrgetter('join', 'damage_coordinate_x', 'damage_coordinate_y')):
        grouped_data.append(list(group))
        
    context = {'grouped_data': grouped_data}
    # テンプレートをレンダリング
    return render(request, 'infra/bridge_table.html', context)
    #context = {'bridge_table': FullReportData.objects.filter(infra=pk), 'grouped_data': grouped_data}
    # テンプレートをレンダリング
    #return render(request, 'infra/bridge_table.html', context)
def ajax_file_send(request):
    if request.method == 'POST': # HTTPリクエストがPOSTメソッドかつ
        if 'upload-file' in request.FILES: # アップロードされたファイルがrequest.FILESに入っている場合
            myfile = request.FILES['upload-file'] # 受け取ったファイルをmyfileという変数に代入
            fs = FileSystemStorage() # FileSystemStorageのインスタンスを生成(システム上にファイルを保存する準備)
            filename = fs.save(myfile.name, myfile) # myfileを指定した名前で保存し、保存したファイルの名前をfilename変数に格納
            uploaded_file_url = fs.url(filename) # 保存したファイルにアクセスするためのURLを生成
            # success時のレスポンスはJSON形式で返すならこちらを使う
            return JsonResponse({'upload_file_url': uploaded_file_url})
            # HTMLページを返す場合はこちらを使う
            # context = {'damage_table': sorted_text_list}
            # return render(request, 'table.html', context)
        else:
            # ファイルがPOSTされていない場合はエラーレスポンスを返す
            return HttpResponseBadRequest('添付ファイルが見つかりませんでした。') # File is not attached
    else:
        # POSTメソッドでない場合はエラーレスポンスを返す
        return HttpResponseBadRequest('無効な作業です。') # Invalid request method

# << ファイルアップロード(プライマリーキーで分類分け) >>
def upload_directory_path(instance, filename):
    # プライマリーキーを取得する
    primary_key = instance.pk
    # 'documents/プライマリーキー/filename' のパスを返す
    return 'uploads/{}/{}'.format(primary_key, filename)

# class Upload(models.Model):
#     file = models.FileField(upload_to=upload_directory_path)

# << 所見一覧 >>
def observations_list(request, article_pk, pk):
    context = {}

    table = Table.objects.filter(id=pk).first()
    print(f"table_name:{table}")

    if table.dxf:
        encoded_url_path = table.dxf.url
    decoded_url_path = urllib.parse.unquote(encoded_url_path)
    # 絶対パスと合体
    dxf_filename = os.path.join(settings.BASE_DIR, decoded_url_path.lstrip('/'))
    
    context["object"] = table
    context["buttons"] = table.infra.径間数 * " "
    
    if "search_title_text" in request.GET:
        search_title_text = request.GET["search_title_text"]
    else:
        search_title_text = "1径間"

    second_search_title_text = "損傷図"
    
    sorted_items = create_picturelist(request, table, dxf_filename, search_title_text, second_search_title_text)
    """"""
    # 全パーツデータを取得
    print(f"Received article_pk: {article_pk}, id: {pk}")
    
    infra_name = table.infra.title
    print(f"infra_name:{infra_name}")
    parts_data = PartsNumber.objects.filter(infra=pk)
    print(f"parts_data:{parts_data}")
    
    material_replace_map = {
        "鋼": "S",
        "コンクリート": "C",
        "アスファルト": "A",
        "ゴム": "R",
        "その他": "X",
    }
    
    lank_order = ['a', 'b', 'c', 'd', 'e']  # ランクの順序をリストで定義
    def get_lank_value(damage_name):
        """damage_nameのランク部分を取得する"""
        if "-" in damage_name:
            return damage_name.split('-')[-1]
        return None
    
    for part in parts_data:
        part_full_name = f"{part.parts_name} {part.symbol}{part.number}"

        # FullReportDataから該当するデータを取得
        report_data_list = FullReportData.objects.filter(
            parts_name=part_full_name,
            infra=part.infra
        )

        for report_data in report_data_list:
            print(f"report_data_list:{report_data.damage_name}")
                        
            # DamageListに必要なフィールドを含むインスタンスを作成
            damage_list_entry = DamageList(
                parts_name = part.parts_name, # 主桁
                symbol = part.symbol, # Mg
                number = part.number, # 0101
                material = part.material, # S,C
                main_parts = "〇" if part.main_frame else "",  # 主要部材のフラグ
                damage_name = report_data.damage_name, # ⑦剥離・鉄筋露出-d
                damage_max_lank = '',
                damage_min_lank = '',
                classification = '', # 損傷写真帳のデータ入力を反映
                pattern = '', # 損傷写真帳のデータ入力を反映
                span_number = part.span_number,
                infra = part.infra
            )

            try:
                # DamageListインスタンスを保存
                damage_list_entry.save()
                
            except IntegrityError:
                # 重複データがある場合の処理
                print("データが存在しています。")
                # 必要に応じてログを記録したり、他の処理を追加したりできます
                continue  # 次のループに進む
            
            """所見用のクラス登録"""
            damage_name = report_data.damage_name.split('-')[0] if '-' in report_data.damage_name else report_data.damage_name
            
            main_parts_list_left = ["主桁", "PC定着部"] # 左の数字
            main_parts_list_right = ["横桁", "橋台"] # 右の数字
            main_parts_list_zero = ["床版"] # 00になる場合
            
            parts_name = f"{part.parts_name} {part.number}"
            
            if any(word in parts_name for word in main_parts_list_left):
                left = parts_name.find(" ")
                number2 = parts_name[left+1:]
                number_part = re.search(r'[A-Za-z]*(\d+)', number2).group(1)
                result_parts_name = parts_name[:left]+" "+number_part[:2] # 主桁 03
            elif any(word in parts_name for word in main_parts_list_right):
                right = parts_name.find(" ")
                number2 = parts_name[right+1:]
                number_part = re.search(r'[A-Za-z]*(\d+)', number2).group(1)
                if len(number_part) < 5:
                    result_parts_name = parts_name[:right]+" "+number_part[2:] # 横桁 02
                else:
                    result_parts_name = parts_name[:right]+" "+number_part[2:] # 横桁 103
            elif any(word in parts_name for word in main_parts_list_zero):
                right = parts_name.find(" ")
                result_parts_name = parts_name[:right]+" 00"
            else:
                right = parts_name.find(" ")
                result_parts_name = parts_name[:right]
            
            damage_comment_entry = DamageComment(
                parts_name = result_parts_name, # 主桁 01
                material = part.material, # S,C
                main_parts = "〇" if part.main_frame else "", # 主要部材のフラグ
                damage_name = damage_name,
                damage_max_lank = '', # e
                damage_min_lank = '', # b
                picture = '',
                jadgement = '',
                comment = '',
                cause = '',
                span_number = part.span_number,
                infra = part.infra
            )
   
            try:
                # DamageListインスタンスを保存
                damage_comment_entry.save()
                
            except IntegrityError:
                # 重複データがある場合の処理
                print("データが存在しています。")
                # 必要に応じてログを記録したり、他の処理を追加したりできます
                continue  # 次のループに進む
            
    return render(request, 'observer_list.html', {'data': DamageComment.objects.filter(infra=pk),'article_pk': article_pk, 'pk': pk})
    """
    # TODO:関数化して、別コードでも使用できるようにする
    # 番号登録のデータを別の(FullReportData)モデルに合体させる
    # 損傷写真帳のデータと番号登録のデータを合体、重複の削除と並び替え
    result_items = []

    for item in sorted_items:
        join_items = item.get('join', [])
        pictures = item.get('this_time_picture', [])
        
        # 各 join 要素に picture を追加
        for join_item in join_items:
            join_item['this_time_picture'] = pictures
        
        result_items.append({'join': join_items})

    # joinキーのみを抽出
    join_values = [item['join'] for item in result_items]

    # join値を1行にまとめる
    flattened_join = [join_item for sublist in join_values for join_item in sublist]

    # << 番号登録のデータを呼び出す >>
    parts_numbers = PartsNumber.objects.filter(infra=pk)
    #print(f"parts_numbers：{parts_numbers}")
    number_create = []

    for parts_number in parts_numbers:
        dic = {}

        dic['parts_name'] = [parts_number.parts_name.部材名]
        dic['symbol'] = [parts_number.symbol]
        dic['number'] = [parts_number.number]

        materials = ""
        for material in parts_number.material.all():
            materials += material.材料 + ":"

        # 鋼、その他、プラスチックの場合
        # 鋼:その他:プラスチック: になる。
        # 最後の1文字を取り除いた文字を新しいmaterialsに入れる。

        materials = materials[:-1]
        dic['material'] = [materials]

        if parts_number.main_frame:
            dic['main_frame'] = ["〇"]
        else:
            dic['main_frame'] = ["✕"]

        number_create.append(dic)
        
    #print(f"number_create:{number_create}")
    #print(f"flattened_join:{flattened_join}")
    
    # << 材料の置換 >>
    replace_dict = {
        '鋼': 'S',
        'コンクリート': 'C',
        'その他': 'X'
    }

    # 置換処理
    for part in number_create:
        part['material'] = [replace_dict.get(mat, mat) for mat in part['material']]
        # parts_name と symbol の各要素を結合して新しいリストを作成
        combined = [p + ' ' + s for p, s in zip(part['parts_name'], part['symbol'])]
        # 新しいリストを parts_name に設定（symbol は削除）
        part['parts_name'] = combined
        del part['symbol']

    # << parts_nameを部材名と番号に分割 >>
    split_parts_and_damage = []

    # 各要素に対して処理を行う
    for item in flattened_join:
        combined_string = item['parts_name'][0]
        
        # 正規表現を使って、記号と数字の部分で分割する
        match = re.match(r'(.+ [A-Za-z]+)(\d+)', combined_string)
        
        if match:
            parts_name = match.group(1)
            number = match.group(2)
            
            for damage in item['damage_name']:
                if "-" in damage:
                    damage_name, damage_lank = damage.split("-")
                
                parts_dict = {
                    'parts_name': [parts_name],
                    'number': [number],
                    'damage_name': [damage_name],
                    'damage_lank': [damage_lank],
                    'this_time_picture': item['this_time_picture']  # this_time_pictureを追加
                }
                split_parts_and_damage.append(parts_dict)

    # << 2つのリストを合体 >>
    def sort_and_merge_list(ordered_result, order_dict, material_dict, order_number, order_lank):
        # ソートキーの設定
        def sort_key(item):
            # parts_nameのソートキー
            parts_name_key = order_dict.get(item['parts_name'][0].split()[0], 0)
            
            # numberのソートキー
            number_key = int(item['number'][0]) if item['number'] and item['number'][0].isdigit() else 0
            
            # damage_nameのソートキー (最初の1文字を使用)
            damage_name_initial = item['damage_name'][0][0] if item['damage_name'] else "None"
            damage_name_key = order_number.get(damage_name_initial, 0)
            
            # damage_lankのソートキー
            damage_lank_key = order_lank.get(item['damage_lank'][0], 0) if item['damage_lank'] else 0
            
            return parts_name_key, number_key, damage_name_key, damage_lank_key

        # リストをソート
        ordered_result = sorted(ordered_result, key=sort_key)

        # 重複および合体の処理
        merged_result = []
        for item in ordered_result:
            # 重複をチェックしてマージするか新規追加するか決定
            if not merged_result:
                merged_result.append(item)
            else:
                last_item = merged_result[-1]
                if (last_item['parts_name'] == item['parts_name'] and 
                    last_item['number'] == item['number'] and 
                    last_item['damage_name'] == item['damage_name'] and
                    last_item['main_frame'] == item['main_frame']):
                    
                    # materialの合体
                    if last_item['material'] and item['material']:
                        last_item['material'] = list(set(last_item['material'] + item['material']))
                    elif item['material']:
                        last_item['material'] = item['material']
                    
                    # damage_lankの合体
                    if last_item['damage_lank'] and item['damage_lank']:
                        last_item['damage_lank'] = list(set(last_item['damage_lank'] + item['damage_lank']))
                    elif item['damage_lank']:
                        last_item['damage_lank'] = item['damage_lank']
                else:
                    merged_result.append(item)

        return merged_result

    # 結果格納用のリスト
    result = []

    # sorted_splitをループし、number_createと比較
    for item in split_parts_and_damage:
        found = False
        for nc_item in number_create:
            if item['parts_name'] == nc_item['parts_name'] and item['number'] == nc_item['number']:
                item.update({'material': nc_item['material'], 'main_frame': nc_item['main_frame']})
                found = True
                break
        if 'material' not in item:
            item['material'] = None
        if 'main_frame' not in item:
            item['main_frame'] = None
        result.append(item)

    # number_createの項目を結果に追加
    for nc_item in number_create:
        # sorted_splitに存在しない場合のチェック
        exists = any(item['parts_name'] == nc_item['parts_name'] and item['number'] == nc_item['number'] for item in split_parts_and_damage)
        if not exists:
            result.append({'parts_name': nc_item['parts_name'], 'number': nc_item['number'], 'material': nc_item['material'], 'main_frame': nc_item['main_frame'], 'this_time_picture': None})

    # 指定した順番でキーを整列
    ordered_result = []
    ordered_keys = ['parts_name', 'number', 'material', 'damage_lank', 'damage_name', 'main_frame', 'this_time_picture']

    for item in result:
        ordered_item = {key: item.get(key) for key in ordered_keys}
        ordered_result.append(ordered_item)

    # 入力データ

    order_dict = {"主桁": 1, "横桁": 2, "床版": 3, "PC定着部": 4, "橋台[胸壁]": 5, "橋台[竪壁]": 6, "支承本体": 7, "沓座モルタル": 8, "防護柵": 9, "地覆": 10, "伸縮装置": 11, "舗装": 12, "排水ます": 13, "排水管": 14}
    material_dict = {"S": 1, "C": 2, "X": 3}
    order_number = {"None": 0, "①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5, "⑥": 6, "⑦": 7, "⑧": 8, "⑨": 9, "⑩": 10, "⑪": 11, "⑫": 12, "⑬": 13, "⑭": 14, "⑮": 15, "⑯": 16, "⑰": 17, "⑱": 18, "⑲": 19, "⑳": 20, "㉑": 21, "㉒": 22, "㉓": 23, "㉔": 24, "㉕": 25, "㉖": 26}
    order_lank = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}

    # ソートとマージ
    flattened_join_result = sort_and_merge_list(ordered_result, order_dict, material_dict, order_number, order_lank)
    
    
    # << 部材名と要素番号を結合 >>
    for item in flattened_join_result:
        combined = [p_n  + num for p_n, num in zip(item['parts_name'], item['number'])]
        # 新しいリストを parts_name に設定
        item['parts_name'] = combined
        del item['number'] # キーの削除
    
    main_parts_list_left = ["主桁", "PC定着部"] # 左の数字
    main_parts_list_right = ["横桁", "橋台"] # 右の数字
    main_parts_list_zero = ["床版"] # 00になる場合

    # データをグループ化するための辞書
    grouped_data = defaultdict(lambda: defaultdict(lambda: {'lanks': [], 'pictures': [], 'main_frame': []}))

    def process_item(item):
        name_and_number = item['parts_name'][0]
        
        if any(word in name_and_number for word in main_parts_list_left):
            left = name_and_number.find(" ")
            number2 = name_and_number[left+1:]
            number_part = re.search(r'[A-Za-z]*(\d+)', number2).group(1)
            parts_name = name_and_number[:left]+" "+number_part[:2] # 主桁 03
        elif any(word in name_and_number for word in main_parts_list_right):
            right = name_and_number.find(" ")
            number2 = name_and_number[right+1:]
            number_part = re.search(r'[A-Za-z]*(\d+)', number2).group(1)
            if len(number_part) < 5:
                parts_name = name_and_number[:right]+" "+number_part[2:] # 横桁 02
            else:
                parts_name = name_and_number[:right]+" "+number_part[2:] # 横桁 103
        elif any(word in name_and_number for word in main_parts_list_zero):
            right = name_and_number.find(" ")
            parts_name = name_and_number[:right]+" 00"
        else:
            right = name_and_number.find(" ")
            parts_name = name_and_number[:right]
        
        # << 損傷名の設定 >>
        in_damage = item['damage_name']
        if in_damage == None:
            damage = "NON"
        else:
            damage = ''.join(in_damage)
        
        if damage.startswith('⑰'):
            damage_name = damage
        else:
            first_parenthesis_index = damage.find('(')
            if first_parenthesis_index != -1:  # カッコが見つかった場合
                damage_name = damage[:first_parenthesis_index][1:]
            elif damage == "NON":
                damage_name = damage
            else:
                damage_name = damage[1:]
        # print(f"damage_name:{damage_name}")
        
        # << 損傷ランクの設定 >>
        before_damage_lank = item['damage_lank']
        if before_damage_lank is not None:
            damage_lank = ','.join(before_damage_lank)
        else:
            damage_lank = 'a'
        # print(f"damage_lank：{damage_lank}")
        
        grouped_data[parts_name][damage_name]['lanks'].append(damage_lank)
        if item['this_time_picture']:
            grouped_data[parts_name][damage_name]['pictures'].extend(item['this_time_picture'])
        if item['main_frame'] == ['〇']:
            grouped_data[parts_name][damage_name]['main_frame'].extend(item['main_frame'])
        
    for item in flattened_join_result:
        process_item(item)

    # 重複削除と並び替えを行う関数
    def unique_sorted_lanks(lanks, order_lank):
        unique_lanks = list(sorted(set(lanks), key=lambda x: order_lank[x]))
        return unique_lanks

    # 新しいリストを作成
    order_lank = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
    
    change_observer_list = [
        {'parts_name': [parts], 'damage_name': [damage], 'damage_lank': unique_sorted_lanks(damages['lanks'], order_lank), 'this_time_picture': list(set(damages['pictures'])), 'main_frame': list(set(damages['main_frame']))}
        for parts, damages in grouped_data.items()
        for damage, damages in damages.items()
    ]
    
    for change_key_item in change_observer_list:
        # 'lank'キーがリストの場合はハイフンでつなげる
        if isinstance(change_key_item['damage_lank'], list):
            change_key_item['damage_lank'] = '～'.join(change_key_item['damage_lank'])
        # 'lank'キーが単一の文字列の場合はそのままにする
        elif isinstance(change_key_item['damage_lank'], str):
            change_key_item['damage_lank'] = change_key_item['damage_lank']

    #print(f"change_observer_list:{change_observer_list}")
    """
    # return render(request, 'observer_list.html', {'data': change_observer_list, 'article_pk': article_pk, 'pk': pk})

# TODO:所見コメント用（写真の中央揃えの確認）
def observer_comment(request):
    # 主桁（損傷箇所）、 剥離・鉄筋露出（損傷種類）、d（損傷種類）、 対策区分、 損傷原因
    # これらの組み合わせで表示する内容を変える
    # (損傷箇所)に(cause_of_damage)が原因と推定される(damage_type)が見られる。(judgement_category)
    #     ↓               ↓                               ↓                           ↓
    #    主桁に        経年変化が原因と推定される　　　　鉄筋露出が見られる。　　状況に応じて補修を行う必要がある。
    
    # spesial_combinationに一致した場合は登録した文言を表示、それ以外は上記手順
    spesial_combination = {
        "舗装"-"品質の経年変化"-"土砂詰まり-e"-"M": "舗装に経年による土砂堆積が見られる。維持工事で清掃等の対策を行う必要がある。",
    }
    cause_of_damage = {
        "塩害": "塩化物イオンの侵入",
        "製作・施工不良": "製作・施工不良",
        "防水・排水工不良": "防水の劣化",
        "品質の経年変化": "経年変化",
    }
    damage_type = {
        "剥離・鉄筋露出-c": "コンクリートの剥離",
        "剥離・鉄筋露出-d": "鉄筋露出",
        "剥離・鉄筋露出-e": "断面減少を伴う鉄筋露出",
        "漏水・滞水-e": "漏水・滞水",
        "土砂詰まり-e": "土砂詰まり",
    }
    judgment_category = {
        "B": "状況に応じて補修を行う必要がある。",
        "M": "維持工事で対応する必要がある。",
        "C1": "予防保全の観点から，速やかに補修等を行う必要がある。",
        "C2": "橋梁構造の安全性の観点から，速やかに補修等を行う必要がある。",
        "S1": "詳細調査の必要がある。",
        "S2": "追跡調査の必要がある。",
        "E1": "橋梁構造の安全性の観点から，緊急対応の必要がある。",
        "E2": "その他，緊急対応の必要がある。",
    }
    return render('index.html')

# << 名前とアルファベットを紐付け >>
def names_list(request, article_pk):
    
    alphabet_list = request.POST.getlist("name_alphabet")
    #alphabet_dict = {alphabet_list[i]: alphabet_list[i+1] for i in range(0, len(alphabet_list), 2)}
    #print(alphabet_dict)
    for i in range(0, len(alphabet_list), 2):
        dic = {}
        dic["name"] = alphabet_list[i]
        dic["alphabet"] = alphabet_list[i+1]
        dic["article"] = article_pk
        
        form = NameEntryForm(dic)

        if form.is_valid():
            form.save()
        else:
            print(form.errors) # 入力フォームのエラー内容を表示
            
    # NameEntryには、article_id のフィールドはない、 article に変更
    # name_entries = NameEntry.objects.filter(article_id=article_pk)
    name_entries = NameEntry.objects.filter(article=article_pk)
    
    return render(request, 'names_list.html', {'article_pk': article_pk, "form": NameEntryForm(), 'name_entries': name_entries})

# << 登録した名前を削除 >>
def delete_name_entry(request, entry_id):
    if request.method == 'POST':
        entry = get_object_or_404(NameEntry, pk=entry_id)
        article_pk = entry.article.pk  # 事前に記事のPKを取得
        entry.delete()
        
        # ここでname_entries を作る
        # 削除後にエントリを再度取得しない
        name_entries = NameEntry.objects.filter(article=article_pk)
        return render(request, 'names_list.html', {"form": NameEntryForm()})
    else:
        return render(request, 'names_list.html', {'article_pk': entry.article.pk, "form": NameEntryForm(), 'name_entries': name_entries})

# << 番号登録 >>
def number_list(request, article_pk, pk):
    
    # 同じname属性の値をすべて取り出す
    serial_numbers = request.POST.getlist("serial_number") # ['0101', '0103', '0201', '0203']
    single_numbers = request.POST.getlist("single_number") # ['0101', '0201', '0301', '0401']
    
    new_serial_numbers = []
    #    初期値を0 ↓     回数分 ↓           ↓ 2ずつ足す(0101(index:0),0201(index:2))
    for i in range(0, len(serial_numbers), 2):
        new_serial_numbers.append(serial_numbers[i] + "~" + serial_numbers[i+1])
        #                          0101(index:0) ↑          0103(index:1+1) ↑
        #                          0201(index:2) ↑          0203(index:2+1) ↑
    print(new_serial_numbers) # ['0101~0103', '0201~0203']
    
    # 単一の番号、連続の番号 を部材名と紐付けて保存
    for new_serial_number in new_serial_numbers:
        
        if "~" in new_serial_number:
            # new_serial_number = "0101~0205"
            one = new_serial_number.find("~")

            start_number = new_serial_number[:one]
            end_number = new_serial_number[one+1:]

            # 最初の2桁と最後の2桁を取得
            start_prefix = start_number[:2]
            start_suffix = start_number[2:]
            end_prefix = end_number[:2]
            end_suffix = end_number[2:]

            first_elements = []
            # 決められた範囲内の番号を一つずつ追加
            for prefix in range(int(start_prefix), int(end_prefix)+1):
                for suffix in range(int(start_suffix), int(end_suffix)+1):
                    number_items = "{:02d}{:02d}".format(prefix, suffix)
                    dic = {}
                    dic["number"] = number_items
                    dic["parts_name"] = request.POST.get("parts_name")
                    dic["symbol"] = request.POST.get("symbol")
                    dic["material"] = request.POST.getlist("material")
                    dic["span_number"] = request.POST.get("span_number")
                    dic["main_frame"] = request.POST.get("main_frame") == 'on'
                    dic["infra"] = pk # infraとの紐付け
                    print(f"new_serial_number:{number_items}")
                    
                    # 1個ずつバリデーションして保存する
                    form = PartsNumberForm(dic)

                    if form.is_valid():
                        form.save()
                        parts_number = form.save()
                        parts_number.material.set(request.POST.getlist("material"))
                    else:
                        print(form.errors) # 入力フォームのエラー内容を表示
                        
    # TODO:single_numberが主要部材判定されていない
    for single_number in single_numbers:
        dic = {}
        dic["number"] = single_number
        dic["parts_name"] = request.POST.get("parts_name")
        dic["symbol"] = request.POST.get("symbol")
        dic["material"] = request.POST.getlist("material")
        dic["span_number"] = request.POST.get("span_number")
        dic["main_frame"] = request.POST.getlist("main_frame") == 'on'
        dic["infra"] = pk # infraとの紐付け
        print(single_number)

        # 1個ずつバリデーションして保存する
        form    = PartsNumberForm(dic)

        if form.is_valid():
            form.save()
            parts_number = form.save()
            parts_number.material.set(request.POST.getlist("material"))
        else:
            print(form.errors)
        
    parts_names = PartsName.objects.all()
    # materials = Material.objects.all()
    return render(request, 'number_entry.html', {'article_pk': article_pk, 'pk': pk, "form": PartsNumberForm(), "parts_names":parts_names})

# 部材名と記号を紐付けるAjaxリクエスト
def get_symbol(request):
    part_id = request.GET.get('part_id')
    try:
        parts_name = PartsName.objects.get(id=part_id)
        return JsonResponse({'symbol': parts_name.記号})
    except PartsName.DoesNotExist:
        return JsonResponse({'error': 'PartsName not found'}, status=404)
    
# 番号表示  
def number_view(request):
    # PartsNumberモデルから1件データを取り出し
    parts_number = PartsNumber.objects.get(id=1)
    # 抽出した数字を文字列として結合
    result = ""
    # 4桁 か 4桁~4桁 のいずれか
    if len(parts_number.number) == 4:
        # 4桁
        result  = parts_number.number
    else:
        # 4桁~4桁
        # ~ で区切る必要がある。 [ "3000","3000" ]
        numbers = parts_number.number.split("~")
        start   = numbers[0]
        end     = numbers[1]
        # 最初の2桁と最後の2桁を取得
        start_prefix = start[:2]
        start_suffix = start[2:]
        end_prefix = end[:2]
        end_suffix = end[2:]

        for prefix in range(int(start_prefix), int(end_prefix)+1):
            for suffix in range(int(start_suffix), int(end_suffix)+1):
                result += "{:02d}{:02d}\n".format(prefix, suffix)

    print(result)

# << 橋梁緒言の選択肢 >>
def infraregulations_view(request):
    form = BridgeCreateForm()
    regulations = Regulation.objects.all()
    context = {
        'form': form,
        'regulations': regulations,
    }
    return render(request, 'infra_create.html', context)

def infraloadWeights_view(request):
    form = BridgeCreateForm()
    loadWeights = LoadWeight.objects.all()
    context = {
        'form': form,
        'loadWeights': loadWeights,
    }
    return render(request, 'infra_create.html', context)

def infraloadGrades_view(request):
    form = BridgeCreateForm()
    loadGrades = LoadGrade.objects.all()
    context = {
        'form': form,
        'loadGrades': loadGrades,
    }
    return render(request, 'infra_create.html', context)

def infrarulebooks_view(request):
    form = BridgeCreateForm()
    rulebooks = Rulebook.objects.all()
    context = {
        'form': form,
        'rulebooks': rulebooks,
    }
    return render(request, 'infra_create.html', context)

def infraapproachs_view(request):
    form = BridgeCreateForm()
    approachs = Approach.objects.all()
    context = {
        'form': form,
        'approachs': approachs,
    }
    return render(request, 'infra_create.html', context)

def infrathirdpartys_view(request):
    form = BridgeCreateForm()
    thirdpartys = Thirdparty.objects.all()
    context = {
        'form': form,
        'thirdpartys': thirdpartys,
    }
    return render(request, 'infra_create.html', context)

def infraunderConditions_view(request):
    form = BridgeCreateForm()
    underConditions = UnderCondition.objects.all()
    context = {
        'form': form,
        'underConditions': underConditions,
    }
    return render(request, 'infra_create.html', context)

def infraregulations_view(request):
    form = BridgeUpdateForm()
    regulations = Regulation.objects.all()
    context = {
        'form': form,
        'regulations': regulations,
    }
    return render(request, 'infra_update.html', context)

def infraloadWeights_view(request):
    form = BridgeUpdateForm()
    loadWeights = LoadWeight.objects.all()
    context = {
        'form': form,
        'loadWeights': loadWeights,
    }
    return render(request, 'infra_update.html', context)

def infraloadGrades_view(request):
    form = BridgeUpdateForm()
    loadGrades = LoadGrade.objects.all()
    context = {
        'form': form,
        'loadGrades': loadGrades,
    }
    return render(request, 'infra_update.html', context)

def infrarulebooks_view(request):
    form = BridgeUpdateForm()
    rulebooks = Rulebook.objects.all()
    context = {
        'form': form,
        'rulebooks': rulebooks,
    }
    return render(request, 'infra_update.html', context)

def infraapproachs_view(request):
    form = BridgeUpdateForm()
    approachs = Approach.objects.all()
    context = {
        'form': form,
        'approachs': approachs,
    }
    return render(request, 'infra_update.html', context)

def infrathirdpartys_view(request):
    form = BridgeUpdateForm()
    thirdpartys = Thirdparty.objects.all()
    context = {
        'form': form,
        'thirdpartys': thirdpartys,
    }
    return render(request, 'infra_update.html', context)

def infraunderConditions_view(request):
    form = BridgeUpdateForm()
    underConditions = UnderCondition.objects.all()
    context = {
        'form': form,
        'underConditions': underConditions,
    }
    return render(request, 'infra_update.html', context)

# << 指定したInfra(pk)に紐づくTableのエクセルの出力 >>
def excel_output(request, article_pk, pk):
    # 指定したInfraに紐づく Tableを取り出す
    table = Table.objects.filter(infra=pk).first()
    #print(table.dxf.url) # 相対パス
    
    # 絶対パスに変換
    encoded_url_path = table.dxf.url
    decoded_url_path = urllib.parse.unquote(encoded_url_path) # URLデコード
    dxf_filename = os.path.join(settings.BASE_DIR, decoded_url_path.lstrip('/'))
    #print(dxf_filename)
    #       ↑ を読んで絶対パスを作る

    # 径間の数をamountに格納
    infra   = Infra.objects.filter(id=pk).first()
    amount  = infra.径間数
    
    def duplicate_sheet(wb, sheet_name, suffix):
        """元のシートを複製して、指定したタイトルのシートを作成"""
        original_sheet = wb[sheet_name]
        # シートを複製
        copied_sheet = wb.copy_worksheet(original_sheet)
        # コピーシートのタイトルを更新
        copied_sheet.title = f"{sheet_name}-{suffix}"
        return copied_sheet

    def set_print_area_and_page_view(sheet, start_col, end_col):
        """印刷範囲と改ページプレビューを設定する"""
        # 最大行を取得
        max_row = sheet.max_row
        # 印刷範囲の設定を修正
        print_area = f"{start_col}1:{end_col}{max_row}"
        sheet.print_area = print_area

        # 改ページプレビューを有効にする
        sheet.sheet_view.view = "pageBreakPreview"

    # 元のファイルのパス（例: `10_only.xlsm`）
    original_file_path = '10_only.xlsm'

    # エクセルファイルを読み込む
    wb = openpyxl.load_workbook(original_file_path, keep_vba=True)

    # 複製元のシートを選択 (例: 'その１０')
    original_sheet_name = 'その１０'
    ws = wb[original_sheet_name]

    # 例えば10個の複製シートを作成
    num_copies = amount
    start_col = 'A'  # 印刷範囲の開始列
    end_col = 'CD'  # 印刷範囲の終了列
    for i in range(1, num_copies + 1):
        copied_sheet = duplicate_sheet(wb, original_sheet_name, i)
        set_print_area_and_page_view(copied_sheet, start_col, end_col)
        copied_sheet['A65'] = "python" # 半角スペースの代わり（エクセルが終わった際に置換で削除）
    
    for number in range(1,amount+1):
                                # ↓ 径間番号の指定。
        search_title_text = f"{number}径間"
        second_search_title_text = "損傷図"
        action_sheet_name = f"その１０-{number}" # シート名を作成
        # print(f"シート名{ws_name}")
        ws = wb[action_sheet_name] # シート名を指定
        
        # 1回の実行で作れるのは、径間の1個分しか作れない。エクセルのシート1枚。
        sorted_items = create_picturelist(request, table, dxf_filename, search_title_text, second_search_title_text)

        # lastがNoneでないデータを残す
        filtered_data = [item for item in sorted_items if item['this_time_picture'] is not None]
        # print(filtered_data)

        # this_time_pictureの要素が複数ある場合、分割する
        output_data = []
        for entry in filtered_data:
            for picture in entry['this_time_picture']:
                new_entry = entry.copy()
                new_entry['this_time_picture'] = [picture]
                output_data.append(new_entry)
                
        # 行の開始地点と増加するステップを定義
        partsname_and_number_row = 10 # 部材名・要素番号
        damagename_and_lank_row = 11 # 損傷の種類・損傷程度
        picture_start_row = 13 # 損傷写真
        lasttime_lank_row = 15 # 前回損傷程度
        damage_memo_row = 17 # 損傷メモ
        step = 14
        num_positions = len(output_data) * 3  # データ数に3列分を掛けています

        # 関連する列を定義
        picture_columns = ["E", "AE", "BE"]
        left_columns = ["I", "AI", "BI"]
        right_columns = ["R", "AR", "BR"]
        bottom_columns = ["T", "AT", "BT"]

        # セル位置のリストを生成 ↓
        partsname_cell_positions = [] # 部材名
        number_cell_positions = [] # 要素番号
        damagename_cell_positions = [] # 損傷の種類
        lank_cell_positions = [] # 損損傷程度
        picture_cell_positions = [] # 損傷写真
        lasttime_lank_cell_positions = [] # 前回損傷程度
        damage_memo_cell_positions = [] # 損傷メモ

        for i in range(num_positions // len(picture_columns)):
            partsname_cell_positions.append([f"{col}{partsname_and_number_row + i * step}" for col in left_columns])
            number_cell_positions.append([f"{col}{partsname_and_number_row + i * step}" for col in right_columns])
            damagename_cell_positions.append([f"{col}{damagename_and_lank_row + i * step}" for col in left_columns])
            lank_cell_positions.append([f"{col}{damagename_and_lank_row + i * step}" for col in right_columns])
            picture_cell_positions.append([f"{col}{picture_start_row + i * step}" for col in picture_columns])
            lasttime_lank_cell_positions.append([f"{col}{lasttime_lank_row + i * step}" for col in bottom_columns])
            damage_memo_cell_positions.append([f"{col}{damage_memo_row + i * step}" for col in bottom_columns])
            
        join_partsname_cell_positions = [item for sublist in partsname_cell_positions for item in sublist]
        join_number_cell_positions = [item for sublist in number_cell_positions for item in sublist]
        join_damagename_cell_positions = [item for sublist in damagename_cell_positions for item in sublist]
        join_lank_cell_positions = [item for sublist in lank_cell_positions for item in sublist]
        join_picture_cell_positions = [item for sublist in picture_cell_positions for item in sublist]
        join_lasttime_lank_cell_positions = [item for sublist in lasttime_lank_cell_positions for item in sublist]
        join_damage_memo_cell_positions = [item for sublist in damage_memo_cell_positions for item in sublist]
        # セル位置のリストを生成 ↑

        number_change = {
        '①': '腐食',
        '②': '亀裂',
        '③': 'ゆるみ・脱落',
        '④': '破断',
        '⑤': '防食機能の劣化',
        '⑥': 'ひびわれ',
        '⑦': '剥離・鉄筋露出',
        '⑧': '漏水・遊離石灰',
        '⑨': '抜け落ち',
        '⑩': '補修・補強材の損傷',
        '⑪': '床版ひびわれ',
        '⑫': 'うき',
        '⑬': '遊間の異常',
        '⑭': '路面の凹凸',
        '⑮': '舗装の異常',
        '⑯': '支承部の機能障害',
        '⑰': 'その他',
        '⑱': '定着部の異常',
        '⑲': '変色・劣化',
        '⑳': '漏水・滞水',
        '㉑': '異常な音・振動',
        '㉒': '異常なたわみ',
        '㉓': '変形・欠損',
        '㉔': '土砂詰まり',
        '㉕': '沈下・移動・傾斜',
        '㉖': '洗掘',
        }

        """ 写真の動作 """
        # 最大の写真サイズ（幅、高さ）
        max_width, max_height = 240, 180 # 4:3

        # 位置を追跡するカウンタ
        cell_counter = 0

        def convert_backslash_to_slash(path):
            return path.replace("/", "\\")
        
        def hide_sheet_copy_and_paste(wb, sheet_name):
            """シートを再表示してコピーその後非表示に設定"""

            hide_sheet = wb['ページ１０']
            hide_sheet.sheet_state = 'visible'

            # コピーする行の範囲を指定します
            copy_start_row = 2
            copy_end_row = 29

            # コピーする行のデータとスタイルを保持するリストを作成します
            rows_to_copy = []
            merges_to_keep = []

            for row_idx in range(copy_start_row, copy_end_row + 1):
                row_data = []
                for cell in hide_sheet[row_idx]:
                    cell_data = {
                        'value': cell.value,
                        'font': copy(cell.font),
                        'border': copy(cell.border),
                        'fill': copy(cell.fill),
                        'number_format': cell.number_format,
                        'protection': copy(cell.protection),
                        'alignment': copy(cell.alignment)
                    }
                    row_data.append(cell_data)
                row_data.append(hide_sheet.row_dimensions[row_idx].height)
                rows_to_copy.append(row_data)

            # 元のシートのセル結合情報を取得
            for merge in hide_sheet.merged_cells.ranges:
                if (copy_start_row <= merge.min_row <= copy_end_row) or \
                    (copy_start_row <= merge.max_row <= copy_end_row):
                    merges_to_keep.append(copy(merge))
            
            sheet = wb[action_sheet_name]
            
            # コピー先の行を挿入します
            # A列の一番下の行番号を取得
            max_row = sheet.max_row
            while sheet['A' + str(max_row)].value is None and max_row > 0:
                max_row -= 1
            insert_at_row = max_row
            # print(f"max_row：{max_row}")
            
            # シフトする行の高さを保持するリストを作成します
            heights = []
            for row_idx in range(insert_at_row, sheet.max_row + 1):
                heights.append(sheet.row_dimensions[row_idx].height)
            
            # 指定行から下の行をシフト
            sheet.insert_rows(insert_at_row, amount=(copy_end_row - copy_start_row + 1))

            # 行の高さを元に戻す
            for i, height in enumerate(heights):
                sheet.row_dimensions[insert_at_row + i + (copy_end_row - copy_start_row + 1)].height = height
            
            # コピーされた行を挿入
            for i, row_data in enumerate(rows_to_copy):
                new_row = insert_at_row + i
                for j, cell_data in enumerate(row_data[:-1]):
                    cell = sheet.cell(row=new_row, column=j + 1)
                    cell.value = cell_data['value']
                    cell.font = cell_data['font']
                    cell.border = cell_data['border']
                    cell.fill = cell_data['fill']
                    cell.number_format = cell_data['number_format']
                    cell.protection = cell_data['protection']
                    cell.alignment = cell_data['alignment']
                sheet.row_dimensions[new_row].height = row_data[-1]

            # セル結合をコピー
            for merged_range in merges_to_keep:
                new_min_row = merged_range.min_row - copy_start_row + insert_at_row
                new_max_row = merged_range.max_row - copy_start_row + insert_at_row
                new_merge_range = "{}{}:{}{}".format(
                    openpyxl.utils.get_column_letter(merged_range.min_col),
                    new_min_row,
                    openpyxl.utils.get_column_letter(merged_range.max_col),
                    new_max_row
                )
                sheet.merge_cells(new_merge_range)
                
            # 最大行を取得
            max_row = sheet.max_row
            # 印刷範囲の設定を修正
            # start_colとend_colの取得方法が不明だったため、適宜修正してください。
            start_col = "A"
            end_col = 'CD'
            print_area = f"{start_col}1:{end_col}{max_row}"
            sheet.print_area = print_area    
            
            hide_sheet.sheet_state = 'hidden'
            
        for item in output_data:
            # 3列目(インデックスが2)でpictureキーに写真が設定されている場合
            if cell_counter % 2 == 0 and item['last_time_picture'] is not None:
                # 3列目を空白にするため、インデックスを1つ追加
                cell_counter += 1
            # pictureキーに写真が設定されていても、3列目でなければOK
            else:
                pass
            
            if cell_counter % 6 == 5 and cell_counter > 10:
                # プログラム4｜マクロ実行
                hide_sheet_copy_and_paste(wb, ws)

            # 現在の画像を貼り付ける動作
            for this_image_path in item['this_time_picture']:
                
                decoded_picture_path = urllib.parse.unquote(this_image_path) # URLデコード
                full = settings.STATICFILES_DIRS[0]
                sub_image_path = os.path.join(full, decoded_picture_path.lstrip('/'))
                full_image_path = sub_image_path.replace("/", "\\")
                # print(full_image_path)
                if os.path.exists(full_image_path):
                    # print('true')
                    # print(full_image_path)
                    cell_pos = picture_cell_positions[cell_counter // len(picture_columns)][cell_counter % len(picture_columns)]  # 所定のセル位置
                    # print(f"cell_pos:{cell_pos}")
                    # 画像を開いてリサイズ
                    pil_img = pil_img = PILImage.open(full_image_path)
                    width, height = pil_img.size
                    aspect_ratio = width / height

                    if aspect_ratio > max_width / max_height:
                        new_width = min(width, max_width)
                        new_height = new_width / aspect_ratio
                    else:
                        new_height = min(height, max_height)
                        new_width = new_height * aspect_ratio

                    resized_img = pil_img.resize((int(new_width), int(new_height)))

                    # 一時ファイル用のテンポラリディレクトリを作成
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                        resized_img_path = tmp.name

                    # 画像を一時ファイルに保存
                    resized_img.save(resized_img_path)

                    # openpyxl用の画像オブジェクトを作成
                    img = OpenpyxlImage(resized_img_path)

                    # セルの位置に画像を貼り付け
                    img.anchor = cell_pos
                    ws.add_image(img)
                    cell_counter += 1  # カウンタを進める
                else:
                    print('false')

            # 過去の画像を貼り付ける動作
            if item['last_time_picture'] and os.path.exists(item['last_time_picture']):
                img_path = os.path.abspath(item['last_time_picture'])
                # print(img_path)
                cell_pos = picture_cell_positions[cell_counter // len(picture_columns)][cell_counter % len(picture_columns)]
                # print(f"cell_pos:{cell_pos}")
                pil_img = pil_img = PILImage.open(img_path)
                width, height = pil_img.size
                aspect_ratio = width / height

                if aspect_ratio > max_width / max_height:
                    new_width = min(width, max_width)
                    new_height = new_width / aspect_ratio
                else:
                    new_height = min(height, max_height)
                    new_width = new_height * aspect_ratio

                resized_img = pil_img.resize((int(new_width), int(new_height)))

                # 一時ファイル用のテンポラリディレクトリを作成
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    resized_img_path = tmp.name

                # 画像を一時ファイルに保存
                resized_img.save(resized_img_path)

                # openpyxl用の画像オブジェクトを作成
                img = OpenpyxlImage(resized_img_path)

                # セルの位置に画像を貼り付け
                img.anchor = cell_pos
                ws.add_image(img)
                cell_counter += 1  # カウンタを進める
                
        """ 写真の動作 """
                
        # データの入力
        data_index = 0

        for item, part_pos, number_pos, name_pos, lank_pos, memo_pos, picture_pos in zip_longest(output_data, join_partsname_cell_positions, join_number_cell_positions, join_damagename_cell_positions, join_lank_cell_positions, join_damage_memo_cell_positions, join_picture_cell_positions, fillvalue=None):
            
            if (data_index == 2 or data_index % 2 == 3) and item['last_time_picture'] is not None:
                data_index += 1

            part_cell = join_partsname_cell_positions[data_index]
            number_cell = join_number_cell_positions[data_index]
            name_cell = join_damagename_cell_positions[data_index]
            post_lank_cell = join_lank_cell_positions[data_index]
            pre_lank_cell = join_lasttime_lank_cell_positions[data_index]
            memo_cell = join_damage_memo_cell_positions[data_index]
            
            # print(part_cell) # I10
            
        # メモに入れるための固定コード　↓
            # firstキーの内容を所定の書式に変更
            try:
                first_data = item['parts_name'][0][0] # 排水管 Dp0101
                split_space = first_data.split(" ")
                first_part_data = split_space[0] # 排水管

                match = re.search(r'\d+', split_space[1])
                first_number_data = match.group() if match else '' # 0101

                if part_cell:
                    ws[part_cell] = first_part_data # 排水管
                if number_cell:
                    ws[number_cell] = first_number_data # 0101

                second_data = item['damage_name'][0][0] # ①腐食(小小)-b
                second_damage_name = second_data[0] # ①
                second_name_data = number_change.get(second_damage_name, second_damage_name) # 腐食
                second_lank_data = second_data[-1] # b

                if name_cell:
                    ws[name_cell] = second_name_data # 腐食
                if post_lank_cell:
                    ws[post_lank_cell] = second_lank_data # b

                memo_data = item['textarea_content'] # 損傷メモ 
                if memo_cell:
                    ws[memo_cell] = memo_data

                if item['last_time_picture'] is not None:
                    data_index += 2
                else:
                    data_index += 1
                    
            except (TypeError, KeyError):
                if part_cell:
                    ws[part_cell] = ""
                if number_cell:
                    ws[number_cell] = ""
                if name_cell:
                    ws[name_cell] = ""
                if post_lank_cell:
                    ws[post_lank_cell] = ""
                if memo_cell:
                    ws[memo_cell] = ""
                
        # メモに入れるための固定コード　↑

    # 現在の日時を取得してファイル名に追加
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    # 新しいファイル名の生成
    new_filename = f"{timestamp}_Macro_{original_file_path}"
    # デスクトップのパス
    # desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    # 保存するファイルのフルパス
    # save_path = os.path.join(desktop_path, new_filename)
    """"""
    #メモリ空間内に保存
    virtual = BytesIO()
    wb.save(virtual)

    #バイト文字列からバイナリを作る
    binary = BytesIO(virtual.getvalue())

    return FileResponse(binary, filename = new_filename)

# << 指定したInfra(pk)に紐づくTableのエクセルの出力 >>
def dxf_output(request, article_pk, pk):
    # pythoncom.CoInitialize() # COMライブラリを初期化
    #try:
        # 指定したInfraに紐づく Tableを取り出す
        table = Table.objects.filter(infra=pk).first()
        # print(table.dxf.url) # 相対パス
        
        # 絶対パスに変換
        encoded_url_path = table.dxf.url
        decoded_url_path = urllib.parse.unquote(encoded_url_path) # URLデコード
        dxf_filename = os.path.join(settings.BASE_DIR, decoded_url_path.lstrip('/'))
        # print(dxf_filename)
        #      ↑ dxfファイルのフルパス
        
        # ファイルをバイトデータとして読み込む
        with open(dxf_filename, 'rb') as f:
            binary = BytesIO(f.read())
        
        infra_name = Infra.objects.filter(id=pk).first()
        file_name = infra_name.title
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        dxf_filename = file_name + "_" + timestamp + ".dxf"
        #レスポンスをする
        return FileResponse(binary, filename = dxf_filename)
    #finally:
        #pythoncom.CoUninitialize()

# << sorted_itemsを受け取り、番号登録と合わせ、所見用・一覧用に整える >>
# TODO:関数の当てはめ用
def sorted_items_and_number_arrange(request):
    return render("index.html") # エラー回避でindex指定

# << dxfから要素を抽出・整列してsorted_itemsに渡す >>
def create_picturelist(request, table, dxf_filename, search_title_text, second_search_title_text):
    
    def find_square_around_text(dxf_filename, target_text, second_target_text):
        doc = ezdxf.readfile(dxf_filename)
        msp = doc.modelspace()
        
        text_positions = [] # 見つかったテキストの位置を格納するためのリストを作成
        
        extracted_text = []

        # MTEXTエンティティの各要素をtextという変数に代入してループ処理
        for mtext_insert_point in msp.query('MTEXT'): # モデルスペース内の「MTEXT」エンティティをすべて照会し、ループ処理
            if mtext_insert_point.dxf.text == target_text: # エンティティのテキストが検索対象のテキストと一致した場合
                text_insertion_point = mtext_insert_point.dxf.insert # テキストの挿入点(dxf.insert)を取得します。
                text_positions.append(text_insertion_point[0]) # 挿入点のX座標をリストに保存
                break

        if not text_positions: # text_positionsリストが空の場合(見つけられなかった場合)
            for mtext_insert_point in msp.query('MTEXT'): # モデルスペース内の「MTEXT」エンティティをすべて照会し、ループ処理
                if mtext_insert_point.dxf.text == second_target_text: # エンティティのテキストが検索対象のテキストと一致した場合
                    text_insertion_point = mtext_insert_point.dxf.insert # テキストの挿入点(dxf.insert)を取得します。
                    text_positions.append(text_insertion_point[0]) # 挿入点のX座標をリストに保存
                    break
        
        # Defpointsレイヤーで描かれた正方形枠の各要素をsquare変数に代入してループ処理
        for defpoints_square in msp.query('LWPOLYLINE[layer=="Defpoints"]'): # 
            if len(defpoints_square) == 4: # 正方形(=4辺)の場合
                square_x_values = [four_points[0] for four_points in defpoints_square] # squareというリストをループして各点(point)からx座標(インデックス0の要素)を抽出
                square_min_x = min(square_x_values) # 枠の最小X座標を取得
                square_max_x = max(square_x_values) # 枠の最大X座標を取得
                
            # 文字のX座標が枠の最小X座標と最大X座標の間にあるかチェック
            # text_positionsの各要素をtext_x_positionという変数に代入してforループを処理
            for text_x_position in text_positions:
                
                # 文字の座標がDefpoints枠のX座標内にある場合
                if square_min_x <= text_x_position <= square_max_x:
                    
                    # print(list(square)) 4点の座標を求める 
                    left_top_point = list(defpoints_square)[0][0] # 左上の座標
                    right_top_point = list(defpoints_square)[1][0] # 右上の座標
                    right_bottom_point = list(defpoints_square)[2][0] # 右下の座標
                    left_bottom_point = list(defpoints_square)[3][0] # 左下の座標

                    defpoints_max_x = max(left_top_point,right_top_point,left_bottom_point,right_bottom_point) # X座標の最大値
                    defpoints_min_x = min(left_top_point,right_top_point,left_bottom_point,right_bottom_point) # X座標の最小値
                    
        # 指定したX座標範囲内にあるテキストを探す
        for circle_in_text in msp.query('MTEXT'):
            if defpoints_min_x <= circle_in_text.dxf.insert.x <= defpoints_max_x and circle_in_text.dxf.layer != 'Defpoints':
            # MTextのテキストを抽出する
                text = circle_in_text.plain_text()
                x, y, _ = circle_in_text.dxf.insert
                if not text.startswith("※"):
                    cad_data = text.split("\n") if len(text) > 0 else [] # .split():\nの箇所で配列に分配
                    # if len(cad_data) > 0 and not text.startswith("※") and not any(keyword in text for keyword in ["×", ".", "損傷図"]):
                    if len(cad_data) > 0 and not any(keyword in text for keyword in ["×", ".", "損傷図"]) and not text.endswith("径間"):
                # 改行を含むかどうかをチェックする(and "\n" in cad):# 特定の文字列で始まるかどうかをチェックする: # 特定の文字を含むかどうかをチェックする
                        related_text = "" # 見つけたMTextと関連するDefpointsレイヤの文字列を代入する変数
                # MTextの下、もしくは右に特定のプロパティ(Defpoints)で描かれた文字を探す
                        for neighbor in msp.query('MTEXT[layer=="Defpoints"]'): # DefpointsレイヤーのMTextを抽出
                        # MTextの挿入位置と特定のプロパティで描かれた文字の位置を比較する
                            if entity_extension(circle_in_text, neighbor):
                            # 特定のプロパティ(Defpoints)で描かれた文字のテキストを抽出する
                                related_text = neighbor.plain_text()
                                defx, defy, _ = neighbor.dxf.insert
                            #extracted_text.append(neighbor_text)
                                break # 文字列が見つかったらbreakによりforループを終了する

                        if  len(related_text) > 0: #related_textに文字列がある＝Defpointsレイヤから見つかった場合
                            cad_data.append(related_text[:]) # cad_dataに「部材名～使用写真」までを追加
                            cad_data.append([str(x), str(y)]) # 続いてcad_dataに「MTEXT」のX,Y座標を追加
                    #最後にまとめてcad_dataをextracted_textに追加する
                        extracted_text.append(cad_data[:] + [[str(defx), str(defy)]]) # extracted_textに「MTEXTとその座標」およびdefのX,Y座標を追加
                        
    # << ※特記なき損傷の抽出用 ↓ >>                            
                else:
                    lines = text.split('\n')# 改行でテキストを分割してリスト化
                    sub_text = [[line] for line in lines]# 各行をサブリストとして持つ多重リストを構築

                    pattern = r"\s[\u2460-\u3256]"# 文字列のどこかにスペース丸数字の並びがあるかをチェックする正規表現パターン
                    pattern_start = r"^[\u2460-\u3256]"  # 文字列の開始が①～㉖であることをチェックする正規表現パターン
                    pattern_anywhere = r"[\u2460-\u3256]"  # 文字列のどこかに①～㉖があるかをチェックする正規表現パターン
                    last_found_circle_number = None  # 最後に見つかった丸数字を保持する変数

                    # リストを逆順でループし、条件に応じて処理
                    for i in range(len(sub_text)-1, -1, -1):  # 後ろから前にループ
                        item = sub_text[i][0]  # textリストの各サブリストの最初の要素（[0]）をitem変数に代入（地覆 ㉓-c）
                        if item.startswith("※"):
                            sub_text.remove(sub_text[i]) # 配列から除外する
                        elif re.search(pattern, item):  # itemが正規表現patternと一致している場合（スペース丸数字の並びがある）
                            last_found = item  # last_found変数にitem要素を代入（地覆 ㉓-c）
                            # print(last_found) 丸数字が付いている要素のみ出力
                        elif 'last_found' in locals():  # last_foundが定義されている（要素が代入されている）場合のみ
                            space = last_found.replace("　", " ")
                            # 大文字スペースがあれば小文字に変換
                            second = space.find(" ", space.find(" ") + 1)#10
                            # 2つ目のスペース位置まで抽出
                            sub_text[i][0] = item + last_found[second:]
                            # item:スペース丸数字の並びがない文字列
                            # last_found:スペース丸数字の並びがある文字列
                            # last_found[second:]:スペースを含めた文字列
                        elif re.match(pattern_start, item): # 文字列が①～㉖で開始するかチェック
                            last_found_circle_number = item # 丸数字の入っている要素を保持
                            sub_text.remove(sub_text[i])
                        else:
                            if last_found_circle_number is not None and not re.search(pattern_anywhere, item):
                                # 要素に丸数字が含まれておらず、直前に丸数字が見つかっている場合
                                sub_text[i][0] += " " + last_found_circle_number  # 要素の末尾に丸数字を追加

                    for sub_list in sub_text:
                        # サブリストの最初の要素を取得してスペース区切りで分割
                        split_items = sub_list[0].split()
                        
                        # 分割した要素から必要なデータを取り出して新しいサブリストに格納
                        header = split_items[0] + " " + split_items[1]  # 例：'主桁 Mg0101'
                        status = split_items[2]  # 例：'①-d'
                        # photo_number = '写真番号-00'
                        # defpoints = 'defpoints'
                        
                        # 新しい形式のサブリストを作成してprocessed_listに追加
                        # new_sub_list = [header, status, photo_number, defpoints]
                        new_sub_list = [header, status]
                        extracted_text.append(new_sub_list)

                        new_sub_list.append([str(x), str(y)])
    # << ※特記なき損傷の抽出用 ↑ >>
        return extracted_text

    def entity_extension(mtext, neighbor):
        # MTextの挿入点
        mtext_insertion = mtext.dxf.insert
        # 特定のプロパティ(Defpoints)で描かれた文字の挿入点
        neighbor_insertion = neighbor.dxf.insert
        #テキストの行数を求める
        text = mtext.plain_text()
        text_lines = text.split("\n") if len(text) > 0 else []
        # 改行で区切ったリスト数→行数
        text_lines_count = len(text_lines)
        
        # Defpointsを範囲内とするX座標範囲
        x_start = mtext_insertion[0]  # X開始位置
        x_end  = mtext_insertion[0] + mtext.dxf.width # X終了位置= 開始位置＋幅
        y_start = mtext_insertion[1] + mtext.dxf.char_height # Y開始位置
        y_end  = mtext_insertion[1] - mtext.dxf.char_height * (text_lines_count + 1) # 文字の高さ×(行数+1)
        
        # MTextの下、もしくは右に特定のプロパティで描かれた文字が存在するかどうかを判定する(座標：右が大きく、上が大きい)
        if (neighbor_insertion[0] >= x_start and neighbor_insertion[0] <= x_end):
            #y_endの方が下部のため、y_end <= neighbor.y <= y_startとする
            if (neighbor_insertion[1] >= y_end and neighbor_insertion[1] <= y_start):
                return True
        
        return False

    extracted_text = find_square_around_text(dxf_filename, search_title_text, second_search_title_text) # 関数の定義
    # リストを処理して、スペースを追加する関数を定義
    def add_spaces(text):
        # 正規表現でアルファベットと数字の間にスペースを挿入
        return re.sub(r'(?<! )([a-zA-Z]+)(\d{2,})', r' \1\2', text)

    # 変更されたリストを保存するための新しいリスト
    new_extracted_text = []

    # 各サブリストを処理
    for sub_extracted_text in extracted_text:
        # 先頭の文字列を修正
        if " " not in sub_extracted_text[0]:
            sub_extracted_text[0] = add_spaces(sub_extracted_text[0])
        # 新しいリストに追加
        new_extracted_text.append(sub_extracted_text)

    extracted_text = new_extracted_text

    for index, data in enumerate(extracted_text):
        # 最終項目-1まで評価
        if index < (len(extracted_text) -1):
            # 次の位置の要素を取得
            next_data = extracted_text[index + 1]
            # 特定の条件(以下例だと、１要素目が文字s1,s2,s3から始まる）に合致するかチェック
            if ("月" in next_data[0] and "日" in next_data[0]) or ("/" in next_data[0]) and (re.search(r"[A-Z]", next_data[0], re.IGNORECASE) and re.search(r"[0-9]", next_data[0])):
                # 合致する場合現在の位置に次の要素を併合 and "\n" in cad
                data.extend(next_data)
                # 次の位置の要素を削除
                extracted_text.remove(next_data)
    # extracted_text = [['主桁 Mg0101', '①-d', '写真番号-00', 'defpoints'], ['主桁 Mg0902', '⑦-c', '写真番号-00', 'defpoints']]

    # それぞれのリストから文字列のみを抽出する関数(座標以外を抽出)
        def extract_text(data):
            extracted = []  # 空のリストを用意
            removed_elements = []  # バックアップ用リスト

            pattern = r'[\u2460-\u3256]'  # ⓵～㉖

            for list_item in data:  # list_item変数に要素を代入してループ処理
                # print(list_item)
                item_extracted = [item for item in list_item if isinstance(item, str)]
                
                if item_extracted:  # item_extractedが空でないことを確認
                    # 最後の要素に特定の文字が含まれているかどうかをチェック
                    contains_symbols = bool(re.search(pattern, item_extracted[-1]))

                    # '月'と'日'が最後の要素に含まれているかどうかをチェック
                    if '月' in item_extracted[-1] and '日' in item_extracted[-1] and not contains_symbols:
                        extracted.append(item_extracted[:-2])
                        # 座標や日時を削除し、removed_elementsに保存
                        removed_elements.append([item for item in list_item if item not in item_extracted[:-2]])
                    else:
                        extracted.append(item_extracted)
                        # 座標や日時を削除し、removed_elementsに保存
                        removed_elements.append([item for item in list_item if item not in item_extracted])
                else:
                    extracted.append([])
                    removed_elements.append(list_item)

            return extracted, removed_elements  # extractedの結果を関数に返す

        # 関数を使って特定の部分を抽出
        extracted_text, removed_elements = extract_text(extracted_text)

        first_item = []
        current_detail = None  # 現在処理しているdetailを追跡

        for text, removed in zip(extracted_text, removed_elements):  # 1つずつのリスト
            result_list = []
            for item in text:# 1つずつの要素
            # 各条件を個別に確認する
                space_exists = re.search(r"\s+", item) is not None # スペースを含む
                alpha_exists = re.search(r"[a-zA-Z]+", item) is not None # アルファベットを含む
                digits_exists = re.search(r"\d{2,}", item) is not None # 2桁以上の数字を含む
            
                if space_exists and alpha_exists and digits_exists:
                # 新しいdetail項目を作成し、resultsに追加します
                    current_detail = {'detail': item, 'items': []}
                    result_list.append(current_detail)
                
                else:
                # 既存のdetailのitemsに現在の項目を追加
                    if current_detail is not None:
                        current_detail['items'].append(item)
                    
        # 元の要素を結果に追加
            for elem in removed:
                result_list.append(elem)

        #print(result_list)
            first_item.append(result_list)
        
        #print(first_item)
        extracted_text = first_item
            
        sub_first_item = [] 
        for check_sub_list in extracted_text:
            first_sub_item = []
            for first_sub_list in check_sub_list:
                # 各条件を個別に確認する
                space_exists = re.search(r"\s+", str(first_sub_list)) is not None # スペースを含む
                alpha_exists = re.search(r"[a-zA-Z]+", str(first_sub_list)) is not None # アルファベットを含む
                digits_exists = re.search(r"\d{2,}", str(first_sub_list)) is not None # 2桁以上の数字を含む
                # 正規表現を使って、コンマの直後に数字以外の文字が続く場所を見つけます。
                pattern = re.compile(r',(?![0-9])')
                # print(sub_list)
        # リスト内包表記で各要素をチェックして、条件に合致する場合は置き換えを行います。
                if space_exists and alpha_exists and digits_exists and not "月" in first_sub_list:
                    # sub_list自体を文字列に変換するのではなく、detailフィールドのみを操作する
                    detail_str = first_sub_list['detail']
                    # detail_strのカンマの直後に`</br>`タグを挿入
                    processed_str = pattern.sub(",", detail_str)
                    # processed_strをMarkup関数を使ってHTML安全なマークアップに変換
                    markup_str = Markup(processed_str)
                    # markup_strをリストに包む
                    wrapped_markup_str = [markup_str]
                    # first_sub_itemリストに追加
                    first_sub_item.append(wrapped_markup_str)
            sub_first_item.append(first_sub_item)
        # [[[Markup('横桁 Cr0503')]], [[Markup('主桁 Mg0110')], [Markup('床版 Ds0101')]], [[Markup('横桁 Cr0802')]], [[Markup('排水ます Dr0102,0201')]], [[Markup('排水ます Dr0202')]], [[Markup('PC定着部 Cn1101')]], [[Markup('排水ます Dr0102,0201,0202')]]]

            def process_item(item):
                if isinstance(item, Markup):
                    item = str(item)
                
                if ',' in item:
                    sub_items = item.split(',')
                    for i, sitem in enumerate(sub_items):
                        if i > 0 and sitem[0].isnumeric():
                            before_sub_item = sub_items[i - 1]
                            before_sub_item_splitted = before_sub_item.split()
                            before_sub_item_prefix = before_sub_item_splitted[0]
                            before_sub_item_suffix = ''
                            
                            for char in before_sub_item_splitted[1]:
                                if char.isnumeric():
                                    break
                                else:
                                    before_sub_item_suffix += char
                            
                            sub_items[i] = before_sub_item_prefix + ' ' + before_sub_item_suffix + sitem
                    item = ",".join(sub_items)
                
                return item.split(',')

            first_item = []
            for sub_one in sub_first_item:
                append2 = []
                for text_items in sub_one:
                    result_items = []
                    for item in text_items:
                        processed_items = process_item(item)
                        result_items.extend(processed_items)
                    append2.append(result_items)
                first_item.append(append2)

        # << ◆損傷種類(second)の要素◆ >> 
        # リストの各要素から記号を削除する関数
        def remove_symbols(other_items):
            symbols = ['!', '[', ']', "'"]

            processed_other_items = []
            for item in other_items:
                processed_item = ''.join(c for c in item if c not in symbols)
                processed_other_items.append(processed_item)

            return processed_other_items
        
        # それ以外の要素(損傷名)を抽出
        pattern = r'[\u2460-\u2473\u3251-\u3256].*-[a-zA-Z]' # 丸数字とワイルドカードとアルファベット
        second_items = []
        for second_sub_list in extracted_text:
            filtered_sub_list = []
            for damage_item in second_sub_list:
                if 'items' in damage_item:
                # sub_list自体を文字列に変換するのではなく、detailフィールドのみを操作する
                    detail_damage = damage_item['items']
                    for split_detail_damage in detail_damage:
                        if "," in split_detail_damage:
                            join_detail_damage = ""
                            middle_damage = split_detail_damage.split(",")
                            join_detail_damage = middle_damage
                        else:
                            join_detail_damage = detail_damage
                            
                    filtered_sub_list.append(join_detail_damage)
            second_items.append(filtered_sub_list)

        third_items = []
        bottom_item = []
        damage_coordinate = []
        picture_coordinate = []
        for other_sub_list in extracted_text:
            list_count = sum(isinstance(item, list) for item in other_sub_list) # リストの中にリストがいくつあるか数える
            
            if list_count == 2: # 座標が2つのとき=Defpointsが存在するとき
                bottom_item.append(other_sub_list[-3]) # 最後から3番目の要素を抽出（写真番号-00）
                third_items.append(other_sub_list[-4]) # 最後から4番目の要素を抽出（Defpoints）
                damage_coordinate.append(other_sub_list[-2])
                picture_coordinate.append(other_sub_list[-1])
            else: # Defpointsがない時
                bottom_item.append("") # bottom:写真番号なし
                third_items.append(None) # third:Defpointsなし
                damage_coordinate.append(other_sub_list[-1]) # damage:
                picture_coordinate.append(None) # picture:写真指定なし
        #print(other_sub_list)
        
        result_items = []# 配列を作成
        for item in bottom_item:# text_itemsの要素を1つずつitem変数に入れてforループする
            if ',' in item:# 要素の中にカンマが含まれている場合に実行
                pattern = r',(?![^(]*\))'
                sub_items = re.split(pattern, item)# カンマが含まれている場合カンマで分割
                extracted_item = []# 配列を作成
                for item in sub_items:# bottom_itemの要素を1つずつitem変数に入れてforループする
                    for p in range(len(item)):#itemの文字数をiに代入
                        if "A" <= item[p].upper() <= "Z" and p < len(item) - 1 and item[p+1].isnumeric():#i文字目がアルファベットかつ、次の文字が数字の場合
                            extracted_item.append(item[:p+1]+"*/*"+item[p+1:])# アルファベットと数字の間に*/*を入れてextracted_itemに代入
                            break
                join = ",".join(extracted_item)# 加工した内容をカンマ区切りの１つの文字列に戻す
                result_items.append(join)# result_itemsに格納

            else:# ifがfalseの場合(カンマが含まれていない場合)
                non_extracted_item = ''
                for j in range(len(item)):
                    if "A" <= item[j].upper() <= "Z" and j < len(item) - 1 and item[j+1].isnumeric():#i文字目がアルファベットかつ、次の文字が数字の場合
                        non_extracted_item = item[:j+1]+"*/*"+item[j+1:]#アルファベットまでをextracted_itemに代入
                    elif non_extracted_item == '':
                        non_extracted_item = item
                result_items.append(non_extracted_item)

        def remove_parentheses_from_list(last):
            pattern = re.compile(r"\([^()]*\)")
            result = [pattern.sub("", string) for string in last]
            return result

        last_item = remove_parentheses_from_list(result_items)

        damage_table = []  # 空のリストを作成

        # first_itemの要素の数だけループ処理
        for i in range(len(first_item)):
            try:
                third = third_items[i]
            except IndexError:
                third = None
            
            # ['NON-a', '9月7日 S404', '9月7日 S537', '9月8日 S117,9月8日 S253']
            if len(last_item)-1 < i:
                break

            if isinstance(last_item[i], list):
                continue
            else:
                # 組み合わせを収集するリスト
                replacements = []

                # name_entriesの取得 NameEntry.objects.all()
                # tableにarticleが紐付いているため、そこから取得(tableのinfraのarticle(id))
                name_entries = NameEntry.objects.filter(article = table.infra.article)
                # print(name_entries)

                # 置換情報を収集する
                for name_entry in name_entries:
                    replacements.append((name_entry.alphabet, name_entry.name))
                replacements.append((" ", "　"))
                # print(f'replacements: {replacements}')
                # 置換リストをキーの長さで降順にソート
                sorted_replacements = sorted(replacements, key=lambda x: len(x[0]), reverse=True)

                # 置換関数を定義
                def replace_all(text, replacements):
                    return reduce(lambda acc, pair: acc.replace(pair[0], pair[1]), replacements, text)
                
                name_item = replace_all(last_item[i], sorted_replacements)
                #name_item = last_item[i].replace("S", "佐藤").replace("H", "濵田").replace(" ", "　")
            # name_item に格納されるのは 'NON-a', '9月7日 佐藤*/*404', '9月7日 佐藤*/*537', '9月8日 佐藤*/*117,9月8日 佐藤*/*253'のいずれか
            
            pattern = r',(?![^(]*\))'
            dis_items = re.split(pattern, name_item)#「9月8日 S*/*117」,「9月8日 S*/*253」
            # コンマが付いていたら分割
            
            time_result = []
            current_date = ''  # 現在の日付を保持する変数
            for time_item in dis_items:
                #print(f"このデータは：{time_item}")
                # 先頭が数字で始まるかチェック（日付として扱えるか）
                if re.match(r'^\d', time_item):
                    current_date = re.match(r'^\d+月\d+日', time_item).group(0)  # 日付を更新
                    time_result.append(time_item)  # 日付がある項目はそのまま追加
                else:
                    # 日付がない項目は、現在の日付を先頭に追加
                    time_result.append(''.join([current_date, '　', time_item]))

            sub_dis_items = ['infra/static/infra/img/' + item + ".jpg" for item in time_result]
            # dis_itemsの要素の数だけ、分割した各文字の先頭に「infra/static/infra/img/」各文字の後ろに「.jpg」を追加
            # ['infra/static/infra/img/9月8日 S*/*117.jpg', 'infra/static/infra/img/9月8日 S*/*253.jpg']
            # print(f"このデータは：{sub_dis_items}")
            photo_paths = []
            # photo_pathsリストを作成
            for item in sub_dis_items:
                #print(f"item：{item}")
                sub_photo_paths = glob.glob(item)
                photo_paths.extend(sub_photo_paths)
                # photo_pathsリストにsub_photo_pathsを追加
            #print(f"photo_paths：{photo_paths}")
            if len(photo_paths) > 0:# photo_pathにはリストが入るため、[i]番目の要素が0より大きい場合
                picture_urls = [''.join(photo_path).replace('infra/static/', '') for photo_path in photo_paths]
                # photo_pathsの要素の数だけphoto_pathという変数に代入し、forループを実行
                # photo_pathという1つの要素の'infra/static/'を空白''に置換し、中間文字なしで結合する。
                # picture_urlsという新規配列に格納する。
            else:# それ以外の場合
                picture_urls = None
                #picture_urlsの値は[None]とする。

    # << ◆写真メモを作成するコード◆ >>

            bridge_damage = [] # すべての"bridge"辞書を格納するリスト

            bridge = {
                "parts_name": first_item[i],
                "damage_name": second_items[i] if i < len(second_items) else None  # second_itemsが足りない場合にNoneを使用
            }
            bridge_damage.append(bridge)
            
    # << ◆1つ1つの部材に対して損傷を紐付けるコード◆ >>
            first_element = bridge_damage[0]

            # 'first'キーの値にアクセス
            first_value = first_element['parts_name']

            first_and_second = []
            #<<◆ 部材名が1種類かつ部材名の要素が1種類の場合 ◆>>
            if len(first_value) == 1: # 部材名称が1つの場合
                if len(first_value[0]) == 1: # 要素が1つの場合
                    # カッコを1つ減らすためにリストをフラットにする
                    flattened_first = [first_buzai_item for first_buzai_sublist in first_value for first_buzai_item in first_buzai_sublist]
                    first_element['parts_name'] = flattened_first
                    # 同様に 'second' の値もフラットにする
                    second_value = first_element['damage_name']
                    flattened_second = [second_name_item for second_name_sublist in second_value for second_name_item in second_name_sublist]
                    first_element['damage_name'] = flattened_second
                    
                    first_and_second.append(first_element)
                    #print(first_and_second) # [{'first': ['排水管 Dp0102'], 'second': ['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e']}]
                    
                #<<◆ 部材名が1種類かつ部材名の要素が複数の場合 ◆>>
                else: # 別の部材に同じ損傷が紐付く場合
                        # 元のリストから各要素を取得
                    for first_buzai_item in bridge_damage:
                        #print(item)
                        before_first_elements = first_buzai_item['parts_name'][0]  # ['床版 Ds0201', '床版 Ds0203']
                        first_elements = []

                        for first_buzai_second_name in before_first_elements:
                            if "～" in first_buzai_second_name:

                                first_step = first_buzai_second_name

                                if " " in first_step:
                                    # 部材記号の前にスペースが「含まれている」場合
                                    first_step_split = first_step.split()

                                else:
                                    # 部材記号の前にスペースが「含まれていない」場合
                                    first_step_split = re.split(r'(?<=[^a-zA-Z])(?=[a-zA-Z])', first_step) # アルファベット以外とアルファベットの並びで分割
                                    first_step_split = [kara for kara in first_step_split if kara] # re.split()の結果には空文字が含まれるので、それを取り除く

                                # 正規表現
                                number = first_step_split[1]
                                # マッチオブジェクトを取得
                                number_part = re.search(r'[A-Za-z]*(\d+～\d+)', number).group(1)

                                one = number_part.find("～")

                                start_number = number_part[:one]
                                end_number = number_part[one+1:]

                                # 最初の2桁と最後の2桁を取得
                                start_prefix = start_number[:2]
                                start_suffix = start_number[2:]
                                end_prefix = end_number[:2]
                                end_suffix = end_number[2:]

                                # 「主桁 Mg」を抽出
                                prefix_text = first_step_split[0] + " " + re.match(r'[A-Za-z]+', number).group(0)

                                # 決められた範囲内の番号を一つずつ追加
                                for prefix in range(int(start_prefix), int(end_prefix)+1):
                                    for suffix in range(int(start_suffix), int(end_suffix)+1):
                                        number_items = "{}{:02d}{:02d}".format(prefix_text, prefix, suffix)
                                        first_elements.append(number_items)
                            else:
                                first_elements.append(first_buzai_second_name)
                        
                        
                        second_elements = first_buzai_item['damage_name'][0]  # ['⑦剥離・鉄筋露出-d']

                        
                        # first の要素と second を一対一で紐付け
                        for first_buzai_second_name in first_elements:
                            first_and_second.append({'parts_name': [first_buzai_second_name], 'damage_name': second_elements})

                #print(first_and_second) # [{'first': '床版 Ds0201', 'second': '⑦剥離・鉄筋露出-d'}, {'first': '床版 Ds0203', 'second': '⑦剥離・鉄筋露出-d'}]

            #<<◆ 部材名が複数の場合 ◆>>
            else:
                for double_item in bridge_damage:
                    first_double_elements = double_item['parts_name'] # [['支承本体 Bh0101'], ['沓座モルタル Bm0101']]
                    second_double_elements = double_item['damage_name'] # [['①腐食(小小)-b', '⑤防食機能の劣化(分類1)-e'], ['⑦剥離・鉄筋露出-c']]
                    
                    for break_first, break_second in zip(first_double_elements, second_double_elements):
                        first_and_second.append({'parts_name': break_first, 'damage_name': break_second})

            for damage_parts in bridge_damage:
                # print(damage_parts)
                if isinstance(damage_parts["damage_name"], list):  # "second"がリストの場合
                    filtered_second_items = []
                    for sublist in damage_parts["damage_name"]:
                        if isinstance(sublist, list):  # サブリストがリストである場合
                            if any(item.startswith('①') for item in sublist) and any(item.startswith('⑤') for item in sublist):
                                # ⑤で始まる要素を取り除く
                                filtered_sublist = [item for item in sublist if not item.startswith('⑤')]
                                filtered_second_items.append(filtered_sublist)
                            else:
                                filtered_second_items.append(sublist)
                        else:
                            filtered_second_items.append([sublist])
                    
                    # フィルタリング後のsecond_itemsに対して置換を行う                
                    #pavement_items = {"first": first_item[i], "second": filtered_second_items}
                        
            combined_list = []
            if damage_parts["damage_name"] is not None:
                combined_second = filtered_second_items #if i < len(updated_second_items) else None
            else:
                combined_second = None
            
            combined = {"parts_name": first_item[i], "damage_name": combined_second}
            combined_list.append(combined)
            request_list = combined_list[0]
            # <<◆ secondの多重リストを統一させる ◆>>
            try:
                # データを取得する
                check_request_list = request_list['parts_name'][1]

                # 条件分岐
                if isinstance(check_request_list, list):
                    request_list
                    #print(request_list)
                    
            except (KeyError, IndexError) as e:
                # KeyError や IndexError の例外が発生した場合の処理

                # secondの多重リストをフラットなリストに変換
                flat_list = [item for sublist in request_list['damage_name'] for item in sublist]
                # フラットなリストを再びサブリストに変換して格納
                request_list['damage_name'] = [flat_list]
                # 完成目標の確認
                
                test = request_list['damage_name'][0]

            # 先頭が文字（日本語やアルファベットなど）の場合
            def all_match_condition(lst):
                """
                リスト内のすべての項目が特定条件に一致するか確認します。
                ただし、空のリストの場合、Falseを返します。
                """
                # 空のリストの場合は False を返す
                if not lst:
                    return False
                
                pattern = re.compile(r'\A[^\W\d_]', re.UNICODE)
                return all(pattern.match(item) for item in lst)

            if all_match_condition(test):
                request_list
            else:
                request_list['damage_name'] = [request_list['damage_name']]

            #<< ◆損傷メモの作成◆ >>
            replacement_patterns = {
                "①腐食(小小)-b": "腐食", # 1
                "①腐食(小大)-c": "拡がりのある腐食",
                "①腐食(大小)-d": "板厚減少を伴う腐食",
                "①腐食(大大)-e": "板厚減少を伴う拡がりのある腐食",
                "③ゆるみ・脱落-c": "ボルト、ナットにゆるみ・脱落（●本中●本）",
                "③ゆるみ・脱落-e": "ボルト、ナットにゆるみ・脱落（●本中●本）", # 3
                "④破断-e": "鋼材の破断", # 4
                "⑤防食機能の劣化(分類1)-e": "点錆", # 5
                "⑥ひびわれ(小小)-b": "最大幅0.0mmのひびわれ", # 6
                "⑥ひびわれ(小大)-c": "最大幅0.0mmかつ間隔0.5m未満のひびわれ",
                "⑥ひびわれ(中小)-c": "最大幅0.0mmのひびわれ",
                "⑥ひびわれ(中大)-d": "最大幅0.0mmかつ間隔0.5m未満のひびわれ",
                "⑥ひびわれ(大小)-d": "最大幅0.0mmのひびわれ",
                "⑥ひびわれ(大大)-e": "最大幅0.0mmかつ間隔0.5m未満のひびわれ",
                "⑦剥離・鉄筋露出-c": "コンクリートの剥離", # 7
                "⑦剥離・鉄筋露出-d": "鉄筋露出",
                "⑦剥離・鉄筋露出-e": "断面減少を伴う鉄筋露出",
                "⑧漏水・遊離石灰-c": "漏水", # 8
                "⑧漏水・遊離石灰-d": "遊離石灰",
                "⑧漏水・遊離石灰-e": "著しい遊離石灰・泥や錆汁の混入を伴う漏水",
                "⑨抜け落ち-e": "コンクリート塊の抜け落ち", # 9
                "⑪床版ひびわれ-b": "最大幅0.0mmの1方向ひびわれ",
                "⑪床版ひびわれ-c": "最大幅0.0mmの1方向ひびわれ",
                "⑪床版ひびわれ-d": "最大幅0.0mmの1方向ひびわれ",
                "⑪床版ひびわれ-e": "最大幅0.0mmの角落ちを伴う1方向ひびわれ", # 11
                "⑫うき-e": "コンクリートのうき", # 12
                "⑮舗装の異常-c": "最大幅0.0mmのひびわれ",
                "⑮舗装の異常-e": "最大幅0.0mmのひびわれ・舗装の土砂化", # 15
                "⑯定着部の異常-c": "定着部の損傷。",
                "⑯定着部の異常(分類2)-e": "定着部の著しい損傷", # 16
                "⑳漏水・滞水-e": "漏水・滞水", # 20
                "㉓変形・欠損-c": "変形・欠損", # 23
                "㉓変形・欠損-e": "著しい変形・欠損",
                "㉔土砂詰まり-e": "土砂詰まり", # 24
            }

            def describe_damage(unified_request_list):
                described_list = []
                
                for damage in unified_request_list:
                    if damage in replacement_patterns:
                        described_list.append(replacement_patterns[damage])
                    elif damage.startswith('⑰'):
                        match = re.search(r'(?<=:)(.*?)(?=\)-e)', damage)
                        if match:
                            described_list.append(match.group(1))
                    else:
                        pattern = r'[\u3248-\u3257](.*?)-'
                        match = re.search(pattern, damage)
                        if match:
                            described_list.append(match.group(1))
                        else:
                            described_list.append(damage)  # フォールバックとしてそのまま返す
                return ','.join(described_list)

            # 各ケースに対して出力を確認:
            def generate_report(unified_request_list):
                primary_damages = []
                processed_related_damages = []
                #print(f"unified_request_list：{unified_request_list}")
                first_items = unified_request_list['parts_name']
                #print(first_items) # [['支承本体 Bh0101'], ['沓座モルタル Bm0101']]
                second_items = unified_request_list['damage_name']
                #print(second_items) # [['①腐食(小小)-b', '⑤防食機能の劣化(分類1)-e'], ['⑦剥離・鉄筋露出-c']]
                primary_damages_dict = {}

                for first_item, second_item in zip(first_items, second_items):
                    element_names = [f.split()[0] for f in first_item] # カッコ内の要素について、スペースより前を抽出
                    #print(f"element_names：{element_names}") # ['支承本体'], ['沓座モルタル']
                    damage_descriptions = describe_damage(second_item) # 辞書で置換
                    #print(f"damage_descriptions：{damage_descriptions}") # 腐食,点錆, 剥離
                    
                    if len(element_names) == 1: # ['主桁', '横桁', '対傾構']：これはだめ
                        primary_damages.append(f"{element_names[0]}に{damage_descriptions}が見られる。")
                        #print(f"primary_damages：{primary_damages}") # ['支承本体に腐食,点錆が見られる。', '沓座モルタルに剥離が見られる。']
                    else:
                        element_names = list(dict.fromkeys(element_names))            
                        joined_elements = "および".join(element_names[:-1]) + "," + element_names[-1]
                        if joined_elements.startswith(","):
                            new_joined_elements = joined_elements[1:]
                        else:
                            new_joined_elements = joined_elements
                        primary_damages.append(f"{new_joined_elements}に{damage_descriptions}が見られる。")

                    for elem in first_item:
                        primary_damages_dict[elem] = second_item[:]

                primary_description = "また".join(primary_damages)
                    
                for elem_name, elem_number in zip(first_items, second_items): # 主桁 Mg0101
                    # リストをフラットにする関数
                    def flatten_list(nested_list):
                        return [item for sublist in nested_list for item in sublist]
                    
                    # 辞書から 'first' と 'second' の値を取り出す
                    first_list = request_list['parts_name']
                    second_list = request_list['damage_name']

                    # 'first' の要素数を数える
                    first_count = sum(len(sublist) for sublist in first_list)

                    # 'second' の要素数を数える
                    second_count = sum(len(sublist) for sublist in second_list)
                    # フラットにしたリストを比較
                    if flatten_list(first_items) != elem_name and flatten_list(second_items) != elem_number:
                        sub_related_damages = []
                        for first_item in first_items:
                            for elem in first_item:
                                if elem in primary_damages_dict:
                                    formatted_damages = ",".join(list(dict.fromkeys(primary_damages_dict[elem])))
                                    sub_related_damages.append(f"{elem}:{formatted_damages}")
                                    #print(f"sub_related_damages：{sub_related_damages}") # ['支承本体 Bh0101:①腐食(小小)-b,⑤防食機能の劣化(分類1)-e', '沓座モルタル Bm0101:⑦剥離・鉄筋露出-c']

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

                                else:
                                    # 2つ目以降の要素の場合
                                    parts = damage.split(',')
                                    second_related_damages.append(damage)
                                    

                        # 処理後のリストを格納するための新しいリスト
                        processed_related_damages = []
                        #print(f"second_related_damages：{second_related_damages}")
                        for damage in second_related_damages:
                            colon_index = damage.find(":")
                            if colon_index != -1:
                                before_colon_part = damage[:colon_index].strip()
                                after_colon_part = damage[colon_index + 1:].strip()
                                #print(f"damage[colon_index + 1:]：{damage}")
                                if before_colon_part and after_colon_part:
                                    processed_damage = f"{before_colon_part}:{after_colon_part}"
                                    processed_related_damages.append(processed_damage)
                        #print(f"after_colon_part：{processed_related_damages}")
                        
                    elif first_count < 2 and second_count < 2: # {'first': [['横桁 Cr0803']], 'second': [['⑦剥離・鉄筋露出-d']]}
                        None
                    elif first_count > 1 and second_count < 2: # {'first': [['床版 Ds0201', '床版 Ds0203']], 'second': [['⑦剥離・鉄筋露出-d']]}
                        first_items_from_first = first_item[1:]
                        related_damage_list = ','.join(first_items_from_first)# カンマ区切りの文字列に結合
                        related_second_item = ','.join(second_item)
                        processed_related_damages.append(f"{related_damage_list}:{related_second_item}")
                    elif first_count < 2 and second_count > 1: # {'first': [['横桁 Cr0503']], 'second': [['⑦剥離・鉄筋露出-d', '⑰その他(分類6:施工不良)-e']]}
                        second_items_from_second = second_item[1:]
                        related_damage_list = ','.join(second_items_from_second)# カンマ区切りの文字列に結合
                        processed_related_damages.append(f"{','.join(elem_name)}:{related_damage_list}")
                    else:#  len(elem_name) > 1 and len(elem_number) > 1: # {'first': [['排水管 Dp0101', '排水管 Dp0102']], 'second': [['①腐食(小大)-c', '⑤防食機能の劣化(分類1)-e']]}
                        related_damage_list = ','.join(second_item)
                        processed_related_damages.append(f"{','.join(elem_name)}:{related_damage_list}")


                related_description = ""
                if processed_related_damages:
                    related_description = "\n【関連損傷】\n" + ", ".join(processed_related_damages)

                return f"{primary_description} {related_description}".strip()

            combined_data = generate_report(request_list)
            #print(combined_data)
            
                    # \n文字列のときの改行文字
            items = {'parts_name': first_item[i], 'damage_name': second_items[i], 'join': first_and_second, 
                     'picture_number': third, 'this_time_picture': picture_urls, 'last_time_picture': None, 'textarea_content': combined_data, 
                     'damage_coordinate': damage_coordinate[i], 'picture_coordinate': picture_coordinate[i]}

            damage_table.append(items)


        #優先順位の指定
        order_dict = {"主桁": 1, "横桁": 2, "床版": 3, "PC定着部": 4, "橋台[胸壁]": 5, "橋台[竪壁]": 6, "支承本体": 7, "沓座モルタル": 8, "防護柵": 9, "地覆": 10, "伸縮装置": 11, "舗装": 12, "排水ます": 13, "排水管": 14}
        order_number = {"None": 0, "①": 1, "②": 2, "③": 3, "④": 4, "⑤": 5, "⑥": 6, "⑦": 7, "⑧": 8, "⑨": 9, "⑩": 10, "⑪": 11, "⑫": 12, "⑬": 13, "⑭": 14, "⑮": 15, "⑯": 16, "⑰": 17, "⑱": 18, "⑲": 19, "⑳": 20, "㉑": 21, "㉒": 22, "㉓": 23, "㉔": 24, "㉕": 25, "㉖": 26}
        order_lank = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
                
        # <<◆ リストの並び替え ◆>>
        def sort_key_function(sort_item):
            first_value = sort_item['parts_name'][0][0] # firstキーの最初の要素
            #print(first_value) # 主桁 Mg0901

            if " " in first_value:
                # 部材記号の前にスペースが「含まれている」場合
                first_value_split = first_value.split()
                #print(first_value_split) # ['主桁', 'Mg0901']
            else:
                # 部材記号の前にスペースが「含まれていない」場合
                first_value_split = re.split(r'(?<=[^a-zA-Z])(?=[a-zA-Z])', first_value) # アルファベット以外とアルファベットの並びで分割
                first_value_split = [x for x in first_value_split if x] # re.split()の結果には空文字が含まれるので、それを取り除く
                #print(f"first_value_split：{first_value_split}") # ['主桁', 'Mg0901']

            first_name_key = order_dict.get(first_value_split[0], float('inf'))
            #print(first_name_key) # 1
            if "～" in first_value_split[1]:
                match = re.search(r'[A-Za-z]+(\d{2,})(\D)', first_value_split[1])
                if match:
                    first_number_key = int(match.group(1))
            else:
                first_number_key = int(first_value_split[1][2:])
            #print(first_number_key) # 901

            if sort_item['damage_name'][0][0]:  # `second`キーが存在する場合
                second_value = sort_item['damage_name'][0][0] # secondキーの最初の要素
                #print(second_value) # ⑰その他(分類6:異物混入)-e
                second_number_key = order_number.get(second_value[0], float('inf'))  # 先頭の文字を取得してorder_numberに照らし合わせる
                #print(second_number_key) # 17
                second_lank_key = order_lank.get(second_value[-1], float('inf'))  # 末尾の文字を取得してorder_lankに照らし合わせる
                #print(second_lank_key) # 5
            else:
                second_number_key = float('inf')
                second_lank_key = float('inf')
                    
            return (first_name_key, first_number_key, second_number_key, second_lank_key)

        sorted_items = sorted(damage_table, key=sort_key_function)
        
    return sorted_items