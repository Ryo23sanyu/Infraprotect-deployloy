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
  fields = ('title', 'span_number', 'length', 'full_width', 'code', 'live_load', 'load_grade', 'rule_book', 'top_structure', 'bottom_structure', 'under_structure', 'proximity_method', 'traffic_regulation', 'third_party', 'coastline_distance', 'road_conditions', 'notices', 'category')
  success_url = reverse_lazy('list-infra')
  
class DeleteInfraView(LoginRequiredMixin, DeleteView):
  template_name = 'infra/infra_delete.html'
  model = Infra
  success_url = reverse_lazy('list-infra')
  
class UpdateInfraView(LoginRequiredMixin, UpdateView):
  template_name = 'infra/infra_update.html'
  model = Infra
  fields = ('title', 'span_number', 'length', 'full_width', 'code', 'live_load', 'load_grade',  'rule_book','top_structure', 'bottom_structure', 'under_structure', 'proximity_method', 'traffic_regulation', 'third_party', 'coastline_distance', 'road_conditions', 'notices', 'category')
  success_url = reverse_lazy('list-infra')
  
def infra_view(request):
  if request.method == 'POST':
    load_grade = request.POST.get('load_grade', None)
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
  
