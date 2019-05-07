from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone #Applicant
from django.contrib.auth import login,logout,authenticate

import os #To delete applicants docs

from django.core.paginator import Paginator, EmptyPage, InvalidPage #For pagination

from django.views.generic.edit import DeleteView #ClassBased Views (Delete for now)
from django.core.urlresolvers import reverse_lazy #ClassBased Views (Delete for now)
from django.http import Http404 #ClassBased Views (Delete Reminder for now)

import operator #opening_view
from operator import or_, and_ #For opening_view
from django.core.mail import EmailMultiAlternatives, send_mail, EmailMessage #To send emails
from django.db.models import Q ,get_model #Q:opening_view, get_model:reminder_new
from datetime import datetime #To calculate todays date #activitynew_view, applicationnew_view

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION #to track changes made by users
from django.contrib.contenttypes.models import ContentType #to track changes made by users
from django.utils.encoding import force_unicode #to track changes made by users

from django.contrib.auth.models import User
from django.db.models.aggregates import Count
from prosoft.files.models import (
	Activity,
	Applicant,
	Applicant_Doc,
	Application,
	Member,
	Opening,
	Profile,
	Profile_Doc,
	Reminder,
	Skill,
	Tracking,
	Vendor,
	)
from prosoft.files.forms import (
	activity_Form,
	activity_app_Form,
	activity_edit_Form,
	applicationedit_Form,
	applicationnew_Form,
	profile_applicant_Form,
	applicationnew_profile_Form,
	applicationnew_opening_Form,
	applicantdocnew_Form,
	applicationnewboth_Form,
	login_Form,
	applicant_Form,
	opening_Form,
	skill_Form,
	skilledit_Form,
	#skillprofileedit_Form,
	profile_Form,
	profiledocnew_Form,
	profile_edit_Form,
	recruiter_Form,
	recruiteredit_Form,
	reminder_Form,
	search_Form,
	UpdatePasswordForm,
	vendor_Form,
)

def get_months(months,years):
	if (months != '' or years != ''):
		if months == '':
			months = 0
		if years == '':
			years = 0
		total = int(months) + int(years)*12
	else:
		total = None
	return total

def main_view(request):
	# Applicants:
	applicants_tot = Applicant.objects.filter(active=True).annotate(profiles_count=Count('profile')).annotate(app_count=Count('profile__applications'))
	applicants_tot_c = applicants_tot.count()
	applicants = applicants_tot[:7]
	applicants_counter = applicants.count()
	#Profiles:
	profiles_tot = Profile.objects.all().prefetch_related('skills','skills_sec').annotate(app_count=Count('applications')).select_related('applicant','applicant__state','applicant__country').order_by('applicant__firstname')
	profiles_tot_c = profiles_tot.count()
	profiles = profiles_tot[:7]
	profiles_counter = profiles.count()
	#Activities:
	activities_tot = Activity.objects.all().prefetch_related('application','recruiter')
	activities_tot_c = activities_tot.count()
	activities = activities_tot[:7]
	activities_counter = activities.count()
	#Openings:
	#openings = Opening.objects.filter(active=True).annotate(app_count=Count('applications'))[:7]
	openings_tot = Opening.objects.filter(active=True).prefetch_related('skills').annotate(app_count=Count('applications'))
	openings_tot_c = openings_tot.count()
	openings = openings_tot[:7]
	openings_counter = openings.count()

	cxt = {
		'applicants':applicants,'applicants_tot_c':applicants_tot_c,'applicants_counter':applicants_counter,
		'profiles':profiles, 'profiles_tot_c':profiles_tot_c,'profiles_counter':profiles_counter, 
		'activities':activities ,'activities_tot_c':activities_tot_c, 'activities_counter':activities_counter,
		'openings':openings, 'openings_tot_c':openings_tot_c, 'openings_counter':openings_counter,
		}
	return render_to_response('_main.html',cxt,context_instance=RequestContext(request))
	
def searchquick_view(request):
	if request.method == "POST":
		form = search_Form(request.POST or None)
		if form.is_valid():
			search = form.cleaned_data['search']
			search = search.strip()#Removes beginning and ending blanks
			return searchquickres_view(request,0,search,1)
	return searchquickres_view(request)

def searchquickres_view(request,alert=None,search=None,page=None):
	cxt = {}
	if (len(search) > 0):
		# Applicants
		applicants = Applicant.objects.filter(active=True).prefetch_related('state','country').annotate(profiles_count=Count('profile'))
		search_list = search.lower().split(' ')
		applicants = applicants.filter(reduce(or_, [Q(firstname__icontains=c)|Q(lastname__icontains=c) for c in search_list])).distinct()
		counter_applicants = applicants.count()
		# Profiles:
		profiles = Profile.objects.all().prefetch_related('applicant').annotate(app_count=Count('applications'))
		profiles = profiles.filter(reduce(or_, [Q(applicant__firstname__icontains=c)|
												Q(applicant__lastname__icontains=c) |
												Q(skills__name__icontains=c) 
												for c in search_list])).distinct().prefetch_related('applicant')
		profiles_counter = profiles.count()
		# Applications
		applications = Application.objects.all().prefetch_related('profile','opening').annotate(activities_count=Count('activities'))
		applications = applications.filter(reduce(or_, [Q(profile__applicant__firstname__icontains=c)|Q(profile__applicant__lastname__icontains=c)|Q(opening__role__icontains=c) for c in search_list])).distinct()
		applications_counter = applications.count()
		cxt = {'search':search,'applicants':applicants,'counter_applicants':counter_applicants,'profiles':profiles,'profiles_counter':profiles_counter,'applications':applications,'applications_counter':applications_counter}
		return render_to_response('searchquickresults.html',cxt,context_instance=RequestContext(request))
	return render_to_response('searchquickresults.html',cxt,context_instance=RequestContext(request))
	
def reports_view(request):
	return render_to_response('reports.html',context_instance=RequestContext(request))
"""
def history_view(request):
	#logs = LogEntry.objects.exclude(change_message="No fields changed.").annotate(uname=Member.objects.get(pk=2)).order_by('-action_time')[:20]
	logs = LogEntry.objects.all().order_by('-action_time')[:20]
	logCount = LogEntry.objects.exclude(change_message="No fields changed.").order_by('-action_time')[:20].count()
	members = Member.objects.all()
	#return render(request, template, {"logs":logs, "logCount":logCount})
	cxt = {"logs":logs, "logCount":logCount,  "members":members}
	return render_to_response('history.html',cxt,context_instance=RequestContext(request))
"""
########################################
#######    T R A C K I N G       #######
########################################
def RegisterTracking(recruiter,type,datetime,entity,entity_id=None,entity_field=None,old=None,new=None,extrainfo=None):
	tracking = Tracking()
	tracking.recruiter = recruiter
	tracking.datetime = datetime
	tracking.type = type
	tracking.entity = entity
	tracking.entity_id = entity_id
	tracking.entity_field = entity_field
	tracking.old = old
	tracking.new = new
	tracking.extrainfo = extrainfo
	tracking.save()
	print datetime
	print tracking.datetime

def trackings_view(request, page=None):
	member = Member.objects.get(user=request.user)
	if member.role < 3:
		#tracking = Tracking.objects.all()[:100]
		objects = Tracking.objects.all()
		paginator = Paginator(objects,30)
		try:
			page = int(page)
		except:
			page = 1
		try:
			paginatorlist = paginator.page(page)
		except (EmptyPage, InvalidPage):
			paginatorlist = paginator.page(paginator.num_pages)
		cxt = {'paginatorlist':paginatorlist}
		#trackingCount = tracking.count()
		#cxt = {"tracking":tracking, "trackingCount":trackingCount}
		return render_to_response('trackings.html',cxt,context_instance=RequestContext(request))
	return render_to_response('no_permission.html',context_instance=RequestContext(request))
	
def tracking_view(request, id):
	member = Member.objects.get(user=request.user)
	if member.role < 3:
		obj = Tracking.objects.get(id=id)
		return render_to_response('tracking.html',{'obj':obj,},context_instance=RequestContext(request))
	return render_to_response('no_permission.html',context_instance=RequestContext(request))
	
class TrackingDelete(DeleteView):
	model = Tracking
	success_url = reverse_lazy('view_trackings')

########################################
#######    S Y S T E M       #######
########################################
"""
def SaveEmailQueue(username,obj,action,url=None):
	send = EmailQueue()
	send.date = datetime.now()
	send.username = username
	send.object = obj
	send.action = action
	if url:
		send.url_plus = url
	send.sent_flag = False
	send.save()
"""
########################################
#######      A C C O U N T       #######
########################################
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')
	
def login_view(request):
	next = mensa = ""
	user_sent = ""
	user = User.objects.none()
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "GET":
			next = request.GET.get('next')
			if next:
				print "There is next: "+next
		if request.method == "POST":
			next = request.GET.get('next')
			form = login_Form(request.POST)
			if form.is_valid():
				username_form = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username_form,password=password)
				#print "autenticated!"
				if usuario is not None:
					login(request,usuario)
					# the password verified for the user
					if next:
						return HttpResponseRedirect(next)
					return HttpResponseRedirect('/')
				else:
					mensa = 1 #Wrong username or passwrod
			else:
				#print "Form not valid"
				ctx = {'form':form,'next':next,'user_req':user}
				return render_to_response('login.html',ctx,context_instance=RequestContext(request))
	form = login_Form(initial={'username':user_sent})
	ctx = {'form':form,'next':next,'user_req':user,'mensa':mensa}
	return render_to_response('login.html',ctx,context_instance=RequestContext(request))

def account_password_view(request):
	req_user = request.user
	if request.method == "POST":
		form = UpdatePasswordForm(request.POST, instance=req_user)
		form.actual_user = req_user
		if form.is_valid():
			password = form.cleaned_data['password']
			req_user.set_password(password)
			form.save()
			logout(request)
			return HttpResponseRedirect('/login/')
		else:
			ctx = {'form':form }
			return render_to_response('account_password.html',ctx,context_instance=RequestContext(request))
	form = UpdatePasswordForm(instance=req_user)
	form.actual_user = req_user
	ctx = {'form':form, 'user':req_user}
	return render_to_response('account_password.html',ctx,context_instance=RequestContext(request))

########################################
#######    A C T I V I T Y     #########
########################################

def activities_view(request):
	objs = Activity.objects.all().prefetch_related('application','recruiter')
	objs_counter = objs.count()
	cxt = {'objs':objs,'counter':objs_counter}
	return render_to_response('activities.html',cxt,context_instance=RequestContext(request))

def activities_rpt_view(request):
	objs = Activity.objects.all().prefetch_related('application','recruiter')
	counter = objs.count()
	cxt = {'objs':objs, 'counter':counter}
	return render_to_response('activities_rpt.html',cxt,context_instance=RequestContext(request))

def activity_view(request, id):
	obj = Activity.objects.get(id=id)
	objs_total = Activity.objects.filter(application=obj.application).exclude(pk=obj.id).count()
	objs = Activity.objects.filter(application=obj.application).exclude(pk=obj.id).order_by('-datetime')[:10]
	counter = objs.count()
	cxt = {'obj':obj, 'objs':objs, 'counter':counter,'total':objs_total}
	return render_to_response('activity.html',cxt,context_instance=RequestContext(request))

def activity_rpt_view(request, id):
	obj = Activity.objects.get(id=id)
	cxt = {'obj':obj,}
	return render_to_response('activity_rpt.html',cxt,context_instance=RequestContext(request))

def qsearch_activity_view(request):
	search = ""
	objs = Activity.objects.all().prefetch_related('application','application__profile__applicant','application__opening','recruiter')
	if request.method == "POST":
		form = search_Form(request.POST or None)
		if form.is_valid():
			search = form.cleaned_data['search']
			if search != "":
				search_list = search.lower().split(' ')
				objs = objs.filter(reduce(or_, [Q(application__profile__applicant__firstname__icontains=c)|Q(application__profile__applicant__firstname__icontains=c)|Q(application__opening__role__icontains=c) for c in search_list])).distinct()
	objs_counter = objs.count()
	cxt = {'search':search,'objs':objs,'counter':objs_counter}
	return render_to_response('activities.html',cxt,context_instance=RequestContext(request))

