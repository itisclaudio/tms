from prosoft.files.models import Reminder
from django import template

register = template.Library()

@register.inclusion_tag('reminders_private_tag.html')

def show_reminders(user):
	#objs = Reminder.objects.filter(active=1).select_related('dish','owner__user').order_by('-datetime')[:4]
	#objs = Reminder.objects.filter(active=1).select_related('recruiter').order_by('-datetime')[:4]
	objs = Reminder.objects.filter(active=True,recruiter=user).order_by('-datetime')[:4]
	#print "in show_reminders"
	#objs = Reminder.objects.all()
	return {'objs': objs,}
