from django.shortcuts import render, redirect
from django.http import FileResponse
from django.utils.encoding import escape_uri_path
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from .models import Course, Teacher, File
from .forms import UploadForm
from login.models import User


def index(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    user = User.objects.get(sno=request.session['user_sno'])
    course_list = Course.objects.order_by('cno')
    teacher_list = Teacher.objects.order_by("tno")
    file_set = File.objects.order_by("-create_time")

    pag_file = Paginator(file_set, 8)
    if request.method == "GET":
        page = request.GET.get('page')
        try:
            file_list = pag_file.page(page)
        except PageNotAnInteger:
            file_list = pag_file.page(1)
        except InvalidPage:
            return HttpResponse('找不到页面的内容')
        except EmptyPage:
            file_list = pag_file.page(pag_file.num_pages)
    else:
        file_list = pag_file.page(1)

    ctx = {'user': user, 'course_list': course_list, 'teacher_list': teacher_list, 'file_list': file_list}
    return render(request, 'index.html', ctx)


def course_detail(request, course_cno):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    course = Course.objects.get(pk=course_cno)
    ctx = {
        'course': course,
        'teachers': course.teacher_set.all()
    }
    return render(request, 'courses/detail.html', ctx)


def teacher_detail(request, teacher_tno):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    teacher = Teacher.objects.get(pk=teacher_tno)
    ctx = {
        'teacher': teacher,
        'courses': teacher.course.all()
    }
    return render(request, 'teachers/detail.html', ctx)


def upload_file(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    upload_form = UploadForm()
    message = ""
    return render(request, 'upload_file.html', locals())


def upload_file_action(request):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    if request.method == 'POST':
        upload_form = UploadForm(request.POST, request.FILES)
        if upload_form.is_valid():
            title = upload_form.cleaned_data.get('title')
            course = upload_form.cleaned_data.get('course')
            introduction = upload_form.cleaned_data.get('introduction')
            file = upload_form.cleaned_data.get('file')
            user = User.objects.get(sno=request.session['user_sno'])
            File.objects.create(title=title, course=course, user=user, introduction=introduction, file=file)
            return redirect(r"/course/")
    message = '文件上传失败！'
    return render(request, 'upload_file.html', {'message': message})


def download_file(request, file_id):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    file = File.objects.get(id=file_id)
    file.downloads += 1
    file.save()
    response =FileResponse(open('./upload/'+str(file.file),'rb') )
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="{0}"'.format(escape_uri_path(str(file.file)))
    return response


def like_file(request, file_id):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    file = File.objects.get(id=file_id)
    user = User.objects.get(sno=request.session['user_sno'])
    if user not in file.like_users.all():
        file.likes += 1
        file.like_users.add(user)
        file.save()
    return redirect("/course/")


def delete_file(request, file_id):
    if not request.session.get('is_login', None):
        return redirect("/login/login/")
    file = File.objects.get(id=file_id)
    file.delete()
    return redirect("/course/")
