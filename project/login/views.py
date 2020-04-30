from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from . import forms, models
from bbs.models import Post, Comment, Tag, Category, Message


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/login/')
    return render(request, 'login/index.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('/login/index/')
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            sno = login_form.cleaned_data.get('sno')
            password = login_form.cleaned_data.get('password')

            try:
                user = models.User.objects.get(sno=sno)
            except:
                message = '用户不存在！'
                return render(request, 'login/login.html', locals())

            if user.password == password:
                request.session['is_login'] = True
                request.session['user_sno'] = user.sno
                request.session['user_name'] = user.name
                request.session['user_nickname'] = user.nickname
                request.session['user_email'] = user.email
                request.session['user_sex'] = user.get_sex_display()
                request.session['user_institute'] = user.get_institute_display()
                request.session['user_major'] = user.major
                request.session['user_fans'] = user.fans
                request.session['user_photo_url'] = user.photo_clipped.url
                return redirect('/login/index/')
            else:
                message = '密码不正确！'
                return render(request, 'login/login.html', locals())
        else:
            return render(request, 'login/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/login/index/')

    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            sno = register_form.cleaned_data.get('sno')
            name = register_form.cleaned_data.get('name')
            nickname = register_form.cleaned_data.get('nickname')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')
            institute = register_form.cleaned_data.get('institute')
            major = register_form.cleaned_data.get('major')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=sno)
                if same_name_user:
                    message = '用户名已经存在'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'login/register.html', locals())

                new_user = models.User()
                new_user.sno = sno
                new_user.name = name
                new_user.nickname = nickname
                new_user.password = password1
                new_user.email = email
                new_user.sex = sex
                new_user.institute = institute
                new_user.major = major
                new_user.save()

                return redirect('/login/login/')
        else:
            return render(request, 'login/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    request.session.flush()
    return redirect("/login/login/")


def about(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    sign_nick = False
    sign_email = False
    sign_photo = False
    return render(request, 'login/about.html',
                  {'sign_nick': sign_nick, 'sign_email': sign_email, 'sign_photo': sign_photo})


def editpwd(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    user = models.User.objects.get(sno=request.session['user_sno'])
    pwd0 = request.POST.get('pwd0')
    pwd1 = request.POST.get('pwd1')
    pwd2 = request.POST.get('pwd2')
    message = ""

    if pwd0 and pwd0 != user.password:
        message = "修改失败！原密码输入有误！"
        return render(request, 'login/about.html', {'message': message})
    if pwd1 == pwd2 and pwd1:
        user.password = pwd1
        user.save()
        return redirect("/about/")
    else:
        message = "修改失败！两次输入的密码不同，请重新输入！"
        return render(request, 'login/about.html', {'message': message})


def editnickname(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    nickname = request.POST.get('nickname')
    if nickname:
        user = models.User.objects.get(sno=request.session['user_sno'])
        user.nickname = nickname
        user.save()
        request.session['user_nickname'] = user.nickname
        return redirect("/about/")
    else:
        sign = True
        return render(request, 'login/about.html', {'sign_nick': sign})


def editemail(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    email = request.POST.get('email')
    users = models.User.objects.all()
    message = ""

    if not email:
        sign = True
        return render(request, 'login/about.html', {'sign_email': sign, "message": message})
    for user in users:
        if email == user.email:
            message = "该邮箱已被注册！"
            sign = True
            return render(request, 'login/about.html', {'sign_email': sign, "message": message})
    user = models.User.objects.get(sno=request.session['user_sno'])
    user.email = email
    user.save()
    request.session['user_email'] = user.email
    return redirect("/about/")


def editphoto(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        if photo:
            user = models.User.objects.get(sno=request.session['user_sno'])
            user.photo = photo
            user.save()
            request.session['user_photo_url'] = user.photo_clipped.url
            return redirect("/about/")
        else:
            sign = True
            return render(request, 'login/about.html', {'sign_photo': sign})


def info(request, sno):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    user1 = models.User.objects.get(sno=request.session['user_sno'])
    user2 = models.User.objects.get(sno=sno)
    if user1.sno == user2.sno:
        sign1 = False
    else:
        sign1 = True
    if user1.sno != user2.sno and user2 in user1.follow.all():
        sign2 = True
    else:
        sign2 = False
    return render(request, 'login/info.html', {'user': user2, 'sign1': sign1, 'sign2': sign2})


def likes(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    user = models.User.objects.get(sno=request.session['user_sno'])
    likes_list = user.like_users.order_by('-create_time')
    paginator = Paginator(likes_list, 10)
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
    return render(request, 'login/likes.html', {'posts': posts, "length": len(likes_list)})


def posts(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    user = models.User.objects.get(sno=request.session['user_sno'])
    posts_list = user.author.order_by('-create_time')
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
    return render(request, 'login/posts.html', {'posts': posts, "length": len(posts_list)})


def comments(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    user = models.User.objects.get(sno=request.session['user_sno'])
    comments_list = user.comments.order_by('-created')
    paginator = Paginator(comments_list, 10)
    if request.method == "GET":
        page = request.GET.get('page')
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except InvalidPage:
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
    else:
        comments = paginator.page(1)
    return render(request, 'login/comments.html', {'comments': comments, "length": len(comments_list)})


def send(request, sno):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    sender = models.User.objects.get(sno=request.session['user_sno'])
    receiver = models.User.objects.get(sno=sno)
    title = request.POST.get('title')
    content = request.POST.get('content')
    Message.objects.create(title=title, content=content, sender=sender, receiver=receiver)
    return info(request, sno)


def mailbox(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    user = models.User.objects.get(sno=request.session['user_sno'])
    messages_list = Message.objects.filter(receiver=user).order_by('-created')
    paginator = Paginator(messages_list, 10)
    if request.method == "GET":
        page = request.GET.get('page')
        try:
            messages = paginator.page(page)
        except PageNotAnInteger:
            messages = paginator.page(1)
        except InvalidPage:
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            messages = paginator.page(paginator.num_pages)
    else:
        messages = paginator.page(1)
    return render(request, 'login/mailbox.html', {'messages': messages, "length": len(messages_list)})


def follow(request, sno):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    user = models.User.objects.get(sno=request.session['user_sno'])
    followed_user = models.User.objects.get(sno=sno)
    sign1 = True
    message1 = ""
    if followed_user not in user.follow.all():
        followed_user.fans += 1
        followed_user.save()
        user.follow.add(followed_user)
        user.save()
    else:
        message1 = "您已经关注过TA了"
    sign2 = True
    ctx = {'user': followed_user, 'message1': message1, 'sign1': sign1, 'sign2': sign2}
    return render(request, 'login/info.html', ctx)


def follow_cancel(request, sno):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    user = models.User.objects.get(sno=request.session['user_sno'])
    followed_user = models.User.objects.get(sno=sno)
    message1 = ""
    followed_user.fans -= 1
    followed_user.save()
    user.follow.remove(followed_user)
    user.save()
    sign2 = False
    sign1 = True
    ctx = {'user': followed_user, 'message1': message1, 'sign1': sign1, 'sign2': sign2}
    return render(request, 'login/info.html', ctx)


def follows(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    user = models.User.objects.get(sno=request.session['user_sno'])
    follow_list = user.follow.order_by('-fans')
    paginator = Paginator(follow_list, 10)
    if request.method == "GET":
        page = request.GET.get('page')
        try:
            follow_set = paginator.page(page)
        except PageNotAnInteger:
            follow_set = paginator.page(1)
        except InvalidPage:
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            follow_set = paginator.page(paginator.num_pages)
    else:
        follow_set = paginator.page(1)
    return render(request, 'login/follows.html', {'follow_set': follow_set, "length": len(follow_list)})


def posts_ta(request, sno):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    user = models.User.objects.get(sno=sno)
    posts_list = user.author.order_by('-create_time')
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
    return render(request, 'login/posts_ta.html', {'user': user, 'posts': posts, "length": len(posts_list)})


def followers(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    me = models.User.objects.get(sno=request.session['user_sno'])
    follower_list = []
    users = models.User.objects.all()
    for user in users:
        follow_list = user.follow.order_by('-fans')
        if me in follow_list:
            follower_list.append(user)

    paginator = Paginator(follower_list, 10)
    if request.method == "GET":
        page = request.GET.get('page')
        try:
            follower_set = paginator.page(page)
        except PageNotAnInteger:
            follower_set = paginator.page(1)
        except InvalidPage:
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            follower_set = paginator.page(paginator.num_pages)
    else:
        follower_set = paginator.page(1)
    return render(request, 'login/followers.html', {'follower_set': follower_set, "length": len(follower_list)})