def activityedit_view(request, id):
	obj = Activity.objects.get(pk=id)
	initial_data = {'notes':obj.notes,'type':obj.type}
	activities = Activity.objects.filter(application=obj.application).exclude(pk=obj.id)
	if request.method == "POST":
		form = activity_edit_Form(request.POST, initial=initial_data)
		if form.is_valid():
			type = form.cleaned_data['type']
			notes = form.cleaned_data['notes']
			obj.datetime = datetime.now()
			obj.type = type
			obj.notes = notes
			obj.save() # Save info to Database
			if form.has_changed():
				for item in form.changed_data:
					if item == 'type':
						old = dict(form.INTERACTION_TYPE)[initial_data[item]]
						new = dict(form.INTERACTION_TYPE)[form.cleaned_data[item]]
						RegisterTracking(request.user,'1',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,item,old,new,None)
					else:
						RegisterTracking(request.user,'1',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,item,initial_data[item],form.cleaned_data[item],None)
			#return HttpResponseRedirect('/activity/%s/'%(obj.id))
			return redirect('view_activity', id=obj.id)
		else:
			ctx = {'form':form,'activities':activities}
			return render_to_response('activity_edit.html',ctx,context_instance=RequestContext(request))
	form = activity_edit_Form(initial=initial_data)
	ctx = {'form':form,'obj':obj,'activities':activities}
	return render_to_response('activity_edit.html',ctx,context_instance=RequestContext(request))

def activitynew_view(request):
	activities_total = Activity.objects.all().distinct().count()
	activities = Activity.objects.all().select_related('application','application__profile','recruiter').prefetch_related('application__opening__skills','application__profile__skills')[:10]
	objs_counter = activities.count()
	if request.method == "POST":
		form = activity_Form(request.POST)
		if form.is_valid():
			#print "Form Valid"
			application = form.cleaned_data['application']
			type = form.cleaned_data['type']
			notes = form.cleaned_data['notes']
			newobj = Activity()
			newobj.application = application
			newobj.recruiter = request.user
			newobj.datetime = datetime.now()
			newobj.type = type
			newobj.notes = notes
			newobj.save() # Save info to Database
			applic = Application.objects.get(pk=application.id)
			applic.status = "2"
			applic.save()
			RegisterTracking(request.user,'2',timezone.localtime(timezone.now()),newobj._meta.model_name,newobj.id,None,None,None,None)
			#return HttpResponseRedirect('/application/%s/'%(newobj.application.id))
			return redirect('view_application', id=newobj.application.id)
		else:
			ctx = {'form':form,'activities':activities}
			return render_to_response('activity_new.html',ctx,context_instance=RequestContext(request))
	form = activity_Form()
	ctx = {'form':form,'activities':activities,'counter':objs_counter,'total':activities_total}
	return render_to_response('activity_new.html',ctx,context_instance=RequestContext(request))

def activitynew_application_view(request, application_id):
	obj = Application.objects.get(pk=application_id)
	activities_total = Activity.objects.filter(application=application_id).count()
	activities = Activity.objects.filter(application=application_id).prefetch_related('application','recruiter')[:10]
	counter = activities.count()
	if request.method == "POST":
		form = activity_app_Form(request.POST)
		if form.is_valid():
			#print "Form Valid"
			type = form.cleaned_data['type']
			notes = form.cleaned_data['notes']
			newobj = Activity()
			newobj.application = obj
			newobj.recruiter = request.user
			newobj.datetime = datetime.now()
			newobj.type = type
			newobj.notes = notes
			newobj.save() # Save info to Database
			obj.status = '2'
			obj.save()
			RegisterTracking(request.user,'2',timezone.localtime(timezone.now()),newobj._meta.model_name,newobj.id,None,None,None,None)
			#return HttpResponseRedirect('/application/%s/'%(newobj.application.id))
			return redirect('view_application', id=newobj.application.id)
		else:
			ctx = {'form':form,'obj':obj,'activities':activities,'counter':counter,'total':activities_total}
			return render_to_response('activity_app_new.html',ctx,context_instance=RequestContext(request))
	form = activity_app_Form(initial={'application':obj})
	ctx = {'form':form,'obj':obj,'activities':activities,'counter':counter,'total':activities_total}
	return render_to_response('activity_app_new.html',ctx,context_instance=RequestContext(request))

def activity_delete_view(request, id):
	req_user = request.user
	obj = Activity.objects.get(pk=id)
	if obj.recruiter == req_user:
		# User requesting = recruiter owner of activity.
		extra = '<b>Application:</b> %s<br/><b>Type:</b> %s<br/> <b>Notes:</b> %s' % (obj.application, obj.get_type_display(), obj.notes )
		RegisterTracking(request.user,'3',timezone.localtime(timezone.now()),obj._meta.model_name.capitalize(),None,None,None,None,extra)
		# Proceed to delete
		obj.delete()
		return redirect('view_main')
	else:
		# Request user is not owner of entity,
		# Do not delete and redirect
		return redirect('view_main')
	
########################################
#######   A P P L I C A N T    #########
########################################

def applicants_view(request):
	objs = Applicant.objects.filter(active=True).annotate(profiles_count=Count('profile')).annotate(app_count=Count('profile__applications'))
	objs_counter = objs.count()
	cxt = {'objs':objs,'counter':objs_counter}
	return render_to_response('applicants.html',cxt,context_instance=RequestContext(request))
	
def applicants_rpt_view(request):
	objs = Applicant.objects.filter(active=True).annotate(profiles_count=Count('profile')).annotate(app_count=Count('profile__applications'))
	objs_counter = objs.count()
	cxt = {'objs':objs,'counter':objs_counter}
	return render_to_response('applicants_rpt.html',cxt,context_instance=RequestContext(request))
	
def qsearch_applicant_view(request):
	search = ""
	objs = Applicant.objects.filter(active=True).prefetch_related('state','country').annotate(profiles_count=Count('profile'))
	if request.method == "POST":
		form = search_Form(request.POST or None)
		if form.is_valid():
			search = form.cleaned_data['search']
			if search != "":
				search_list = search.lower().split(' ')
				objs = objs.filter(reduce(or_, [Q(firstname__icontains=c)|Q(lastname__icontains=c) for c in search_list])).distinct()
	objs_counter = objs.count()
	cxt = {'search':search,'objs':objs,'counter':objs_counter}
	return render_to_response('applicants.html',cxt,context_instance=RequestContext(request))
	
def applicant_view(request, id):
	obj = Applicant.objects.get(id=id)
	documents = Applicant_Doc.objects.filter(applicant=obj).order_by('-datetime')
	profiles_total = Profile.objects.filter(applicant__id=id).annotate(app_count=Count('applications')).prefetch_related('skills','skills_sec').distinct().count()
	profiles = Profile.objects.filter(applicant__id=id).annotate(app_count=Count('applications')).prefetch_related('skills','skills_sec').distinct()[:10]
	objs_counter = profiles.count()
	cxt = {'obj':obj,'profiles':profiles,'documents':documents,'counter':objs_counter,'total':profiles_total}
	return render_to_response('applicant.html',cxt,context_instance=RequestContext(request))

def applicant_rpt_view(request, id):
	obj = Applicant.objects.get(id=id)
	documents = Applicant_Doc.objects.filter(applicant=obj).order_by('-datetime')
	profiles = Profile.objects.filter(applicant__id=id).prefetch_related('skills','skills_sec')
	cxt = {'obj':obj,'profiles':profiles,'documents':documents}
	return render_to_response('applicant_rpt.html',cxt,context_instance=RequestContext(request))

def applicantnew_view(request):
	if str(request.user) == "Visitor":
		raise Http404
	if request.method == "POST":
		form = applicant_Form(request.POST)
		if form.is_valid():
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']
			email = form.cleaned_data['email']
			dob = form.cleaned_data['dob']
			phone_1 = form.cleaned_data['phone_1']
			phone_2= form.cleaned_data['phone_2']
			work_status = form.cleaned_data['work_status']
			available = form.cleaned_data['available']
			righttorep = form.cleaned_data['righttorep']
			relocation = form.cleaned_data['relocation']
			country = form.cleaned_data['country']
			address = form.cleaned_data['address']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			t_exp_months = form.cleaned_data['t_exp_months']
			t_exp_years = form.cleaned_data['t_exp_years']
			us_exp_months = form.cleaned_data['us_exp_months']
			us_exp_years = form.cleaned_data['us_exp_years']
			education = form.cleaned_data['education']
			besttime = form.cleaned_data['besttime']
			salary_cur = form.cleaned_data['salary_cur']
			obj = Applicant()
			obj.firstname = firstname
			obj.lastname = lastname
			obj.email = email
			obj.dob = dob
			obj.phone_1 = phone_1
			obj.phone_2 = phone_2
			obj.work_status = work_status
			obj.available = available
			obj.righttorep = righttorep
			obj.relocation = relocation
			obj.country = country
			obj.address = address
			obj.city = city
			obj.state = state
			obj.zipcode = zipcode
			#Converts years and months to months total if value is != than 99 (empty):
			if (t_exp_months != '' or t_exp_years != ''):
				if t_exp_months == '':
					t_exp_months = 0
				if t_exp_years == '':
					t_exp_years = 0
				obj.experience = int(t_exp_months) + int(t_exp_years)*12
			else:
				obj.experience = None
			if (us_exp_months != '' or us_exp_years != ''):
				if us_exp_months == '':
					us_exp_months = 0
				if us_exp_years == '':
					us_exp_years = 0
				obj.usexperience = int(us_exp_months) + int(us_exp_years)*12
			else:
				obj.usexperience = None
			obj.education = education
			obj.besttime = besttime
			obj.salary_cur = salary_cur
			obj.active = True
			obj.updated = timezone.localtime(timezone.now())
			obj.created = timezone.localtime(timezone.now())
			obj.save() # Save info to Database
			extra = '<b>Name: </b> %s<br/><b>Work Status:</b> %s' % (obj ,dict(form.WORK_STATUS)[obj.work_status])
			RegisterTracking(request.user,'2',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,None,None,None,extra)
			return redirect('view_applicant', id=obj.id)
		else:
			ctx = {'form':form}
			return render_to_response('applicant_new.html',ctx,context_instance=RequestContext(request))
	form= applicant_Form()
	ctx = {'form':form}
	return render_to_response('applicant_new.html',ctx,context_instance=RequestContext(request))

def applicantedit_view(request, id):
	if str(request.user) == "Visitor":
		raise Http404
	obj = Applicant.objects.get(pk=id)
	initial_data={'firstname':obj.firstname,'lastname':obj.lastname,'email':obj.email,
		'dob':obj.dob,'phone_1':obj.phone_1 ,'phone_2':obj.phone_2 ,'work_status':obj.work_status, 
		'available':obj.available ,'relocation':obj.relocation ,'righttorep':obj.righttorep,
		'country':obj.country ,'address':obj.address ,'city':obj.city ,'state':obj.state ,
		'zipcode':obj.zipcode ,'t_exp_months':str(obj.monthsexp) ,'t_exp_years':str(obj.yearsexp) ,
		'us_exp_months':str(obj.usmonthsexp) ,'us_exp_years':str(obj.usyearsexp) ,'education':obj.education ,
		'besttime':obj.besttime ,'salary_cur':obj.salary_cur}
	if request.method == "POST":
		form = applicant_Form(request.POST, initial=initial_data)
		if form.is_valid():
			#print "Form Valid"
			firstname = form.cleaned_data['firstname']
			lastname = form.cleaned_data['lastname']
			email = form.cleaned_data['email']
			dob = form.cleaned_data['dob']
			phone_1 = form.cleaned_data['phone_1']
			phone_2= form.cleaned_data['phone_2']
			work_status = form.cleaned_data['work_status']
			available = form.cleaned_data['available']
			righttorep = form.cleaned_data['righttorep']
			relocation = form.cleaned_data['relocation']
			country = form.cleaned_data['country']
			address = form.cleaned_data['address']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			t_exp_months = form.cleaned_data['t_exp_months']
			t_exp_years = form.cleaned_data['t_exp_years']
			us_exp_months = form.cleaned_data['us_exp_months']
			us_exp_years = form.cleaned_data['us_exp_years']
			education = form.cleaned_data['education']
			besttime = form.cleaned_data['besttime']
			salary_cur = form.cleaned_data['salary_cur']
			obj.firstname = firstname
			obj.lastname = lastname
			obj.email = email
			obj.dob = dob
			obj.phone_1 = phone_1
			obj.phone_2 = phone_2
			obj.work_status = work_status
			obj.available = available
			obj.righttorep = righttorep
			obj.relocation = relocation
			obj.country = country
			obj.address = address
			obj.city = city
			obj.state = state
			obj.zipcode = zipcode
			#Converts years and months to months total if value is != (empty):
			if (t_exp_months != '' or t_exp_years != ''):
				if t_exp_months == '':
					t_exp_months = 0
				if t_exp_years == '':
					t_exp_years = 0
				obj.experience = int(t_exp_months) + int(t_exp_years)*12
			else:
				obj.experience = None
			if (us_exp_months != '' or us_exp_years != ''):
				if us_exp_months == '':
					us_exp_months = 0
				if us_exp_years == '':
					us_exp_years = 0
				obj.usexperience = int(us_exp_months) + int(us_exp_years)*12
			else:
				obj.usexperience = None
				#obj.usexperience = ReturnMonths(us_exp_months,us_exp_months)
			obj.education = education
			obj.besttime = besttime
			obj.salary_cur = salary_cur
			obj.updated = timezone.localtime(timezone.now())
			obj.save() # Save info to Database
			if form.has_changed():
				for item in form.changed_data:
					RegisterTracking(request.user,'1',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,item,initial_data[item],form.cleaned_data[item],None)
			#return HttpResponseRedirect('/applicant/%s/'%(obj.id))
			return redirect('view_applicant', id=obj.id)
		else:
			ctx = {'form':form,'obj':obj}
			return render_to_response('applicant_edit.html',ctx,context_instance=RequestContext(request))
	form = applicant_Form(initial=initial_data)
	ctx = {'form':form,'obj':obj}
	return render_to_response('applicant_edit.html',ctx,context_instance=RequestContext(request))

