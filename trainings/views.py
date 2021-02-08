from datetime import date
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View

from utils.functions import display_name
from .models import Discipline, Training, TrainerBio
from messaging.models import TrainingMessage


class MyTrainingsView(View):
    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            raise Http404()

        trainigns_trainee = Training.objects.filter(trainees=request.user.pk).order_by('start_date')
        trainigns_trainer = Training.objects.filter(trainer=request.user.pk).order_by('start_date')
        messagges = TrainingMessage.objects.filter(
                        Q(training__in=trainigns_trainee)|Q(training__in=trainigns_trainer)
                        ).order_by('created_on')

        context = {
            'name': display_name(request.user),
            'trainings_trainee': trainigns_trainee,
            'trainings_trainer': trainigns_trainer,
            'today_date': date.today(),
            'messages': messagges,
        }

        return render(request, 'trainings/my_trainings.html', context)

    def post(self, request, *args, **kwargs):

        message = TrainingMessage()

        data = request.POST
        body = data['message']
        trainng_pk=data['training_pk']

        message.author = request.user
        message.body = body
        message.training=Training.objects.filter(pk=trainng_pk).get()
        message.save()

        return redirect('my_trainings')


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


class TrainerBioView(View):
    def get(self, request, *args, **kwargs):
        trainer_bios = TrainerBio.objects.all()

        context = {
            'name': display_name(request.user),
            'trainers': trainer_bios,
        }

        return render(request, 'trainings/trainers.html', context)        
