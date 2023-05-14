from django import forms



class PlaygroundFrom(forms.Form):
    text = forms.CharField( 
        label="Enter text to analize",
        widget=forms.Textarea(attrs={
            'class': 'col-12'
        })
        )