def applicantdocnew_view(request, applicant):
	obj = Applicant.objects.get(pk=applicant)
	documents = Applicant_Doc.objects.filter(applicant=obj).order_by('-datetime')
	if request.method == "POST":
		form = applicantdocnew_Form(request.POST, request.FILES)
		if form.is_valid():
			document = form.cleaned_data['document']
			type = form.cleaned_data['type']
			newobj = Applicant_Doc()
			newobj.applicant = obj
			newobj.type = type
			newobj.datetime = timezone.localtime(timezone.now())
			newobj.document = document
			newobj.save() # Save info to Database
			extra = '<b>Applicant: </b> %s<br/><b>Type:</b> %s<br/><b>Document:</b> %s' % (newobj.applicant ,dict(form.DOC_TYPE)[newobj.type], str(newobj.document).replace ("docs/", ""))
			RegisterTracking(request.user,'2',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,'Document',None,None,extra)
			#return HttpResponseRedirect('/applicant/%s/'%(newobj.applicant.id))
			return redirect('view_applicant', id = newobj.applicant.id)
		else:
			### Form not valid, Return ###
			#print "Form not valid: "+str(form.errors.as_text)
			ctx = {'form':form,'obj':obj,'documents':documents}
			return render_to_response('applicantdoc_new.html',ctx,context_instance=RequestContext(request))
	form = applicantdocnew_Form()
	cxt = {'form':form,'obj':obj,'documents':documents}
	return render_to_response('applicantdoc_new.html',cxt,context_instance=RequestContext(request))
#000
def applicant_doc_delete_view(request, id):
	try:
		obj = Applicant_Doc.objects.get(pk=id)
		applicant = obj.applicant
		extra = '<b>Applicant: </b> %s<br/><b>Type:</b> %s<br/><b>Document:</b> %s' % (applicant ,obj.get_type_display(), str(obj.document).replace ("docs/", ""))
		RegisterTracking(request.user,'3',timezone.localtime(timezone.now()),applicant._meta.model_name,applicant.id,'Document',None,None,extra)
		## Deleting actual file in media/docs:
		ruta = str(obj.document.path)
		os.remove(ruta)
		## Deleting database row:
		obj.delete()
		return redirect('view_applicant', id = applicant.id)
	except Applicant_Doc.DoesNotExist:
		raise Http404()
#111
def applicantdelete_view(request, id):
	if str(request.user) == "Visitor":
		raise Http404
	info = 0
	obj = Applicant.objects.get(id=id)
	o = Profile.objects.filter(applicant=obj).distinct()
	docs_count = Applicant_Doc.objects.filter(applicant=obj).count()
	documents = Applicant_Doc.objects.filter(applicant=obj).order_by('-datetime')
	if request.method == "POST":
		if len(o) > 0:
			info = 1
			ctx = {'info':info,'obj':obj,'profiles':o}
			return render_to_response('applicant_delete.html',ctx,context_instance=RequestContext(request))
		else:
			if not Profile.objects.filter(applicant=obj).exists():
				if docs_count > 0:
					## There are docs, delete them
				#if instance.file:
					#if os.path.isfile(instance.file.path):
						#os.remove(instance.file.path)
					for doc in documents:
						ruta = str(doc.document.path)
						os.remove(ruta)
						doc.delete()
				extra = '<b>Applicant:</b> %s' % (obj)
				RegisterTracking(request.user,'3',timezone.localtime(timezone.now()),obj._meta.model_name.capitalize(),None,None,None,None,extra)
				obj.delete()
				return redirect('view_applicants')
	if len(o) > 0:
		info = 1
	ctx = {'info':info,'obj':obj,'profiles':o,'docs_count':docs_count,'docs':documents}
	return render_to_response('applicant_delete.html',ctx,context_instance=RequestContext(request))

	###############################
	#####  T R A C K I N G    #####
	###############################
class TrackingDelete(DeleteView):
	model = Tracking
	success_url = reverse_lazy('view_trackings')

########################################
#######   A P P L I C A T I O N   ######
########################################

def applications_view(request, active=None, mine=None):
	objs = Application.objects.all().select_related('profile__applicant','opening__state').prefetch_related('opening__skills').annotate(activities_count=Count('activities')).order_by('-updated')
	title_all = title_my = ""
	if active == '1':
		title_all = "Active"
		objs = objs.filter(active=active)
	if mine == '1':
		title_my = "My"
		objs = objs.filter(recruiter=request.user)
	objs_counter = objs.count()
	cxt = {'objs':objs,'counter':objs_counter,'active':active,'mine':mine,'title_all':title_all,'title_my':title_my}
	return render_to_response('applications.html',cxt,context_instance=RequestContext(request))

def applications_rpt_view(request):
	objs = Application.objects.all().select_related('profile__applicant','opening__state').prefetch_related('opening__skills').annotate(activities_count=Count('activities'))
	objs_counter = objs.count()
	cxt = {'objs':objs,'counter':objs_counter}
	return render_to_response('applications_rpt.html',cxt,context_instance=RequestContext(request))

def qsearch_application_view(request):
	search = ""
	#objs = Applicant.objects.filter(active=True).prefetch_related('state','country').annotate(profiles_count=Count('profile'))
	objs = Application.objects.all().prefetch_related('profile','opening').annotate(activities_count=Count('activities'))
	if request.method == "POST":
		form = search_Form(request.POST or None)
		if form.is_valid():
			search = form.cleaned_data['search']
			if search != "":
				search_list = search.lower().split(' ')
				objs = objs.filter(reduce(or_, [Q(profile__applicant__firstname__icontains=c)|Q(profile__applicant__lastname__icontains=c)|Q(opening__role__icontains=c) for c in search_list])).distinct()
	objs_counter = objs.count()
	cxt = {'search':search,'objs':objs,'counter':objs_counter}
	return render_to_response('applications.html',cxt,context_instance=RequestContext(request))

def application_view(request, id):
	obj = Application.objects.get(pk=id)
	#objs = Application.objects.all().select_related('profile__applicant','opening__state').prefetch_related('opening__skills').annotate(activities_count=Count('activities'))
	activities_total = Activity.objects.filter(application=obj).count()
	activities = Activity.objects.filter(application=obj).prefetch_related('application','recruiter').order_by('-datetime')[:10]
	activities_counter = activities.count()
	#START: Value is bool but form returns unicode or str, but I need the same type so it doesn't triger has_change when there is no change
	active = "False"
	if obj.active == True:
		active = "True"
	#END
	dt = obj.submitted.date() #In has_change I compare initial values with cleaned_form values, so I have to clear time to only use date
	initial_data={'rate':obj.rate, 'active':active, 'submitted':dt}
	if request.method == "POST":
		form = applicationedit_Form(request.POST, initial=initial_data)
		if form.is_valid():
			rate = form.cleaned_data['rate']
			submitted = form.cleaned_data['submitted']
			active = form.cleaned_data['active']
			if active == "True":
				active = True
			else:
				active = False
			obj.active = active
			obj.rate = rate
			obj.submitted = submitted
			obj.save() # Save info to Database
			if form.has_changed():
				for item in form.changed_data:
					RegisterTracking(request.user,'1',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,item,initial_data[item],form.cleaned_data[item],None)
			return HttpResponseRedirect('/application/%s/'%(obj.id))
		else:
			ctx = {'form':form,'obj':obj,'activities':activities,'counter':activities_counter}
			return render_to_response('application.html',ctx,context_instance=RequestContext(request))
	form = applicationedit_Form(initial=initial_data)
	ctx = {'form':form,'obj':obj,'activities':activities,'counter':activities_counter,'total':activities_total}
	return render_to_response('application.html',ctx,context_instance=RequestContext(request))
	
def application_rpt_view(request, id):
	obj = Application.objects.get(id=id)
	cxt = {'obj':obj,}
	return render_to_response('application_rpt.html',cxt,context_instance=RequestContext(request))

"""
def applicationedit_view(request, id):
	objs = Application.objects.all().select_related('profile__applicant','opening__state').prefetch_related('opening__skills').annotate(activities_count=Count('activities'))
	obj = objs.get(pk=id)
	initial_data={'rate':obj.rate, 'active':obj.active, 'submitted':obj.submitted}
	print "in application edit"
	if request.method == "POST":
		form = applicationedit_Form(request.POST, initial=initial_data)
		if form.is_valid():
			active = form.cleaned_data['active']
			rate = form.cleaned_data['rate']
			#submitted
			obj.active = active
			obj.rate = rate
			obj.save() # Save info to Database
			if form.has_changed():
				print "has changed"
				for item in form.changed_data:
					print item
					RegisterTracking(request.user,'1',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,item,initial_data[item],form.cleaned_data[item])
			#return HttpResponseRedirect('/application/%s/'%(obj.id))
			return redirect('view_application', id = obj.id)
		else:
			ctx = {'form':form,'obj':obj,'objs':objs,'counter':objs_counter}
			return render_to_response('application_edit.html',ctx,context_instance=RequestContext(request))
	form = applicationedit_Form(initial=initial_data)
	objs_counter = objs.count()
	ctx = {'form':form,'obj':obj,'objs':objs,'counter':objs_counter}
	return render_to_response('application_edit.html',ctx,context_instance=RequestContext(request))
"""
def applicationnew_view(request, profile_id=None, opening_id=None):
	if str(request.user) == "Visitor":
		raise Http404
	objs = Application.objects.all().select_related('profile__applicant','opening__state').prefetch_related('opening__skills').annotate(activities_count=Count('activities'))
	objs_counter = objs.count()
	if request.method == "POST":
		#print "in POST"
		form = applicationnew_Form(request.POST)
		if form.is_valid():
			#print "From Valid"
			profile_id = form.cleaned_data['profile']
			profile = Profile.objects.get(pk=profile_id)
			opening_id = form.cleaned_data['opening']
			opening = Opening.objects.get(pk=opening_id)
			submitted = form.cleaned_data['submitted']
			rate = form.cleaned_data['rate']
			obj = Application()
			obj.profile = profile
			obj.opening = opening
			obj.rate = rate
			obj.recruiter = request.user
			obj.datetime = datetime.now()
			obj.status = '1'
			obj.submitted = submitted
			obj.updated = timezone.localtime(timezone.now())
			obj.created = timezone.localtime(timezone.now())
			obj.active = True
			obj.save() # Save info to Database
			extra = '<b>Submitted:</b> %s<br/><b>Profile:</b> %s<br/><b>Opening:</b> %s<br/><b>Rate:</b> %s' % (obj.submitted.strftime("%b %d, %Y - %I:%M %p"),obj.profile,obj.opening,obj.rate)
			RegisterTracking(request.user,'2',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,None,None,None,extra)
			#return HttpResponseRedirect('/application/%s/'%(obj.id))
			return redirect('view_application', id = obj.id)
		else:
			#print "Form not valid: "+str(form.errors.as_text)
			ctx = {'form':form,'objs':objs,'counter':objs_counter}
			return render_to_response('application_new.html',ctx,context_instance=RequestContext(request))
	INITIAL = {}
	if profile_id:
		profile = Profile.objects.get(pk=profile_id)
		INITIAL['profile'] = profile
	if opening_id:
		opening = Opening.objects.get(pk=opening_id)
		INITIAL['opening'] = opening
	if not INITIAL:
		# No profile or opening sent to initialize form
		form = applicationnew_Form()
	else:
		# Profile and/or opening sent, initialize form
		form = applicationnew_Form(initial=INITIAL)
	ctx = {'form':form,'objs':objs,'counter':objs_counter}
	return render_to_response('application_new.html',ctx,context_instance=RequestContext(request))

