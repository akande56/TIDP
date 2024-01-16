from django.forms import modelformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest
from .models import Schedule_Meeting
from .forms import NotesForm, SetUpMeetingFor, NewMeetingForm
from django.contrib import messages
# Create your views here.
from accounts.models import Account

class Meeting(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        meetings = Schedule_Meeting.objects.all()
        form = NewMeetingForm()
        
        context = {
            'form': form,
            "meetings": meetings
        }
        return render(request, "new/meeting.html", context)

    def post(self, request, **kwargs):
        form = NewMeetingForm(request.POST, request.FILES)
        
        if form.is_valid():
            my_account = Account.objects.get(user=request.user)
            instance = form.save(commit=False)
            instance.scheduled_by = my_account
            print (form.errors)
            meeting_attachmment = self.request.FILES.get('attachment')
            if not meeting_attachmment:
                return HttpResponseBadRequest('No file provided.')

            # Additional validation if needed, e.g., check if it's an image
            if not meeting_attachmment.content_type.startswith('image'):
                return HttpResponseBadRequest('Invalid file type. Please upload an image.')

            instance.attachment = meeting_attachmment
            instance.save()
            messages.success(request, 'Meeting Created Sucessfully')
        return redirect('meeting')


class MeetingDetails(LoginRequiredMixin, View):

    def get(self, request, id, **kwargs):
        meeting = Schedule_Meeting.objects.get(id=id)
        form = NotesForm()
        form_setting = SetUpMeetingFor()
        context = {
            "meeting": meeting,
            'form_setting': form_setting,
            'form': form
        }
        return render(request, "meeting_details.html", context)


    def post(self, request, id, **kwargs):
        meeting = Schedule_Meeting.objects.get(id=id)
        form = NotesForm(request.POST)
        setting_form = SetUpMeetingFor(request.POST, request.FILES)

        if form.is_valid():
            meeting.notes = form.cleaned_data["content"]
            meeting.done = True
            meeting.save()
            messages.success(request, 'Noted Saved SUccessfully')
        
        if setting_form.is_valid():
            meeting = Schedule_Meeting.objects.get(id=id)
            print (setting_form.cleaned_data["paticipants"])
            for paticipant in setting_form.cleaned_data["paticipants"]:
                
                meeting.paticipants.add(paticipant)
            meeting.venue = setting_form.cleaned_data["venue"]
            meeting.title = setting_form.cleaned_data["title"]
            meeting.scheduled = True
            meeting.save()
            messages.success(request, 'Metting Scheduled Successfully')
        
        return redirect('meeting_details', id=id)



class UpdateMeetingView(View):
    template_name = 'new/meeting.html'
    def post(self, request, meeting_id):
        meeting = get_object_or_404(Schedule_Meeting, id=meeting_id)
        form = NewMeetingForm(request.POST, request.FILES, instance=meeting)

        if form.is_valid():
            form.save()
            messages.success(request, 'Meeting updated successfully!')
            return redirect('meeting')  # Redirect to your meeting list URL
        else:
            messages.error(request, 'Error updating meeting. Please check the form.')
            print(form.errors)
        meetings = Schedule_Meeting.objects.all()
        context = {
        'form': form, 
        'meeting': meeting, 
        'meetings': meetings}
        return render(request, self.template_name, context)

