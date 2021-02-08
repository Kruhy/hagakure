from django.contrib import admin

from .models import TrainingMessage


class TrainingMessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'training', 'created_on', 'body',)


admin.site.register(TrainingMessage,TrainingMessageAdmin)