def application_delete_view(request, id):
	if str(request.user) == "Visitor":
		raise Http404
	req_user = request.user
	obj = Application.objects.get(pk=id)
	print "Deleting application"
	if obj.recruiter == req_user:
		# User requesting = recruiter owner of application.
		# Proceed to delete 
		extra = '<b>Submitted:</b> %s<br/><b>Profile:</b> %s<br/><b>Opening:</b> %s<br/><b>Rate:</b> %s' % (obj.submitted.strftime("%b %d, %Y - %I:%M %p"),obj.profile,obj.opening,obj.rate)
		RegisterTracking(request.user,'3',timezone.localtime(timezone.now()),obj._meta.model_name.capitalize(),None,None,None,None,extra)
		obj.delete()
		return redirect('view_applications')
	else:
		# Request user is not owner of entity,
		# Do not delete and redirect
		return redirect('view_application',id=id)

#### chech APPLICATION DELETE! YA HAY UNA
"""class ApplicationDelete(DeleteView):
	model = Application
	success_url = reverse_lazy('view_application')
	def dispatch(self, request, *args, **kwargs):
		## Making sure that only authors can delete Articles
		obj = self.get_object()
		if obj.recruiter != self.request.user:
			return redirect('view_application', id = obj.id)
		extra = '<b>Date and Time:</b> %s<br/><b>Content:</b> %s' % (obj.datetime.strftime("%b %d, %Y - %I:%M %p"), obj.content)
		RegisterTracking(request.user,'3',timezone.localtime(timezone.now()),obj._meta.model_name.capitalize(),None,None,None,None,extra)
		return super(ApplicationDelete, self).dispatch(request, *args, **kwargs)"""

def applicationnew_both_view(request, profile_id, opening_id):
	if str(request.user) == "Visitor":
		raise Http404
	profile = Profile.objects.get(pk=profile_id)
	opening = Opening.objects.get(pk=opening_id)
	# Check if applications already exists.
	# This consistency if is somebody type the URL
	# This would never been sent from a profile or opening page
	try:
		application = Application.objects.get(profile=profile, opening=opening)
		# The Application for the Opening and Profile already exists!
		# Redirect to the application
		return HttpResponseRedirect('/application/%s/'%(application.id))
	except Application.DoesNotExist:
		# Latest applications
		applications_total = Application.objects.all().count()
		applications = Application.objects.all().select_related('profile__applicant','opening__state').prefetch_related('opening__skills').annotate(activities_count=Count('activities')).order_by('-updated')[:10]
		applications_counter = applications.count()
		if request.method == "POST":
			form = applicationnewboth_Form(request.POST)
			if form.is_valid():
				rate = form.cleaned_data['rate']
				submitted = form.cleaned_data['submitted']
				obj = Application()
				obj.profile = profile
				obj.opening = opening
				obj.recruiter = request.user
				obj.submitted = submitted
				obj.updated = timezone.localtime(timezone.now())
				obj.created = timezone.localtime(timezone.now())
				obj.datetime = timezone.localtime(timezone.now())
				obj.status = '1'
				obj.save() # Save info to Database
				extra = '<b>Submitted:</b> %s<br/><b>Profile:</b> %s<br/><b>Opening:</b> %s<br/><b>Rate:</b> %s' % (obj.submitted.strftime("%b %d, %Y - %I:%M %p"),obj.profile,obj.opening,obj.rate)
				RegisterTracking(request.user,'2',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,None,None,None,extra)
				#return HttpResponseRedirect('/application/%s/'%(obj.id))
				return redirect('view_application', id = obj.id)
			else:
				form.fields["opening"].queryset = openings
				ctx = {'form':form,'profile':profile,'applications':applications,'counter':applications_counter,'total':applications_total}
				return render_to_response('application_new_both.html',ctx,context_instance=RequestContext(request))
		form = applicationnewboth_Form()
		ctx = {'form':form,'profile':profile,'opening':opening,'applications':applications,'counter':applications_counter,'total':applications_total,}
		return render_to_response('application_new_both.html',ctx,context_instance=RequestContext(request))

def applicationnew_opening_view(request, opening_id):
	if str(request.user) == "Visitor":
		raise Http404
	## When new application button is pressed from next to opening title, this passes the profile.
	#profile = Profile.objects.prefetch_related('skills').select_related('applicant','applicant__state').get(pk=profile_id)
	opening = Opening.objects.prefetch_related('skills').get(pk=opening_id)
	
	applications_total = Application.objects.filter(opening=opening).count()
	applications = Application.objects.filter(opening=opening).select_related('profile__applicant','opening__state').prefetch_related('opening__skills').annotate(activities_count=Count('activities')).order_by('-updated')[:10]
	applications_counter = applications.count()
	
	#applications = Application.objects.filter(opening=opening).select_related('profile','recruiter').order_by('-datetime')
	profiles_to_exclude = list([o.profile.id for o in applications])
	skills = opening.skills.all()
	if skills:
		tag_qs = reduce(operator.or_, (Q(skills=x) for x in skills))
		profiles = Profile.objects.filter(tag_qs).prefetch_related('skills').exclude(id__in=profiles_to_exclude).distinct()
	if request.method == "POST":
		form = applicationnew_opening_Form(request.POST)
		if form.is_valid():
			profile = form.cleaned_data['profile']
			rate = form.cleaned_data['rate']
			submitted = form.cleaned_data['submitted']
			newobj = Application()
			newobj.profile = profile
			newobj.opening = opening
			newobj.recruiter = request.user
			newobj.datetime = datetime.now()
			newobj.rate = rate
			newobj.submitted = submitted
			newobj.status = '1'
			newobj.save() # Save info to Database
			extra = '<b>Submitted:</b> %s<br/><b>Profile:</b> %s<br/><b>Opening:</b> %s<br/><b>Rate:</b> %s' % (newobj.submitted.strftime("%b %d, %Y - %I:%M %p"),newobj.profile,newobj.opening,newobj.rate)
			RegisterTracking(request.user,'2',timezone.localtime(timezone.now()),newobj._meta.model_name,newobj.id,None,None,None,extra)
			return redirect('view_application', id = newobj.id)
		else:
			form.fields["profile"].queryset = profiles
			ctx = {'form':form,'opening':opening,'applications':applications,'counter':applications_counter,'total':applications_total}
			return render_to_response('application_new_opening.html',ctx,context_instance=RequestContext(request))
	form = applicationnew_opening_Form()
	form.fields["profile"].queryset = profiles
	ctx = {'form':form,'opening':opening,'applications':applications,'counter':applications_counter,'total':applications_total}
	return render_to_response('application_new_opening.html',ctx,context_instance=RequestContext(request))

def applicationnew_profile_view(request, profile_id):
	if str(request.user) == "Visitor":
		raise Http404
	## New application coming from /profiles/
	profile = Profile.objects.prefetch_related('skills').select_related('applicant','applicant__state').get(pk=profile_id)
	
	applications_total = Application.objects.filter(profile=profile).count()
	applications = Application.objects.filter(profile=profile).select_related('profile__applicant','opening__state').prefetch_related('opening__skills').annotate(activities_count=Count('activities')).order_by('-updated')[:10]
	applications_counter = applications.count()
	
	#applications = Application.objects.filter(profile=profile).select_related('profile','recruiter').order_by('-datetime')
	openings_to_exclude = list([o.opening.id for o in applications])
	skills = profile.skills.all()
	if skills:
		tag_qs = reduce(operator.or_, (Q(skills=x) for x in skills))
		openings = Opening.objects.filter(tag_qs).prefetch_related('skills').select_related('state').exclude(id__in=openings_to_exclude).distinct()
	#print "Profile sent: "+str(profile)
	if request.method == "POST":
		form = applicationnew_profile_Form(request.POST)
		if form.is_valid():
			opening = form.cleaned_data['opening']
			rate = form.cleaned_data['rate']
			submitted = form.cleaned_data['submitted']
			newobj = Application()
			newobj.profile = profile
			newobj.opening = opening
			newobj.recruiter = request.user
			newobj.rate = rate
			newobj.submitted = submitted
			newobj.datetime = datetime.now()
			newobj.status = '1'
			newobj.save() # Save info to Database
			extra = '<b>Submitted:</b> %s<br/><b>Profile:</b> %s<br/><b>Opening:</b> %s<br/><b>Rate:</b> %s' % (newobj.submitted.strftime("%b %d, %Y - %I:%M %p"),newobj.profile,newobj.opening,newobj.rate)
			RegisterTracking(request.user,'2',timezone.localtime(timezone.now()),newobj._meta.model_name,newobj.id,None,None,None,extra)
			return redirect('view_application', id = newobj.id)
		else:
			form.fields["opening"].queryset = openings
			ctx = {'form':form,'profile':profile,'applications':applications,'counter':applications_counter,'total':applications_total}
			return render_to_response('application_new_profile.html',ctx,context_instance=RequestContext(request))
	form = applicationnew_profile_Form()
	form.fields["opening"].queryset = openings
	ctx = {'form':form,'profile':profile,'applications':applications,'counter':applications_counter,'total':applications_total}
	return render_to_response('application_new_profile.html',ctx,context_instance=RequestContext(request))
	
########################################
#######   O P E N I N G S    ###########
########################################
	
def openings_view(request):
	objs = Opening.objects.filter(active=True).prefetch_related('skills').annotate(app_count=Count('applications'))
	#profiles = Profile.objects.all().prefetch_related('skills','skills_sec').select_related('applicant','applicant__state','applicant__country')
	objs_counter = objs.count()
	cxt = {'objs':objs,'counter':objs_counter}
	return render_to_response('openings.html',cxt,context_instance=RequestContext(request))
	
def qsearch_opening_view(request):
	search = ""
	#objs = Opening.objects.all().prefetch_related('applicant').annotate(app_count=Count('applications'))
	objs = Opening.objects.filter(active=True).prefetch_related('skills').annotate(app_count=Count('applications'))
	print objs
	if request.method == "POST":
		form = search_Form(request.POST or None)
		if form.is_valid():
			search = form.cleaned_data['search']
			if search != "":
				search_list = search.lower().split(' ')
				objs = objs.filter(reduce(or_, [Q(role__icontains=c)|Q(skills__name__icontains=c)|Q(skills__description__icontains=c) for c in search_list])).distinct()
	objs_counter = objs.count()
	cxt = {'search':search,'objs':objs,'counter':objs_counter}
	return render_to_response('openings.html',cxt,context_instance=RequestContext(request))

def openings_rpt_view(request):
	objs = Opening.objects.filter(active=True).prefetch_related('skills').annotate(app_count=Count('applications'))
	objs_counter = objs.count()
	cxt = {'objs':objs,'counter':objs_counter}
	return render_to_response('openings_rpt.html',cxt,context_instance=RequestContext(request))

