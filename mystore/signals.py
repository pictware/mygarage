from django.contrib.auth.signals import user_logged_in
from .models import ColorPalette

def set_profile_values(sender, user, request, **kwargs):
    request.session['colors'] = ColorPalette.get_user_palette(request.user)

user_logged_in.connect(set_profile_values)
