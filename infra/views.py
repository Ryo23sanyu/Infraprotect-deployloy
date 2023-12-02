from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Infra
from .models import Article
from django.contrib.auth.mixins import LoginRequiredMixin

class ListInfraView(LoginRequiredMixin, ListView):
  template_name = 'infra/infra_list.html'
  model = Infra

class DetailInfraView(LoginRequiredMixin, DetailView):
  template_name = 'infra/infra_detail.html'
  model = Infra
  
class CreateInfraView(LoginRequiredMixin, CreateView):
  template_name = 'infra/infra_create.html'
  model = Infra
  fields = ('title', 'span_number', 'length', 'full_width', 'category')
  success_url = reverse_lazy('list-infra')
  
class DeleteInfraView(LoginRequiredMixin, DeleteView):
  template_name = 'infra/infra_confirm_delete.html'
  model = Infra
  success_url = reverse_lazy('list-infra')
  
class UpdateInfraView(LoginRequiredMixin, UpdateView):
  template_name = 'infra/infra_update.html'
  model = Infra
  fields = ('title', 'span_number', 'length', 'full_width', 'category')
  success_url = reverse_lazy('list-infra')
  
def index_view(request):
  order_by = request.GET.get('order_by', 'span_number')
  object_list = Infra.objects.order_by(order_by)
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
  fields = ('title', 'article_name', 'number', 'other')
  success_url = reverse_lazy('list-article')
  
class DeleteArticleView(LoginRequiredMixin, DeleteView):
  template_name = 'infra/article_confirm_delete.html'
  model = Article
  success_url = reverse_lazy('list-article')
  
class UpdateArticleView(LoginRequiredMixin, UpdateView):
  template_name = 'infra/article_update.html'
  model = Article
  fields = ('title', 'article_name', 'number', 'other')
  success_url = reverse_lazy('list-article')
  
# class ArticleInfraView(LoginRequiredMixin, DetailView):
 # template_name = 'infra/infra_article.html'
 #  model = Article