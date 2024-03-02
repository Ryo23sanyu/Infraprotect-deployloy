from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
import pandas as pd
from .models import Infra
from .models import Article
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FileUploadForm, UploadForm
from .forms import PhotoUploadForm
from .models import Photo, Panorama
import os
from django.contrib.auth.decorators import login_required
import ezdxf
from ezdxf.entities.mtext import MText
import tkinter
import tkinter.filedialog
from PIL import Image, ImageTk

class ListInfraView(LoginRequiredMixin, ListView):
    template_name = 'infra/infra_list.html'
    model = Infra # 使用するモデル「infra」
    def get_queryset(self, **kwargs):
        # モデル検索のクエリー。Infra.objects.all() と同じ結果で全ての Infra
        queryset = super().get_queryset(**kwargs)
        # パスパラメータpkによりarticleを求める
        article = Article.objects.get(id = self.kwargs["pk"])
        # 求めたarticleを元にモデル検索のクエリーを絞り込む
        queryset = queryset.filter(article=article)
        # 絞り込んだクエリーをDjangoに返却し表示データとしてもらう
        return queryset

    def get_context_data(self, **kwargs):
        # HTMLテンプレートでの表示変数として「article_id」を追加。
        # 値はパスパラメータpkの値→取り扱うarticle.idとなる
        kwargs["article_id"] = self.kwargs["pk"]
        return super().get_context_data(**kwargs)


class DetailInfraView(LoginRequiredMixin, DetailView):
    template_name = 'infra/infra_detail.html'
    model = Infra
    def get_context_data(self, **kwargs):
        # HTMLテンプレートでの表示変数として「article_id」を追加。
        # 値はパスパラメータpkの値→取り扱うarticle.idとなる
        kwargs["article_id"] = self.kwargs["pk"]
        return super().get_context_data(**kwargs)
  
class CreateInfraView(LoginRequiredMixin, CreateView):
  template_name = 'infra/infra_create.html'
  model = Infra
  fields = ('title', '径間数', '橋長', '全幅員', 'latitude', 'longitude', '橋梁コード', '活荷重', '等級', '適用示方書', '上部構造形式', '下部構造形式', '基礎構造形式', '近接方法', '交通規制', '第三者点検の有無', '海岸線との距離', '路下条件', '特記事項', 'カテゴリー', 'article')
  success_url = reverse_lazy('detail-infra')
  # def get_success_url(self):
    # return reverse_lazy('detail-infra', kwargs={'pk': self.kwargs["pk"]})
  def form_valid(self, form):
    #ここのobjectはデータベースに登録を行うmodelつまりInfraの１レコードです。
    #formはModelFormと呼ばれるフォームの仕組みで、saveを実行すると関連付いているモデルとして登録を行う動きをします。
    object = form.save(commit=False)
    #ここでのobjectは登録対象のInfraモデル１件です。登録処理を行いPKが払い出された情報がobjectです
    #今回はarticle_id、つまりarticleオブジェクトが無いのでこれをobjectに設定します。
    #articleオブジェクトを検索しobjectに代入する事で登録できます。
    article = Article.objects.get( id = self.kwargs["pk"] )
    # id = 1 のarticleを検索
        # article = Article.objects.get(id = 1 )
    object.案件名 = article
    # titleの項目に「A」を設定
        # article.title = "A"
    #設定したのちsaveを実行し更新します。
    object.save()
    return super().form_valid(form)
  def get_success_url(self):
    pk = self.kwargs.get("pk")  # キーが存在しない場合はNoneを返す
    if pk is not None:
        return reverse_lazy('detail-infra', kwargs={'pk': pk})
    else:
        # pkが存在しない場合の処理を記述する
        # 例えば該当するURLがない場合にはトップページにリダイレクトするなど
        return reverse_lazy('list-infra', kwargs={'pk': pk})

class DeleteInfraView(LoginRequiredMixin, DeleteView):
  template_name = 'infra/infra_delete.html'
  model = Infra
  success_url = reverse_lazy('list-infra')
  
