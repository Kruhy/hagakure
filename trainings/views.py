from datetime import date
from django.shortcuts import render, redirect
from django.views import View

from utils.functions import display_name
from .models import Discipline, Training


class MyTrainingsView(View):
    def get(self, request, *args, **kwargs):
        trainigns_trainee = Training.objects.filter(trainees=request.user.pk).order_by('start_date')
        trainigns_trainer = Training.objects.filter(trainer=request.user.pk).order_by('start_date')

        context = {
            'name': display_name(request.user),
            'trainings_trainee': trainigns_trainee,
            'trainings_trainer': trainigns_trainer,
            'today_date': date.today(),
        }

        return render(request, 'trainings/my_trainings.html', context)


class TrainingsListView(View):
    def get(self, request, *args, **kwargs):
        trainings = Training.objects.filter(start_date__lte=date.today(), end_date__gte=date.today())
        disciplines = Discipline.objects.all()
        
        context = {
            'name': display_name(request.user),
            'trainings': trainings,
            'disiciplines': disciplines,
            'today_date': date.today(),
        }

        return render(request, 'trainings/trainings.html', context)
