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
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import path


from .views import AddGalleryView, EditGalleryView, GalleriesView, GalleriesListView, GalleryView


urlpatterns = [
    path('', GalleriesView.as_view(), name='galleries'),
    path('<int:pk>/<slug:slug>', GalleryView.as_view(), name='gallery'),
    path('list/', login_required(GalleriesListView.as_view()), name='galleries_list'),
    path('add/', login_required(AddGalleryView.as_view()), name='gallery_add'),
    path('edit/<int:pk>', login_required(EditGalleryView.as_view()), name='gallery_edit')
]
