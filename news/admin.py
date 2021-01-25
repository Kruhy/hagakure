from django.contrib import admin

from .models import News


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'expiration_date', 'is_published', 'is_public', 'author',)


admin.site.register(News, NewsAdmin)
