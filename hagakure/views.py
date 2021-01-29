from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views import View

from utils.functions import display_name

from trainings.models import Training, Weekday
from articles.models import Article
from news.models import News

User = get_user_model()


class LandingPageView(View):
    def get(self, request, *args, **kwargs):
        week_beggining_date = date.today() - timedelta(days=date.today().weekday())

        weekdays = Weekday.objects.all().order_by('order')

        day1_trainings = Training.objects.filter(
            weekdays__order=1,
            start_date__lte=week_beggining_date + timedelta(days=0),
            end_date__gte=week_beggining_date + timedelta(days=0),
            ).order_by('start_hour')
        day2_trainings = Training.objects.filter(
            weekdays__order=2,
            start_date__lte=week_beggining_date + timedelta(days=1),
            end_date__gte=week_beggining_date + timedelta(days=1),
            ).order_by('start_hour')
        day3_trainings = Training.objects.filter(
            weekdays__order=3,
            start_date__lte=week_beggining_date + timedelta(days=2),
            end_date__gte=week_beggining_date + timedelta(days=2),
            ).order_by('start_hour')
        day4_trainings = Training.objects.filter(
            weekdays__order=4,
            start_date__lte=week_beggining_date + timedelta(days=3),
            end_date__gte=week_beggining_date + timedelta(days=3),
            ).order_by('start_hour')
        day5_trainings = Training.objects.filter(
            weekdays__order=5,
            start_date__lte=week_beggining_date + timedelta(days=4),
            end_date__gte=week_beggining_date + timedelta(days=4),
            ).order_by('start_hour')
        day6_trainings = Training.objects.filter(
            weekdays__order=6,
            start_date__lte=week_beggining_date + timedelta(days=5),
            end_date__gte=week_beggining_date + timedelta(days=5),
            ).order_by('start_hour')
        day7_trainings = Training.objects.filter(
            weekdays__order=7,
            start_date__lte=week_beggining_date + timedelta(days=6),
            end_date__gte=week_beggining_date + timedelta(days=6),
            ).order_by('start_hour')

        if request.user.is_authenticated:
            articles = Article.objects.filter(is_published=True).order_by('-created_on')[:5]
        else:
            articles = Article.objects.filter(is_published=True, is_public=True).order_by('-created_on')[:5]

        if request.user.is_authenticated:
            news = News.objects.filter(is_published=True, expiration_date__lte=date.today()).order_by('-created_on')[:5]
        else:
            news = News.objects.filter(is_published=True, is_public=True, expiration_date__lte=date.today()).order_by('-created_on')[:5]

        context = {
            'name': display_name(request.user),
            'day1_trainings': day1_trainings,
            'day2_trainings': day2_trainings,
            'day3_trainings': day3_trainings,
            'day4_trainings': day4_trainings,
            'day5_trainings': day5_trainings,
            'day6_trainings': day6_trainings,
            'day7_trainings': day7_trainings,
            'weekdays': weekdays,
            'articles': articles,
            'all_news': news,
        }
        return render(request, 'hagakure/index.html', context)


class AboutView(View):
    def get(self, request, *args, **kwargs):
        context = {'name': display_name(request.user), }
        return render(request, 'hagakure/about_us.html', context)
