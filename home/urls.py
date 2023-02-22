import imp
from django.urls import path
from django.views.generic.base import TemplateView
from .views import (
    UnitView,
    Dashboard,
    NewMail,
    UsersView,
    UserStateView,
    UserGroupDetail,
    UnitDetailsView,
    RemoveUserFromGroup,
    SystemSettings,
    PaymentView
)

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('settings/', SystemSettings.as_view(), name='system_settings'),
    path('settings/users/', UsersView.as_view(), name='users_view'),
    path('settings/user/<int:id>/', UserStateView.as_view(), name='user_state'),
    path("settings/unit/", UnitView.as_view(), name="units_view"),
    path("payment/", PaymentView.as_view(), name="payment"),

    path('settings/group/user/<int:id>/<slug:slug>/remove/', RemoveUserFromGroup.as_view(), name='remove_user_from_group'),
    
    path("settings/<slug:slug>/group/", UserGroupDetail.as_view(), name="group_detail"),
    path('settings/unit/<slug:slug>/', UnitDetailsView.as_view(), name='unit_detail'),
]

