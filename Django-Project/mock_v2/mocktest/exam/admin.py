from django.contrib import admin

from .models import Course, Student, Result

# Register your models here.
# admin.site.register(Exam),
admin.site.register((Course, Student, Result))
