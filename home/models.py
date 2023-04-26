from django.db import models

from accounts.models import Account
from .utility import suglify_pre_save, suglify_post_save
from django.db.models.signals import pre_save, post_save

# Create your models here.
UNIT_TYPE = (
    ('Minister/DG', 'Minister/DG'),
    ('Secretery', 'Secretery'),
    ('Department', 'Department'),
)


class Unit(models.Model):
    name = models.CharField(max_length=255)
    unit_type = models.CharField(max_length=100, choices=UNIT_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    users = models.ManyToManyField(Account, blank=True)

    def __str__(self):
        return self.name
    

pre_save.connect(suglify_pre_save, sender=Unit)
post_save.connect(suglify_post_save, sender=Unit)
