from django import forms
from django.forms import EmailInput,PasswordInput
from django.contrib.auth import authenticate


from account.models import Account


class AccountAuthenticationForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('email', 'password')
		widgets = {
			'email': EmailInput(attrs={
                'class': "form-control form-control-lg", 
                'style': 'max-width: 300px;',
                'placeholder': 'Email'
                }),
			'password': PasswordInput(attrs={
				'class': "form-control form-control-lg", 
                'style': 'max-width: 300px;',
                'placeholder': 'Password'
			}
			)

		}

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login or password")