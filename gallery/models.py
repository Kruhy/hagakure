from django.db import models
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
from django.urls import reverse

User = get_user_model()


class Gallery(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('gallery', kwargs={'pk':self.pk, 'slug': slugify(self.title)})


def get_image_filename(instance, filename):
    title = instance.gallery.title
    slug = slugify(title)
    return "gallery/{}/{}".format(slug, filename)


class Image(models.Model):
    gallery = models.ForeignKey(Gallery, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_image_filename, verbose_name='Image')
    order = models.IntegerField(default=None, null=True, blank=True)
