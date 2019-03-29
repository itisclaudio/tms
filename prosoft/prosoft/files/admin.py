from django.contrib import admin
from prosoft.files.models import (
	Applicant,
	Applicant_Doc,
	Skill,
	State,
	Country,
	Member,
	Opening,
	Profile,
	Profile_Doc,
	Application,
	Activity,
	Reminder,
	Tracking,
	Vendor,
	)

class applicantAdmin(admin.ModelAdmin):
	list_display = ('id','firstname','lastname')
	list_filter = ('active',)
	search_fields = ['lastname','firstname']
	#fields = ('title','first_name','last_name','sex','dob','photo')

class applicationAdmin(admin.ModelAdmin):
	list_display = ('id','profile','opening')
	list_filter = ('profile',)

class countryAdmin(admin.ModelAdmin):
	list_display = ('id','code','name')
	search_fields = ['code','name']

class memberAdmin(admin.ModelAdmin):
	list_display = ('id','user','role')
	
class openingAdmin(admin.ModelAdmin):
	list_display = ('id','role','open','contract','work_auth')
	search_fields = ['code','name']
	
class stateAdmin(admin.ModelAdmin):
	list_display = ('id','code','name')
	search_fields = ['code','name']

class skillAdmin(admin.ModelAdmin):
	list_display = ('id','name','description')
	search_fields = ['name','description']

class vendorAdmin(admin.ModelAdmin):
	list_display = ('id','name','contactname','updated','created',)
	search_fields = ['name',]
	
class profiledocAdmin(admin.ModelAdmin):
	list_display = ('id','location',)

class ReminderAdmin(admin.ModelAdmin):
	list_display = ('id','__unicode__','content','private','active',)
	search_fields = ['model_name',]
	list_filter = ('recruiter',)
	
class TrackingAdmin(admin.ModelAdmin):
	list_display = ('id','__unicode__','get_type_display','entity','entity_field',)
	search_fields = ['entity',]
	list_filter = ('recruiter',)
	
class applicantdocAdmin(admin.ModelAdmin):
	list_display = ('id','document',)
	
admin.site.register(Applicant, applicantAdmin)
admin.site.register(Applicant_Doc, applicantdocAdmin)
admin.site.register(Skill, skillAdmin)
admin.site.register(State, stateAdmin)
admin.site.register(Country, countryAdmin)
admin.site.register(Member, memberAdmin)
admin.site.register(Opening, openingAdmin)
admin.site.register(Profile)
admin.site.register(Profile_Doc, profiledocAdmin)
admin.site.register(Application, applicationAdmin)
admin.site.register(Activity)
admin.site.register(Reminder, ReminderAdmin)
admin.site.register(Tracking, TrackingAdmin)
admin.site.register(Vendor, vendorAdmin)