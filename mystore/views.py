from django.shortcuts import render

from django.views.generic import ListView
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.urls import reverse

from .models import ColorPalette, Profile, Item, Type
import operator
from functools import reduce
# Create your views here.

class CardList(ListView):
    model = Item
    template_name = 'main_cards.html'



    def get_queryset(self):
        item_id = self.s_itemcontent()
        if item_id > 0:
            return Item.objects.filter(Q(id=item_id) | Q(place__id=item_id))
        text = self.s_text()
        if text != '':
            text_list = text.split()
            #return Item.objects.filter(finder__contains=text)
            return Item.objects.filter( reduce(operator.or_, (Q(finder__icontains=q) for q in text_list)  )   )

        else:
            q=Item.objects.all()
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not ('colors' in self.request.session):
            self.request.session['colors'] = ColorPalette.get_user_palette(self.request.user)
        return context

    def s_itemcontent(self):
        item_id_s = self.request.GET.get('itemcontent', '')
        try:  return int(item_id_s)
        except: return 0

    def s_text(self):
        return self.request.GET.get('text', '').lower()



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
    return HttpResponseRedirect((reverse('home')+'?'+request.GET.urlencode()) if request.GET.urlencode() != '' else reverse('home'))

def setRandomColor(request):
    Profile.clear_palette(request.user)
    request.session['colors'] = ColorPalette.get_user_palette(request.user)
    return HttpResponseRedirect((reverse('home')+'?'+request.GET.urlencode()) if request.GET.urlencode() != '' else reverse('home'))




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
    return HttpResponseRedirect((reverse('home')+'?'+request.GET.urlencode()) if request.GET.urlencode() != '' else reverse('home'))
