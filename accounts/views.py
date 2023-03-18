from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from .models import Institutions
from accounts.models import Account
from accounts.forms import (
    UserRegistrationForm,
    UserLoginForm,
)

def home(request):
    pass

def login_(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data['password']
        try:
            # User Is form Institution 
            user = User.objects.get(username=username)
            if user.is_active:
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    if next:
                        return redirect(next)
                    return redirect("dashboard")
                else:
                    messages.success(
                        request, 'Username/Password does not match')
            messages.success(
                    request, 'Authorisation Error Contact Admin To Regain Access')
        except Exception as e:
            messages.success(
                request, 'Username/Password does not match {}'.format(e))
    context = {
        'form': form
    }
    return render(request, "authentication.html", context)



from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.generic import View
from .forms import ApplicantFormSignUp
from accounts.models import Account, ApplicantFiles
from django.contrib.auth.models import User
# Create your views here.


class RegisterApplicant(View):
    
    def get(self, request, **kwargs):
        context = {
            'form': ApplicantFormSignUp
        }
        return render(request, "registration.html", context)

    
    def post(self, request, **kwargs):
        form = ApplicantFormSignUp(request.POST, request.FILES)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['email']).exists():
                messages.error(request, "Your Account Has been Registered kindly login")
                return redirect('login')
            user = User()
            user.first_name = form.cleaned_data['full_name']
            user.email = form.cleaned_data['email']
            user.username = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            documents = request.FILES.getlist("business_profile")
            try:
                with transaction.atomic():
                    user.save()
                    if form.cleaned_data['key'] != "":
                        institution = Institutions.objects.create(
                            name=form.cleaned_data['full_name'],
                            address=form.cleaned_data['address'],
                        )
                        account = Account.objects.create(
                            user=user,
                            institution=institution
                        )
                        for document in documents:
                            ApplicantFiles.objects.create(
                                account=account, 
                                document=document
                                )
                        messages.success(request, "Your Institution will undergo a verification review kindly check you email for the verification link ")
                        return redirect('login')
                    for document in documents:
                        ApplicantFiles.objects.create(
                            account=account, 
                            document=document
                            )
                    messages.success(request, "Account created successfully")
                    return redirect('login')
                    
            except Exception as e:
                messages.success(request, "Exception: {}".format(e))
                return redirect("register")        
            
        messages.success(request, "Form Error: {}".format(form.errors))
        return redirect("register")


class OnBoarding(View, LoginRequiredMixin):

    def get(self, request, **kwargs):
        context = {
            'contractors': Account.objects.filter(user_persona__persona_tier=11)
        }
        return render(request, "new/on_boarding.html", context)
        

class PaymentView(LoginRequiredMixin, View):
    template = "new/payment.html"

    def get(self, request, **kwargs):

        return render(request, "new/payment.html")