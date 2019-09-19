from django.contrib import admin

# Register your models here.

from .models import Event, OldEvent, Question

admin.site.register(Event)
admin.site.register(OldEvent)
admin.site.register(Question)
