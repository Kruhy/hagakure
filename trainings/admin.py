from django.contrib import admin

from .models import AgeCategory, Discipline, Dojo, Training, Weekday


class AgeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DojoAdmin(admin.ModelAdmin):
    list_display = ('name', 'city',)


class TrainingAdmin(admin.ModelAdmin):
    list_display = ('name', 'dojo', 'start_date', 'end_date', 'start_hour',)


class WeekdayAdmin(admin.ModelAdmin):
    list_display = ('order', 'name',)


admin.site.register(AgeCategory, AgeCategoryAdmin)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(Dojo, DojoAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(Weekday, WeekdayAdmin)
