from django.template import Library
from django.core.cache import cache
from django.utils.http import urlquote
from django.utils.hashcompat import md5_constructor

register = Library()

def invalidate_template_cache(fragment_name, *variables):
    args = md5_constructor(u':'.join([urlquote(var) for var in variables]))
    cache_key = 'template.cache.%s.%s' % (fragment_name, args.hexdigest())
    cache.delete(cache_key)
    return

def reset_cache(parser, token):
    """
    This will reset the template cache for a given set of arguments

    Usage::

        {% load reset_cache %}
        {% if [condition] %}
            {% reset_cache [fragment_name] %}
        {% endif %}


    This tag also supports varying by a list of arguments::

        {% load reset_cache %}
        {% if [condition] %}
            {% reset_cache [fragment_name] [var1] [var2] ..  %}
        {% endif %}

        
    Which follows the built-in cache template tag structure

        {% load cache %}
        {% cache [expire_time] [fragment_name] %}
            .. some expensive processing ..
        {% endcache %}

        {% load cache %}
        {% cache [expire_time] [fragment_name] [var1] [var2] .. %}
            .. some expensive processing ..
        {% endcache %}

    Note that the reset_cache doesn't pass the [expire_time] variable
    """
    
    tokens = token.contents.split()
    if len(tokens) < 2:
        raise TemplateSyntaxError(u"'%r' tag requires at least 1 argument." % tokens[0])
    invalidate_template_cache(tokens[1], tokens[2:])
    return 
    
register.tag('reset_cache', reset_cache)
