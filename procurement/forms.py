from django import forms
from accounts.models import Account, UserPersona 


class ContractorFormSignUp(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'haroun@gmail.com'}))
    full_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Full Name'}))
    company_name = forms.CharField(required=True, widget=forms.TextInput())
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Strong Password'}))
    