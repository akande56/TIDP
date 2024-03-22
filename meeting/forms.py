from django import forms
from .models import Schedule_Meeting, Agenda
from ckeditor.widgets import CKEditorWidget
from crispy_forms.helper import FormHelper


class NotesForm(forms.Form):
    content = forms.CharField(required=True, widget=CKEditorWidget())


class SetUpMeetingFor(forms.ModelForm):
        
     class Meta:
        model = Schedule_Meeting
        fields = ('paticipants', 'venue', 'title')


# class NewMeetingForm(forms.ModelForm):
#     class Meta:
#         model = Schedule_Meeting
#         exclude = ('id', 'draft', 'minutes_of_meeting', 'done', 'scheduled_by', 'status')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['attachment'].required = False


class ScheduleMeetingForm(forms.ModelForm):
    class Meta:
        model = Schedule_Meeting
        fields = ['title', 'start_on', 'end_on', 'start_time', 'end_time', 'paticipants', 'venue', 'description', 'draft', 'minutes_of_meeting', 'done', 'scheduled_by', 'attachment', 'address', 'link', 'status']
        widgets = {
            'participants': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'minutes_of_meeting': forms.Textarea(attrs={'class': 'form-control'}),
            # 'attachment': forms.ClearableFileInput(),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'link': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ['agenda', 'minutes']
        widgets = {
            'agenda': forms.TextInput(attrs={'class': 'form-control'}),
            'minutes': forms.TimeInput(attrs={'class': 'form-control'}),
        }

AgendaFormset = forms.inlineformset_factory(
    Schedule_Meeting,
    Agenda,
    form=AgendaForm,
    extra=1,
    can_delete=True
)