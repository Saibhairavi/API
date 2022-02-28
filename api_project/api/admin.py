from django.contrib import admin
from .models import Employee
# Register your models here.

#after creating a Employee db model in models.py register here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display=['id','eno','ename','esal','eaddr']

admin.site.register(Employee,EmployeeAdmin)
#register both the classes
