from django.db import models


class User(models.Model):
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

    id = models.CharField(max_length=128, unique=True, primary_key=True)  # 学号
    name = models.CharField(max_length=128)  # 名字
    nickname = models.CharField(max_length=128, default='--')  # 昵称
    password = models.CharField(max_length=256)  # 密码
    email = models.EmailField(unique=True)  # 邮箱
    sex = models.CharField(max_length=32, choices=gender)  # 性别（选择）
    institute = models.CharField(max_length=256, choices=school)  # 学院（选择）
    major = models.CharField(max_length=256, default='--')  # 专业（暂时为填写）
    c_time = models.DateTimeField(auto_now_add=True)  # 注册时间

    def __str__(self):
        return self.id

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"
