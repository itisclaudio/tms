from prosoft.files.models import Tracking
from django import template

register = template.Library()

@register.inclusion_tag('trackings_tag.html')

def show():
	trackings = Tracking.objects.filter(show=True).prefetch_related('recruiter')[:5]
	return {'objs': trackings,}
