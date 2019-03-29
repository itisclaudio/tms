from django.db import models
from django.utils import timezone #Applicant
from django.contrib.auth.models import User #Process
from datetime import datetime #Profile,Applicant


class Skill (models.Model):
	name        	= models.CharField(max_length=75, unique=True)
	description		= models.TextField(max_length=4000, null=True, blank=True)
	def __unicode__(self):
		if self.description:
			return "%s | %s"%(self.name[:20],self.description[:40])
		else:
			return "%s"%(self.name[:20])
	class Meta:
		ordering = ('name',)

class State(models.Model):
	name        = models.CharField(max_length=35)
	code 		= models.CharField(max_length=2)
	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ('name',)
		
class Country(models.Model):
	code 		= models.CharField(max_length=2, null=True, blank=True)
	name        = models.CharField(max_length=45)
	def __unicode__(self):
		return self.name
	class Meta:
		ordering = ('name',)
		
class Applicant (models.Model):
	WORK_STATUS = (('1', "US Citizen"),('2', "Work Permit/Legal Resident"),('3', "Work Visa/H1"),('4', "Not Authorized"),)
	firstname		= models.CharField(max_length=75)
	lastname        = models.CharField(max_length=75)
	email 			= models.EmailField(max_length=90, null=True, blank=True)
	dob				= models.DateField(null=True ,blank=True)
	phone_1			= models.CharField(max_length=35, null=True ,blank=True) # Best number to be reached
	phone_2			= models.CharField(max_length=35, null=True ,blank=True)
	work_status 	= models.CharField(max_length=1, choices=WORK_STATUS, default='1')
	availability 	= models.DateField(blank=True, null=True, default=timezone.now)
	relocation 		= models.BooleanField(default=False) # Open to relocate? 1=Yes, 0=No
	righttorep 		= models.BooleanField(default=False, verbose_name=u"Right to Represent")#Right to represent
	address			= models.CharField(max_length=200, null=True ,blank=True)
	city			= models.CharField(max_length=65, null=True ,blank=True,verbose_name=u"City",  help_text=u"Enter city")
	state			= models.ForeignKey(State, null=True ,blank=True)
	country			= models.ForeignKey(Country, null=True ,blank=True)
	zipcode			= models.CharField(max_length=10, null=True ,blank=True)
	#profiles 		= models.ManyToManyField(Skill, related_name='profiles', through='Profile', blank=True)
	experience		= models.IntegerField(null=True ,blank=True) # Total years of experience
	usexperience	= models.IntegerField(null=True ,blank=True) # Experience in the US
	education		= models.CharField(max_length=200, null=True ,blank=True) #School and grade
	besttime		= models.CharField(max_length=200, null=True ,blank=True)#Best time to be reached
	salary_cur		= models.CharField(max_length=40, null=True ,blank=True) #Current Salary
	salary_exp		= models.CharField(max_length=40, null=True ,blank=True) #Salary expectations
	active			= models.BooleanField(default=True ,blank=True)
	def __unicode__(self):
		return "%s %s"%(self.firstname,self.lastname)

	@property
	def monthsexp(self):
		mod = ''
		if self.experience:
			months = self.experience
			mod = months % 12
		return mod

	@property
	def yearsexp(self):
		years = ''
		if self.experience:
			months = self.experience
			years = months/12
		return years

	@property
	def usmonthsexp(self):
		mod = ''
		if self.usexperience:
			months = self.usexperience
			mod = months % 12
		return mod

	@property
	def usyearsexp(self):
		years = ''
		if self.usexperience:
			months = self.usexperience
			years = months/12
		return years

	#def age(self):
	#	return int((datetime.date.today() - self.dob).days / 365.25  )
	class Meta:
		ordering = ('lastname','firstname',)

def generate_applicant_doc_name(instance,filename):
	print "in generate_applicant_doc_name"
	ext = filename.split('.')[-1]
	rightnow = timezone.now()	
	type = instance.type
	if type == '1':
		type = 'rtr'
	if type == '2':
		type = 'visa'
	if type == '3':
		type = 'id'
	if type == '2':
		type = 'nda'
	date = "%s-%s-%s_%s%s" %(str(rightnow.year),str(rightnow.month),str(rightnow.day),str(rightnow.hour),str("{0:0>2}".format(rightnow.minute)))
	f_name = instance.applicant.firstname.strip()
	f_name =  f_name.lower().replace(" ", "_").replace("'", "").replace(".", "")
	l_name = instance.applicant.lastname.strip()
	l_name =  l_name.lower().replace(" ", "_").replace("'", "").replace(".", "")
	return "docs/%s-%s_%s-%s.%s" %(type,f_name,l_name,date,ext.lower())
		
