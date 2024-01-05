from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Infra
from .models import Article
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FileUploadForm
from .forms import PhotoUploadForm
from .models import Photo

class ListInfraView(LoginRequiredMixin, ListView):
  template_name = 'infra/infra_list.html'
  model = Infra

class DetailInfraView(LoginRequiredMixin, DetailView):
  template_name = 'infra/infra_detail.html'
  model = Infra
  
class CreateInfraView(LoginRequiredMixin, CreateView):
  template_name = 'infra/infra_create.html'
  model = Infra
  fields = ('title', '径間数', '橋長', '全幅員', '橋梁コード', '活荷重', '等級', '適用示方書', '上部構造形式', '下部構造形式', '基礎構造形式', '近接方法', '交通規制', '第三者点検の有無', '海岸線との距離', '路下条件', '特記事項', 'カテゴリー')
  success_url = reverse_lazy('list-infra')
  
class DeleteInfraView(LoginRequiredMixin, DeleteView):
  template_name = 'infra/infra_delete.html'
  model = Infra
  success_url = reverse_lazy('list-infra')
  
class UpdateInfraView(LoginRequiredMixin, UpdateView):
  template_name = 'infra/infra_update.html'
  model = Infra
  fields = ('title', '径間数', '橋長', '全幅員', '橋梁コード', '活荷重', '等級', '適用示方書', '上部構造形式', '下部構造形式', '基礎構造形式', '近接方法', '交通規制', '第三者点検の有無', '海岸線との距離', '路下条件', '特記事項', 'カテゴリー')
  success_url = reverse_lazy('list-infra')
  
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
  fields = ('title', 'article_name', 'number', 'manager', 'other')
  success_url = reverse_lazy('list-article')
  
class DeleteArticleView(LoginRequiredMixin, DeleteView):
  template_name = 'infra/article_confirm_delete.html'
  model = Article
  success_url = reverse_lazy('list-article')
  
class UpdateArticleView(LoginRequiredMixin, UpdateView):
  template_name = 'infra/article_update.html'
  model = Article
  fields = ('title', 'article_name', 'number', 'manager', 'other')
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
  
