from django.contrib import admin

from .models import AgeCategory, Discipline, Dojo, Level, Training, Weekday


class AgeCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)


class DisciplineAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)


class DojoAdmin(admin.ModelAdmin):
    list_display = ('name', 'city',)


class TrainingAdmin(admin.ModelAdmin):
    list_display = ('name', 'dojo', 'start_date', 'end_date', 'start_hour',)


class WeekdayAdmin(admin.ModelAdmin):
    list_display = ('order', 'name',)


class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description',)


admin.site.register(AgeCategory, AgeCategoryAdmin)
admin.site.register(Discipline, DisciplineAdmin)
admin.site.register(Dojo, DojoAdmin)
admin.site.register(Training, TrainingAdmin)
admin.site.register(Weekday, WeekdayAdmin)
admin.site.register(Level, LevelAdmin)