def opening_view(request, id):
	obj = Opening.objects.get(id=id)
	skills = obj.skills.all()
	profiles = Profile.objects.none()
	#print skills
	applications_total = Application.objects.filter(opening=obj).count()
	applications = Application.objects.filter(opening=obj).select_related('profile__applicant','opening__state').prefetch_related('opening__skills').annotate(activities_count=Count('activities'))[:10]
	applications_counter = applications.count()
	if skills:
		applications_related = Application.objects.filter(opening=obj)
		to_exclude = [o.id for o in applications_related]#Make sure you retrive id only
		exclude_list = list(to_exclude)
		#print exclude_list
		tag_qs = reduce(operator.or_, (Q(skills=x) for x in skills))
		#profiles = Profile.objects.filter(tag_qs).distinct().exclude(applications__in=exclude_list)
		profiles_total = Profile.objects.filter(tag_qs).distinct().exclude(applications__in=exclude_list).count()
		profiles = Profile.objects.filter(tag_qs).distinct().exclude(applications__in=exclude_list).prefetch_related('skills').annotate(app_count=Count('applications')).select_related('applicant','applicant__state','applicant__country')
		profiles_counter = profiles.count()
	cxt = {'obj':obj,'applications':applications,'profiles':profiles,'counter':applications_counter,'total':applications_total,'profiles_counter':profiles_counter,'profiles_total':profiles_total}
	#ctx = {'obj':obj, 'objs':objs, 'counter':counter,'total':objs_count}
	return render_to_response('opening.html',cxt,context_instance=RequestContext(request))

def opening_rpt_view(request, id):
	obj = Opening.objects.get(id=id)
	skills = obj.skills.all()
	profiles = Profile.objects.none()
	#print skills
	applications = Application.objects.filter(opening=obj)[:7]
	if skills:
		tag_qs = reduce(operator.or_, (Q(skills=x) for x in skills))
		profiles = Profile.objects.filter(tag_qs).distinct()
	cxt = {'obj':obj,'applications':applications,'profiles':profiles}
	return render_to_response('opening_rpt.html',cxt,context_instance=RequestContext(request))

def openingnew_view(request):
	if str(request.user) == "Visitor":
		raise Http404
	if request.method == "POST":
		form = opening_Form(request.POST)
		if form.is_valid():
			startdate = form.cleaned_data['startdate']
			role = form.cleaned_data['role']
			skills_list = request.POST.getlist('skills')
			responsibilities = form.cleaned_data['responsibilities']
			education = form.cleaned_data['education']
			rate = form.cleaned_data['rate']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			duration_months = form.cleaned_data['duration_months']
			duration_years = form.cleaned_data['duration_years']
			exp_months = form.cleaned_data['exp_months']
			exp_years = form.cleaned_data['exp_years']
			contract = form.cleaned_data['contract']
			level = form.cleaned_data['level']
			work_auth = form.cleaned_data['work_auth']
			vendor = form.cleaned_data['vendor']
			partnerinfo = form.cleaned_data['partnerinfo']
			endclientinfo = form.cleaned_data['endclientinfo']
			open = form.cleaned_data['open']
			obj = Opening()
			obj.startdate = startdate
			obj.role = role
			obj.education = education
			obj.responsibilities = responsibilities
			obj.rate = rate
			obj.city = city
			obj.state = state
			obj.duration = get_months(duration_months,duration_years)
			obj.experience = get_months(exp_months,exp_years)
			obj.contract = contract
			obj.level = level
			obj.work_auth = work_auth
			obj.vendor = vendor
			obj.endclientinfo = endclientinfo
			obj.partnerinfo = partnerinfo
			obj.open = open
			obj.updated = timezone.localtime(timezone.now())
			obj.created = timezone.localtime(timezone.now())
			obj.active = True
			obj.save() # Save info to Database
			for skill in skills_list:
				obj.skills.add(skill)
			extra = '<b>Role: </b> %s<br/><b>Skills:</b> %s' % (obj.role ,obj.skills)
			RegisterTracking(request.user,'2',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,None,None,None,extra)
			return redirect('view_opening', id = obj.id)
		else:
			ctx = {'form':form}
			return render_to_response('opening_new.html',ctx,context_instance=RequestContext(request))
	form= opening_Form()
	ctx = {'form':form}
	return render_to_response('opening_new.html',ctx,context_instance=RequestContext(request))

def openingedit_view(request, id):
	if str(request.user) == "Visitor":
		raise Http404
	obj = Opening.objects.get(pk=id)
	skills = Skill.objects.filter(open_skills_main__id=obj.id)
	#print skills
	initial_data={
		'startdate':obj.startdate,'role':obj.role,'responsibilities':obj.responsibilities,
		'rate':obj.rate ,'city':obj.city ,'state':obj.state,'duration_months':obj.monthsdur ,
		'duration_years':obj.yearsdur ,'exp_months':obj.monthsexp ,'exp_years':obj.yearsexp ,
		'contract':obj.contract ,'work_auth':obj.work_auth,'vendor':obj.vendor,
		'endclientinfo':obj.endclientinfo, 'partnerinfo':obj.partnerinfo, 'posted':obj.posted,
		'education':obj.education,'level':obj.level,'open':obj.open,'skills':skills}
	if request.method == "POST":
		form = opening_Form(request.POST, initial=initial_data)
		if form.is_valid():
			startdate = form.cleaned_data['startdate']
			role = form.cleaned_data['role']
			skills1 = form.cleaned_data['skills']
			skills_list = request.POST.getlist('skills')
			skill_n = Skill.objects.filter(pk__in=skills_list)
			posted = form.cleaned_data['posted']
			responsibilities = form.cleaned_data['responsibilities']
			education = form.cleaned_data['education']
			rate = form.cleaned_data['rate']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			duration_months = form.cleaned_data['duration_months']
			duration_years = form.cleaned_data['duration_years']
			exp_months = form.cleaned_data['exp_months']
			exp_years = form.cleaned_data['exp_years']
			contract = form.cleaned_data['contract']
			level = form.cleaned_data['level']
			work_auth = form.cleaned_data['work_auth']
			vendor = form.cleaned_data['vendor']
			endclientinfo = form.cleaned_data['endclientinfo']
			partnerinfo = form.cleaned_data['partnerinfo']
			open = form.cleaned_data['open']
			obj.startdate = startdate
			obj.role = role
			obj.responsibilities = responsibilities
			obj.education = education
			obj.rate = rate
			obj.city = city
			obj.state = state
			obj.duration = get_months(duration_months,duration_years)
			obj.experience = get_months(exp_months,exp_years)
			obj.contract = contract
			obj.level = level
			obj.work_auth = work_auth
			obj.vendor = vendor
			obj.endclientinfo = endclientinfo
			obj.partnerinfo = partnerinfo
			obj.open = open
			obj.updated = timezone.localtime(timezone.now())
			obj.save() # Save info to Database
			### Skills Changed? ###
			if skills != skill_n:
				### Save main Skills
				for skill_o in skills:
					obj.skills.remove(skill_o.id)#.delete()
				for skill in skill_n:
					obj.skills.add(skill.id)
			if form.has_changed():
				for item in form.changed_data:
					#print item
					if item == 'skills':
						skills_list = set(skill.name for skill in skills)
						old = ', '.join(skills_list)
						new = ', '.join(skill.name for skill in skills1)
						RegisterTracking(request.user,'1',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,item,old,new,None)
					elif item == 'open':
						## Change 'True' to 'Open' and/or 'False' to 'Closed'
						old = new = 'Closed'
						if initial_data[item] == True:
							old = 'Open'
						if form.cleaned_data[item] == True:
							new = 'Open'
						RegisterTracking(request.user,'1',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,item,old,new,None)
					else:
						RegisterTracking(request.user,'1',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,item,initial_data[item],form.cleaned_data[item],None)
			return redirect('view_opening', id = obj.id)
		else:
			ctx = {'form':form,'obj':obj}
			return render_to_response('opening_edit.html',ctx,context_instance=RequestContext(request))
	form = opening_Form(initial=initial_data)
	ctx = {'form':form,'obj':obj,'skills':skills}
	return render_to_response('opening_edit.html',ctx,context_instance=RequestContext(request))
	
def openingdelete_view(request, id):
	if str(request.user) == "Visitor":
		raise Http404
	info = 0
	obj = Opening.objects.get(id=id)
	o = Application.objects.filter(opening=obj).distinct()
	if request.method == "POST":
		if len(o) > 0:
			info = 1
			ctx = {'info':info,'obj':obj,'applications':o}
			return render_to_response('opening_delete.html',ctx,context_instance=RequestContext(request))
		else:
			if not Application.objects.filter(opening=obj).exists():
				#extra = '<b>Opening:</b> %s' % (obj)
				RegisterTracking(request.user,'3',timezone.localtime(timezone.now()),obj._meta.model_name.capitalize(),None,None,None,None,obj)
				obj.delete()
				return redirect('view_openings')
	if len(o) > 0:
		info = 1
	ctx = {'info':info,'obj':obj,'applications':o}
	return render_to_response('opening_delete.html',ctx,context_instance=RequestContext(request))

########################################
#######   P R O F I L E S    ###########
########################################
	
def profiles_view(request):
	#objs = Profile.objects.all().prefetch_related('skills','skills_sec').annotate(app_count=Count('applications')).select_related('applicant','applicant__state','applicant__country')
	objs = Profile.objects.all().prefetch_related('skills').annotate(app_count=Count('applications')).select_related('applicant','applicant__state','applicant__country')
	objs_counter = objs.count()
	cxt = {'objs':objs,'counter':objs_counter}
	return render_to_response('profiles.html',cxt,context_instance=RequestContext(request))
	
def profiles_rpt_view(request):
	objs = Profile.objects.all().prefetch_related('skills','skills_sec').annotate(app_count=Count('applications')).select_related('applicant','applicant__state','applicant__country')
	objs_counter = objs.count()
	cxt = {'objs':objs,'counter':objs_counter}
	return render_to_response('profiles_rpt.html',cxt,context_instance=RequestContext(request))
		
def profile_view(request, id):
	obj = Profile.objects.prefetch_related('skills','skills_sec').select_related('applicant').get(id=id)
	#print obj
	applications = Application.objects.filter(profile=obj).select_related('profile','recruiter').order_by('-updated')
	#print applications
	documents = Profile_Doc.objects.filter(profile=obj).order_by('-datetime')
	applications_related = Application.objects.filter(profile=obj)
	to_exclude = [o.id for o in applications_related]#Make sure you retrive id only
	exclude_list = list(to_exclude)
	skills = obj.skills.all()
	tag_qs = reduce(operator.or_, (Q(skills=x) for x in skills))
	openings_total = Opening.objects.filter(tag_qs).exclude(application__in = exclude_list).distinct().count()
	openings = Opening.objects.filter(tag_qs).exclude(application__in=exclude_list).prefetch_related('skills').annotate(app_count=Count('applications')).select_related('state').distinct()
	objs_counter = openings.count()
	cxt = {'obj':obj,'applications':applications,'openings':openings,'documents':documents,'counter':objs_counter,'total':openings_total}
	return render_to_response('profile.html',cxt,context_instance=RequestContext(request))
	
def profile_rpt_view(request, id):
	obj = Profile.objects.prefetch_related('skills','skills_sec').select_related('applicant').get(id=id)
	skills = obj.skills.all()
	applications = Application.objects.filter(profile=obj).select_related('profile','recruiter').order_by('-datetime')
	documents = Profile_Doc.objects.filter(profile=obj).order_by('-datetime')
	cxt = {'obj':obj,'applications':applications,'documents':documents}
	return render_to_response('profile_rpt.html',cxt,context_instance=RequestContext(request))

def qsearch_profile_view(request):
	search = ""
	objs = Profile.objects.all().prefetch_related('applicant').annotate(app_count=Count('applications'))
	if request.method == "POST":
		form = search_Form(request.POST or None)
		if form.is_valid():
			search = form.cleaned_data['search']
			if search != "":
				#print search
				search_list = search.lower().split(' ')
				objs = objs.filter(reduce(or_, [Q(applicant__firstname__icontains=c)|Q(applicant__lastname__icontains=c) for c in search_list])).distinct().prefetch_related('applicant')
	objs_counter = objs.count()
	cxt = {'search':search,'objs':objs,'counter':objs_counter}
	return render_to_response('profiles.html',cxt,context_instance=RequestContext(request))

