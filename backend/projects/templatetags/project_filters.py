from django import template
import json

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter and return a list of trimmed items"""
    if isinstance(value, str):
        return [item.strip() for item in value.split(delimiter) if item.strip()]
    elif isinstance(value, list):
        return value
    return []

@register.filter
def trim(value):
    """Remove leading and trailing whitespace from a string"""
    if isinstance(value, str):
        return value.strip()
    return value

@register.filter
def get_technologies(project):
    """Get technologies as a list, handling both string and list formats"""
    if hasattr(project, 'technologies'):
        techs = project.technologies
        if isinstance(techs, str):
            # Handle JSON string
            try:
                parsed = json.loads(techs)
                if isinstance(parsed, list):
                    return parsed
            except (json.JSONDecodeError, TypeError):
                pass
            # Handle comma-separated string
            return [tech.strip() for tech in techs.split(',') if tech.strip()]
        elif isinstance(techs, list):
            return techs
    return []

@register.filter
def join_with_comma(value):
    """Join a list with commas"""
    if isinstance(value, list):
        return ', '.join(str(item) for item in value)
    return value

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary"""
    return dictionary.get(key) if dictionary else None