from django.forms import modelformset_factory
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest, JsonResponse
from .models import Schedule_Meeting, Agenda
from .forms import NotesForm, SetUpMeetingFor, ScheduleMeetingForm,  AgendaFormset
from django.contrib import messages
# Create your views here.
from accounts.models import Account

# class Meeting(LoginRequiredMixin, View):
#     def get(self, request, **kwargs):
#         meetings = Schedule_Meeting.objects.all()
#         form = ScheduleMeetingForm()
#         agenda_formset = AgendaFormset()
        
#         context = {
#             'form': form,
#             "meetings": meetings,
#             'agenda_formset': agenda_formset
#         }
#         return render(request, "new/meeting.html", context)

#     def post(self, request, **kwargs):
#         form = ScheduleMeetingForm(request.POST, request.FILES)
#         agenda_formset = AgendaFormset(request.POST)
#         if form.is_valid() and agenda_formset.is_valid():
#             my_account = Account.objects.get(user=request.user)
#             instance = form.save(commit=False)
#             instance.scheduled_by = my_account
#             print (form.errors)
#             meeting_attachmment = self.request.FILES.get('attachment')
#             if not meeting_attachmment:
#                 return HttpResponseBadRequest('No file provided.')

#             # Additional validation if needed, e.g., check if it's an image
#             if not meeting_attachmment.content_type.startswith('image'):
#                 return HttpResponseBadRequest('Invalid file type. Please upload an image.')

#             instance.attachment = meeting_attachmment
#             instance.save()
#             for agenda_form in agenda_formset:
#                 if agenda_form.is_valid():  # Validate each agenda form
#                     agenda = agenda_form.save(commit=False)  # Save agenda data without saving yet
#                     agenda.meeting = instance  # Assign agenda to the current meeting
#                     agenda.save()
#             messages.success(request, 'Meeting Created Sucessfully')
#         return redirect('meeting')


def meeting(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        start_on = request.POST.get('start_on')
        end_on = request.POST.get('end_on')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        venue = request.POST.get('venue')
        description = request.POST.get('description')
        attachment = request.FILES.get('attachment')
        if not attachment:
            return HttpResponseBadRequest('No file provided.')

        # Additional validation if needed, e.g., check if it's an image
        if not attachment.content_type.startswith('image'):
            return HttpResponseBadRequest('Invalid file type. Please upload an image.')

        participants = request.POST.getlist('participants')
        address = request.POST.get('address')
        link = request.POST.get('link')
        agendas = request.POST.getlist('agenda[]')
        minutes = request.POST.getlist('minutes[]')
       
        # Create Schedule_Meeting instance
        my_account = Account.objects.get(user=request.user)

        meeting = Schedule_Meeting.objects.create(
            scheduled_by = my_account,
            title=title,
            start_on=start_on,
            end_on=end_on,
            start_time=start_time,
            end_time=end_time,
            venue=venue,
            description=description,
            attachment=attachment,
            address=address,
            link=link
        )
        # Add participants
        for participant_id in participants:
            meeting.paticipants.add(participant_id)
        meeting.save()

        # Create Agenda instances
        minutes = [int(minute) for minute in minutes if minute.isdigit()]
        for agenda, minute in zip(agendas, minutes):
            a = Agenda.objects.create(meeting=meeting, agenda=agenda, minutes=minute)
            a.save()
        messages.success(request, 'Meeting Created Sucessfully')
        return redirect('meeting') 
    else:
        participants = Account.objects.exclude(user_persona__persona_tier=11)

        meetings = Schedule_Meeting.objects.all()
        return render(request, 'new/meeting.html', {'participants': participants, 'meetings': meetings})


def delete_agenda(request, agenda_id):
    if request.method == 'POST':
        try:
            agenda = Agenda.objects.get(id=agenda_id)
            agenda.delete()
            return JsonResponse({'message': 'Agenda item deleted successfully.'}, status=200)
        except Agenda.DoesNotExist:
            return JsonResponse({'error': 'Agenda item not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method or not an AJAX request.'}, status=400)


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



# class UpdateMeetingView(View):
#     template_name = 'new/meeting.html'
#     def post(self, request, meeting_id):
#         meeting = get_object_or_404(Schedule_Meeting, id=meeting_id)
#         form = NewMeetingForm(request.POST, request.FILES, instance=meeting)

#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Meeting updated successfully!')
#             return redirect('meeting')  # Redirect to your meeting list URL
#         else:
#             messages.error(request, 'Error updating meeting. Please check the form.')
#             print(form.errors)
#         meetings = Schedule_Meeting.objects.all()
#         context = {
#         'form': form, 
#         'meeting': meeting, 
#         'meetings': meetings}
#         return render(request, self.template_name, context)


def edit_meeting(request, meeting_id):
    meeting = Schedule_Meeting.objects.get(pk=meeting_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        start_on = request.POST.get('start_on')
        end_on = request.POST.get('end_on')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        venue = request.POST.get('venue')
        description = request.POST.get('description')
        attachment = request.FILES.get('attachment')
        if attachment:
            if attachment.content_type.startswith('image'):
                return HttpResponseBadRequest('Invalid file type. Please upload an image.')
            if meeting.attachment:
                meeting.attachment.delete(save=False)
            meeting.attachment = attachment

        participants = request.POST.getlist('participants')
        address = request.POST.get('address')
        link = request.POST.get('link')
        agendas = request.POST.getlist('agenda[]')
        minutes = request.POST.getlist('minutes[]')
       
        # Update meeting instance
        meeting.title = title
        meeting.start_on = start_on
        meeting.end_on = end_on
        meeting.start_time = start_time
        meeting.end_time = end_time
        meeting.venue = venue
        meeting.description = description
        meeting.attachment = attachment
        meeting.address = address
        meeting.link = link

        # Update participants
        meeting.paticipants.clear()
        for participant_id in participants:
            meeting.paticipants.add(participant_id)
        print('scu....')
        meeting.save()
        
        # Update or create agenda instances
        meeting.agendas.all().delete()  # Clear existing agendas
        for agenda, minute in zip(agendas, minutes):
            if agenda and minute:  # Ignore empty agenda or minute values
                Agenda.objects.create(
                    meeting=meeting,
                    agenda=agenda,
                    minutes=int(minute)  # Convert minutes to integer
                )

        messages.success(request, 'Meeting updated successfully')
        return redirect('meeting')
    else:
        participants = Account.objects.exclude(user_persona__persona_tier=11)
        meetings = Schedule_Meeting.objects.all()
    context = {
        'participants': participants,
        'meetings': meetings
    }
    return render(request, 'new/meeting.html', context)


def delete_schedule_meeting(request, meeting_id):
    if request.method == 'POST':
        meeting = get_object_or_404(Schedule_Meeting, pk=meeting_id)
        meeting.agendas.all().delete()
        meeting.delete()
        messages.success(request, 'Meeting deleted successfully.')
    else:
        messages.error(request, 'Invalid request method.')
    # Fetch updated data after deletion
    participants = Account.objects.exclude(user_persona__persona_tier=11)
    meetings = Schedule_Meeting.objects.all()
    context = {
        'participants': participants,
        'meetings': meetings
    }
    return render(request, 'new/meeting.html', context)