from django.shortcuts import render

from django.views.generic import ListView
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.urls import reverse

from .models import ColorPalette, Profile, Item, Type, Request
import operator
from functools import reduce
# Create your views here.

class CardList(ListView):
    model = Item
    template_name = 'main_cards.html'

    def get_queryset(self):
        par_set = self.load_int_list('itemcontent')
        if par_set:
            return Item.objects.filter( reduce(operator.or_, ((Q(id=q) | Q(place__id=q)) for q in par_set)  )   )
        par_set = self.load_text_list('text')
        if par_set:
            return Item.objects.filter( reduce(operator.or_, (Q(finder__icontains=q) for q in par_set)  )   )
        par_set = self.load_int_list('types')
        if par_set:
            s=reduce(operator.or_, (Q(id=q) for q in par_set)  )
            paths=Type.objects.filter( s )
            s1= reduce(operator.or_, (Q(type__root_path__startswith=q.root_path) for q in paths)  )
            return Item.objects.filter(s1)
        par_set = self.load_int_list('type')
        if par_set:
            return Item.objects.filter( reduce(operator.or_, (Q(type__id=q) for q in par_set)  )   )
        par_set = self.load_int_list('path')
        if par_set:
            return Item.get_place_tree(par_set[0])
        else:
            q=Item.objects.all()
        return q

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not ('colors' in self.request.session):
            self.request.session['colors'] = ColorPalette.get_user_palette(self.request.user)
        context['links'] = Request.get_links()
        context['buttons'] = Request.get_buttons()
        return context

    def load_text_list(self,parameter):
        return self.request.GET.get(parameter, '').lower().split()

    def load_int_list(self,parameter):
        type_id_s = self.request.GET.get(parameter, '').split()
        r=list()
        try:
            for item_s in type_id_s:
                item_i = int(item_s)
                r.append(item_i)
            return r
        except: return None



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
