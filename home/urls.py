import imp
from django.urls import path
from django.views.generic.base import TemplateView
from .views import (
    UnitView,
    Dashboard,
    NewMail,
    UserPersonaView,
    UsersView,
    UserStateView,
    UserGroupDetail,
    UnitDetailsView,
    RemoveUserFromGroup,
    DashboardOld,
    
)
from config.views import LandingInfoView

urlpatterns = [
    path('dashboard/', Dashboard.as_view(), name='dashboard'),

    path('dashboard/old/', DashboardOld.as_view()),

    path('settings/landing', LandingInfoView.as_view(), name='landing_info'),

    path('settings/users/', UsersView.as_view(), name='users_view'),
    path('settings/user/<int:id>/', UserStateView.as_view(), name='user_state'),

    path('settings/group/user/<int:id>/<slug:slug>/remove/', RemoveUserFromGroup.as_view(), name='remove_user_from_group'),
    
    path("settings/user/persona", UserPersonaView.as_view(), name="user_persona"),
    path("settings/<slug:slug>/group/", UserGroupDetail.as_view(), name="group_detail"),

    path("settings/unit/", UnitView.as_view(), name="units_view"),
    path('settings/unit/<slug:slug>/', UnitDetailsView.as_view(), name='unit_detail'),
]

