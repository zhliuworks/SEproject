from django import forms
from . import models

CATEGORY = models.Category.objects.all()
TAG = models.Tag.objects.all()


class PostForm(forms.Form):
    title = forms.CharField(label="题目", required=True, max_length=50)
    content = forms.CharField(label="内容", widget=forms.Textarea())
    category = forms.ModelChoiceField(label="类别", queryset=CATEGORY, empty_label='请选择分类')
    tag = forms.ModelChoiceField(label="标签", queryset=TAG)