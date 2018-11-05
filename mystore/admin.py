from django.contrib import admin

# Register your models here.
from .models import Layer,Item,Type

admin.site.register(Layer)
#admin.site.register(Item)
admin.site.register(Type)

@admin.register(Item)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'full_name', 'place_path')
