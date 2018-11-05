from django.shortcuts import render

from django.views.generic import ListView
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import Layer, Item, Type

# Create your views here.

class CardList(ListView):
    model = Item
    template_name = 'main_cards.html'

    def get_queryset(self):
        q=Item.objects.all()
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


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
