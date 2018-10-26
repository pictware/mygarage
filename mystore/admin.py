from django.contrib import admin

# Register your models here.
from .models import Layer,Item,Type

admin.site.register(Layer)
admin.site.register(Item)
admin.site.register(Type)
