from django.shortcuts import render, redirect
from .models import Material
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ArticleForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages


class HomeListView(ListView):
    model = Material
    template_name = 'index.html'
    context_object_name = 'list_material'

class HomeDetailView(DetailView):
    model = Material
    template_name = 'detail.html'
    context_object_name = 'get_material'


class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False
        
    def form_valid(self,form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)



class ArticleCreateView(CustomSuccessMessageMixin, CreateView):
    model = Material
    template_name = 'edit_page.html'
    form_class = ArticleForm
    success_url = reverse_lazy('edit_page')
    success_msg = 'Запись создана'
    def get_context_data(self,**kwargs):
       kwargs['list_material'] = Material.objects.all().order_by('-id')
       return super().get_context_data(**kwargs)


class ArticleUpdateView(UpdateView):
    model = Material
    template_name = 'edit_page.html'
    form_class = ArticleForm
    success_url = reverse_lazy('edit_page')
    def get_context_data(self,**kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

class ArticleDeleteView(DeleteView):
    model = Material
    template_name = 'edit_page.html'
    success_url = reverse_lazy('edit_page')
