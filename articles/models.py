from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse

from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()


class ArticleCategory(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=128)
    category = models.ManyToManyField(ArticleCategory)
    body = RichTextUploadingField()
    created_on = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    synopsis = RichTextUploadingField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'pk':self.pk, 'slug': slugify(self.title)})
