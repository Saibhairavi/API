from django.db import models

# Create your models here.

# Employee table in db with columns eno,ename,esal,eaddr
class Employee(models.Model):
    eno=models.IntegerField()
    ename=models.CharField(max_length=100)
    esal=models.FloatField()
    eaddr=models.CharField(max_length=100)

    def __str__(self):
        return self.ename
