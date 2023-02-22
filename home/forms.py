from django import forms
from accounts.models import Account, Application
from home.models import Unit

class ApplicantForm(forms.ModelForm):
    
    class Meta:
        model = Unit
        fields = ('name', 'unit_type')


class UnitForm(forms.ModelForm):
    
    class Meta:
        model = Unit
        fields = ('name', 'unit_type')


class AddUsertoUnit(forms.Form):

    staff = forms.ModelChoiceField(
        required=True,
        queryset=Account.objects.all(),
        )

