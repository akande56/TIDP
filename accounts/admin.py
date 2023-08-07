from django.contrib import admin
from .models import Account, UserPersona, Contractors,ContractorDocument

# Register your models here.
admin.site.register(Account)
admin.site.register(UserPersona)
admin.site.register(Contractors)
admin.site.register(ContractorDocument)