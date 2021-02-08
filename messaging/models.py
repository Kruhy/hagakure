from django.db import models
from django.contrib.auth import get_user_model


from trainings.models import Training

User = get_user_model()


class TrainingMessage(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    body = models.CharField(max_length=256)
