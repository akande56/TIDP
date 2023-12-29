from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse

from accounts.models import (
    Account, 
    UserPersona, 
    Contractors,
    Notification,
)
from .forms import (
    # UserRegistrationForm,
    UserLoginForm,
)



def login_(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data['password']
        try:
            user = Account.objects.get(user__username=username)

            if user:
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    if next:
                        return redirect(next)
                    return redirect("dashboard")
                else:
                    messages.success(
                        request, 'Username/Password does not match')
            else:
                messages.success(
                    request, 'Authorisation Error Contact Admin To Regain Access')
        except Exception as e:
            messages.success(
                request, 'Username/Password does not match'.format())
    context = {
        'form': form
    }
    return render(request, "authentication.html", context)



def show_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(user=user, is_read=False)[:5]  # Limit to the latest 5
    return JsonResponse({'notifications': [{'message': n.message, 'created_at': n.created_at} for n in notifications]})

def mark_notifications_as_read(request):
    user = request.user
    Notification.objects.filter(user=user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})