from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class MembersBio(models.Model):
    member = models.ForeignKey(User, related_name='member', on_delete=models.CASCADE)
    bio = models.TextField()
    photo = models.ImageField(upload_to='members/')

    def __str__(self):
        return "{} {}".format(self.member.first_name, self.member.last_name)
