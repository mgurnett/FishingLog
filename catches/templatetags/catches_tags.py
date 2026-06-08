from django import template
from catches.models import *

register = template.Library()

@register.simple_tag
def week_list():
    weeks = Week.objects.all()
    return {'weeks': weeks}

@register.simple_tag
def density_display(area, stock_num):
    try:
        # Convert both to float to handle decimals and prevent integer division issues
        return f"{(float(stock_num) / float(area) /100):.0f} fish/ha"
    except (ValueError, ZeroDivisionError, TypeError):
        # Return an empty string or 0 if there's a math/type error (e.g., division by zero)
        return ''