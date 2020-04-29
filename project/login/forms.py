from django import forms
from captcha.fields import CaptchaField


class UserForm(forms.Form):
    sno = forms.CharField(label="学号", max_length=128, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Student ID", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))
    captcha = CaptchaField(label='验证码')


class RegisterForm(forms.Form):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    school = (
        ('chuan_jian', "船舶海洋与建筑工程学院"),
        ('ji_dong', "机械动力与工程学院"),
        ('dian_yuan', "电子信息与电气工程学院"),
        ('cai_liao', "材料科学与工程学院"),
        ('shu_xue', "数学科学学院"),
        ('wu_li', "物理与天文学院"),
        ('hua_xue', "化学化工学院"),
        ('sheng_ming', "生命科学技术学院"),
        ('sheng_yi_gong', "生物医学工程学院"),
        ('an_tai', "安泰经济与管理学院"),
        ('qi_ta', "其它"),  # 暂时写到这儿
    )

    sno = forms.CharField(label="学号", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label="名字", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    nickname = forms.CharField(label="昵称", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    sex = forms.ChoiceField(label="性别", choices=gender)
    institute = forms.ChoiceField(label="学院", choices=school)
    major = forms.CharField(label="专业", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label="验证码")
