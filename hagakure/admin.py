from django.contrib import admin

from .models import MembersBio


class MembersBioAdmin(admin.ModelAdmin):
    list_display = ('member', 'bio',)


admin.site.register(MembersBio, MembersBioAdmin)
