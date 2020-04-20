from django import forms
from . import models

CATEGORY = models.Category.objects.all()
TAG = models.Tag.objects.all()


class PostForm(forms.Form):
    title = forms.CharField(label="题目", required=True, max_length=50)
    content = forms.CharField(label="内容", widget=forms.Textarea())
    category = forms.ModelChoiceField(label="类别", queryset=CATEGORY, empty_label='请选择分类')
    tag = forms.ModelChoiceField(label="标签", queryset=TAG)


class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.widgets.TextInput())
    reply_comment_id = forms.IntegerField()

    def clean_reply_comment_id(self):
        reply_comment_id = self.cleaned_data['reply_comment_id']
        if reply_comment_id < 0:
            raise forms.ValidationError('回复出错')
        elif reply_comment_id == 0:
            self.cleaned_data['parent'] = None
        elif models.Comment.objects.filter(pk=reply_comment_id).exists():
            self.cleaned_data['parent'] = models.Comment.objects.get(pk=reply_comment_id)
        else:
            raise forms.ValidationError('回复出错')
        return reply_comment_id



