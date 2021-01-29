from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View

from utils.functions import display_name

from .forms import AddGalleryForm, AddImagesForm
from .models import Gallery, Image


class GalleriesView(View):

    def get(self, request, *args, **kwargs):
        cover_photos = {}
        
        if request.user.is_staff:
            galleries = Gallery.objects.all().order_by('-created_on')
        elif request.user.is_authenticated:
            galleries = Gallery.objects.filter(is_published=True).all().order_by('-created_on')
        else:
            galleries = Gallery.objects.filter(is_published=True, is_public=True).all().order_by('-created_on')

        for gallery in galleries:
            cover_photos[gallery] = (Image.objects.filter(gallery=gallery).order_by('order')[0])

        context = {
            'name': display_name(request.user),
            'galleries': galleries,
            'images': cover_photos,
        }

        return render(request, 'gallery/galleries.html', context)


class GalleryView(View):

    def get(self, request, *args, **kwargs):
        gallery_pk = kwargs['pk']
        gallery = Gallery.objects.filter(pk=gallery_pk).get()

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


class GalleriesListView(View):

    def get(self, request, *args, **kwargs):
        
        if not request.user.is_staff:
            raise Http404()

        galleries = Gallery.objects.all().order_by('-created_on')
        image_count = {}

        for gallery in galleries:
            image_count[gallery] = Image.objects.filter(gallery=gallery).count()

        context = {
            'name': display_name(request.user),
            'galleries': galleries,
            'image_count': image_count,
        }

        return render(request, 'gallery/galleries_list.html', context)
    
    def post(self, request, *args, **kwargs):

        galleries = Gallery.objects.all()
        
        is_published_list =  request.POST.getlist('is_published')
        is_public_list = request.POST.getlist('is_public')

        for gallery in galleries:
            if str(gallery.pk) in is_published_list:
                gallery.is_published = True
            else:
                gallery.is_published = False

            if str(gallery.pk) in is_public_list:
                gallery.is_public = True
            else:
                gallery.is_public = False
            
            gallery.save()

        return redirect('galleries_list')



class AddGalleryView(View):

    def get(self, request, *args, **kwargs):

        if not request.user.is_staff:
            raise Http404()

        context = {
            'name': display_name(request.user),
        }

        return render(request, 'gallery/gallery_add.html', context)

    def post(self, request, *args, **kwargs):

        gallery_form = AddGalleryForm(request.POST)
        images_form = AddImagesForm(request.POST, request.FILES)

        image_files = request.FILES.getlist('file_field')

        gallery = Gallery()

        if gallery_form.is_valid():
            gallery_data = gallery_form.cleaned_data

            gallery.title = gallery_data['title']
            gallery.description = gallery_data['description']
            gallery.author = request.user
            gallery.is_published = gallery_data['is_published']
            gallery.is_public = gallery_data['is_public']
            gallery.save()

            if images_form.is_valid():                
                for image_file in image_files:
                    Image.objects.create(gallery=gallery, image=image_file)

                return redirect('galleries_list')

        return redirect('gallery_add')
        

class EditGalleryView(View):

    def get(self, request, *args, **kwargs):

        if not request.user.is_staff:
            raise Http404()
        
        gallery_pk = kwargs['pk']
        gallery = Gallery.objects.filter(pk=gallery_pk).get()
        images = Image.objects.filter(gallery=gallery).all().order_by('order')

        context = {
            'name': display_name(request.user),
            'gallery': gallery,
            'images': images,
        }

        return render(request, 'gallery/gallery_edit.html', context)

    def post(self, request, *args, **kwargs):

        gallery_form = AddGalleryForm(request.POST)
        images_form = AddImagesForm(request.POST, request.FILES)

        gallery_pk = kwargs['pk']
        gallery = Gallery.objects.filter(pk=gallery_pk).get()
        images = Image.objects.filter(gallery=gallery).all()

        image_files = request.FILES.getlist('file_field')

        # change order of existing photos in gallery
        for image in images:
            order = images_form.data['order-{}'.format(image.pk)]
            if order == '':
                order = None
            image.order = order
            image.save()
            
        # add new photos if any
        if images_form.is_valid():
            for image_file in image_files:
                Image.objects.create(gallery=gallery, image=image_file)
        
        images = Image.objects.filter(gallery=gallery).all()
        
        # overwrite gallery fields with new values
        if gallery_form.is_valid():
            gallery_data = gallery_form.cleaned_data

            gallery.title = gallery_data['title']
            gallery.description = gallery_data['description']
            gallery.is_published = gallery_data['is_published']
            gallery.is_public = gallery_data['is_public']
            gallery.save()

        # remove photos marked for deleting
        images_to_remove = request.POST.getlist('delete')

        for image_pk in images_to_remove:
            Image.objects.filter(pk=image_pk).delete()

        return redirect('gallery_edit', gallery_pk)
