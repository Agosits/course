from django.contrib import admin

# Register your models here.
from .models import Course,Student,Grade,Teacher,Major

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Grade)
admin.site.register(Teacher)
admin.site.register(Major)