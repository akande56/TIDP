from django import forms
from django.core.exceptions import ValidationError
from accounts.models import Account, UserPersona ,Contractors,ContractorDocument
from .models import Precurement, Procurement_tender_doc


Tender = (
    ('open tender', 'open tender'),
    ('selective tender', 'selective tender'),
    ('direct labour', 'direct labour')
)
Priority = (
   ('HIGHEST', 'HIGHEST'),
    ('MEDIUM', 'MEDIUM'),
    ('LOW', 'LOW'),
    ('LOWEST', 'LOWEST')
)

class ContractorFormSignUp(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'placeholder': 'haroun@gmail.com'}))
    full_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Full Name'}))
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Username'}))
    company_name = forms.CharField(required=True, widget=forms.TextInput())
    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={'placeholder': 'Strong Password'}))
    category_choices = [
        ('Software', 'Software'),
        ('Telecommunication', 'Telecommunication'),
        ('Construction', 'Construction'),
        ('Others', 'Others'),
    ]
    category = forms.ChoiceField(choices=category_choices)


class PrecurmentCreateForm(forms.ModelForm):
        
    class Meta:
        model = Precurement
        fields = '__all__'

    title = forms.CharField(max_length=20, required=True, widget=forms.TextInput(
        attrs={'placeholder': 'Project Name'}
    ))
    category_choices = [
        ('Software', 'Software'),
        ('Telecommunication', 'Telecommunication'),
        ('Construction', 'Construction'),
        ('Others', 'Others'),
    ]
    category = forms.ChoiceField(choices=category_choices)
    responsibilty = forms.CharField(max_length=20, required=True, 
    widget=forms.TextInput(
        attrs={'placeholder': 'Role in Project'}
    ))
    contractors = forms.ModelMultipleChoiceField(
        queryset=Contractors.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    tender_type = forms.ChoiceField(choices=Tender)
    description = forms.CharField(max_length=40, required=True, 
    widget=forms.Textarea(
        attrs={'placeholder': 'Project details'}
    ))
    budget = forms.CharField(max_length=20)
    priority = forms.ChoiceField(choices=Priority)
    project_file = forms.ImageField(required=False)
    

class PrecurmentEditForm(forms.ModelForm):
    class Meta:
        model = Precurement
        exclude = ['tender_type']  
    

    
class ContractorDocumentForm(forms.ModelForm):
    class Meta:
        model = ContractorDocument
        fields = ['title', 'file']

    def clean(self):
        cleaned_data = super().clean()
        # file = cleaned_data.get('file')

        # Add custom validation for the file field if needed
        # For example, you can check the file size or format here

        return cleaned_data



class TenderDocumentForm(forms.ModelForm):
    class Meta:
        model = Procurement_tender_doc
        fields = ['file']

    file = forms.ImageField(label='Tender Document', required=True)