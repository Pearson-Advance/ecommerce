from __future__ import absolute_import

from crum import get_current_request
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from opaque_keys.edx.keys import CourseKey

register = template.Library()


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

    if request.site:
        return getattr(request.site.siteconfiguration, name)

    return getattr(settings, name)


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
