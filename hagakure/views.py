from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import View

User = get_user_model()

class LandingPageView(View):

    def get(self, request, *args, **kwargs):        
        
        context = {'name': display_name(request.user), }
        return render(request, 'hagakure/index.html', context)


class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'hagakure/about_us.html')


class NewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'hagakure/news.html')


class TrainingsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'hagakure/trainings.html')


class ArticlesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'hagakure/articles.html')


class GalleriesView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'hagakure/galleires_list.html')


class TrainersView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'hagakure/trainers.html')


class GalleryDetailsView(View):
    def get(self, request, *args, **kwargs):
            return render(request, 'hagakure/gallery_details.html')


def display_name(active_user):

    if active_user.nick:
        display_name = active_user.nick
    else:
        display_name = active_user.first_name

    return display_name
