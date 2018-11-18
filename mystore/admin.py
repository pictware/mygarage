from django.contrib import admin

# Register your models here.
from .models import ColorPalette, Profile, Item,Type, Request


admin.site.register(ColorPalette)
admin.site.register(Profile)



@admin.register(Item)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'full_name', 'place_path')

@admin.register(Type)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'full_name', 'root_path')

@admin.register(Request)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'query_text', 'is_up_button', 'icon_class', 'is_down_link', 'link_text')
