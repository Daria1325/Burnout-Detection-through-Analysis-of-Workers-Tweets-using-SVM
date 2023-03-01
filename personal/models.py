from django.db import models

from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver


def upload_location(instance,filename):
    file_path ='avatar/{employee_id}'.format(
        employee_id = str(instance.employee_id)
    )
    return file_path

class States(models.Model):
    state_id =models.CharField(max_length=10,null=False,blank=False, primary_key=True)
    note = models.CharField(max_length=50,null=False,blank=False)
    status =models.CharField(max_length=10,null=False,blank=False)
    progress =models.CharField(max_length=10,null=False,blank=False)

    def __str__(self):
        return self.note

class Employees(models.Model):
    employee_id = models.CharField(max_length=10,null=False,blank=False, primary_key=True)
    name = models.CharField(max_length=30,null=False,blank=False)
    sex =models.CharField(max_length=1,null=False,blank=False)
    birth_date = models.DateField(verbose_name="birth date")
    join_date = models.DateField(verbose_name="join date")
    position =models.CharField(max_length=30,null=False,blank=False)
    avatar = models.ImageField(upload_location=upload_location, null=True)
    state_id = models.ForeignKey(States, blank=True)

    def __str__(self):
        return self.name

class Usernames(models.Model):
    employee_id =models.ForeignKey(Employees, on_delete=models.CASCADE, primary_key=True)
    username =models.CharField(max_length=30,null=True)

    def __str__(self):
        return self.username


    
class Results(models.Model):
    employee_id =models.ForeignKey(Employees, on_delete=models.CASCADE, primary_key=True)
    scan_date = models.DateField(auto_now_add=True, verbose_name="scan date", primary_key=True)
    percent_N = models.FloatField()
    percent_S =models.FloatField()
    percent_L=models.FloatField()
    count_N = models.IntegerField()
    count_S =models.IntegerField()
    count_L =models.IntegerField()