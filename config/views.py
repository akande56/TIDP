from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View


# Create your views here.
class LandingInfoView(LoginRequiredMixin, View):
    
    def get(self, request, **kwargs):
        context = {
            'landing_nav': "active"
        }
        return render(request, "landing_edit.html", context)
