from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
from .views import (
    login_,
    show_notifications,
    mark_notifications_as_read,
)


urlpatterns = [
    path('login/', login_, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('ajax/show-notifications/', show_notifications, name='show_notifications'),
    path('ajax/mark-notifications-as-read/', mark_notifications_as_read, name='mark_notifications_as_read'),
]           