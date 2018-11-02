from django.shortcuts import render

from django.views.generic import ListView
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404

from .models import Layer, Item, Type

# Create your views here.

class MainList(ListView):
    model = Item
    context_object_name = 'item_none'
    template_name = 'main_cards.html'

    def get_queryset(self):
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