class UpdateInfraView(LoginRequiredMixin, UpdateView):
  template_name = 'infra/infra_update.html'
  model = Infra
  fields = ('title', '径間数', '橋長', '全幅員', 'latitude', 'longitude', '橋梁コード', '活荷重', '等級', '適用示方書', '上部構造形式', '下部構造形式', '基礎構造形式', '近接方法', '交通規制', '第三者点検の有無', '海岸線との距離', '路下条件', '特記事項', 'カテゴリー', 'article')
  success_url = reverse_lazy('detail-infra')
  def get_success_url(self):
    return reverse_lazy('detail-infra', kwargs={'pk': self.kwargs["pk"]})
  
def infra_view(request):
  if request.method == 'POST':
    等級 = request.POST.get('等級', None)
    # load_gradeを使って必要な処理を行う
    # 例えば、選択されたload_gradeに基づいてデータをフィルタリングして表示するなど

  # 通常のビューロジック
  # ・・・
  return render(request, 'infra/infra_detail.html')

def index_view(request):
  order_by = request.GET.get('order_by', '案件名')
  object_list = Article.objects.order_by(order_by)
  return render(request, 'infra/index.html', {'object_list': object_list})

# def index_view(request):
  # order_by = request.GET.get('order_by', 'span_number')
  # object_list = Infra.objects.order_by(order_by)
  # return render(request, 'infra/index.html', {'object_list': object_list})

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
  
# class ArticleInfraView(LoginRequiredMixin, DetailView):
 # template_name = 'infra/infra_article.html'
 #  model = Article
 
def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_upload_success')
    else:
        form = FileUploadForm()
    return render(request, 'infra/file_upload.html', {'form': form})

def file_upload_success(request):
    return render(request, 'infra/file_upload_success.html')
  
def photo_list(request):
    photos = Photo.objects.all()
    return render(request, 'infra/photo_list.html', {'photos': photos})

