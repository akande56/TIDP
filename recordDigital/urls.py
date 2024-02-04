"""recordDigital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from correspondance import views
from home.views import (
    home
)
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('', include("home.urls")),
    path('procurement/', include("procurement.urls")),
    path('account/', include("accounts.urls")),
    path('meet/', include("meeting.urls")),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('correspondance/', include("correspondance.urls")),
    # path('ckeditor/', include("ckeditor_uploader.urls")),    
    # path('__debug__/', include('debug_toolbar.urls')),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# path('', include('pwa.urls')),

