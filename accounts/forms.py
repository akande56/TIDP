from django import forms

from accounts.models import Account, ApplicantFiles, Institutions, ApplicationType


class ApplicantApplicationForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter Full Name'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(
        attrs={'placeholder': ' Email Address'}))
    certification = forms.FileField()


class SettingsForm(forms.ModelForm):

    class Meta:
            model = Institutions
            fields = ('name', "address", 'logo')


class ApplicantTypeForm(forms.ModelForm):

    class Meta:
            model = ApplicationType
            fields = ('name', "category", 'fee', "template")


    
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
    


class ApplicantFormSignUp(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'haroun@gmail.com'}))
    full_name = forms.CharField(required=False, widget=forms.TextInput(
        ))
    address = forms.CharField(required=False, widget=forms.TextInput(
        ))
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Strong Password'}))
    key = forms.CharField(required=False, widget=forms.HiddenInput(
        attrs={'placeholder': 'Strong Password'}))
    business_profile = forms.FileField(required=False)


class AdditionalDocumentForm(forms.ModelForm):
    class Meta:
        model = ApplicantFiles
        fields = ('document',)


