"""filters to be used in template
Filter that can carry out complex python operation in template files
Need to be placed in 'templatetags' folder of each 'INSTALLED_APP' folder for it to work
Need to include template

Each filter function will need to have a '@request.filter(name='[NAME]') above
This makes sure that this can be used in the template files under the format
arg1|NAME(arg2, agr3, ...)
"""

from django import template
import RequestManager.constants as constants
from RequestManager.models import Request

register = template.Library()


@register.filter(name='get_product_area_str')
def get_product_area_str(item: Request):
    """Get the product area string from the product area int field

    Parameters
    ----------
    item : Request
        the Request item to be displayed
    """
    try:
        return constants.PRODUCT_AREA[item.product_area-1][1]
    except Exception as e:
        return "Unknown Area"

