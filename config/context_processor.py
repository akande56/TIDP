from django.template.loader import get_template
from django.contrib.auth.models import User
from accounts.models import Account
from django.shortcuts import redirect
from accounts.models import Account
from home.models import Unit
import datetime

def user(request):
    values = {
        'today': datetime.datetime.now()
    }
    if request.user.is_authenticated and Account.objects.filter(user=request.user).exists():
        values['account'] = Account.objects.get(user=request.user)
        return values
    return values
