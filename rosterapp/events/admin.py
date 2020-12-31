from django.contrib import admin
from .models import Event,Availability,FinalRoster
# Register your models here.
admin.site.register(Event)
admin.site.register(Availability)
admin.site.register(FinalRoster)