class Applicant_Doc(models.Model):
	DOC_TYPE = (('', "-Select Type-"),('1', "RTR (Right to Represent)"),('2', "Visa copy (H1B, OPT)"),('3', "Photo ID (DL, EAD card)"),('4', "NDA (Non-discloser Agreement)"),)
	applicant	= models.ForeignKey(Applicant)
	document	= models.FileField(upload_to=generate_applicant_doc_name,null=True ,blank=True)
	type		= models.CharField(max_length=1, choices=DOC_TYPE, default='1',null=False)
	datetime	= models.DateTimeField(default=timezone.now)
	def __unicode__(self):
		#return unicode(self.profile)
		return "%s / %s"%(self.get_type_display(), self.applicant)

	class Meta:
		ordering = ('-datetime',)
		
	def __str__(self):
		return self.document.name
	
#
class Profile(models.Model):
	applicant	= models.ForeignKey(Applicant)
	#skill		= models.ForeignKey(Skill)
	#skills 		= models.ManyToManyField(Skill, related_name='profiles', through='Profile', blank=True)
	skills 		= models.ManyToManyField(Skill)
	skills_sec	= models.ManyToManyField(Skill, related_name='skills_sec', blank=True)
	experience	= models.IntegerField(null=True ,blank=True)
	datetime	= models.DateTimeField(default=timezone.now)
	def __unicode__(self):
		#date = "%s-%s-%s %s:%s" %(str(self.datetime.year),str(self.datetime.month),str(self.datetime.day),str(self.datetime.hour),str("{0:0>2}".format(self.datetime.minute)))
		#date = "%s-%s-%s" %(str(self.datetime.year),str(self.datetime.month),str(self.datetime.day))
		#ret = "%s | %s "%(date, self.applicant[:15])
		#ret = "%s | %s "%(date, self.applicant)
		skill = ", ".join(str(seg.name) for seg in self.skills.all())
		ret = "%s | %s "%(self.applicant, skill)
		#ret = "%s | %s "%(date, self.applicant)
		if self.applicant.state:
			ret = "%s | %s "%(ret, self.applicant.state.code)
		#if self.skills:
			#skill = ", ".join(str(seg.name) for seg in self.skills.all())
			#skills = self.skills.all()
			#ret = "%s | %s "%(ret, skill)
		return ret

	def yearsexp(self):
		years = ''
		if self.experience:
			months = self.experience
			years = months/12
		return years

	def monthsexp(self):
		mod = ''
		if self.experience:
			months = self.experience
			mod = months % 12
		return mod

	class Meta:
		ordering = ('-datetime','applicant',)

def generate_doc_name(instance,filename):
	print "in generate_doc_name"
	ext = filename.split('.')[-1]
	rightnow = timezone.now()	
	type = instance.type
	if type == '1':
		type = 'resume'
	if type == '2':
		type = 'cover_letter'
	date = "%s-%s-%s_%s%s" %(str(rightnow.year),str(rightnow.month),str(rightnow.day),str(rightnow.hour),str("{0:0>2}".format(rightnow.minute)))
	#skill = instance.profile.skill.name.lower().replace(" ", "_").replace("'", "").replace(".", "")
	f_name = instance.profile.applicant.firstname.strip()
	f_name =  f_name.lower().replace(" ", "_").replace("'", "").replace(".", "")
	l_name = instance.profile.applicant.lastname.strip()
	l_name =  l_name.lower().replace(" ", "_").replace("'", "").replace(".", "")
	#return "docs/%s-%s_%s-%s-%s.%s" %(type,f_name,l_name,skill,date,ext.lower())
	return "docs/%s-%s_%s-%s.%s" %(type,f_name,l_name,date,ext.lower())

