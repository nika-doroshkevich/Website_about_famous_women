from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect

from .forms import AddPostForm
from .models import *

menu = [{'title': "About site", 'url_name': 'about'},
        {'title': "Add article", 'url_name': 'add_page'},
        {'title': "Feedback", 'url_name': 'contact'},
        {'title': "Login", 'url_name': 'login'}
        ]


def index(request):
    posts = Women.objects.all()

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Main Page',
        'category_selected': 0
    }

    return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'menu': menu, 'title': 'About site'})


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    return render(request, 'women/add_page.html', {'form': form, 'menu': menu, 'title': 'Add an article'})


def contact(request):
    return HttpResponse("Feedback")


def login(request):
    return HttpResponse("Login")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Page not found</h1>")


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'category_selected': post.category_id
    }

    return render(request, 'women/post.html', context=context)


def show_category(request, category_id):
    posts = Women.objects.filter(category_id=category_id)

    if len(posts) == 0:
        raise Http404()

    context = {
        'posts': posts,
        'menu': menu,
        'title': 'Display by category',
        'category_selected': category_id
    }

    return render(request, 'women/index.html', context=context)
