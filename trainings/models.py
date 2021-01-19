from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Discipline(models.Model):

    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Weekday(models.Model):
    name = models.CharField(max_length=16)
    order = models.IntegerField()

    def __str__(self):
        return self.name


class Dojo(models.Model):
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=8)
    address = models.CharField(max_length=128)
    def __str__(self):
        return self.name


class AgeCategory(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Level(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Training(models.Model):

    name = models.CharField(max_length=64)
    start_date = models.DateField()
    end_date = models.DateField()
    start_hour = models.TimeField()
    lenght = models.IntegerField()
    weekdays = models.ManyToManyField(Weekday)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    age_category = models.ForeignKey(AgeCategory, on_delete=models.CASCADE)
    trainer = models.ForeignKey(User, related_name='trainer', on_delete=models.CASCADE)
    dojo = models.ForeignKey(Dojo, on_delete=models.CASCADE)
    trainees = models.ManyToManyField(User, related_name='trainee')
    level = models.ForeignKey(Level, on_delete=models.CASCADE)


    def __str__(self):
        return "{} ({}, {} - {}, {})".format(self.discipline, self.dojo, self.start_date, self.end_date, self.start_hour.strftime("%H:%M"))
