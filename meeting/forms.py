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
        exclude = ('id', "attachment", "draft", "minutes_of_meeting", 'done', 'scheduled_by')
