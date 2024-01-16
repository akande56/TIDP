from tokenize import blank_re
from django.db import models
from django.dispatch import receiver
from accounts.models import Account
from home.models import Unit
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
SENDING_STAGE = (
    ('Clearing', 'Clearing'),
    ('Done', 'Done'),
)
RECEIVER_STAGE = (
    ('Clearing', 'Clearing'),
    ('Protocol', 'Protocol'),
    ('Done', 'Done'),
)
# Create your models here.


class Folder(models.Model): #Correspondance
    title = models.CharField(max_length=255)
    unique_identifier = models.CharField(max_length=8)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True)
    draft = models.BooleanField(default=True)
    archive = models.BooleanField(default=False)
    urgent = models.BooleanField(default=False)


class Folder_Content(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    content = RichTextUploadingField(blank=True, null=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class File(models.Model):
    media = models.ImageField(upload_to="memo_file/") #previoiusly file field
    folder_content = models.ForeignKey(Folder_Content, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000, blank=True, null=True)

class Routing(models.Model):
    send_to = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True, related_name='creator')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    forwarded_by = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, related_name='reciever')
    intended_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, blank=True)
    initiated_unit = models.ForeignKey(Unit, on_delete=models.CASCADE, blank=True, related_name='initiated_unit')
    viewed = models.BooleanField(default=False)
    stared = models.BooleanField(default=False)
    created = models.TimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    sender_stage = models.CharField(max_length=200, choices=SENDING_STAGE)
    reciever_stage = models.CharField(max_length=200, choices=RECEIVER_STAGE, null=True, blank=True)
    send = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]
    
    def filter_by_instance(self, instance):    
        content_type = ContentType.objects.get_for_model(instance)
        comments = Comment.objects.filter(
            content_type=content_type,
            object_id=instance.id
        )
        return comments

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance)
        return content_type.pk

    @property
    def comments(self):
        instance = self
        qs = self.filter_by_instance(instance)
        return qs

class Comment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()
    visible = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    def __str__(self):
        return self.content

    class Meta:
        ordering = ["-timestamp", "-updated"]

    