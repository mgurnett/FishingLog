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
        return f"{(float(stock_num) / float(area) / 100):.0f} fish/ha"
    except (ValueError, ZeroDivisionError, TypeError):
        # Return an empty string or 0 if there's a math/type error
        return ''

@register.simple_tag
def full_history_average(stockings_list):
    try:
        total_fish = 0
        unique_years = set()
        
        for stock in stockings_list:
            if stock.number and stock.date_stocked:
                # 1. Clean formatting commas from the numbers
                clean_num = str(stock.number).replace(',', '').strip()
                total_fish += float(clean_num)
                
                # 2. Track the unique years
                unique_years.add(stock.date_stocked.year)
                
        year_count = len(unique_years)
        if year_count > 0:
            return f"{total_fish / year_count:.0f}"
    except Exception:
        pass
    return "0"