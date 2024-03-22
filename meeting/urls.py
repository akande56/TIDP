from django.urls import path
from .views import (
   meeting,
   MeetingDetails,
   edit_meeting,
   delete_agenda,
   delete_schedule_meeting,
)

urlpatterns = [
    path('meeting/', meeting, name='meeting'),
    path('meeting/<int:id>/view/', MeetingDetails.as_view(), name='meeting_details'),
    path('meeting/<int:meeting_id>/edit/', edit_meeting, name='edit_meeting'),
    path('meeting/meet/delete_agenda/<int:agenda_id>/', delete_agenda, name='delete_agenda'),
    path('meetings/<int:meeting_id>/delete/', delete_schedule_meeting, name='delete_schedule_meeting'),
]

