from django.db import models
from accounts.models import Contractors, User

Tender = (
    ('open tender', 'open tender'),
    ('selective tender', 'selective tender'),
    ('internal labour', 'internal labour')
)
Priority = (
    ('HIGHEST', 'HIGHEST'),
    ('MEDIUM', 'MEDIUM'),
    ('LOW', 'LOW'),
    ('LOWEST', 'LOWEST')
)

class Precurement(models.Model):
    title = models.CharField(max_length=20,help_text='contract title')
    category = models.CharField(max_length=20, choices=Tender, help_text='broadcast range')
    responsibilty = models.CharField(max_length=20) 
    start_date = models.DateField()
    end_date = models.DateField()
    tender_type =  models.CharField(max_length=20, choices=Tender, help_text='audience')
    contractor = models.ForeignKey(Contractors, on_delete=models.CASCADE, related_name='project_contractors', null=True, blank=True ,default=None)
    description = models.CharField(max_length=30, default='details of project')
    budget = models.CharField(max_length=20)
    priority =models.CharField(max_length=20,choices=Priority, default=3) 
    
    def __str__(self):
        return str(self.title)



class Precurement_contractors(models.Model):
    """Model definition for Precurement_contractors."""
    invite = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invited')
    precurement = models.ForeignKey(Precurement, on_delete=models.CASCADE, related_name='advertisedPrecurement')
    class Meta:
        """Meta definition for Precurement_contractors."""

        verbose_name = 'Precurement_contractors'
        verbose_name_plural = 'Precurement_contractors'

    def __str__(self):
        """Unicode representation of Precurement_contractors."""
        return str(self.invite.last_name)
