from django import forms
from accounts.models import Account, UserPersona 
from home.models import Unit

class CreatePersonaForm(forms.ModelForm):
    
    class Meta:
        model = UserPersona
        fields = ('name', 'description', 'persona_tier')


class UnitForm(forms.ModelForm):
    
    class Meta:
        model = Unit
        fields = ('name', 'unit_type')


class AddUsertoUnit(forms.Form):

    staff = forms.ModelChoiceField(
        required=True,
        queryset=Account.objects.all(),
        )