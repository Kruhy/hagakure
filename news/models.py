from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


class News(models.Model):
    title = models.CharField(max_length=128)
    body = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    expiration_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news', kwargs={'pk':self.pk, 'slug': slugify(self.title)})
