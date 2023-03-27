from django import forms
from django.forms import DateInput
from datetime import date as dt
from personal.models import Employee



class ScanFrom(forms.Form):
    date = forms.DateField(
        initial=dt.today(),
        label="Scan date",
        widget=forms.DateInput(attrs={
            'type':'date',
            'class': 'form-control validate',
            'style': 'max-width: 300px;',
            'placeholder': 'Enter date',
            'max': dt.today()
        }))
    
    positionsFromModel = list(set(Employee.objects.all().values_list('position', flat=True)))
    position_choices = [("All","All")]
    for position in positionsFromModel:
        position_choices.append((position,position))

    position = forms.ChoiceField(
        label ="Position" ,
        choices=position_choices,
        widget=forms.Select(attrs={
            'class': 'form-control validate',
            'style': 'max-width: 300px;'
        })
        )