from django import forms
from django.forms import DateInput
from datetime import date as dt



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
    position = forms.ChoiceField(
        label ="Position" ,
        choices=[('backend_developer',"Backend Developer"),('project_manager','Project Manager'),('designer','Designer')],
        widget=forms.Select(attrs={
            'class': 'form-control validate',
            'style': 'max-width: 300px;'
        })
        )