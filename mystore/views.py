from django.shortcuts import render

from django.views.generic import ListView
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import ColorPalette, Profile, Item, Type

# Create your views here.

class CardList(ListView):
    model = Item
    template_name = 'main_cards.html'

    def get_queryset(self):
        q=Item.objects.all()
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not ('colors' in self.request.session):
            self.request.session['colors'] = ColorPalette.get_user_palette(self.request.user)
        return context

class Colors(ListView):
    model = ColorPalette
    template_name = 'colors.html'

    def get_queryset(self):
        q=ColorPalette.objects.all().order_by('?')[0:6]
        return q

def setColor(request, id):
    palette = get_object_or_404(ColorPalette, id=id)
    Profile.save_palette(request.user, palette)
    request.session['colors'] = ColorPalette.get_palette(palette)
    return HttpResponseRedirect("/")

def setRandomColor(request):
    Profile.clear_palette(request.user)
    request.session['colors'] = ColorPalette.get_user_palette(request.user)
    return HttpResponseRedirect("/")




def changemode(request, mode="photo"):
    if (mode == "list"):
        request.session['hide_photo'] = False
        request.session['is_list'] = True
    elif (mode == "nophoto"):
        request.session['hide_photo'] = True
        request.session['is_list'] = False
    else:
        request.session['hide_photo'] = False
        request.session['is_list'] = False
    return HttpResponseRedirect("/")
