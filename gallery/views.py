from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View

from utils.functions import display_name

from .models import Gallery, Image


class AllGalleriesView(View):
    def get(self, request, *args, **kwargs):
        cover_photos = {}
        
        # handling different user types and publication status
        if request.user.is_staff:
            galleries = Gallery.objects.all()
        elif request.user.is_authenticated:
            galleries = Gallery.objects.filter(is_published=True).all()
        else:
            galleries = Gallery.objects.filter(is_published=True, is_public=True).all()

        for gallery in galleries:
            cover_photos[gallery] = (Image.objects.filter(gallery=gallery).order_by('order')[0])

        context = {
            'name': display_name(request.user),
            'galleries': galleries,
            'images': cover_photos,
        }

        return render(request, 'gallery/galleries_list.html', context)


class GalleryView(View):
    def get(self, request, *args, **kwargs):
        gallery_pk = kwargs['pk']
        gallery = Gallery.objects.filter(pk=gallery_pk).get()

        # handling different user types and publication status
        if not gallery.is_published and not request.user.is_staff:
            raise Http404("Gallery does not exist!")
        elif not gallery.is_published and not request.user.is_authenticated:
            raise Http404("Gallery does not exist!")
        
        images = Image.objects.filter(gallery=gallery).all().order_by('order')

        context = {
            'name': display_name(request.user),
            'gallery': gallery,
            'images': images,
        }

        return render(request, 'gallery/gallery_details.html', context)
    