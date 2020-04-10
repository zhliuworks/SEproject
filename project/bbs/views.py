from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models, forms
from login.models import User


def index(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    posts = models.Post.objects.all()
    ctx = {'posts': posts}
    return render(request,'bbs/index.html',ctx)


def bbs_detail(request, post_id):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    post = models.Post.objects.get(pk=post_id)
    ctx = {'post': post, 'tags': post.tags.all()}
    return render(request, 'bbs/detail.html', ctx)


def post_edit_page(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    post_form = forms.PostForm()
    return render(request, 'bbs/edit_page.html', locals())


def post_edit_page_action(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            title = post_form.cleaned_data.get('title')
            content = post_form.cleaned_data.get('content')
            category = post_form.cleaned_data.get('category')
            tag = post_form.cleaned_data.get('tag')

    author = User.objects.get(sno=request.session['user_sno'])

    post = models.Post.objects.create(title=title, content=content, author=author, category=category)
    post.tags.add(tag)

    posts = models.Post.objects.all()
    return render(request, 'bbs/index.html', {'posts': posts})