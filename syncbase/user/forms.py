from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django import forms

class NewAccountForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):
        pwd = self.cleaned_data.get('password')

        if not pwd:
            raise forms.ValidationError("You must enter a password")
        validate_password(pwd)
        return pwd


    def clean_confirm_password(self):
        pwd1 = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('confirm_password')

        if not pwd2:
            raise forms.ValidationError("You must confirm your password")
        if pwd1 != pwd2:
            raise forms.ValidationError("Your passwords do not match")
        return pwd2

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput,
            'password_confirm': forms.PasswordInput
        }
