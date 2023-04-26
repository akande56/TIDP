import imp
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, Group
PERSONA = (
    (1, 'Tier 1 Minister | DG | CEO | Chief Register'), 
    (2, 'Tier 2 Permanent Sec | VC'),
    (3, 'Tier 3 Director'),
    (4, 'Tier 4 Deputy Director'),
    (5, 'Tier 5 Assistant Duputy Director'),
    (6, 'Tier 6 Clerical Officer'),
    (7, 'Tier 7 Protocol Oficer'),
    (8, 'Tier 8 Other'),
    (9, 'Tier 9 Registry Officer'),
    (10, 'Tier ICT Personal'),
    (11, 'Tier 11 Contractors'),
    
)

# Create your models here.
class UserPersona(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    persona_tier = models.IntegerField(choices=PERSONA)
    no_of_user = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "{}: {}".format(self.persona_tier, self.name)

    def no_of_user(self):
        return Account.objects.filter(user_persona__id=self.id).count()



class Account(models.Model):
    user_persona = models.ForeignKey(UserPersona, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic_url = models.CharField(max_length=500, default=0)
    
    def __str__(self):
        return "{}: {} in the {}".format(self.user.first_name, self.user_persona.name, self.unit_set.first())

    def is_image(self):
        if self.image:
            return True
        return False
    def get_profile_url(self):
        return reverse('user_profile', args=[self.id])

    def get_activation_url(self):
        return reverse('account_activation', args=[self.user.id])



class Contractors(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    business_profile = models.FileField('')