def photo_upload(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        form = PhotoUploadForm()
    return render(request, 'infra/photo_upload.html', {'form': form})

def selected_photos(request):
    selected_photo_ids = request.POST.getlist('selected_photos')
    selected_photos = Photo.objects.filter(id__in=selected_photo_ids)
    return render(request, 'infra/selected_photos.html', {'selected_photos': selected_photos})
  
# 写真の表示
  
def image_list(request):

    """ 
    # 写真フォルダのパスを指定する
    photo_folder = R'C:\work\django\myproject\myvenv\Infraproject\infra\static\infra\img'

    # 写真フォルダ内の画像ファイルを取得する
    image_files = os.listdir(photo_folder)
    """
    
    # 特定のディレクトリ内の全てのファイルパスをリストで取得したい場合はglobを使うと良い。    
    import glob

    files = glob.glob( "infra/static/infra/img/*"  )

    # ページに表示する際、"infra/static/" を削除する。
    image_files = []
    for file in files:
        image_files.append( file.replace("infra/static/", "") )

    # テンプレートに画像ファイルの一覧を渡してレンダリングする
    return render(request, 'image_list.html', {'image_files': image_files})

# 会社別に表示

#@login_required
#def my_view(request):
    #user = request.user
    # 会社情報を使ってコンテンツをフィルタリングする処理
    #filtered_data = Data.objects.filter(company=user.company)
    #return render(request, 'template.html', {'filtered_data': filtered_data})
  
# 全景写真

# def panorama_list(request):
#     panorama = Panorama.objects.all()
#     return render(request, 'panorama_list.html', {'panorama': panorama})

def panorama_list(request):
    panoramas = Panorama.objects.all()
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_panoramas')
        for panorama in panoramas:
            if str(panorama.id) in selected_ids:
                panorama.checked = True
            else:
                panorama.checked = False
            panorama.save()
        return redirect('panorama_list')  # 再描画のためにリダイレクト

    return render(request, 'panorama_list.html', {'panoramas': panoramas})



def panorama_upload(request):
    if request.method == 'POST':
        image = request.FILES['image']
        checked = request.POST.get('checked', False)
        panorama = Panorama.objects.create(image=image, checked=checked)
        return redirect('panorama_list')
    return render(request, 'panorama_upload.html')
   
# 番号表示  
  
from django.http import HttpResponse

def number_view(request):
    start = "0101"
    end = "0206"

    # 最初の2桁と最後の2桁を取得
    start_prefix = start[:2]
    start_suffix = start[2:]
    end_prefix = end[:2]
    end_suffix = end[2:]

    # 抽出した数字を文字列として結合
    result = ""
    for prefix in range(int(start_prefix), int(end_prefix)+1):
        for suffix in range(int(start_suffix), int(end_suffix)+1):
            result += "{:02d}{:02d}\n".format(prefix, suffix)

    return HttpResponse(result)

# <<テーブルの作成>>

def table_view(request):

    dxf = ezdxf.readfile(R'C:\work\django\myproject\myvenv\Infraproject\uploads\12_損傷橋.dxf') # ファイルにアップロードしたdxfファイル名

    cad_read = []
    for entity in dxf.entities:
        if type(entity) is MText: # or type(entity) is Text: MTextとTextが文字列を表す(https://ymt-lab.com/post/2021/ezdxf-read-dxf-file/)
            cad =  entity.plain_text() # plain_text(読める文字)に変換
            cad_data = cad.split("\n") if len(cad) > 0 else [] # .split():\nの箇所で配列に分配
            if len(cad_data) > 0 and "\n" in cad and not cad.startswith("※") and not any(keyword in cad for keyword in ["×", "."]):
             # 改行を含むかどうかをチェックする:# 特定の文字列で始まるかどうかをチェックする: # 特定の文字を含むかどうかをチェックする
                    cad_read.append(cad_data)

# 先頭の要素を抽出
    first_item = [sub_list[0] for sub_list in cad_read]
# それ以外の要素を抽出
    # リストの各要素から記号を削除する
    def remove_symbols(other_items):
        symbols = ['!', '[', ']', "'"]

        processed_other_items = []
        for item in other_items:
            processed_item = ''.join(c for c in item if c not in symbols)
            processed_other_items.append(processed_item)
    
        return processed_other_items
    other_items = [sub_list[1:-1] for sub_list in cad_read]
    middle_items = remove_symbols(other_items)
    
# 最後の要素を抽出
    last_item = [sub_list[-1] for sub_list in cad_read]

    damage_table = []  # 空のリストを作成

# ループで各要素を辞書型に変換し、空のリストに追加
    for i in range(len(first_item)):
        item = {'first': first_item[i], 'second': middle_items[i], 'third': last_item[i]}
        damage_table.append(item)
        
    context = {'damage_table': damage_table}  # テンプレートに渡すデータ
    return render(request, 'table.html', context)

# 番号表示

def sample_view(request):# 追加
    start = "0101"
    end = "0206"

# 最初の2桁と最後の2桁を取得
    start_prefix = start[:2]
    start_suffix = start[2:]
    end_prefix = end[:2]
    end_suffix = end[2:]

# 抽出した数字を表示
    result = ""# 追加
    for prefix in range(int(start_prefix), int(end_prefix)+1):
        for suffix in range(int(start_suffix), int(end_suffix)+1):
            result += "{:02d}{:02d}".format(prefix, suffix)
        
    return HttpResponse(result)# 追加

# <<ファイルアップロード(プライマリーキーで分類分け)>>

def upload_directory_path(instance, filename):
    # プライマリーキーを取得する
    primary_key = instance.pk
    # 'documents/プライマリーキー/filename' のパスを返す
    return 'uploads/{}/{}'.format(primary_key, filename)

class Upload(models.Model):
    file = models.FileField(upload_to=upload_directory_path)

# <<写真表示>>
save_path = "C:\work\django\myproject\myvenv\Infraproject\infra\static\infra\img"
def display_photo(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
    # フォームが有効な場合は、選択された写真を特定のフォルダに保存します
            photo = form.cleaned_data['photo']
            file_name = photo.name  # 写真のファイル名を取得します
            file_path = os.path.join(save_path, file_name)  # ファイルの保存先のパスを作成します

            with open(file_path, 'wb') as f:
                for chunk in photo.chunks():
                    f.write(chunk)  # 写真のデータをファイルに書き込みます

        return render(request, 'image_list.html', {'photo': photo})
    else:
        form = UploadForm()
    return render(request, 'upload_photo.html', {'form': form})