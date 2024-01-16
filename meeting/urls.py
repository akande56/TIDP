from django.urls import path
from .views import (
   Meeting,
   MeetingDetails,
   UpdateMeetingView,
)

urlpatterns = [
    path('meeting/', Meeting.as_view(), name='meeting'),
    path('meeting/<int:id>/view/', MeetingDetails.as_view(), name='meeting_details'),
    path('meeting/<int:meeting_id>/edit/', UpdateMeetingView.as_view(), name='edit_meeting'),
]

