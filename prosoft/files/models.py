from django.db import models
from django.utils import timezone #Applicant
from django.contrib.auth.models import User #Process
from datetime import datetime #Profile,Applicant
"""
class EmailQueue(models.Model):
	##Stores information to be sent by email 
	date	= models.DateTimeField(default=timezone.now)
	username	= models.CharField(max_length=30, null=True ,blank=True)
	subject	= models.CharField(max_length=120, null=True ,blank=True)
	object	= models.CharField(max_length=30, null=True ,blank=True)
	url_plus	= models.CharField(max_length=300, null=True ,blank=True)
	sent_flag	= models.BooleanField(default=False)
"""
class Member(models.Model):
	ROLE = ((0, "Developer"),(1, "Admin"),(2, "Manager"),(3, "Recruiter"),)
	user	= models.OneToOneField(User)
	role	= models.IntegerField(null=True ,blank=True, choices=ROLE, default=3)

class Skill (models.Model):
	name        	= models.CharField(max_length=75, unique=True)
	description		= models.TextField(max_length=4000, null=True, blank=True)
	def __unicode__(self):
		return self.name
			
	def save(self, *args, **kwargs):
		if self.name:
			self.name = self.name.strip()
		if self.description:
			self.description = self.description.strip()
		super(Skill, self).save(*args, **kwargs)

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
	WORK_STATUS = (('1', "USC"),('2', "GC"),('3', "H1"),('4', "EAD"),('5', "TN"),('9', "Not Authorized"))
	firstname		= models.CharField(max_length=75)
	lastname        = models.CharField(max_length=75)
	email 			= models.EmailField(max_length=90, null=True, blank=True)
	dob				= models.DateField(null=True ,blank=True)
	phone_1			= models.CharField(max_length=35, null=True ,blank=True) # Best number to be reached
	phone_2			= models.CharField(max_length=35, null=True ,blank=True)
	work_status 	= models.CharField(max_length=1, choices=WORK_STATUS, default='3')
	availability 	= models.DateField(blank=True, null=True, default=timezone.now)
	available 		= models.BooleanField(default=True) # 1,True=Yes, 0,False=No
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
	updated			= models.DateTimeField(default=timezone.now)
	created			= models.DateTimeField(default=timezone.now)
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
	#	return int((datetime.now() - self.dob).days / 365.25  )
	class Meta:
		ordering = ('firstname','lastname',)

def generate_applicant_doc_name(instance,filename):
	#print "in generate_applicant_doc_name"
	ext = filename.split('.')[-1]
	rightnow = timezone.now()
	type = instance.type
	if type == '1':
		type = 'rtr'
	if type == '2':
		type = 'visa'
	if type == '3':
		type = 'id'
	if type == '4':
		type = 'nda'
	if type == '5':
		type = 'doc'
	date = "%s-%s-%s_%s%s" %(str(rightnow.year),str(rightnow.month),str(rightnow.day),str(rightnow.hour),str("{0:0>2}".format(rightnow.minute)))
	f_name = instance.applicant.firstname.strip()
	f_name =  f_name.lower().replace(" ", "_").replace("'", "").replace(".", "")
	l_name = instance.applicant.lastname.strip()
	l_name =  l_name.lower().replace(" ", "_").replace("'", "").replace(".", "")
	return "docs/%s_%s-%s-%s.%s" %(f_name,l_name,type,date,ext.lower())
		
class Applicant_Doc(models.Model):
	DOC_TYPE = (('', "-Select Type-"),('1', "RTR (Right to Represent)"),('2', "Visa"),('3', "Photo ID"),('4', "NDA (Non-discloser Agreement)"),('5', "Other"),)
	applicant	= models.ForeignKey(Applicant)
	document	= models.FileField(upload_to=generate_applicant_doc_name,null=True ,blank=True)
	type		= models.CharField(max_length=1, choices=DOC_TYPE, default='2',null=False)
	datetime	= models.DateTimeField(default=timezone.now)
	def __unicode__(self):
		#return unicode(self.profile)
		return "%s / %s"%(self.get_type_display(), self.applicant)

	class Meta:
		ordering = ('-datetime',)
		
	def __str__(self):
		return self.document.name

class Profile(models.Model):
	applicant	= models.ForeignKey(Applicant)
	skills 		= models.ManyToManyField(Skill)
	skills_sec	= models.ManyToManyField(Skill, related_name='skills_sec', blank=True)
	experience	= models.IntegerField(null=True ,blank=True)
	datetime	= models.DateTimeField(default=timezone.now)
	salary		= models.CharField(max_length=40, null=True ,blank=True) #Salary expectations
	updated		= models.DateTimeField(default=timezone.now)
	created		= models.DateTimeField(default=timezone.now)
	def __unicode__(self):
		skills = ""
		for skill in self.skills.all():
			skills = skills+" ["+skill.name+"]"
		ret = "%s %s"%(self.applicant, skills)
		return ret

	@property
	def yearsexp(self):
		years = ''
		if self.experience:
			months = self.experience
			years = months/12
		return str(years)
	@property
	def monthsexp(self):
		mod = ''
		if self.experience:
			months = self.experience
			mod = months % 12
		return str(mod)

	class Meta:
		ordering = ('applicant',)

