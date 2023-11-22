from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import AddPostForm
from .models import *

menu = [{'title': "About site", 'url_name': 'about'},
        {'title': "Add article", 'url_name': 'add_page'},
        {'title': "Feedback", 'url_name': 'contact'},
        {'title': "Login", 'url_name': 'login'}
        ]


class WomenHome(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Main Page'
        context['category_selected'] = 0
        return context

    def get_queryset(self):
        return Women.objects.filter(is_published=True)


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'About site'})


class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add an article'
        context['menu'] = menu
        return context


def contact(request):
    return HttpResponse("Feedback")


def login(request):
    return HttpResponse("Login")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")


class ShowPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context


class WomenCategory(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Category - ' + str(context['posts'][0].category)
        context['menu'] = menu
        context['category_selected'] = context['posts'][0].category_id
        return context
