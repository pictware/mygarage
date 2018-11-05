from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.db.models import Q
from django.db.models import Value
from django.db.models.functions import Replace

# Create your models here.
class Layer(models.Model):
    #Layer for your storage - garages, shalves, boxes and other
    #Example:
    # 1 - "the garage"
    # 2 - "shalves"
    # 3 - "storages" (boxes, bags etc.)
    # 4 - "things" (clothes, toys, bikes, tools etc.)

    level = models.IntegerField()
    name = models.CharField(max_length=64)

    class Meta:
        ordering = ['level']
    def __str__(self):
        return self.name

class Item(models.Model):
    #Items - clothes, toys, bikes, tools and what do you store in your garage?
    #
    #Bags, boxes, shalves are items too :) and the garage too :)))
    name = models.CharField(max_length=64)
    text = models.CharField(max_length=1024, default='', blank=True, verbose_name='Text')
    layer = models.ForeignKey('Layer', on_delete=models.SET_NULL, null=True, verbose_name='Layer of item')
    number_suffix = models.CharField(max_length=64, default='', blank=True,verbose_name='Suffix of number')
    type = models.ForeignKey('Type', on_delete=models.SET_NULL, null=True, verbose_name='Type of item')
    place = models.ForeignKey('Item', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Where is Item?')


    class Meta:
        ordering = ['pk']
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

class Type(models.Model):
    #Titles of types of your items - "boots","jacket","tool","spare part", etc.
    name = models.CharField(max_length=64)
    root = models.ForeignKey('Type', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Root of type')
    root_path = models.CharField(max_length=1024, default='', blank=True,verbose_name='Tree_path')
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
