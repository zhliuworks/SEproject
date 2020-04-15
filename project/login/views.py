from django.shortcuts import render
from django.shortcuts import redirect
from . import forms, models


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