class Profile_Doc(models.Model):
	#DOC_TYPE = (('1', "Resume"),('2', "Cover letter"),('3', "RTR (Right to Represent)"),('4', "Visa copy (H1B, OPT)"),('5', "Photo ID (DL, EAD card)"),('6', "NDA (Non-discloser Agreement)"),)
	DOC_TYPE = (('', "-Select Type-"),('1', "Resume"),('2', "Cover letter"),)
	profile		= models.ForeignKey(Profile)
	location	= models.FileField(upload_to=generate_doc_name,null=True ,blank=True)
	type		= models.CharField(max_length=1, choices=DOC_TYPE, default='1')
	datetime	= models.DateTimeField(default=timezone.now)
	def __unicode__(self):
		#return unicode(self.profile)
		return "%s / %s"%(self.get_type_display(), self.profile)

	class Meta:
		ordering = ('-datetime',)
		
	def __str__(self):
		return self.location.name
#000
class Opening (models.Model):
	WORK_AUTHORIZATION = (('', "-Select Type-"),('1', "US Citizen"),('2', "Work Permit/Legal Resident"),('3', "Work Visa/H1"),)
	CONTRACT_TYPE = (('', "-Select Type-"),('1', "Full time/Direct"),('2', "Contract to hire"),('3', "Contract"),)
	startdate		= models.DateField(blank=True, default=timezone.now)
	role			= models.CharField(max_length=75)
	skills 			= models.ManyToManyField(Skill, related_name='open_skills_main', blank=True)
	skills_sec		= models.ManyToManyField(Skill, related_name='open_skills_sec', blank=True)
	responsibilities = models.TextField(max_length=4000, null=True ,blank=True)
	rate			= models.CharField(max_length=35, null=True ,blank=True)
	city			= models.CharField(max_length=65, null=True ,blank=True)
	state			= models.ForeignKey(State, null=True ,blank=True)
	duration		= models.IntegerField(null=True ,blank=True)
	experience		= models.IntegerField(null=True ,blank=True) # Total years of experience needed
	contract		= models.CharField(max_length=1, choices=CONTRACT_TYPE, default='1',null=True ,blank=True)
	work_auth		= models.CharField(max_length=1, choices=WORK_AUTHORIZATION, default='1',null=True ,blank=True)
	applications	= models.ManyToManyField(Profile, related_name='applications', through='Application', blank=True)
	active			= models.BooleanField(default=True ,blank=True)

	def __unicode__(self):
		ret = self.role[:20]
		skill = ", ".join(str(seg.name) for seg in self.skills.all())
		ret = "%s | %s "%(ret, skill)
		if self.state:
			ret = "%s | %s "%(ret, self.state.code)
		return ret

	def yearsdur(self):
		years = ''
		if self.duration:
			months = self.duration
			years = months/12
		return years

	def monthsdur(self):
		mod = ''
		if self.duration:
			months = self.duration
			mod = months % 12
		return mod

	def yearsexp(self):
		years = ''
		if self.experience:
			months = self.experience
			years = months/12
		return years

	def monthsexp(self):
		mod = ''
		if self.experience:
			months = self.experience
			mod = months % 12
		return mod

	class Meta:
		ordering = ('startdate',)

class Application(models.Model):
	APPLICATION_STATUS = (('', "-Select Status-"),('1', "New"),('2', "Ongoing"),('3', "Ended"),)
	profile			= models.ForeignKey(Profile)
	opening			= models.ForeignKey(Opening)
	recruiter		= models.ForeignKey(User, blank=True)
	datetime		= models.DateTimeField(default=timezone.now)
	#recruiter 		= models.ManyToManyField(User, related_name='recruiter', through='Activity', blank=True)
	activities 		= models.ManyToManyField(User, related_name='activities', through='Activity', blank=True)
	status			= models.CharField(max_length=1, choices=APPLICATION_STATUS, default='1')
	def __unicode__(self):
		return "%s - %s"%(self.opening, self.profile)
	class Meta:
		ordering = ('status','-datetime',)
		unique_together = ('profile', 'opening',)

class Activity(models.Model):
	INTERACTION_TYPE = (('1', "Phone call"),('2', "In Person"),('3', "No Interaction"),)
	application		= models.ForeignKey(Application)
	recruiter		= models.ForeignKey(User)
	datetime		= models.DateTimeField(default=timezone.now)
	type			= models.CharField(max_length=1, choices=INTERACTION_TYPE, default='1')
	notes 			= models.TextField(max_length=4000, null=True ,blank=True)
	def __unicode__(self):
		return "%s, %s"%(self.application,self.datetime)
	class Meta:
		ordering = ('-datetime',)
