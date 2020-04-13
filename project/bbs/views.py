from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models, forms
from login.models import User


def index(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    posts = models.Post.objects.all()
    ctx = {'posts': posts}
    return render(request, 'bbs/index.html', ctx)


def bbs_detail(request, post_id):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    post = models.Post.objects.get(pk=post_id)
    ctx = {'post': post, 'tags': post.tags.all()}
    return render(request, 'bbs/detail.html', ctx)


def post_edit_page(request, post_id):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    if str(post_id) == '0':
        post_form = forms.PostForm()
        return render(request, 'bbs/edit_page.html', locals())
    post = models.Post.objects.get(pk=post_id)
    return render(request, 'bbs/edit_page.html', {'post': post})


def post_edit_page_action(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    title = request.POST.get('title', '默认标题')
    content = request.POST.get('content', '默认内容')
    post_id = request.POST.get('post_id_hidden', '0')
    if str(post_id) == '0':
        if request.method == 'POST':
            post_form = forms.PostForm(request.POST)
            if post_form.is_valid():
                title = post_form.cleaned_data.get('title')
                content = post_form.cleaned_data.get('content')
                category = post_form.cleaned_data.get('category')
                tag = post_form.cleaned_data.get('tag')

            author = User.objects.get(sno=request.session['user_sno'])

            post_new = models.Post.objects.create(title=title, content=content, author=author, category=category)
            post_new.tags.add(tag)

            posts = models.Post.objects.all()
            return render(request, 'bbs/index.html', {'posts': posts})

    post = models.Post.objects.get(pk=post_id)
    post.title = title
    post.content = content
    post.save()
    return render(request, 'bbs/edit_page.html', {'post': post})
