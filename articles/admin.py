from django.contrib import admin

from .models import Article, ArticleCategory


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'is_published', 'is_public', 'author',)


admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(Article, ArticleAdmin)
