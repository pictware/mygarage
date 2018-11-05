from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape, escape
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def set_nbsp(value, autoescape=True):
    return mark_safe(escape(value).replace(' ', '&nbsp;'))

@register.filter(needs_autoescape=True)
@stringfilter
def set_shy(value, autoescape=True):
    return mark_safe(escape(value).replace('&lt;wbr&gt;', '<wbr>'))


@register.filter(name='has_group')
def has_group(user_id, group_name):
    try:
        result=User.objects.get(pk=user_id).groups.filter(name=group_name).exists()
    except:
        result=False
    return result
