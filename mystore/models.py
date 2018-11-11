from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models import Q
from django.db.models import Value
from django.db.models.functions import Replace
from django.contrib.auth.models import User
from random import randint


# Create your models here.
class ColorPalette(models.Model):
    primary = models.CharField(max_length=64)
    secondary = models.CharField(max_length=64)
    tertiary = models.CharField(max_length=64)

    def get_palette(p):
        return {'primary':p.primary,'secondary':p.secondary,'tertiary':p.tertiary}


    def get_user_palette(user):
        p = None
        if user.is_authenticated:
            try:
                p = Profile.objects.get(user = user).color_palette
            except: None;
        if not p:
            count = ColorPalette.objects.all().count()
            random_index = randint(0, count - 1)
            p = ColorPalette.objects.all()[random_index]
        if p:
            return ColorPalette.get_palette(p)
        else:
            return {'primary':'f5ffc3','secondary':'612147','tertiary':'7dd8c7'}



class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    color_palette = models.OneToOneField('ColorPalette', null=True, blank=True, on_delete=models.SET_NULL)

    def clear_palette(user):
        if user.is_authenticated:
            try:
                pf = Profile.objects.get(user=user)
                pf.color_palette = None
                pf.save()
            except:
                None;
        return

    def save_palette(user, palette):
        if user.is_authenticated:
            try:
                pf, created = Profile.objects.get_or_create(user=user)
                pf.color_palette = palette
                pf.save()
            except:
                None;
        return


class Item(models.Model):
    #Items - clothes, toys, bikes, tools and what do you store in your garage?
    #
    #Bags, boxes, shalves are items too :) and the garage too :)))
    name = models.CharField(max_length=64)
    text = models.CharField(max_length=1024, default='', blank=True, verbose_name='Text')
    number_suffix = models.CharField(max_length=64, default='', blank=True,verbose_name='Suffix of number')
    type = models.ForeignKey('Type', on_delete=models.SET_NULL, null=True, verbose_name='Type of item')
    place = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Where is Item?')
    place_path = models.CharField(max_length=1024, default='', blank=True,verbose_name='Place tree path')

    class Meta:
        ordering = ['place_path']
    def __str__(self):
        return self.full_name()

    def full_name(self):
        ret = self.name
        number = self.full_number()
        ret = (ret + ' %s' % number) if number != '' else ret
        return ret

    def full_number(self):
        ret = ''
        ret += self.type.prefix() if self.type else ret
        if ret != '' and self.number_suffix != '':
            ret += self.type.item_separator
        ret += self.number_suffix
        return ret

    def full_place(self, wbr=False):
        ret = ''
        i = self
        iterations_count = getattr(settings, 'MYGARAGE_PLACE_MAX_ITERATIONS', 2)
        place_separator = getattr(settings, 'MYGARAGE_PLACE_SEPARATOR', '\\')
        while i.place and iterations_count > 0:
            ret = i.place.full_name() + ((place_separator + ('<wbr>' if wbr else '')) if ret !='' else '') + ret
            i = i.place
            iterations_count -= 1
        return ret

    def full_text(self):
        ret = self.text
        return ret

