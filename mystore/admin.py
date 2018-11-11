from django.contrib import admin

# Register your models here.
from .models import ColorPalette, Profile, Item,Type


admin.site.register(ColorPalette)
admin.site.register(Profile)
admin.site.register(Type)

@admin.register(Item)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'full_name', 'place_path')