def generate_doc_name(instance,filename):
	ext = filename.split('.')[-1]
	rightnow = timezone.now()
	type = instance.type
	if type == '1':
		type = 'resume'
	if type == '2':
		type = 'cover_letter'
	if type == '3':
		type = 'certification'
	if type == '4':
		type = 'recommendation'
	if type == '5':
		type = 'other_doc'
	date = "%s-%s-%s_%s%s" %(str(rightnow.year),str(rightnow.month),str(rightnow.day),str(rightnow.hour),str("{0:0>2}".format(rightnow.minute)))
	#skill = instance.profile.skill.name.lower().replace(" ", "_").replace("'", "").replace(".", "")
	f_name = instance.profile.applicant.firstname.strip()
	f_name =  f_name.lower().replace(" ", "_").replace("'", "").replace(".", "")
	l_name = instance.profile.applicant.lastname.strip()
	l_name =  l_name.lower().replace(" ", "_").replace("'", "").replace(".", "")
	#return "docs/%s-%s_%s-%s-%s.%s" %(type,f_name,l_name,skill,date,ext.lower())
	return "docs/%s_%s-%s-%s.%s" %(f_name,l_name,type,date,ext.lower())

class Profile_Doc(models.Model):
	#DOC_TYPE = (('1', "Resume"),('2', "Cover letter"),('3', "RTR (Right to Represent)"),('4', "Visa copy (H1B, OPT)"),('5', "Photo ID (DL, EAD card)"),('6', "NDA (Non-discloser Agreement)"),)
	DOC_TYPE = (('', "-Select Type-"),('1', "Resume"),('2', "Cover letter"),('3', "Certification"),('4', "Letter of recommendation"),('5', "Other"),)
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
class Vendor (models.Model):
	name			= models.CharField(max_length=100)
	contactname      = models.CharField(max_length=100, null=True, blank=True)
	email 			= models.EmailField(max_length=90, null=True, blank=True)
	phone			= models.CharField(max_length=35, null=True ,blank=True)
	address			= models.CharField(max_length=200, null=True ,blank=True)
	moreinfo		= models.CharField(max_length=400, null=True ,blank=True)
	updated			= models.DateTimeField(default=timezone.now, null=True ,blank=True)
	created			= models.DateTimeField(default=timezone.now, null=True ,blank=True)
	active			= models.BooleanField(default=True ,blank=True)
	class Meta:
		ordering = ('name',)
	def __unicode__(self):
		return self.name
	def save(self, *args, **kwargs):
		self.updated = timezone.localtime(timezone.now())
		super(Vendor, self).save(*args, **kwargs)

class Opening (models.Model):
	WORK_AUTHORIZATION = (('', "-Select Type-"),('1', "USC"),('2', "GC"),('3', "H1"),('4', "EAD"),('5', "TN"),)
	CONTRACT_TYPE = (('', "-Select Type-"),('1', "FT"),('2', "C2C"),('3', "Contract"),)
	EDUCATION_TYPE = (('', "-Education level-"),('1', "High School"),('2', "Bachelor's"),('3', "Master's"),('4', "PhD"),)
	LEVEL = (('', "-Select Level-"),('1', "Entry"),('2', "Intermediate "),('3', "Senior "),)
	startdate		= models.DateField(blank=True, null=True, default=timezone.now)
	posted			= models.DateField(blank=True, default=timezone.now)
	role			= models.CharField(max_length=75)
	skills 			= models.ManyToManyField(Skill, related_name='open_skills_main', blank=True)
	skills_sec		= models.ManyToManyField(Skill, related_name='open_skills_sec', blank=True)
	responsibilities = models.TextField(max_length=4000, null=True ,blank=True)
	rate			= models.CharField(max_length=35, null=True ,blank=True)
	city			= models.CharField(max_length=65, null=True ,blank=True)
	state			= models.ForeignKey(State, null=True ,blank=True)
	duration		= models.IntegerField(null=True ,blank=True)
	experience		= models.IntegerField(null=True ,blank=True) # Total years of experience needed
	education		= models.CharField(max_length=1, choices=EDUCATION_TYPE, null=True ,blank=True)
	level			= models.CharField(max_length=1, choices=LEVEL, null=True ,blank=True)
	contract		= models.CharField(max_length=1, choices=CONTRACT_TYPE,null=True ,blank=True)
	work_auth		= models.CharField(max_length=1, choices=WORK_AUTHORIZATION, null=True ,blank=True)
	applications	= models.ManyToManyField(Profile, related_name='applications', through='Application', blank=True)
	vendor			= models.ForeignKey(Vendor, null=True ,blank=True)
	updated			= models.DateTimeField(default=timezone.now)
	created			= models.DateTimeField(default=timezone.now)
	open			= models.BooleanField(default=True ,blank=True)
	endclientinfo	= models.CharField(max_length=300, null=True ,blank=True)
	partnerinfo		= models.CharField(max_length=300, null=True ,blank=True)
	active			= models.BooleanField(default=True ,blank=True)

	def __unicode__(self):
		ret = self.role
		skills = ""
		for skill in self.skills.all():
			skills = skills+" ["+skill.name+"]"
		ret = "%s%s"%(ret, skills)
		if self.state:
			ret = "%s %s"%(ret, self.state.code)
		return ret
	@property
	def yearsdur(self):
		years = ''
		if self.duration:
			months = self.duration
			years = months/12
		return str(years)
	@property
	def monthsdur(self):
		mod = ''
		if self.duration:
			months = self.duration
			mod = months % 12
		return str(mod)
	@property
	def yearsexp(self):
		years = ''
		if self.experience:
			months = self.experience
			years = months/12
		return str(years)
	@property
	def monthsexp(self):
		mod = ''
		if self.experience:
			months = self.experience
			mod = months % 12
		return str(mod)

	def save(self, *args, **kwargs):
		if self.role:
			self.role = self.role.strip()
		super(Opening, self).save(*args, **kwargs)

	class Meta:
		ordering = ('role',)
