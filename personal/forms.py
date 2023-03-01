from django import forms


class DateInput(forms.DateInput):
    input_type = 'date'
    attrs = {
                'class': "form-control validate", 
                'style': 'max-width: 300px;',
                'placeholder': 'Enter date'
                }

class ScanFrom(forms.Form):
    date = forms.DateField(label="Scan date", widget=DateInput)

    position = forms.ChoiceField(label ="Position" ,choices=[('backend_developer',"Backend Developer"),('project_manager','Project Manager'),('designer','Designer')])