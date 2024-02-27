from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
from .views import (
    login_,
    show_notifications,
    mark_notifications_as_read,
    ChangePasswordView,
    # CustomPasswordResetView, 
    SignatureView,
)


urlpatterns = [
    path('login/', login_, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('ajax/show-notifications/', show_notifications, name='show_notifications'),
    path('ajax/mark-notifications-as-read/', mark_notifications_as_read, name='mark_notifications_as_read'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('update_signature/', SignatureView.as_view(), name='update_signature'),
    # path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
]