def profile_doc_delete_view(request, id):
	if str(request.user) == "Visitor":
		raise Http404
	try:
		obj = Profile_Doc.objects.get(pk=id)
		profile = obj.profile
		extra = '<b>Profile: </b> %s<br/><b>Type:</b> %s<br/><b>Document:</b> %s' % (profile ,obj.get_type_display(), str(obj.location).replace ("docs/", ""))
		RegisterTracking(request.user,'3',timezone.localtime(timezone.now()),profile._meta.model_name,profile.id,'Document',None,None,extra)
		obj.delete()
		return redirect('view_profile', id = profile.id)
	except Profile_Doc.DoesNotExist:
		raise Http404()

def profiledocnew_view(request, profile):
	if str(request.user) == "Visitor":
		raise Http404
	obj = Profile.objects.get(pk=profile)
	documents = Profile_Doc.objects.filter(profile=obj).order_by('-datetime')
	if request.method == "POST":
		form = profiledocnew_Form(request.POST, request.FILES)
		if form.is_valid():
			location = form.cleaned_data['document']
			type = form.cleaned_data['type']
			newobj = Profile_Doc()
			newobj.profile = obj
			newobj.type = type
			#newobj.datetime = datetime.today()
			newobj.datetime = timezone.localtime(timezone.now())
			newobj.location = location
			newobj.save() # Save info to Database
			extra = '<b>Profile: </b> %s<br/><b>Type:</b> %s<br/><b>Document:</b> %s' % (newobj.profile ,dict(form.DOC_TYPE)[newobj.type], str(newobj.location).replace ("docs/", ""))
			RegisterTracking(request.user,'2',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,'Document',None,None,extra)
			return HttpResponseRedirect('/profile/%s/'%(newobj.profile.id))
		else:
			### Form not valid, Return ###
			#print "Form not valid: "+str(form.errors.as_text)
			ctx = {'form':form,'obj':obj,'documents':documents}
			return render_to_response('profiledoc_new.html',ctx,context_instance=RequestContext(request))
	form = profiledocnew_Form()
	cxt = {'form':form,'obj':obj,'documents':documents}
	return render_to_response('profiledoc_new.html',cxt,context_instance=RequestContext(request))		

def profilenew_view(request, applicant=None):
	if str(request.user) == "Visitor":
		raise Http404
	profiles_total = Profile.objects.all().count()
	profiles = Profile.objects.all().prefetch_related('skills','skills_sec').annotate(app_count=Count('applications')).select_related('applicant','applicant__state','applicant__country').order_by('-datetime')[:10]
	counter = profiles.count()
	if applicant != None:#Applicant sent
		#print "applicant sent: "+ applicant
		obj = Applicant.objects.get(pk=applicant)
		#profiles = Profile.objects.filter(applicant__id=obj.id)
	if request.method == "POST":
		form = profile_Form(request.POST, request.FILES)
		if form.is_valid():
			applicant = form.cleaned_data['applicant']
			skills = form.cleaned_data['skills']
			exp_months = form.cleaned_data['exp_months']
			exp_years = form.cleaned_data['exp_years']
			salary = form.cleaned_data['salary']
			skills_list = request.POST.getlist('skills')
			#skills_sec_list = request.POST.getlist('skills_sec')
			newobj = Profile()
			newobj.applicant = applicant
			newobj.datetime = datetime.now()
			newobj.experience = get_months(exp_months,exp_years)
			newobj.salary = salary
			newobj.updated = timezone.localtime(timezone.now())
			newobj.created = timezone.localtime(timezone.now())
			newobj.save() # Save info to Database
			extra = '<b>Applicant: </b> %s<br/><b>Created:</b> %s<br/><b>Salary:</b> %s' % (newobj.applicant ,newobj.created.strftime("%b %d, %Y - %I:%M %p"),newobj.salary)
			RegisterTracking(request.user,'2',timezone.localtime(timezone.now()),newobj._meta.model_name,newobj.id,None,None,None,extra)
			for skill in skills_list:
				newobj.skills.add(skill)
			return redirect('view_profile', id = newobj.id)
		else:
			ctx = {'form':form,'profiles':profiles,'total':profiles_total,'counter':counter}
			return render_to_response('profile_new.html',ctx,context_instance=RequestContext(request))
	if applicant != None:
		form = profile_Form(initial={'applicant':obj})
	else:
		form = profile_Form()
	ctx = {'form':form,'profiles':profiles,'total':profiles_total,'counter':counter}
	return render_to_response('profile_new.html',ctx,context_instance=RequestContext(request))

def profilenew_appicant_view(request, applicant_id):
	if str(request.user) == "Visitor":
		raise Http404
	## Comes from Applicant and applicants
	obj = Applicant.objects.get(pk=applicant_id)
	profiles_total = Profile.objects.filter(applicant__id=applicant_id).distinct().count()
	profiles = Profile.objects.filter(applicant__id=applicant_id).distinct()[:10]
	counter = profiles.count()
	if request.method == "POST":
		form = profile_applicant_Form(request.POST, request.FILES)
		if form.is_valid():
			skills = form.cleaned_data['skills']
			exp_months = form.cleaned_data['exp_months']
			exp_years = form.cleaned_data['exp_years']
			salary = form.cleaned_data['salary']
			skills_list = request.POST.getlist('skills')
			newobj = Profile()
			newobj.applicant = obj
			newobj.datetime = datetime.now()
			newobj.experience = get_months(exp_months,exp_years)
			newobj.salary = salary
			newobj.updated = timezone.localtime(timezone.now())
			newobj.created = timezone.localtime(timezone.now())
			newobj.save() # Save info to Database
			extra = '<b>Applicant: </b> %s<br/><b>Created:</b> %s<br/><b>Salary:</b> %s' % (newobj.applicant ,newobj.created.strftime("%b %d, %Y - %I:%M %p"),newobj.salary)
			RegisterTracking(request.user,'2',timezone.localtime(timezone.now()),newobj._meta.model_name,newobj.id,None,None,None,extra)
			for skill in skills_list:
				newobj.skills.add(skill)
			return redirect('view_profile', id = newobj.id)
		else:
			ctx = {'form':form,'obj':obj,'profiles':profiles,'counter':counter,'total':profiles_total}
			return render_to_response('profile_applicant_new.html',ctx,context_instance=RequestContext(request))

	form = profile_applicant_Form()
	ctx = {'form':form,'obj':obj,'profiles':profiles,'counter':counter,'total':profiles_total}
	return render_to_response('profile_applicant_new.html',ctx,context_instance=RequestContext(request))

def profileedit_view(request, id):
	if str(request.user) == "Visitor":
		raise Http404
	obj = Profile.objects.get(pk=id)
	skills = Skill.objects.filter(profile__id=obj.id)
	initial_data={'exp_months':obj.monthsexp ,'exp_years':obj.yearsexp,'salary':obj.salary, 'skills':skills}
	documents = Profile_Doc.objects.filter(profile=obj).order_by('-datetime')
	if request.method == "POST":
		form = profile_edit_Form(request.POST, initial=initial_data)
		if form.is_valid():
			exp_months = form.cleaned_data['exp_months']
			exp_years = form.cleaned_data['exp_years']
			salary = form.cleaned_data['salary']
			skills1 = form.cleaned_data['skills']
			skills_list = request.POST.getlist('skills')
			skill_n = Skill.objects.filter(pk__in=skills_list)
			obj.applicant = obj.applicant
			obj.experience = get_months(exp_months,exp_years)
			obj.salary = salary
			obj.updated = timezone.localtime(timezone.now())
			#obj.skills = skills1
			obj.save() # Save info to Database
			### Skills Changed? ###
			if skills != skill_n:
			#if 'skills' in form.changed_data:
				#form.save_m2m()
				### 11 - Save main Skills
				for skill_o in skills:
					obj.skills.remove(skill_o.id)#.delete()
				for skill in skill_n:
					obj.skills.add(skill.id)
			if form.has_changed():
				for item in form.changed_data:
					if item == 'skills':
						skills_list = set(skill.name for skill in skills)
						old = ', '.join(skills_list)
						new = ', '.join(skill.name for skill in skills1)
						RegisterTracking(request.user,'1',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,item,old,new,None)
					else:
						RegisterTracking(request.user,'1',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,item,initial_data[item],form.cleaned_data[item],None)
			return redirect('view_profile', id = obj.id)
		else:
			ctx = {'form':form,'obj':obj}
			return render_to_response('profile_edit.html',ctx,context_instance=RequestContext(request))
	form = profile_edit_Form(initial=initial_data)
	ctx = {'form':form,'obj':obj,'documents':documents,'skills':skills,}
	return render_to_response('profile_edit.html',ctx,context_instance=RequestContext(request))

def profiledelete_view(request, id):
	if str(request.user) == "Visitor":
		raise Http404
	info = 0
	obj = Profile.objects.get(id=id)
	o = Application.objects.filter(profile=obj).distinct()
	docs_count = Profile_Doc.objects.filter(profile=obj).count()
	documents = Profile_Doc.objects.filter(profile=obj).order_by('-datetime')
	if request.method == "POST":
		if len(o) > 0:
			info = 1
			ctx = {'info':info,'obj':obj,'applications':o}
			return render_to_response('profile_delete.html',ctx,context_instance=RequestContext(request))
		else:
			if not Application.objects.filter(profile=obj).exists():
				if docs_count > 0:
					## There are docs, delete them
					for doc in documents:
						ruta = str(doc.location.path)
						os.remove(ruta)
						doc.delete()
				extra = '<b>Profile:</b> %s' % (obj)
				RegisterTracking(request.user,'3',timezone.localtime(timezone.now()),obj._meta.model_name.capitalize(),None,None,None,None,extra)
				obj.delete()
				return redirect('view_profiles')
	if len(o) > 0:
		info = 1
	ctx = {'info':info,'obj':obj,'applications':o,'docs_count':docs_count,'docs':documents}
	return render_to_response('profile_delete.html',ctx,context_instance=RequestContext(request))
	
########################################
#######   R E C R U I T E R    #########
########################################

def recruiter_profile_view(request, id):
	obj = User.objects.get(id=id)
	#activities = Activity.objects.filter(recruiter=obj).order_by('-datetime')
	#cxt = {'obj':obj,'activities':activities}
	objs_count = Activity.objects.filter(recruiter=obj).count()
	objs = Activity.objects.filter(recruiter=obj).prefetch_related('application','recruiter').order_by('-datetime')[:10]
	counter = objs.count()
	ctx = {'obj':obj, 'objs':objs, 'counter':counter,'total':objs_count}
	return render_to_response('recruiter_profile.html',ctx,context_instance=RequestContext(request))

def recruiternew_view(request):
	if str(request.user) == "Visitor":
		raise Http404
	member = Member.objects.get(user=request.user)
	if member.role < 3:
		if request.method == "POST":
			form = recruiter_Form(request.POST)
			if form.is_valid():
				alert = '' #1=email exist,2=username exist
				username = form.cleaned_data['username'].lstrip().rstrip()
				first_name = form.cleaned_data['first_name'].lstrip().rstrip()
				last_name = form.cleaned_data['last_name'].lstrip().rstrip()
				email = form.cleaned_data['email'].lstrip().rstrip()
				temp_pass = form.cleaned_data['temp_pass'].lstrip().rstrip()
				user = User()
				user.username=username
				user.email=email
				user.first_name = first_name
				user.last_name = last_name
				user.set_password(temp_pass)
				user.save()
				member = Member(id=user.id)
				member.user_id = user.id
				member.role = 3
				member.save()
				url_base=request.build_absolute_uri('/')
				subject = "Welcome to Prosoft's Talent Management System (TMS)"
				html_content = "<h1>Welcome to Prosoft's Talent Management System (TMS). </h1>\
								<p>Please <a href='%slogin/'>log in</a> using your temporary username and password.</p> \
								<ul> \
									<li>Username: %s</li> \
									<li>Password: %s</li> \
								</ul> \
								<p>After logging in, please <a href='%saccount_password/'>change your password.</a></p> \
								<p><strong><em>Prosoft's Talent Management System</em></strong></p>"%(url_base,username,temp_pass,url_base)
				msg = EmailMultiAlternatives(subject,html_content,'from@server.com',[email])
				msg.attach_alternative(html_content,'text/html') #Definimos el contenido como HTML
				msg.send() # Enviamos correo
				#End email sent
				return redirect('view_recruiter_profile', id = user.id)
			else:
				ctx = {'form':form}
				return render_to_response('recruiter_new.html',ctx,context_instance=RequestContext(request))
		form= recruiter_Form()
		ctx = {'form':form}
		return render_to_response('recruiter_new.html',ctx,context_instance=RequestContext(request))
	return render_to_response('no_permission.html',context_instance=RequestContext(request))
	
