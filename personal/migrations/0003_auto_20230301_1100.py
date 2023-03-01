# Generated by Django 3.2.17 on 2023-03-01 09:00

from django.db import migrations

def fill_states(apps, schema_editor):
    State = apps.get_model('personal', 'State')

    #Low
    State.objects.create(status="Low", progress = "Stable", note = "Employee stable in LOW risk.")
    State.objects.create(status="Low", note = "Employee is in LOW risk.")
    State.objects.create(status="Low", progress = "Improved", note = "Employee's status improved. LOW risk.")

    #Moderate
    State.objects.create(status="Moderate", note = "Employee in MODERATE risk.")
    State.objects.create(status="Moderate", progress = "Stable", note = "Employee stable in MODERATE risk.")
    State.objects.create(status="Moderate", progress = "Improved", note = "Employee's status improved. MODERATE risk.")
    State.objects.create(status="Moderate", progress = "Worsened", note = "Employee's status worsened. MODERATE risk.")

    #High
    State.objects.create(status="High", progress = "Stable", note = "Employee HIGH risk two times in a row.")
    State.objects.create(status="High", note = "Employee is in HIGH risk.")
    State.objects.create(status="High", progress = "Worsened", note = "Employee's status worsened. HIGH risk.")

    State.objects.create(status="No data", note = "No data")


def fill_employees(apps, schema_editor):
    Employee = apps.get_model('personal', 'Employee')
    Username = apps.get_model('personal', 'Username')

    emp = Employee.objects.create(name="Ludwig Ahgren", sex="M", birth_date="1990-04-06", join_date="2023-03-06", position="Project Manager")
    Username.objects.create(employee_id=emp, username = "LudwigAhgren")
    
    emp = Employee.objects.create(name="Andrii Gordon", sex="M", birth_date="2000-03-06", join_date="2022-05-06", position="Designer")
    Username.objects.create(employee_id=emp, username = "kawaiicryptidx")
    
    emp = Employee.objects.create(name="Alice Robin", sex="F", birth_date="2001-03-22", join_date="2020-07-09", position="Backend Developer")
    Username.objects.create(employee_id=emp, username = "starsalts")
    
    
    emp = Employee.objects.create(name="Tadeusz Giczan", sex="M", birth_date="2003-12-06", join_date="2015-04-06", position="Backend Developer")
    Username.objects.create(employee_id=emp, username = "TadeuszGiczan")
    
    emp = Employee.objects.create(name="Amy Amira", sex="F", birth_date="1998-07-10", join_date="2022-06-06", position="Designer")
    Username.objects.create(employee_id=emp, username = "amiraamou")
    
    emp = Employee.objects.create(name="Sandra Owh", sex="F", birth_date="2000-08-10", join_date="2021-03-06", position="Designer")
    Username.objects.create(employee_id=emp, username = "LikjKat87")
    
    emp = Employee.objects.create(name="Cooper Burbank", sex="M", birth_date="1998-02-10", join_date="2019-03-06", position="Project Manager")
    Username.objects.create(employee_id=emp, username = "coopeydough")


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0002_auto_20230301_1100'),
    ]

    operations = [
        migrations.RunPython(fill_states),
        migrations.RunPython(fill_employees),
    ]

