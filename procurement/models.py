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
category_choices = [
        ('Software', 'Software'),
        ('Telecommunication', 'Telecommunication'),
        ('Construction', 'Construction'),
        ('Others', 'Others'),
    ]

class Precurement(models.Model):
    title = models.CharField(max_length=20,help_text='contract title')
    category = models.CharField(max_length=20, choices=category_choices, help_text='broadcast range')
    responsibilty = models.CharField(max_length=20) 
    start_date = models.DateField()
    end_date = models.DateField()
    tender_type =  models.CharField(max_length=20, choices=Tender, help_text='audience')
    contractor = models.ManyToManyField(Contractors, related_name='project_contractors', null=True, blank=True ,default=None)
    description = models.CharField(max_length=30, default='details of project')
    budget = models.CharField(max_length=20)
    priority =models.CharField(max_length=20,choices=Priority, default=3) 
    project_file = models.ImageField(upload_to='project_files/', null=True, blank=True)
    
    def __str__(self):
        return str(self.title)

# abdulsalam (Archpragmatic)
# model to hold precurement-contractor relationship
# Note: you will noticed i used User as the primary model for invited persona...
# Reason is beacuse invitee are not limited to contractor persona. may include all member of the organization, thus
# to make it easy and have a generalize focus, i used User model

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
        return str(self.precurement.title)



class Procurement_tender_doc(models.Model):
    contractor = models.ForeignKey(Contractors, on_delete=models.CASCADE, related_name='interested_contractor')
    precurement = models.ForeignKey(Precurement, on_delete=models.CASCADE, related_name='procurement')
    file = models.ImageField(upload_to='contractor_tender_doc/')

    class Meta:
        verbose_name = 'Procurement_tender_doc'
        verbose_name_plural = 'Procurement_tender_docs'

    def __str__(self):
        return f"{self.contractor.company_name} - {self.precurement.title}"


class ContractorAward(models.Model):
    procurement = models.ForeignKey(Precurement, on_delete=models.CASCADE)
    contractors = models.ManyToManyField(Contractors)
    award_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    document = models.ImageField(upload_to='awarding_documents/', null=True, blank=True)
    remarks = models.TextField(null=True, blank=True) 