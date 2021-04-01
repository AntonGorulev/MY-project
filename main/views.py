from django.shortcuts import render
from .models import Material
# Create your views here.


def home(request):

    list_material = Material.objects.all()
    context ={
        'name':'Anton',
        'list_material':list_material
    }

    template ='index.html'

    return render(request, template, context)

def detail(request, id):

    get_material = Material.objects.get(id=id)

    context = {
        'get_material':get_material
    }

    template = 'detail.html'

    return render(request, template, context)