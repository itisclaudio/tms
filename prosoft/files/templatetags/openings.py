from prosoft.files.models import Opening
from django import template

register = template.Library()

@register.inclusion_tag('openings_tag.html')

def show():
	openings = Opening.objects.filter(active=True, open=True).prefetch_related('skills').select_related('state')[:4]
	return {'objs': openings,}
