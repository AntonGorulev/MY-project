from django.shortcuts import render, redirect, HttpResponse
from .models import Material
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from .forms import ArticleForm, AuthUserForm, RegisterUserForm, CommentForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from . import forms




class HomeListView(ListView):
    model = Material
    template_name = 'index.html'
    context_object_name = 'list_material'


class CustomSuccessMessageMixin:
    @property
    def success_msg(self):
        return False
 
    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)


class HomeDetailView(CustomSuccessMessageMixin, FormMixin, DetailView):
    model = Material
    template_name = 'detail.html'
    context_object_name = 'get_material'
    form_class = CommentForm
    success_msg = 'Комментарий успешно создан'
    
    
    def get_success_url(self):
        return reverse_lazy( 'main:detail_page', kwargs={'pk':self.get_object().id})
    
    def post(self,request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.article = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ArticleCreateView(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView):
    login_url = reverse_lazy('main:login_page')
    model = Material
    template_name = 'edit_page.html'
    form_class = ArticleForm
    success_url = reverse_lazy('main:edit_page')
    success_msg = 'Запись создана'

    def get_context_data(self, **kwargs):
        kwargs['list_material'] = Material.objects.all().order_by('-id')
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    model = Material
    template_name = 'edit_page.html'
    form_class = ArticleForm
    success_url = reverse_lazy('main:edit_page')

    def get_context_data(self, **kwargs):
        kwargs['update'] = True
        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs


class MyprojectLoginView(LoginView):
    template_name = 'login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('main:edit_page')

    def get_success_url(self):
        return self.success_url


class RegisterUserView(CreateView):
    model = User
    template_name = 'register_page.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('main:edit_page')
    success_msg = 'Пользователь успешно создан'
    
    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class MyProjectLogout(LogoutView):
    next_page = reverse_lazy('main:edit_page')


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Material
    template_name = 'edit_page.html'
    success_url = reverse_lazy('main:edit_page')
    success_msg = 'Запись удалена'

    def post(self, request, *args, **kwargs):
        messages.success(self.request, self.success_msg)
        return super().post(request)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.request.user != self.object.author:
            return self.handle_no_permission()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

@login_required
def view_profile(request):
    return render(request, 'profile.html', {'user': request.user})

def edit_profile(request):
    if request.method == "POST":
        user_form = forms.UserEditForm(data=request.POST,
                                       instance=request.user)
        profile_form = forms.ProfileEditForm(data=request.POST,
                                             instance=request.user.profile,
                                             files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            if not profile_form.cleaned_data['photo']:
                profile_form.cleaned_data['photo'] = request.user.profile.photo
            profile_form.save()
            return render(request, 'profile.html', {'user': request.user})
    else:
        user_form = forms.UserEditForm(instance=request.user)
        profile_form = forms.ProfileEditForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'user_form': user_form,
                                                 'profile_form': profile_form})

