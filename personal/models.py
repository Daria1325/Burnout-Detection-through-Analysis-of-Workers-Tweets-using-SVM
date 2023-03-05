from django.db import models

from django.db.models.signals import post_delete
from django.dispatch import receiver


def upload_location(instance,filename, **kwargs):
    file_path ='avatar/{employee_id}/{filename}'.format(
        employee_id = str(instance.employee_id), filename = filename
    )
    return file_path



class State(models.Model):
    STATUS_OPTIONS = (('L','Low'), ('M','Moderate'), ('H','High'),('N','No data'))
    PROGRESS_OPTIONS = (('I','Improved'), ('S','Stable'), ('W','Worsened'))

    state_id =models.AutoField(primary_key=True)
    note = models.CharField(max_length=50,null=False,blank=False)
    status =models.CharField(max_length=10,choices=STATUS_OPTIONS)
    progress =models.CharField(max_length=10,choices=PROGRESS_OPTIONS)

    def __str__(self):
        return self.note

class Employee(models.Model):
    SEX_OPTIONS = (('M','Male'), ('F','Female'), ('O','Other'))

    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,null=False,blank=False)
    sex =models.CharField(max_length=1, choices=SEX_OPTIONS)
    birth_date = models.DateField(verbose_name="birth date")
    join_date = models.DateField(verbose_name="join date")
    position =models.CharField(max_length=30,null=False,blank=False)
    avatar = models.ImageField(upload_to=upload_location, null=True)
    email = models.EmailField(null=False, blank=True)
    state_id = models.ForeignKey(State, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

@receiver(post_delete, sender = Employee)
def submition_delete(sender, instance, **kwargs):
    instance.avatar.delete(False)


class Username(models.Model):
    employee_id =models.ForeignKey(Employee, on_delete=models.CASCADE, primary_key=True)
    username =models.CharField(max_length=30,null=True)

    def __str__(self):
        return self.username


    
class Result(models.Model):
    employee_id =models.ForeignKey(Employee, on_delete=models.CASCADE)
    scan_date = models.DateField(verbose_name="scan date")
    percent_N = models.FloatField()
    percent_S =models.FloatField()
    percent_L=models.FloatField()
    count_N = models.IntegerField()
    count_S =models.IntegerField()
    count_L =models.IntegerField()

    class Meta:
        unique_together = (("employee_id", "scan_date"),)