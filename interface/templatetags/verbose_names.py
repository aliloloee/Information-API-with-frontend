from django import template
register = template.Library()

@register.filter(name='reveal')
def get_verbose_field_name(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()

# How to use in templates => {% instance|reveal:"field_name" %}