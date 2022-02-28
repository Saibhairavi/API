from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display=['id','name','rollno','marks','gm','gf']
# Register your models here.
admin.site.register(Student,StudentAdmin)


# admin.site.register(Student)