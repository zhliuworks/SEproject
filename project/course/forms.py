from django import forms
from . import models

COURSE = models.Course.objects.all()

class UploadForm(forms.Form):
    title = forms.CharField(label="题目", required=True, max_length=50)
    course = forms.ModelChoiceField(label="课程", queryset=COURSE, empty_label='请选择课程')
    introduction = forms.CharField(label="简介", widget=forms.Textarea(), max_length=256)
    file = forms.FileField(label="文件")
