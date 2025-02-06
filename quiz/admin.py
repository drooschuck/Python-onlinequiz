from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Course, Question

class CourseResource(resources.ModelResource):
    class Meta:
        model = Course

class QuestionResource(resources.ModelResource):
    class Meta:
        model = Question

@admin.register(Course)
class CourseAdmin(ImportExportModelAdmin):
    pass

@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin):
    pass

