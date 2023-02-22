import imp
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, Group
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

CATEGORIES = (
    ('B.SC', 'B.Sc'),
    ('HND', 'HND'),
    ('M.Sc', 'M.Sc'),
    ('PGD', 'PGD'),
    ('PHD', 'PGD'),
    ('Dip', 'Dip'),
    ('NCE', 'NCE'),
)
PERSONA = (
    (1, 'Tier 1 '), 
    (2, 'Tier 2 '),
    (3, 'Tier 3 '),
    (4, 'Tier 4 '),
    (5, 'Tier 5 '),
    (6, 'Tier 6 Clerical/Registry Officer'),
    (7, 'Tier 7 Protocol Oficer'),
    (8, 'Tier 8 Other'),
    (9, 'Tier 9 Registry Officer'),
    (10, 'Tier ICT Personal'),
    (11, 'Tier 11 Contractors'),
    
    
    # 192.168.40.206:8080
)

# Create your models here.
class Institutions(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    logo = models.ImageField(blank=True, null=True)
    

    def __str__(self):
        return "{}".format(self.name)


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institutions, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    profile_pic_url = models.CharField(max_length=500, default=0)
    
    def __str__(self):
        return "{} : {} ".format(self.user.first_name,  self.unit_set.first())

    def get_fullname(self):
        return "{} {}".form(self.user.first_name, self.user.last_name) 

    def is_image(self):
        if self.image:
            return True
        return False
        
    def get_profile_url(self):
        return reverse('user_profile', args=[self.id])

    def get_activation_url(self):
        return reverse('account_activation', args=[self.user.id])



class ApplicationType(models.Model):
    name = models.CharField(max_length=300)
    category = models.CharField(max_length=100, choices=CATEGORIES)
    institutions = models.ForeignKey(Institutions, blank=True, on_delete=models.CASCADE)
    fee = models.IntegerField(blank=True,)
    template = RichTextUploadingField(blank=True, null=True)


class Application(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    applicationtype = models.ForeignKey(ApplicationType, on_delete=models.CASCADE)
    institutions = models.ForeignKey(Institutions, on_delete=models.CASCADE)
    status = models.BooleanField(default=False, blank=True)
    progress = models.IntegerField(default=0, blank=True)


class ApplicantFiles(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    document = models.FileField(upload_to='Applicant/')


class QueryAplicant(models.Model):
    purpose = models.TextField()
    applicant = models.ForeignKey(Account, on_delete=models.CASCADE)

    