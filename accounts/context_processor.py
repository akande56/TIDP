from django.template.loader import get_template
from django.contrib.auth.models import User
from accounts.models import Account
from django.shortcuts import redirect
from accounts.models import User
import datetime

def user(request):
    values = {
        'today': datetime.datetime.now()
    }
    
    if request.user.is_authenticated:
        if Account.objects.filter(user__username=request.user.username).exists():
            values['account'] = Account.objects.get(user__username=request.user.username)
        elif User.objects.filter(username=request.user.username).exists():
            values['account'] = User.objects.get(username=request.user)
        return values
    return values
