from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.generic import View
from .forms import ContractorFormSignUp
from accounts.models import UserPersona, Account, Contractors
from django.contrib.auth.models import User
# Create your views here.

class Procurement(LoginRequiredMixin, View):
    def get(self, request, **kwargs):
        
        context = {
            'contractors': Contractors.objects.all()    
        }
        return render(request, "new/precurement.html", context)

     
    def post(self, request, **kwargs):
        messages.error(request, "Feature not enabled by admin")
        return redirect('procurement')        


class RegisterContractor(View):
    
    def get(self, request, **kwargs):
        context = {
            'form': ContractorFormSignUp
        }
        return render(request, "contractor_registration.html", context)

    
    def post(self, request, **kwargs):
        form = ContractorFormSignUp(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['email']).exists():
                messages.error(request, "Your Account Has been Registered kindly login")
                return redirect('login')
            user = User()
            user.first_name = form.cleaned_data['full_name']
            user.last_name = form.cleaned_data['company_name']
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            try:
                with transaction.atomic():
                    user.save()
                    tier = UserPersona.objects.get(persona_tier=11)
                    Account.objects.create(
                        user=user,
                        user_persona=tier
                    )
                    redirect('contactor_register')
            except UserPersona.DoesNotExist:
                messages.error(request, "Error Contact Support")
                return redirect('login')

        messages.success(request, "A Verification link Has been sent to your email kindly verify")
        return redirect('login')
