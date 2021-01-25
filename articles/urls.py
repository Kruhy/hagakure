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

from .views import AddArticleView, AllArticlesView, ArticleView, ArticlesListView, EditArticleView


urlpatterns = [
    path('', AllArticlesView.as_view(), name='articles'),
    path('<int:pk>/<slug:slug>', ArticleView.as_view(), name='article'),
    path('add/', AddArticleView.as_view(), name='add_article'),
    path('edit/<int:pk>/', EditArticleView.as_view(), name='edit_article'),
    path('list/', ArticlesListView.as_view(), name='article_list'),
]
