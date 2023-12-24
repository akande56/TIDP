from django.core.validators import FileExtensionValidator ## abdul..
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError

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
    (10, 'Tier 10 ICT Personal'),
    (11, 'Tier 11 Contractors'),

)

# Create your models here.
class UserPersona(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    persona_tier = models.IntegerField(choices=PERSONA)
    # no_of_user = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return "{}: {}".format(self.persona_tier, self.name)

    def no_of_user(self):
        return Account.objects.filter(user_persona__id=self.id).count()


class Account(models.Model):
    user_persona = models.ForeignKey(UserPersona, on_delete=models.CASCADE, related_name='ruser_persona') #added related name abduls, for easy query
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ruser_account') #added related name abduls
    profile_pic_url = models.CharField(max_length=500, default=0, null=True)

    def __str__(self):
        return "{}: {} in the {}".format(self.user.first_name, self.user_persona.name, self.unit_set.first())

    def is_image(self):
        if self.profile_pic_url:
            return True
        return False

    def get_profile_url(self):
        return reverse('user_profile', args=[self.id])

    def get_activation_url(self):
        return reverse('account_activation', args=[self.user.id])
    # #to ensure no admin instance is any of persona instance
    # def clean(self):
    #     if self.user.is_superuser:
    #         raise ValidationError("Admin users cannot be associated with UserPersona instances.")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



## abdul starts here....
status = (('verified', 'verified'), ('pending','pending'))
contractor_category = (
    ('Software', 'Software'),
    ('Telecommunication', 'Telecommunication'),
    ('Construction', 'Construction'),
    ('others', 'others')
)


class Contractors(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='contractor_account') #added related name abduls
    company_name  = models.CharField(max_length=60, default='default: company name') #added company name.. Abduls
    status = models.CharField(max_length=50, choices=status, default='pending') 
    category = models.CharField (max_length=50, choices=contractor_category, default='Software')
    def __str__(self):
        return str(self.company_name)


class ContractorDocument(models.Model):
    """Model definition for ContractorDocument."""
    title = models.CharField(max_length=50)
    file = models.ImageField(upload_to='contractor_docs/')
    contractor = models.ForeignKey(Contractors, on_delete=models.CASCADE,null=True,default=None ,related_name='contractor_document')

    class Meta:
        """Meta definition for ContractorDocument."""

        verbose_name = 'ContractorDocument'
        verbose_name_plural = 'ContractorDocuments'

    def __str__(self):
        """Unicode representation of ContractorDocument."""
        return str(self.title)