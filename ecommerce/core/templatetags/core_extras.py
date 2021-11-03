from __future__ import absolute_import

import re

from crum import get_current_request
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from opaque_keys.edx.keys import CourseKey

from ecommerce.extensions.basket.models import Basket
from ecommerce.extensions.order.models import Order, OrderDiscount

register = template.Library()


def get_coupon_name(provided_object):
    """
    The coupon name is extracted from the 'provided_object' argument which could be an
    Order, Basket or OrderDiscount instance.

    Arguments:
        provided_object (Order or Basket or OrderDiscount): Order of the purchase,
        its basket or its OrderDiscount.

    Returns:
        str: Coupon name if found, '' otherwise.
    """
    coupon_name = ''

    if isinstance(provided_object, Order):
        discount = provided_object.basket_discounts.first()
        coupon_name = discount.voucher.name if getattr(discount, 'voucher', None) else ''
    elif isinstance(provided_object, Basket):
        coupon = provided_object.vouchers.first()
        coupon_name = coupon.name if coupon else ''
    elif isinstance(provided_object, OrderDiscount):
        coupon_name = provided_object.voucher.name if provided_object.voucher else ''

    return coupon_name


def has_request_siteconfiguration(request):
    """
    Checks that request has site/siteconfiguration.

    Returns:
        bool: True if request has site/configuration, False otherwise.
    """
    if getattr(request, 'site', None) and getattr(request.site, 'siteconfiguration', None):
        return True

    return False


def is_valid_special_coupon(coupon_name, prefix):
    """Checks if coupon_name matches the regex of a special coupon.
    The format depends on the 'prefix' argument.

    regex: r'[{prefix}]\\d.\\d'
    """
    def is_valid_prefix(prefix):
        """The prefix must be a 1-char long string."""
        if not isinstance(prefix, str):
            return False

        return len(prefix) == 1

    if not is_valid_prefix(prefix):
        return False

    return re.match(
        r'[{prefix}]\d.\d'.format(prefix=prefix),
        coupon_name,
    )


@register.simple_tag
def settings_value(name):
    """
    Retrieve a value from the site configuration or settings.

    Usage:
        {% load core_extras %}

        {% settings_value 'site_setting' as setting %}{{ setting }}
        {% settings_value 'custom_settings' as setting %}{{ setting.my_custom_setting }}

    Raises:
        AttributeError if setting not found.
    """
    request = get_current_request()

    if getattr(request, 'site', None):
        return getattr(request.site.siteconfiguration, name)

    return getattr(settings, name)


@register.simple_tag(name='is_special_coupon')
def is_special_coupon(provided_object):
    """
    Checks if 'provided_object' contains a coupon which its name meets the format criteria of a special coupon.

    - Requirements: The site.siteconfiguration.custom_settings 'REMOVE_SPECIAL_COUPON_OFFER_PREFIX' key
    should be set to properly use this tag.

    - Usage: This tag is aimed to be used for conditional logic, as follows.
        {% load core_extras %}

        {% is_special_coupon order as is_special_coupon %}

        {% if is_special_coupon %}
                Do something...
        {% endif %}

    Arguments:
        provided_object (Order or Basket or OrderDiscount): Order of the purchase,
        its basket or its OrderDiscount.

    Returns:
        bool: True if the coupon name is a valid special coupon, False otherwise.
    """
    coupon_name = get_coupon_name(provided_object)

    if not coupon_name:
        return False

    request = get_current_request()

    if not has_request_siteconfiguration(request):
        return False

    if is_valid_special_coupon(
            coupon_name,
            request.site.siteconfiguration.custom_settings.get('REMOVE_SPECIAL_COUPON_OFFER_PREFIX', '')):
        return True

    return False


@register.filter(name='get_special_coupon_data', is_safe=True)
def get_special_coupon_data(provided_object):
    """
    Retrives a custom message for the special coupon.

    Usage: This filter should only be used in conjuction with is_special_coupon tag, as follows.
        {% load core_extras %}

        {% is_special_coupon order as is_special_coupon %}

        {% if is_special_coupon %}
                {{ provided_object|get_special_coupon_data }}
        {% endif %}

    Arguments:
        provided_object (Order or Basket): Order of the purchase or its basket.

    Returns:
        str: Special coupon message.
    """
    coupon_name = get_coupon_name(provided_object)

    if not coupon_name:
        return ''

    request = get_current_request()

    if not has_request_siteconfiguration(request):
        return ''

    if is_valid_special_coupon(
            coupon_name,
            request.site.siteconfiguration.custom_settings.get('REMOVE_SPECIAL_COUPON_OFFER_PREFIX', '')):
        return '{} {}/{}'.format(
            request.site.siteconfiguration.custom_settings.get('SPECIAL_COUPON_MESSAGE', ''),
            coupon_name[1],
            coupon_name[3],
        )

    return ''


@register.tag(name='captureas')
def do_captureas(parser, token):
    """
    Capture contents of block into context.

    Source:
        https://djangosnippets.org/snippets/545/

    Example:
        {% captureas foo %}{{ foo.value }}-suffix{% endcaptureas %}
        {% if foo in bar %}{% endif %}
    """

    try:
        __, args = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError("'captureas' node requires a variable name.")
    nodelist = parser.parse(('endcaptureas',))
    parser.delete_first_token()
    return CaptureasNode(nodelist, args)


@register.filter(name='course_organization')
def course_organization(course_key):
    """
    Retrieve course organization from course key.

    Arguments:
        course_key (str): Course key.

    Returns:
        str: Course organization.
    """
    return CourseKey.from_string(course_key).org


class CaptureasNode(template.Node):
    def __init__(self, nodelist, varname):
        self.nodelist = nodelist
        self.varname = varname

    def render(self, context):
        output = mark_safe(self.nodelist.render(context).strip())
        context[self.varname] = output
        return ''
