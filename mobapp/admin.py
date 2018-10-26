from django.contrib import admin

from .models import Event, OwnedNumber, Registration

admin.site.register(Event)
admin.site.register(OwnedNumber)
admin.site.register(Registration)
