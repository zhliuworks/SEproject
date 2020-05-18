from haystack import indexes
from .models import Course, Teacher, File


class CourseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Course

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class TeacherIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Teacher

    def index_queryset(self, using=None):
        return self.get_model().objects.all()


class FileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return File

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