def myprofile_view(request):
	obj = User.objects.get(id=request.user.id)
	activities_6 = Activity.objects.filter(recruiter=obj).prefetch_related('application','recruiter').order_by('-datetime')[:10]
	act_tot_c = Activity.objects.filter(recruiter=obj).count()
	activity_showing_count = activities_6.count()
	if request.method == "POST":
		form = recruiteredit_Form(request.POST, instance=request.user)
		form.actual_user = request.user
		if form.is_valid():
			form.save()
			#return redirect('view_myprofile')
			ctx = {'form':form,'obj':obj, 'activities':activities_6, 'counter':activity_showing_count,'total':act_tot_c, 'info':1}
			return render_to_response('myprofile.html',ctx,context_instance=RequestContext(request))
		else:
			ctx = {'form':form,'obj':obj,'activities':activities_6, 'counter':activity_showing_count,'total':act_tot_c}
			return render_to_response('myprofile.html',ctx,context_instance=RequestContext(request))
	form = recruiteredit_Form(instance=request.user)
	form.actual_user = request.user
	ctx = {'form':form,'obj':obj, 'activities':activities_6, 'counter':activity_showing_count,'total':act_tot_c}
	return render_to_response('myprofile.html',ctx,context_instance=RequestContext(request))

def recruiters_view(request):
	member = Member.objects.get(user=request.user)
	if member.role < 3:
		objs = User.objects.all().annotate(activities_count=Count('activity', distinct=True)).annotate(application_count=Count('application', distinct=True))
		objs_counter = objs.count()
		cxt = {'objs':objs,'counter':objs_counter}
		return render_to_response('recruiters.html',cxt,context_instance=RequestContext(request))
	return render_to_response('no_permission.html',context_instance=RequestContext(request))

def recruiters_rpt_view(request):
	objs = User.objects.all().annotate(activities_count=Count('activity', distinct=True)).annotate(application_count=Count('application', distinct=True))
	cxt = {'objs':objs}
	return render_to_response('recruiters_rpt.html',cxt,context_instance=RequestContext(request))
	
def qsearch_recruiter_view(request):
	search = ""
	objs = User.objects.all().annotate(activities_count=Count('activity', distinct=True)).annotate(application_count=Count('application', distinct=True))
	if request.method == "POST":
		form = search_Form(request.POST or None)
		if form.is_valid():
			search = form.cleaned_data['search']
			if search != "":
				search_list = search.lower().split(' ')
				objs = objs.filter(reduce(or_, [Q(first_name__icontains=c)|Q(last_name__icontains=c)|Q(email__icontains=c)|Q(username__icontains=c) for c in search_list])).distinct()
	objs_counter = objs.count()
	cxt = {'search':search,'objs':objs,'counter':objs_counter}
	return render_to_response('recruiters.html',cxt,context_instance=RequestContext(request))
	
########################################
#######   R E M I N D E R S  ###########
########################################

def reminder_view(request, id):
	objs = Reminder.objects.filter(active=True).exclude(id=id)
	objs = objs.exclude(~Q(recruiter=request.user),private=True)[:10]
	obj = Reminder.objects.get(id=id)
	related_count = Reminder.objects.filter(active=True, field_id=obj.id, model_name='reminder').exclude(id=id).count()
	model = obj.model_name
	obj_mod = view_name = None
	if model:
		mymodel = get_model('files', model)
		obj_mod = mymodel.objects.get(pk=obj.field_id)
	counter = objs.count()
	cxt = {'obj':obj, 'objs':objs, 'obj_mod':obj_mod, 'counter':counter, 'related':related_count}
	return render_to_response('reminder.html',cxt,context_instance=RequestContext(request))
	
def reminder_rpt_view(request, id):
	obj = Reminder.objects.get(id=id)
	model = obj.model_name
	obj_mod = view_name = None
	if model:
		mymodel = get_model('files', model)
		obj_mod = mymodel.objects.get(pk=obj.field_id)
	cxt = {'obj':obj, 'obj_mod':obj_mod}
	return render_to_response('reminder_rpt.html',cxt,context_instance=RequestContext(request))

def remindernew_view(request):
	#objs = Reminder.objects.filter(active=True)[:10]
	objs = Reminder.objects.exclude(~Q(recruiter=request.user),private=True)
	counter = 0
	if request.method == "POST":
		form = reminder_Form(request.POST)
		if form.is_valid():
			private = form.cleaned_data['private']
			content = form.cleaned_data['content']
			newobj = Reminder()
			newobj.recruiter = request.user
			newobj.content = content
			newobj.model_name = None
			newobj.field_id = None
			newobj.active = True
			newobj.private = private
			newobj.datetime = timezone.localtime(timezone.now())
			newobj.save() # Save info to Database
			return redirect('view_reminders')
		else:
			### Form not valid, Return ###
			#print "Form not valid: "+str(form.errors.as_text)
			ctx = {'form':form,'obj':obj,'documents':documents}
			return render_to_response('reminder_new.html',ctx,context_instance=RequestContext(request))
	form = reminder_Form()
	counter = objs.count()
	ctx = {'form':form,'objs':objs,'counter':counter}
	return render_to_response('reminder_new.html',ctx,context_instance=RequestContext(request))

def remindernew_view(request, model_name=None, field_id=None):
	objs = Reminder.objects.exclude(~Q(recruiter=request.user),private=True)
	counter = objs.count()
	#print "here"
	obj = None
	model = model_name
	id = field_id
	if model_name:
		#model was send
		mymodel = get_model('files', model_name)
		#print mymodel
		obj = mymodel.objects.get(pk=field_id)
		#print obj
	if request.method == "POST":
		form = reminder_Form(request.POST)
		if form.is_valid():
			private = form.cleaned_data['private']
			content = form.cleaned_data['content']
			newobj = Reminder()
			newobj.recruiter = request.user
			newobj.content = content
			newobj.model_name = model
			newobj.field_id = id
			newobj.private = private
			newobj.datetime = timezone.localtime(timezone.now())
			newobj.save() # Save info to Database
			
			RegisterTracking(request.user,'2',timezone.localtime(timezone.now()),newobj._meta.model_name,newobj.id,None,None,None,None)
			#print newobj
			#return HttpResponseRedirect('/reminders/')
			return redirect('view_reminders')
		else:
			### Form not valid, Return ###
			#print "Form not valid: "+str(form.errors.as_text)
			ctx = {'form':form,'obj':obj,'model':model,'id':field_id,'objs':objs,'counter':counter,}
			return render_to_response('reminder_new.html',ctx,context_instance=RequestContext(request))
	form = reminder_Form()
	ctx = {'form':form,'obj':obj,'model':model,'id':field_id,'counter':counter,'objs':objs}
	return render_to_response('reminder_new.html',ctx,context_instance=RequestContext(request))

def reminderedit_view(request, id):
	if str(request.user) == "Visitor":
		raise Http404
	reminders  = Reminder.objects.all()
	obj = reminders.get(pk=id)
	reminders  = reminders.exclude(pk=id)[:7]
	initial_data={'private':obj.private ,'content':obj.content,'active':obj.active}
	model = None
	if obj.model_name:
		## model was sent
		mymodel = get_model('files', obj.model_name)
		model = mymodel.objects.get(pk=obj.field_id)
	if request.method == "POST":
		form = reminder_Form(request.POST, initial=initial_data)
		if form.is_valid():
			private = form.cleaned_data['private']
			content = form.cleaned_data['content']
			active = form.cleaned_data['active']
			obj.recruiter = request.user
			obj.model_name = obj.model_name
			obj.field_id = obj.field_id
			obj.datetime = timezone.localtime(timezone.now())
			obj.active = active
			obj.private = private
			obj.content = content
			obj.save() # Save info to Database
			if form.has_changed():
				for item in form.changed_data:
					if item == 'private':
						## Change 'True' to 'Private' and/or 'False' to 'Public'
						old = new = 'Public'
						if initial_data[item] == True:
							old = 'Private'
						if form.cleaned_data[item] == True:
							new = 'Private'
						RegisterTracking(request.user,'1',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,item,old,new,None)
					elif item == 'active':
						## Change 'True' to 'Active' and/or 'False' to 'Inactive'
						old = new = 'Inactive'
						if initial_data[item] == True:
							old = 'Active'
						if form.cleaned_data[item] == True:
							new = 'Active'
						RegisterTracking(request.user,'1',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,item,old,new,None)
					else:
						RegisterTracking(request.user,'1',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,item,initial_data[item],form.cleaned_data[item],None)
			return redirect('view_reminder', id = obj.id)
		else:
			### Form not valid, Return ###
			#print "Form not valid: "+str(form.errors.as_text)
			ctx = {'form':form,'obj':obj,'model':model,}
			return render_to_response('reminder_edit.html',ctx,context_instance=RequestContext(request))
	form = reminder_Form(initial=initial_data)
	ctx = {'form':form,'obj':obj,'model':model,}
	return render_to_response('reminder_edit.html',ctx,context_instance=RequestContext(request))

def reminderdelete_view(request, id):
	if str(request.user) == "Visitor":
		raise Http404
	print "in reminderdelete"
	info = 0
	obj = Reminder.objects.get(id=id)
	#o = Reminder.objects.filter(profile=obj).distinct()
	reminders = Reminder.objects.filter(active=True, field_id=obj.id, model_name='reminder').exclude(id=id).distinct()
	if request.method == "POST":
		print "in post"
		if len(reminders) > 0:
			info = 1
			ctx = {'info':info,'obj':obj,'reminders':reminders}
			return render_to_response('reminder_delete.html',ctx,context_instance=RequestContext(request))
		else:
			if not Reminder.objects.filter(active=True, field_id=obj.id, model_name='reminder').exists():
				#extra = '<b>Reminder: </b> %s<br/><b>Content:</b> %s<br/><b>Salary:</b> %s' % (obj ,obj.created.strftime("%b %d, %Y - %I:%M %p"),obj.content)
				extra = '<b>Reminder:</b> %s<br/><b>Content:</b> %s' % (obj,obj.content)
				RegisterTracking(request.user,'3',timezone.localtime(timezone.now()),obj._meta.model_name.capitalize(),None,None,None,None,extra)
				obj.delete()
				return redirect('view_reminders')
	if len(reminders) > 0:
		info = 1
	print "in get"
	ctx = {'info':info,'obj':obj,'reminders':reminders}
	return render_to_response('reminder_delete.html',ctx,context_instance=RequestContext(request))
"""
class ReminderDelete(DeleteView):
	model = Reminder
	success_url = reverse_lazy('view_reminders')
	def dispatch(self, request, *args, **kwargs):
		### Making sure that only authors can delete Articles ###
		obj = self.get_object()
		if obj.recruiter != self.request.user:
			#messages.error(request, 'Document not deleted.')
			return redirect('view_reminder', id = obj.id)
		#messages.success(request, 'Document deleted.')
		extra = '<b>Date and Time:</b> %s<br/><b>Content:</b> %s' % (obj.datetime.strftime("%b %d, %Y - %I:%M %p"), obj.content)
		RegisterTracking(request.user,'3',timezone.localtime(timezone.now()),obj._meta.model_name.capitalize(),None,None,None,None,extra)
		return super(ReminderDelete, self).dispatch(request, *args, **kwargs)
"""
def reminders_view(request, active=None, private=None, mine=None):
	objs = Reminder.objects.exclude(~Q(recruiter=request.user),private=True)
	title_my = title_private = title_all = None
	if active == '1':
		title_all = "Active"
		objs = objs.filter(active=True)
		#Do something
	elif active == '0':
		title_all = "Inactive"
		objs = objs.filter(active=False)
	elif active == None:
		active = '3'
	if mine == '1':
		objs = objs.filter(recruiter=request.user)
		title_my = "My"
	elif mine == None:
		mine = '0'
	if private == '1':
		objs = objs.filter(recruiter=request.user, private=True)
		title_private = "Private"
	elif private == None:
		private = '0'
	objs_counter = objs.count()
	cxt = {'objs':objs,'counter':objs_counter,'active':active,'private':private,'mine':mine,'title_all':title_all,'title_private':title_private,'title_my':title_my}
	return render_to_response('reminders.html',cxt,context_instance=RequestContext(request))

