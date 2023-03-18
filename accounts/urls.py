from django.urls import path
from django.views.generic.base import TemplateView
from .views import login_, RegisterApplicant, PaymentView
from django.contrib.auth.views import LogoutView, PasswordChangeView

urlpatterns = [
    path('login/', login_, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register', RegisterApplicant.as_view(), name='register'),
    path("payment/", PaymentView.as_view(), name="payment"),
]

