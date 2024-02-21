from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
import pandas as pd
from infra.autocad import write_html
from .models import Infra
from .models import Article
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FileUploadForm
from .forms import PhotoUploadForm
from .models import Photo, Panorama
import os
from django.contrib.auth.decorators import login_required

class ListInfraView(LoginRequiredMixin, ListView):
    template_name = 'infra/infra_list.html'
    model = Infra
    def get_queryset(self, **kwargs):
        queryset = super().get_queryset(**kwargs) # Article.objects.all() と同じ結果
    
        # GETリクエストパラメータにkeywordがあれば、それでフィルタする
        #keyword = self.request.GET.get( object.pk )            
        #keyword = Infra.objects.filter(article__id = self.kwargs["pk"] )
        keyword = self.request.GET.get( self.kwargs["pk"] )

        if keyword is not None:
            queryset = queryset.filter(title__contains=keyword)

        return queryset
    


class DetailInfraView(LoginRequiredMixin, DetailView):
    template_name = 'infra/infra_detail.html'
    model = Infra
  
class CreateInfraView(LoginRequiredMixin, CreateView):
  template_name = 'infra/infra_create.html'
  model = Infra
  fields = ('title', '径間数', '橋長', '全幅員', 'latitude', 'longitude', '橋梁コード', '活荷重', '等級', '適用示方書', '上部構造形式', '下部構造形式', '基礎構造形式', '近接方法', '交通規制', '第三者点検の有無', '海岸線との距離', '路下条件', '特記事項', 'カテゴリー')
  success_url = reverse_lazy('detail-infra')
  # def get_success_url(self):
    # return reverse_lazy('detail-infra', kwargs={'pk': self.kwargs["pk"]})
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
  fields = ('title', '径間数', '橋長', '全幅員', 'latitude', 'longitude', '橋梁コード', '活荷重', '等級', '適用示方書', '上部構造形式', '下部構造形式', '基礎構造形式', '近接方法', '交通規制', '第三者点検の有無', '海岸線との距離', '路下条件', '特記事項', 'カテゴリー')
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
  order_by = request.GET.get('order_by', 'title')
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
  fields = ('title', '物件名', '対象数', '担当者名', 'その他')
  success_url = reverse_lazy('list-article')
  
class DeleteArticleView(LoginRequiredMixin, DeleteView):
  template_name = 'infra/article_confirm_delete.html'
  model = Article
  success_url = reverse_lazy('list-article')
  
class UpdateArticleView(LoginRequiredMixin, UpdateView):
  template_name = 'infra/article_update.html'
  model = Article
  fields = ('title', '物件名', '対象数', '担当者名', 'その他')
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
  
# Django上にテーブルを作成
  
def my_view(request):
    df = pd.read_csv("C:\work\django\myproject\myvenv\Infraproject\output.csv")  # 保存したCSVファイルを読み込む

    html = write_html(df, 'future.html')  # HTMLコードを生成

    return HttpResponse(html)
  
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

from django.shortcuts import render

def table_view(request):
    people = [
        {'name': 'Alice', 'age': 25},
        {'name': 'Bob', 'age': 30},
        {'name': 'Charlie', 'age': 35}
    ]
    context = {'people': people}  # テンプレートに渡すデータ
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
