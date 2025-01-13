from django.contrib import admin

# Register your models here.
from .models import City , Date , Time , Weather

admin.site.register(City)
admin.site.register(Date)
admin.site.register(Time)
admin.site.register(Weather)
