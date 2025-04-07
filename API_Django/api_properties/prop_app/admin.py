from django.contrib import admin

from .models import HousingType, Property, Image

admin.site.register(HousingType)
admin.site.register(Property)
admin.site.register(Image)

