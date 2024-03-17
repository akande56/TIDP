from pyexpat import model
from statistics import mode
from django.db import models
from django.db.models import BLANK_CHOICE_DASH
from accounts.models import Account
from ckeditor.fields import RichTextField

VENUE = (
    ("online", "Online"),
    ("physical", "Physical")
)
STATUS = (
    ('up_comming', 'up_comming'),
    ('previous', 'previous'),
    ('all', 'all'),
)
# Create your models here.
class Schedule_Meeting(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    start_on = models.DateField(blank=True, null=True)
    end_on = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    paticipants = models.ManyToManyField(Account, related_name="paticipant")
    venue = models.CharField(max_length=1000, null=True, blank=True, choices=VENUE)
    description = RichTextField(blank=True, null=True)
    agenda = RichTextField(blank=True, null=True)
    draft = models.BooleanField(default=False)
    minutes_of_meeting = RichTextField(blank=True, null=True)
    done = models.BooleanField(default=False)
    scheduled_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    attachment = models.ImageField(upload_to='meetingfiles/', null=True, blank=True) #previously filepath
    created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    link = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=100,choices=STATUS, default='all')

class OnlineMeeting(models.Model):
    meeting = models.ForeignKey(Schedule_Meeting, on_delete=models.CASCADE)
    api = models.CharField(max_length=100)