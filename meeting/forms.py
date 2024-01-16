from django import forms
from .models import Schedule_Meeting
from ckeditor.widgets import CKEditorWidget


class NotesForm(forms.Form):
    content = forms.CharField(required=True, widget=CKEditorWidget())


class SetUpMeetingFor(forms.ModelForm):
        
     class Meta:
        model = Schedule_Meeting
        fields = ('paticipants', 'venue', 'title')


class NewMeetingForm(forms.ModelForm):
    class Meta:
        model = Schedule_Meeting
        exclude = ('id', 'draft', 'minutes_of_meeting', 'done', 'scheduled_by', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['attachment'].required = False