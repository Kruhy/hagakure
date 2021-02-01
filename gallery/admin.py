from django.contrib import admin


from .models import Gallery, Image

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'is_published', 'is_public')


class ImageAdmin(admin.ModelAdmin):
    list_display = ('gallery', 'image',)


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Image, ImageAdmin)
