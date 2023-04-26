from django.urls import path
from .views import (
   Meeting,
   MeetingDetails,
)

urlpatterns = [
    path('', Meeting.as_view(), name='meeting'),
    path('<int:id>/view/', MeetingDetails.as_view(), name='meeting_details'),
]

