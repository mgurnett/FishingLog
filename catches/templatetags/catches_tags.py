from django import template
from catches.models import *

register = template.Library()

@register.simple_tag
def week_list():
    weeks = Week.objects.all()
    return {'weeks': weeks}