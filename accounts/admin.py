from django.contrib import admin
from .models import Account, ApplicantFiles, Institutions

# Register your models here.
admin.site.register(Account)
admin.site.register(ApplicantFiles)
admin.site.register(Institutions)