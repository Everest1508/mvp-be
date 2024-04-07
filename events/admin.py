from django.contrib import admin
from .models import MainEvent, SubEvent,College

class SubEventInline(admin.StackedInline):
    model = SubEvent
    extra = 1

class MainEventAdmin(admin.ModelAdmin):
    inlines = [SubEventInline]

admin.site.register(MainEvent, MainEventAdmin)
admin.site.register(SubEvent)
admin.site.register(College)