#000
class Application(models.Model):
	profile			= models.ForeignKey(Profile)
	opening			= models.ForeignKey(Opening)
	recruiter		= models.ForeignKey(User, blank=True)
	datetime		= models.DateTimeField(default=timezone.now)
	activities 		= models.ManyToManyField(User, related_name='activities', through='Activity', blank=True)
	rate			= models.CharField(max_length=35, null=True ,blank=True)
	datetime		= models.DateTimeField(default=timezone.now)
	updated			= models.DateTimeField(default=timezone.now)
	created			= models.DateTimeField(default=timezone.now)
	submitted		= models.DateTimeField(default=timezone.now)
	active			= models.BooleanField(default=True ,blank=True)
	def __unicode__(self):
		return "%s | %s"%(self.profile.applicant, self.opening)
	class Meta:
		ordering = ('profile','opening',)
		unique_together = ('profile', 'opening',)

class Activity(models.Model):
	INTERACTION_TYPE = (('1', "Phone call"),('2', "In Person"),('3', "No Interaction"),)
	application		= models.ForeignKey(Application)
	recruiter		= models.ForeignKey(User)
	datetime		= models.DateTimeField(default=timezone.now)
	type			= models.CharField(max_length=1, choices=INTERACTION_TYPE, default='1')
	notes 			= models.TextField(max_length=4000, null=True ,blank=True)
	def __unicode__(self):
		return "%s | %s"%(self.application,self.datetime.strftime("%b %d, %Y %I:%M %p"))
	class Meta:
		ordering = ('-datetime',)

class Reminder(models.Model):
	model_name		= models.CharField(max_length=30, null=True ,blank=True)
	field_id		= models.IntegerField(null=True ,blank=True)
	content			= models.TextField(max_length=4000, null=True ,blank=True)
	recruiter		= models.ForeignKey(User, blank=True)
	datetime		= models.DateTimeField(default=timezone.now)
	private			= models.BooleanField(default=True ,blank=True)
	active			= models.BooleanField(default=True ,blank=True)
	def __unicode__(self):
		return "%s - %s"%(self.recruiter, self.datetime.strftime("%b %d, %Y - %I:%M %p"))
	class Meta:
		ordering = ('-datetime',)
		
class Tracking(models.Model):
	TRACKING_TYPE = (('1', "Changed"),('2', "New"),('3', "Deleted"),)
	recruiter		= models.ForeignKey(User)
	datetime		= models.DateTimeField(default=timezone.now)
	type			= models.CharField(max_length=1, choices=TRACKING_TYPE, default='1')
	entity			= models.CharField(max_length=45, null=True ,blank=True)
	entity_id		= models.IntegerField(null=True ,blank=True)
	entity_field	= models.CharField(max_length=45, null=True ,blank=True)
	#url				= models.CharField(max_length=99, null=True ,blank=True)
	old				= models.TextField(max_length=4000, null=True ,blank=True)
	new				= models.TextField(max_length=4000, null=True ,blank=True)
	extrainfo		= models.TextField(max_length=4000, null=True ,blank=True)
	show			= models.BooleanField(default=True ,blank=True)
	def __unicode__(self):
		return "%s | %s"%(self.datetime.strftime("%b %d, %I:%M %p"), self.recruiter)
	class Meta:
		ordering = ('-datetime',)