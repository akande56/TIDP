from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
from .views import login_


urlpatterns = [
    path('login/', login_, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]           