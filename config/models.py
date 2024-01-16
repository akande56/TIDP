from pyexpat import model
from django.db import models


class Home(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()


class Settings(models.Model):
    send_correspondance_to_registry_first  = models.BooleanField(default=True)
    