@receiver(pre_save, sender=Item)
def set_place_path(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Item.objects.get(pk=instance.pk)
        if instance.place:
            path_format = '%s.%'+getattr(settings, 'MYGARAGE_PATH_FORMAT', '6')+'d'
            instance.place_path = path_format % (instance.place.place_path, instance.id)
        else:
            path_format = '%'+getattr(settings, 'MYGARAGE_PATH_FORMAT', '6')+'d'
            instance.place_path = path_format % (instance.id)
        Item.objects.filter(~Q(id=instance.id)).filter(place_path__startswith=old_instance.place_path).\
        update(place_path=Replace('place_path', Value(old_instance.place_path),Value(instance.place_path)))

@receiver(post_save, sender=Item)
def create_place_path(sender, instance, created, **kwargs):
    if created:
        instance.save()
        # we need it, cause for new record we'v not had place_path, update and set_place_path will create it



class Type(models.Model):
    # see description below
    name = models.CharField(max_length=64)
    is_storage = models.BooleanField(default=False, verbose_name="Is it storage?")
    root = models.ForeignKey('Type', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Root of type')
    root_path = models.CharField(max_length=1024, default='', blank=True,verbose_name='Tree path')
    number_type = models.CharField(max_length=64, default='', blank=True,verbose_name='Type part of number')
    item_separator = models.CharField(max_length=64, default='-', blank=True,verbose_name='Item separator for number of this type')
    type_separator = models.CharField(max_length=64, default='', blank=True,verbose_name='Separator for prefix of this type')
    path_separator = models.CharField(max_length=64, default='\\', blank=True,verbose_name='Separator for path of this type')

    class Meta:
        ordering = ['root_path']
    def __str__(self):
        return self.full_name()

    def full_name(self, wbr=False):
        ret = self.name
        i = self
        iterations_count = getattr(settings, 'MYGARAGE_MAX_ITERATIONS', 2)
        while i.root and iterations_count > 0:
            ret = i.root.name + i.root.path_separator + ('<wbr>' if wbr else '') + ret
            i = i.root
            iterations_count -= 1
        return ret

    def full_name_wbr(self):
        return self.full_name(wbr=True)

    def prefix(self):
        ret = self.number_type
        i = self
        iterations_count = getattr(settings, 'MYGARAGE_MAX_ITERATIONS', 3)
        while i.root and iterations_count > 0:
            ret = i.type_separator + ret
            ret = i.root.number_type + ret
            i = i.root
            iterations_count -= 1
        return ret

@receiver(pre_save, sender=Type)
def set_root_path(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Type.objects.get(pk=instance.pk)
        if instance.root:
            path_format = '%s.%'+getattr(settings, 'MYGARAGE_PATH_FORMAT', '6')+'d'
            instance.root_path = path_format % (instance.root.root_path, instance.id)
        else:
            path_format = '%'+getattr(settings, 'MYGARAGE_PATH_FORMAT', '6')+'d'
            instance.root_path = path_format % (instance.id)
        Type.objects.filter(~Q(id=instance.id)).filter(root_path__startswith=old_instance.root_path).\
        update(root_path=Replace('root_path', Value(old_instance.root_path),Value(instance.root_path)))

@receiver(post_save, sender=Type)
def create_root_path(sender, instance, created, **kwargs):
    if created:
        instance.save()
        # we need it, cause for new record we'v not had root_path, update and set_root_path will create it

#class Type
    # Titles of types of your items - "boots","jackets","tools","spare parts", etc.
    #     field "is_storage"  = False
    #
    # Another kind of types is "storages" - "wardrobes", "racks", "boxes", "cases",
    #  "bookcases", "shelves". Garage is a storage too.
    #     field "is_storage"  = True
    #
    # Some types may have root parents:
    #   - for "socks" and "jackets" root is "clothes"
    #   - for "wheels" and "spare parts" root is "auto"
    #   - etc.
    # You can not use a parent root if you do not need it,
    #  but it may allow to organize the correct search for categories of things.
    #
    # ---------------------------------
    #Example for "garage":
    # 1 - "the garage", is_storage = True, no root
    # 2 - "racks", is_storage = True, no root
    # 3 - "boxes and cases", is_storage = True, no root
    #
    # 4 - "clothes", is_storage = False, no root
    # 5 - "outerwear", is_storage = False, root = "clothes"
    # 6 - "underwear", is_storage = False, root = "clothes"
    #
    # 7 - "boots", is_storage = False, no root
    #
    # 8 - "auto", is_storage = False, no root
    # 9 - "spare parts", is_storage = False, root = "auto"
    # 10- "tires", is_storage = False, root = "auto"
    # ...
    # ---------------------------------
    #Example for "library":
    # 1 - "the library", is_storage = True, no root
    # 2 - "bookcases", is_storage = True, no root
    # 3 - "shelves", is_storage = True, no root
    #
    # 4 - "books", is_storage = False, no root
    # 5 - "fiction", is_storage = False, root = "books"
    # 6 - "adventure", is_storage = False, root = "fiction"
    # 7 - "fantasy", is_storage = False, root = "fiction"
    # ...
    # 87- "art & photos", is_storage = False, root = "books"
    # 88- "architecture", is_storage = False, root = "art & photos"
    # 89- "art history", is_storage = False, root = "art & photos"
    # ...
    # ---------------------------------
import mystore.signals
