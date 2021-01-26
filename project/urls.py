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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from hagakure.views import AboutView, GalleriesView, GalleryDetailsView, LandingPageView


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('articles/', include('articles.urls')),
    path('news/', include('news.urls')),
    path('register/', include('registration.urls')),
    path('training/', include('trainings.urls')),
    path('user/', include('auth_ex.urls')),
    path('', LandingPageView.as_view(), name='landing_page'),
    path('about/', AboutView.as_view(), name='about_us'),
    path('galleries/', GalleriesView.as_view(), name='galleries'),
    path('gellery/', GalleryDetailsView.as_view(), name='gallery_details'),
    #TODO: change below in the production as per https://docs.djangoproject.com/en/3.1/howto/static-files/deployment/
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
