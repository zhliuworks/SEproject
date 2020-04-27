from django.contrib import admin
from . import models

admin.site.register(models.Course)
admin.site.register(models.Teacher)
admin.site.register(models.File)
