from django import template
import RequestManager.constants as constants
from RequestManager.models import Request

register = template.Library()

@register.filter(name='get_product_area_str')
def get_product_area_str(item: Request):
    try:
        return constants.PRODUCT_AREA[item.product_area-1][1]
    except Exception as e:
        return "Unknown Area"

