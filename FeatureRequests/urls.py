"""FeatureRequests URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_view
from .settings import STATIC_ROOT, STATIC_URL
from django.conf.urls.static import static

# Add in:
# 1. All the url path in the RequestManager urls.py
# 2. static folder url
urlpatterns = [
    path('admin/', admin.site.urls),
    # All RequestManager related urls
    path('', include('RequestManager.urls')),
    # Login url
    path('login/', auth_view.LoginView.as_view(template_name='RequestManager/login.html'), name='Login'),
    # Logout url
    path('logout/', auth_view.LogoutView.as_view(template_name='RequestManager/logout.html'), name='Logout'),
] + static(STATIC_URL, document_root=STATIC_ROOT)
