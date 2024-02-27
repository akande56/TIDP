from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from accounts.models import Account, UserPersona, Contractors


class BusinessInfoForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter Full Name'}))
    address = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'haroun@gmail.com'}))
    business_profile = forms.FileField()


class UserRegistrationForm(forms.Form):
    full_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter Full Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'haroun@gmail.com'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Strong Password'}))
    password_ = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Strong Password'}))



class UserLoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter Staff ID', 'class': 'text'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password', 'class': 'text'}))



class CreateUserrForm(forms.Form):
    users = forms.ModelChoiceField(
        required=True,
        queryset=Account.objects.all(),
        )


class CreateUserForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter Staff ID', 'class': 'text'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password', 'class': 'text'}))
    fullname = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter Full Name', 'class': 'text'}))
    persona = forms.ModelChoiceField(
        required=True,
        queryset=UserPersona.objects.all(),
        )



class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User  # Your user model


# class CustomPasswordResetForm(forms.Form):
#     username = forms.CharField(max_length=150, required=True)
#     new_password = forms.CharField(widget=forms.PasswordInput, required=True)


class SignatureForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['signature']