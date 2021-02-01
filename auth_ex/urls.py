"""hagakure URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import ChangeEmailView, ChangePasswordView, LogInView, LogOutView, UserDetailsEdit, UserDetailsView, VerifyPasswordView


urlpatterns = [
    path('change_email/', login_required(ChangeEmailView.as_view()), name='change_email'),
    path('change_password/', login_required(ChangePasswordView.as_view()), name='change_password'),
    path('details/', login_required(UserDetailsView.as_view()), name='user_details'),
    path('edit/', login_required(UserDetailsEdit.as_view()), name='user_edit'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('verify_password/', login_required(VerifyPasswordView.as_view()), name='verify_password'),
]
