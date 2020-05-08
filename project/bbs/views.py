from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from . import models, forms
from login.models import User


def index(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    posts_list = models.Post.objects.order_by('-create_time')
    paginator = Paginator(posts_list, 10)
    if request.method == "GET":
        page = request.GET.get('page')
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except InvalidPage:
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
    else:
        posts = paginator.page(1)
    return render(request, 'bbs/index.html', {'posts': posts, "length": len(posts_list)})


def bbs_detail(request, post_id):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    post = models.Post.objects.get(pk=post_id)
    user = User.objects.get(sno=request.session['user_sno'])
    comments = models.Comment.objects.filter(post=post).order_by("-created")
    if user not in post.like_users.all():
        sign_like = False
    else:
        sign_like = True
    if user.sno == post.author.sno:
        sign = True
    else:
        sign = False
    ctx = {'post': post, 'tags': post.tags.all(), 'sign': sign, 'sign_like': sign_like,
           'comments': comments, 'user': user}
    return render(request, 'bbs/detail.html', ctx)


def post_edit_page(request, post_id):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    if str(post_id) == '0':
        post_form = forms.PostForm()
        return render(request, 'bbs/edit_page.html', locals())
    post = models.Post.objects.get(pk=post_id)
    user = User.objects.get(sno=request.session['user_sno'])
    if user.sno != post.author.sno:
        return HttpResponseRedirect(reverse('bbs:detail', args=(post_id,)))
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
                tags = post_form.cleaned_data.get('tag')

            author = User.objects.get(sno=request.session['user_sno'])

            post_new = models.Post.objects.create(title=title, content=content, author=author, category=category)

            for tag in tags:
                post_new.tags.add(tag)

            posts = models.Post.objects.all()
            return index(request)

    post = models.Post.objects.get(pk=post_id)
    post.title = title
    post.content = content
    post.save()
    return HttpResponseRedirect(reverse('bbs:detail', args=(post_id,)))


def like_post(request, post_id):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    post = models.Post.objects.get(pk=post_id)
    user = User.objects.get(sno=request.session['user_sno'])
    comments = post.comment_set.all()
    sign_like = True
    if user not in post.like_users.all():
        post.likes += 1
        post.like_users.add(user)
        post.save()
        return HttpResponseRedirect(reverse('bbs:detail', args=(post_id,)))
    else:
        ctx = {'sign_like': sign_like, 'post': post, 'tags': post.tags.all(), 'comments': comments}
        return render(request, "bbs/detail.html", ctx)


def post_comment_page(request, post_id, comment_id):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    post = models.Post.objects.get(pk=post_id)
    data = {'reply_comment_id': comment_id}
    comment_form = forms.CommentForm(data)
    return render(request, 'bbs/comment_page.html', locals())


def post_comment_page_action(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    post_id = request.POST.get('post_id_hidden', '0')
    content = request.POST.get('content')
    if not content:
        return HttpResponseRedirect(reverse('bbs:comment', args=(post_id,)))
    post = models.Post.objects.get(pk=post_id)
    name = User.objects.get(sno=request.session['user_sno'])
    if request.method == 'POST':
        comment_form = forms.CommentForm(request.POST)
        if comment_form.is_valid():
            content = comment_form.cleaned_data['content']
            parent = comment_form.cleaned_data['parent']
            if parent:
                root = parent.root if parent.root else parent
                reply_to = parent.name
            else:
                root = None
                reply_to = None
            comment = models.Comment.objects.create(post=post, name=name, content=content, parent=parent, root=root, reply_to=reply_to)

    return HttpResponseRedirect(reverse('bbs:detail', args=(post_id,)))


def delete_comment(request, comment_id):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    comment = models.Comment.objects.get(pk=comment_id)
    post_id = comment.post.id
    comment.delete()
    return HttpResponseRedirect(reverse('bbs:detail', args=(post_id,)))


def delete_post(request, post_id):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    post = models.Post.objects.get(pk=post_id)
    post.delete()
    return redirect('/bbs/')
