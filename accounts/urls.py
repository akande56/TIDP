from django.urls import path
from django.views.generic.base import TemplateView
from .views import login_
from django.contrib.auth.views import LogoutView, PasswordChangeView

urlpatterns = [
    path('login/', login_, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