def reminders_rpt_view(request, active=None, private=None, mine=None):
	# active ( 1 = active, 0 = Inactive, 3 or None = All)
	# mine ( 1 = mine, 0 or None = Everybody)
	# private (1 = private, 0 or None = public)
	objs = Reminder.objects.exclude(~Q(recruiter=request.user),private=True)
	title_my = title_private = title_all = None
	if active == '1':
		title_all = "Active"
		objs = objs.filter(active=True)
		#Do something
	elif active == '0':
		title_all = "Inactive"
		objs = objs.filter(active=False)
	elif active == None:
		active = '3'
	if mine == '1':
		objs = objs.filter(recruiter=request.user)
		title_my = "My"
	elif mine == None:
		mine = '0'
	if private == '1':
		objs = objs.filter(recruiter=request.user, private=True)
		title_private = "Private"
	elif private == None:
		private = '0'
	objs_counter = objs.count()
	cxt = {'objs':objs,'counter':objs_counter,'active':active,'private':private,'mine':mine,'title_all':title_all,'title_private':title_private,'title_my':title_my}
	return render_to_response('reminders_rpt.html',cxt,context_instance=RequestContext(request))

def qsearch_reminder_view(request):
	search = ""
	objs = Reminder.objects.all().select_related('recruiter')
	if request.method == "POST":
		form = search_Form(request.POST or None)
		if form.is_valid():
			search = form.cleaned_data['search']
			if search != "":
				search_list = search.lower().split(' ')
				tag_qs = reduce(and_, (Q(content__icontains=x) for x in search_list))
				objs = objs.filter(tag_qs)
	objs_counter = objs.count()
	cxt = {'search':search,'objs':objs,'counter':objs_counter}
	return render_to_response('reminders.html',cxt,context_instance=RequestContext(request))

########################################
#######       V E N D O R      #########
########################################

def vendors_view(request):
	objs = Vendor.objects.filter(active=True).annotate(ope_count=Count('opening'))
	counter = objs.count()
	ctx = {'objs':objs,'counter':counter}
	return render_to_response('vendors.html',ctx,context_instance=RequestContext(request))
	
def qsearch_vendor_view(request):
	search = ""
	objs = Vendor.objects.filter(active=True).annotate(ope_count=Count('opening'))
	if request.method == "POST":
		form = search_Form(request.POST or None)
		if form.is_valid():
			search = form.cleaned_data['search']
			if search != "":
				search_list = search.lower().split(' ')
				objs = objs.filter(reduce(or_, [Q(name__icontains=c)|Q(contactname__icontains=c) for c in search_list])).distinct()
	counter = objs.count()
	ctx = {'search':search,'objs':objs, 'counter':counter}
	return render_to_response('vendors.html',ctx,context_instance=RequestContext(request))
	
def vendors_rpt_view(request):
	objs = Vendor.objects.filter(active=True).annotate(ope_count=Count('opening'))
	counter = objs.count()
	ctx = {'objs':objs,'counter':counter}
	return render_to_response('vendors_rpt.html',ctx,context_instance=RequestContext(request))
	
def vendor_view(request, id):
	obj = Vendor.objects.get(id=id)

	openings_total = Opening.objects.filter(vendor=obj, active=True).count()
	openings = Opening.objects.filter(vendor=obj, active=True).prefetch_related('skills').annotate(app_count=Count('applications'))[:10]
	openings_counter = openings.count()
	
	ctx = {'obj':obj,'openings':openings,'counter':openings_counter,'total':openings_total}
	return render_to_response('vendor.html',ctx,context_instance=RequestContext(request))

def vendornew_view(request):
	if request.method == "POST":
		form = vendor_Form(request.POST)
		if form.is_valid():
			data = form.save()
			extra = '<b>Name:</b> %s' % (data.name)
			RegisterTracking(request.user,'2',timezone.localtime(timezone.now()),data._meta.model_name,data.id,None,None,None,extra)
			return redirect('view_vendor', id = data.id)
		else:
			#print "Form not valid: "+str(form.errors.as_text)
			ctx = {'form':form}
			return render_to_response('vendor_new.html',ctx,context_instance=RequestContext(request))
	form = vendor_Form()
	ctx = {'form':form}
	return render_to_response('vendor_new.html',ctx,context_instance=RequestContext(request))

def vendoredit_view(request, id):
	if str(request.user) == "Visitor":
		raise Http404
	obj = Vendor.objects.get(pk=id)
	initial_data={'name':obj.name,'contactname':obj.contactname,'email':obj.email,'phone':obj.phone,'address':obj.address,'moreinfo':obj.moreinfo,}
	if request.method == "POST":
		form = vendor_Form(request.POST, instance=obj)
		if form.is_valid():
			form.save()
			if form.has_changed():
				for item in form.changed_data:
					RegisterTracking(request.user,'1',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,item,initial_data[item],form.cleaned_data[item],None)
			return redirect('view_vendor', id = obj.id)
		else:
			ctx = {'form':form}
			#print "Form not valid: "+str(form.errors.as_text)
			return render_to_response('vendor_edit.html',ctx,context_instance=RequestContext(request))
	form = vendor_Form(instance=obj)
	ctx = {'form':form,'obj':obj}
	return render_to_response('vendor_edit.html',ctx,context_instance=RequestContext(request))
	
def vendordelete_view(request, id):
	if str(request.user) == "Visitor":
		raise Http404
	info = 0
	obj = Vendor.objects.get(id=id)
	o = Opening.objects.filter(vendor=obj).distinct()
	if request.method == "POST":
		if len(o) > 0:
			info = 1
			ctx = {'info':info,'obj':obj,'openings':o}
			return render_to_response('vendor_delete.html',ctx,context_instance=RequestContext(request))
		else:
			if not Opening.objects.filter(vendor=obj).exists():
				extra = '<b>Name:</b> %s' % (obj.name)
				RegisterTracking(request.user,'3',timezone.localtime(timezone.now()),obj._meta.model_name.capitalize(),None,None,None,None,extra)
				obj.delete()
				return redirect('view_vendors')
				#return HttpResponseRedirect('/vendors/')
	if len(o) > 0:
		info = 1
	ctx = {'info':info,'obj':obj,'openings':o}
	return render_to_response('vendor_delete.html',ctx,context_instance=RequestContext(request))

######################################
#######       S K I L L      #########
######################################

def skills_view(request, page=None):
	objs = Skill.objects.all().annotate(openings_count=Count('open_skills_main', distinct=True)).annotate(profiles_count=Count('profile', distinct=True))
	counter = objs.count()
	paginator = Paginator(objs,30)
	try:
		page = int(page)
	except:
		page = 1
	try:
		paginatorlist = paginator.page(page)
	except (EmptyPage, InvalidPage):
		paginatorlist = paginator.page(paginator.num_pages)
	cxt = {'paginatorlist':paginatorlist, 'counter':counter}
	#cxt = {'objs':objs, 'counter':counter}
	return render_to_response('skills.html',cxt,context_instance=RequestContext(request))

def qsearch_skill_view(request):
	search = ""
	objs = Skill.objects.all()
	if request.method == "POST":
		form = search_Form(request.POST or None)
		if form.is_valid():
			search = form.cleaned_data['search']
			if search != "":
				search_list = search.lower().split(' ')
				objs = objs.filter(reduce(and_, [Q(name__icontains=c) for c in search_list])).distinct()
	counter = objs.count()
	cxt = {'search':search,'objs':objs, 'counter':counter}
	return render_to_response('skills.html',cxt,context_instance=RequestContext(request))

def skills_rpt_view(request):
	objs = Skill.objects.all()
	counter = objs.count()
	cxt = {'objs':objs, 'counter':counter}
	return render_to_response('skills_rpt.html',cxt,context_instance=RequestContext(request))
	
def skill_view(request, id):
	obj = Skill.objects.get(id=id)
	profiles_total = Profile.objects.filter(skills=obj).count()
	profiles = Profile.objects.filter(skills=obj).prefetch_related('skills').annotate(app_count=Count('applications')).select_related('applicant','applicant__state','applicant__country')
	profiles_counter = profiles.count()
	
	openings_total = Opening.objects.filter(skills=obj).count()
	openings = Opening.objects.filter(skills=obj).prefetch_related('skills').annotate(app_count=Count('applications')).select_related('state').distinct()
	opening_counter = openings.count()
	
	ctx = {'obj':obj,
			'profiles_total':profiles_total,'profiles':profiles,'profiles_counter':profiles_counter,
			'openings_total':openings_total,'openings':openings,'opening_counter':opening_counter,
		}
	return render_to_response('skill.html',ctx,context_instance=RequestContext(request))

def skillnew_view(request):
	if str(request.user) == "Visitor":
		raise Http404
	if request.method == "POST":
		form = skill_Form(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			description = form.cleaned_data['description']
			obj = Skill()
			obj.name = name
			obj.description = description
			obj.save() # Save info to Database
			extra = '<b>Name:</b> %s' % (obj.name)
			RegisterTracking(request.user,'2',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,None,None,None,extra)
			return redirect('view_skill', id = obj.id)
			#return HttpResponseRedirect('/skill/%s/'%(obj.id))
		else:
			ctx = {'form':form}
			return render_to_response('skill_new.html',ctx,context_instance=RequestContext(request))
	form= skill_Form()
	ctx = {'form':form}
	return render_to_response('skill_new.html',ctx,context_instance=RequestContext(request))

def skilldelete_view(request, id):
	if str(request.user) == "Visitor":
		raise Http404
	info = 0
	obj = Skill.objects.get(id=id)
	p = Profile.objects.filter(skills=obj).distinct()
	o = Opening.objects.filter(skills=obj).distinct()
	if request.method == "POST":
		if len(p)+len(o) > 0:
			info = 1
			ctx = {'info':info,'obj':obj,'profiles':p ,'openings':o}
			return render_to_response('skill_delete.html',ctx,context_instance=RequestContext(request))
		else:
			if not Opening.objects.filter(skills=obj).exists():
				extra = '<b>Name:</b> %s' % (obj.name)
				RegisterTracking(request.user,'3',timezone.localtime(timezone.now()),obj._meta.model_name.capitalize(),None,None,None,None,extra)
				obj.delete()
				return HttpResponseRedirect('/skills/')
	if len(p)+len(o) > 0:
		info = 1
	ctx = {'info':info,'obj':obj,'profiles':p ,'openings':o}
	return render_to_response('skill_delete.html',ctx,context_instance=RequestContext(request))

def skilledit_view(request, id):
	if str(request.user) == "Visitor":
		raise Http404
	obj = Skill.objects.get(pk=id)
	initial_data={'name':obj.name,'description':obj.description,}
	if request.method == "POST":
		form = skilledit_Form(request.POST, instance=obj)
		form.actual_skill = obj
		if form.is_valid():
			form.save()
			if form.has_changed():
				for item in form.changed_data:
					RegisterTracking(request.user,'1',timezone.localtime(timezone.now()),obj._meta.model_name,obj.id,item,initial_data[item],form.cleaned_data[item],None)
			#return HttpResponseRedirect('/skill/%s/'%(obj.id))
			return redirect('view_skill', id = obj.id)
		else:
			#print "Form not valid: "+str(form.errors.as_text)
			ctx = {'form':form,'obj':obj}
			return render_to_response('skill_edit.html',ctx,context_instance=RequestContext(request))
	form = skilledit_Form(instance=obj)
	form.actual_skill = obj
	ctx = {'form':form,'obj':obj}
	return render_to_response('skill_edit.html',ctx,context_instance=RequestContext(request))


# Error Handlers - Start
def myerror500(request):
	#print '*'*30
	print "in Error 500"
	patherror = request.path
	#template = loader.get_template('500c.html')
	ctx = {'patherror':patherror}
	#return HttpResponse(content=template.render(ctx), content_type='text/html; charset=utf-8', status=500)
	return render_to_response('500c.html',ctx,context_instance=RequestContext(request))

def myerror404(request):
	patherror = request.path	
	ctx = {'patherror':request.path}
	return render_to_response('404c.html',ctx,context_instance=RequestContext(request))
