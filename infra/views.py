from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import WorkListView, ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Infra
from django.contrib.auth.mixins import LoginRequiredMixin

class WorkListInfraView(LoginRequiredMixin, WorkListView):
  template_name = 'infra/infra_work_list.html'
  model = Infra
  
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