from django.shortcuts import render, redirect
from .models import Material
from django.views.generic import ListView, DetailView
from .forms import ArticleForm
from django.urls import reverse
# Create your views here.




class HomeListView(ListView):
    model = Material
    template_name = 'index.html'
    context_object_name = 'list_material'

class HomeDetailView(DetailView):
    model = Material
    template_name = 'detail.html'
    context_object_name = 'get_material'


def edit_page(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
    
    template = 'edit_page.html'
    context ={
          
        'list_material': Material.objects.all(),
        'form': ArticleForm()

    }

    
    return render(request, template, context)

def update_page(request,pk):

    get_article = Material.objects.get(pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance = get_article)
        if form.is_valid():
            form.save()


    template = 'edit_page.html'
    
    context = {

        'get_material': get_article,
        'update':True,
        'form': ArticleForm(instance = get_article),
        
    }
    return render(request, template, context)

def delete_page(request, pk):
    get_article = Material.objects.get(pk=pk)
    get_article.delete()
    return redirect(reverse('edit_page'))   