from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import View

from utils.functions import display_name

from trainings.models import Training

User = get_user_model()

class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        week_beggining_date = date.today() - timedelta(days=date.today().weekday())
        
        monday_trainings = Training.objects.filter(
            weekdays=1,
            start_date__lte=week_beggining_date + timedelta(days=0),
            end_date__gte=week_beggining_date + timedelta(days=0),
            ).order_by('start_hour')
        tuesday_trainings = Training.objects.filter(
            weekdays=2,
            start_date__lte=week_beggining_date + timedelta(days=1),
            end_date__gte=week_beggining_date + timedelta(days=1),
            ).order_by('start_hour')
        wednesday_trainings = Training.objects.filter(
            weekdays=3,
            start_date__lte=week_beggining_date + timedelta(days=2),
            end_date__gte=week_beggining_date + timedelta(days=2),
            ).order_by('start_hour')
        thursday_trainings = Training.objects.filter(
            weekdays=4,
            start_date__lte=week_beggining_date + timedelta(days=3),
            end_date__gte=week_beggining_date + timedelta(days=3),
            ).order_by('start_hour')
        friday_trainings = Training.objects.filter(
            weekdays=5,
            start_date__lte=week_beggining_date + timedelta(days=4),
            end_date__gte=week_beggining_date + timedelta(days=4),
            ).order_by('start_hour')
        saturday_trainings = Training.objects.filter(
            weekdays=6,
            start_date__lte=week_beggining_date + timedelta(days=5),
            end_date__gte=week_beggining_date + timedelta(days=5),
            ).order_by('start_hour')
        sunday_trainings = Training.objects.filter(
            weekdays=7,
            start_date__lte=week_beggining_date + timedelta(days=6),
            end_date__gte=week_beggining_date + timedelta(days=6),
            ).order_by('start_hour')

        context = {
            'name': display_name(request.user),
            'monday_trainings': monday_trainings,
            'tuesday_trainings': tuesday_trainings,
            'wednesday_trainings': wednesday_trainings,
            'thursday_trainings': thursday_trainings,
            'friday_trainings': friday_trainings,
            'saturday_trainings': saturday_trainings,
            'sunday_trainings': sunday_trainings,
        }
        return render(request, 'hagakure/index.html', context)


class AboutView(View):
    def get(self, request, *args, **kwargs):
        context = {'name': display_name(request.user), }
        return render(request, 'hagakure/about_us.html', context)


class NewsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'hagakure/news.html')


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
