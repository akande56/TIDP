from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import (
    PasswordResetView, 
)
from django.views import View
from accounts.models import (
    Account, 
    UserPersona, 
    Contractors,
    Notification,
)
from .forms import (
    # UserRegistrationForm,
    UserLoginForm,
    ChangePasswordForm,
    # CustomPasswordResetForm
    SignatureForm,
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
    notifications = Notification.objects.filter(user=user, is_read=False)[:8]  # Limit to the latest 8
    return JsonResponse({'notifications': [{'message': n.message, 'created_at': n.created_at} for n in notifications]})

def mark_notifications_as_read(request):
    user = request.user
    Notification.objects.filter(user=user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})



class ChangePasswordView(SuccessMessageMixin,PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'new/change_password.html'  # Create this template
    success_url = reverse_lazy('home')
    success_message = "Password changed successfully"


# class CustomPasswordResetView(View):
#     template_name = 'new/custom_password_reset.html'  # Update with your template

#     def get(self, request):
#         form = CustomPasswordResetForm()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request):
#         form = CustomPasswordResetForm(request.POST)

#         if form.is_valid():
#             username = form.cleaned_data['username']
#             new_password = form.cleaned_data['new_password']

#             # Retrieve the user
#             User = get_user_model()
#             user = User.objects.get(username=username)

#             # Update the password
#             user.set_password(new_password)
#             user.save()

#             # Log in the user if needed
#             user = authenticate(request, username=username, password=new_password)
#             if user is not None:
#                 login(request, user)

#             return reverse_lazy('login')  # Update with your success URL

#         return render(request, self.template_name, {'form': form})

class SignatureView(View):
    template_name = 'new/signature_form.html'

    def get(self, request):
        form = SignatureForm()
        current_signature = Account.objects.get(user = request.user).signature
        return render(request, self.template_name, {'form': form, 'current_signature': current_signature})

    def post(self, request):
        form = SignatureForm(request.POST, request.FILES)

        if form.is_valid():
            signature = form.cleaned_data.get('signature')
            account = Account.objects.get(user=request.user)

            # Open the image using Pillow
            with Image.open(signature) as img:
                # Resize the image
                new_width = 100  # Set the desired width
                new_height = 50  # Set the desired height
                resized_img = img.resize((new_width, new_height))

                # Save the resized image to a BytesIO buffer
                buffer = BytesIO()
                resized_img.save(buffer, format='JPEG')
                image_content = buffer.getvalue()

                # Save the resized image to the account's signature field
                account.signature.save('resized_signature.jpg', ContentFile(image_content))

            messages.success(request, 'Signature updated successfully.')
            return redirect('dashboard')
        else:
            print(form.errors)

        return render(request, self.template_name, {'form': form})