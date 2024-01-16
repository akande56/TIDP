from dataclasses import field
from django import forms
from .models import File, Folder, File
from home.models import Unit
from accounts.models import Account
from ckeditor.widgets import CKEditorWidget

class InternalMemoForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=CKEditorWidget())
    send_to = forms.ModelChoiceField(required=True, queryset=Unit.objects.all())
    
    class Meta:
        model = Folder
        fields = ('title', 'urgent')

    '''
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(InternalMemoForm, self).__init__(*args, **kwargs)
        self.fields['send_to'].queryset = Account.objects.filter()
    '''

class MinuteOnMemoForm(forms.Form):
    content = forms.CharField(required=True, widget=CKEditorWidget())
    


class UnitForm(forms.ModelForm):
    
    class Meta:
        model = Unit
        fields = ('name', 'unit_type')


class AddUsertoUnit(forms.Form):

    staff = forms.ModelChoiceField(
        required=True,
        queryset=Account.objects.all(),
        )

'''
class AddUsertoUnit(forms.ModelForm):
    class Meta:
        model = Routing
        fields = ('send_to',)
'''

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('media',)


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    #parent_id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': "Comment",  'rows':"4", "cols": "4", "class": 'form-control'}
    ))