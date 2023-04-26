from django.urls import path
from .views import (
    Procurement,
    RegisterContractor,
)

urlpatterns = [
    path('register', RegisterContractor.as_view(), name='contactor_register'),
    path('', Procurement.as_view(), name='procurement'),
]

