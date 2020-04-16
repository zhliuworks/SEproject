from django.db import models


class Course(models.Model):
    cno = models.CharField(max_length=128, unique=True, primary_key=True)  # 课号
    name = models.CharField(max_length=128)  # 课程名
    credit = models.IntegerField(default=0)  # 学分
    outline = models.CharField(max_length=2048, default='略')  # 授课大纲
    references = models.CharField(max_length=1024, default='略')  # 教材与参考资料
    mean_score = models.FloatField(default=0)  # 平均分
    fail_rate = models.FloatField(default=0)  # 挂科率

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-cno"]
        verbose_name = "课程"
        verbose_name_plural = "课程"


class Teacher(models.Model):
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

    tno = models.CharField(max_length=128, unique=True, primary_key=True)  # 职工号
    name = models.CharField(max_length=128)  # 名字
    title = models.CharField(max_length=128)  # 职称
    email = models.EmailField(unique=True)  # 邮箱
    sex = models.CharField(max_length=32, choices=gender)  # 性别（选择）
    institute = models.CharField(max_length=256, choices=school)  # 学院（选择）
    department = models.CharField(max_length=256, default='--')  # 系（暂时为填写）
    address = models.CharField(max_length=256, default='--')  # 办公室地点
    resume = models.CharField(max_length=2048, default='略')  # 简历

    course = models.ManyToManyField(Course, verbose_name='课程')  # 教授课程

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-tno"]
        verbose_name = "教师"
        verbose_name_plural = "教师"
