from django import forms
from django.forms import extras
from datetime import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm
from prosoft.files.models import (
	Applicant,
	Application,
	Country,
	Member,
	Opening,
	Profile,
	Skill,
	State,
	Vendor,
	)

MONTHS  = (
('', "-Months-"),('0', "0"),('1', "1"),('2', "2"),('3', "3"),('4', "4"),('5', "5"),('6', "6"),('7', "7"),('8', "8"),('9', "9"),('10', "10"),('11', "11"),)
EXP_YEARS  = (
('', "-Years-"),(0, "0"),(1, "1"),(2, "2"),(3, "3"),(4, "4"),(5, "5"),(6, "6"),(7, "7"),(8, "8"),(9, "9"),(10, "10"),(11, "11"),
(12, "12"),(13, "13"),(14, "14"),(15, "15"),(16, "16"),(17, "17"),(18, "18"),(19, "19"),(20, "20"),(21, "20+"),
)
	
class BaseForm(forms.Form):
	def __init__(self, *args, **kwargs):
		super(BaseForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'

class BaseModelForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(BaseModelForm, self).__init__(*args, **kwargs)
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control'
			
class search_Form(forms.Form):
	search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)

##### A C C O U N T ######
class login_Form(BaseForm):
	username = forms.CharField(max_length=75, required=True, widget=forms.TextInput())
	password = forms.CharField(required=True, widget=forms.PasswordInput(render_value=False))

class UpdatePasswordForm(forms.ModelForm):
	current = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Current password'},render_value=False))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'New password'}) ,required=True,  label="New password", help_text='Max 30')
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Repeat your new password'}) ,required=True, label="Repeat your new password")

	def clean_current(self):
		valid = self.actual_user.check_password(self.cleaned_data['current'])
		if not valid:
			raise forms.ValidationError("Password Incorrect")
		return valid

	def clean_password1(self):
		if self.data['password'] != self.data['password2']:
			raise forms.ValidationError('Passwords are not the same')
		return self.data['password']

	class Meta:
		model = User
		fields = ["password"]
		

#############################
#### M A N A G E R      #####
#############################
#000
class recruiter_Form(BaseForm):
	#INTERACTION_TYPE = (('', "-Select Type-"),('1', "Phone call"),('2', "In Person"),('3', "No Interaction"),)
	username	= forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'Username'}),required=True)
	first_name	= forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'First name'}),required=False)
	last_name 	= forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'Last name'}),required=False)
	email		= forms.CharField(max_length=254, min_length=5 ,widget=forms.TextInput(attrs={'placeholder': 'Email'}), required=True)
	temp_pass	= forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'Temporary password'}),required=True)
	
	def clean_username(self):
		if User.objects.filter(username=self.data['username']).exists():
		#if self.data['password'] != self.data['password2']:
			raise forms.ValidationError('Username already exists')
		return self.data['username']

	def clean_email(self):
		if User.objects.filter(username=self.data['email']).exists():
			raise forms.ValidationError('Email already exists')
		return self.data['email']
		
#############################
#### A C T I V I T I Y #####
#############################

class activity_Form(BaseForm):
	INTERACTION_TYPE = (('', "-Select Type-"),('1', "Phone call"),('2', "In Person"),('3', "No Interaction"),)
	application 	= forms.ModelChoiceField(queryset=Application.objects.all().select_related('profile','profile__applicant__state','opening','opening__state').prefetch_related('opening__skills','profile__skills').order_by('profile__applicant__firstname'), required=True)
	recruiter		= forms.ModelChoiceField(queryset=User.objects.all(), required=False)
	datetime 		= forms.DateTimeField(widget=extras.SelectDateWidget(attrs=({'style': 'width: 30%; display: inline-block;'})), initial=datetime.now(), required=False)
	type			= forms.ChoiceField(choices=INTERACTION_TYPE, required=False)
	notes			= forms.CharField(max_length=4000,widget=forms.Textarea(attrs={'cols': 10, 'rows': 10}), required=False)
	
class activity_app_Form(BaseForm):
	INTERACTION_TYPE = (('', "-Select Type-"),('1', "Phone call"),('2', "In Person"),('3', "No Interaction"),)
	recruiter		= forms.ModelChoiceField(queryset=User.objects.all(), required=False)
	datetime 		= forms.DateTimeField(widget=extras.SelectDateWidget(attrs=({'style': 'width: 30%; display: inline-block;'})), initial=datetime.now(), required=False)
	type			= forms.ChoiceField(choices=INTERACTION_TYPE, required=False)
	notes			= forms.CharField(max_length=4000,widget=forms.Textarea(attrs={'cols': 10, 'rows': 10}), required=False)

class activity_edit_Form(BaseForm):
	INTERACTION_TYPE = (('', "-Select Type-"),('1', "Phone call"),('2', "In Person"),('3', "No Interaction"),)
	type			= forms.ChoiceField(choices=INTERACTION_TYPE, required=False)
	notes			= forms.CharField(max_length=4000,widget=forms.Textarea(attrs={'cols': 10, 'rows': 10}), required=False)

##############################
###### A P P L I C A N T #####
##############################
class applicant_Form(BaseForm):
	WORK_STATUS = (('', "-Select Work Status-"),('1', "USC"),('2', "GC"),('3', "H1"),('4', "EAD"),('5', "TN"),('4', "Not Authorized"))
	firstname 	= forms.CharField(max_length=75,widget=forms.TextInput(attrs={'placeholder': 'First name'}),required=True)
	lastname 	= forms.CharField(max_length=75,widget=forms.TextInput(attrs={'placeholder': 'Last name'}),required=True)
	dob 		= forms.DateField(widget=extras.SelectDateWidget(years=range(1940, 2001),attrs=({'style': 'width: 30%; display: inline-block;'})), required=False)
	email 		= forms.EmailField(max_length=90, min_length=5, required=False)
	phone_1 	= forms.CharField(max_length=35,widget=forms.TextInput(attrs={'placeholder': 'Main number'}), required=False)
	phone_2 	= forms.CharField(max_length=35,widget=forms.TextInput(attrs={'placeholder': 'Secondary number'}), required=False)
	work_status = forms.ChoiceField(widget = forms.Select(),choices=WORK_STATUS, required=False)
	relocation = forms.BooleanField(widget=forms.CheckboxInput(attrs={'style':'height:20px;width:20px;'}), initial=False, required=False)
	#availability = forms.DateField(widget=SelectDateWidget(years=[y for y in range(1930,2050)]))
	#availability = forms.DateField(widget=extras.SelectDateWidget(years=range(2017, 2030),attrs=({'style': 'width: 30%; display: inline-block;'})), initial=datetime.now(), required=False)
	available = forms.BooleanField(widget=forms.CheckboxInput(attrs={'style':'height:20px;width:20px;'}), initial=True, required=False)
	righttorep = forms.BooleanField(widget=forms.CheckboxInput(attrs={'style':'height:20px;width:20px;'}), initial=False, required=False)
	country   =  forms.ModelChoiceField(queryset=Country.objects.all(), required=False)
	address 	= forms.CharField(max_length=200, required=False)
	city 		= forms.CharField(max_length=65,widget=forms.TextInput(attrs={'placeholder': 'Enter city'}), required=False)
	state 		= forms.ModelChoiceField(queryset=State.objects.all(), required=False)
	zipcode		= forms.CharField(max_length=10, widget=forms.TextInput(attrs={'placeholder': 'Zip code'}), required=False)
	t_exp_months = forms.ChoiceField(choices=MONTHS, required=False)
	t_exp_years = forms.ChoiceField(choices=EXP_YEARS, required=False)
	us_exp_months = forms.ChoiceField(choices=MONTHS, required=False)
	us_exp_years = forms.ChoiceField(choices=EXP_YEARS, required=False)
	education	= forms.CharField(max_length=200,widget=forms.TextInput(attrs={'placeholder': 'Degree / School'}), required=False)
	besttime	= forms.CharField(max_length=200,widget=forms.TextInput(attrs={'placeholder': 'To be contacted'}), required=False)
	salary_cur	= forms.CharField(max_length=40,widget=forms.TextInput(attrs={'placeholder': 'Current Salary'}), required=False)

class applicantdocnew_Form(BaseForm):
	DOC_TYPE = (('', "-Select Type-"),('1', "RTR (Right to Represent)"),('2', "Visa"),('3', "Photo ID"),('4', "NDA (Non-discloser Agreement)"),('5', "Other"),)
	document  	= forms.FileField(required=True, widget=forms.FileInput(attrs={'class': 'form-control upload'}))
	type		= forms.ChoiceField(choices=DOC_TYPE, required=True)
	
#######################################	
###### A P P L I C A T I O N ##########
#######################################

class applicationnew_profile_Form(BaseForm):
	opening		= forms.ModelChoiceField(queryset=Opening.objects.all(), required=True)
	rate 		= forms.CharField(max_length=35,widget=forms.TextInput(attrs={'placeholder': '$$$'}), required=False)
	submitted	= forms.DateField(widget=extras.SelectDateWidget(years=range(2017, 2030),attrs=({'style': 'width: 26%; display: inline-block;'})), initial=datetime.now(), required=False)

class applicationnew_opening_Form(BaseForm):
	profile		= forms.ModelChoiceField(queryset=Profile.objects.all(), required=True)
	rate 		= forms.CharField(max_length=35,widget=forms.TextInput(attrs={'placeholder': '$$$'}), required=False)
	submitted	= forms.DateField(widget=extras.SelectDateWidget(years=range(2017, 2030),attrs=({'style': 'width: 26%; display: inline-block;'})), initial=datetime.now(), required=False)
#000
class applicationnewboth_Form(BaseForm):
	rate 		= forms.CharField(max_length=35,widget=forms.TextInput(attrs={'placeholder': '$$$'}), required=False)
	submitted	= forms.DateField(widget=extras.SelectDateWidget(years=range(2017, 2030),attrs=({'style': 'width: 26%; display: inline-block;'})), initial=datetime.now(), required=False)

class applicationnew_Form(BaseForm):
	profile		= forms.ModelChoiceField(queryset=Profile.objects.all(), required=True)
	opening		= forms.ModelChoiceField(queryset=Opening.objects.all(), required=True)
	rate 		= forms.CharField(max_length=35,widget=forms.TextInput(attrs={'placeholder': '$$$'}), required=False)
	submitted	= forms.DateField(widget=extras.SelectDateWidget(years=range(2017, 2030),attrs=({'style': 'width: 26%; display: inline-block;'})), initial=datetime.now(), required=False)
	
	def clean_profile(self):
		if self.data['profile']:
			return self.data['profile']
		else:
			raise forms.ValidationError('Profile must not be empty')
	
	def clean_opening(self):
		if self.data['opening']:
			return self.data['opening']
		else:
			raise forms.ValidationError('Opening must not be empty')	
	
	def clean(self,*args, **kwargs):
		self.clean_profile()
		self.clean_opening()
		#cleaned_data = self.cleaned_data
		#if self.clean_profile() and self.clean_opening():
		profile = self.cleaned_data['profile']
		opening = self.cleaned_data['opening']
		if profile and opening:
			try:
				Application.objects.get(profile=profile, opening=opening)
			except Application.DoesNotExist:
				pass
			else:
				raise forms.ValidationError('The Application for the Opening and Profile you selected already exists')
				#raise forms.ValidationError("Application %s / %s already exists"%(cleaned_data['opening'],cleaned_data['profile']))

			# Always return cleaned_data
		return super(applicationnew_Form, self).clean(*args, **kwargs)
		#recruiter	= forms.ModelChoiceField(queryset=User.objects.all(), required=True)
	
class applicationedit_Form(BaseForm):
	#check = forms.BooleanField(label="Active?", initial=True)
	STATUS  	= ((None, "-Select Status-"),(True, "Active"),(False, "Inactive"))
	active		= forms.ChoiceField(widget = forms.Select(),choices=STATUS, required=False)
	rate 		= forms.CharField(max_length=35,widget=forms.TextInput(attrs={'placeholder': '$$$'}), required=False)
	submitted	= forms.DateField(widget=extras.SelectDateWidget(years=range(2017, 2030),attrs=({'style': 'width: 26%; display: inline-block;'})), initial=datetime.now(), required=False)
	
###########################	
#####  O P E N I N G  #####
###########################
class opening_Form(BaseForm):
	DUR_YEARS  = (('', "-Years-"),(0, "0"),(1, "1"),(2, "2"),(3, "3"),(4, "4"),(5, "5"),(6, "Full Time"),)
	WORK_AUTHORIZATION = (('', "-Work Authorization Type-"),('1', "USC"),('2', "GC"),('3', "H1"),('4', "EAD"),('5', "TN"),)
	CONTRACT_TYPE = (('', "-Contract Type-"),('1', "FT"),('2', "C2C"),('3', "Contract"),)
	EDUCATION_TYPE = (('', "-Education level-"),('1', "High School"),('2', "Bachelor's"),('3', "Master's"),('4', "PhD"),)
	LEVEL = (('', "-Select Level-"),('1', "Entry"),('2', "Intermediate "),('3', "Senior "),)
	role 		= forms.CharField(max_length=75,widget=forms.TextInput(attrs={'placeholder': 'Role name'}),required=True)
	skills 		= forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)
	posted 		= forms.DateField(widget=extras.SelectDateWidget(years=range(2016, 2030),attrs=({'style': 'width: 26%; display: inline-block;'})), initial=datetime.now(), required=False)
	startdate = forms.DateField(widget=extras.SelectDateWidget(years=range(2017, 2030),attrs=({'style': 'width: 26%; display: inline-block;'})), required=False)
	responsibilities = forms.CharField(max_length=4000,widget=forms.Textarea(attrs={'cols': 10, 'rows': 10}), required=False)
	rate 		= forms.CharField(max_length=35,widget=forms.TextInput(attrs={'placeholder': '$$$'}), required=False)
	education	= forms.ChoiceField(widget = forms.Select(),choices=EDUCATION_TYPE, required=False)
	city 		= forms.CharField(max_length=65,widget=forms.TextInput(attrs={'placeholder': 'Enter city'}), required=False)
	state 		= forms.ModelChoiceField(queryset=State.objects.all(), required=False)
	education	 = forms.ChoiceField(widget = forms.Select(),choices=EDUCATION_TYPE, required=False)
	level		 = forms.ChoiceField(widget = forms.Select(),choices=LEVEL, required=False)
	duration_months = forms.ChoiceField(choices=MONTHS, required=False)
	duration_years = forms.ChoiceField(choices=DUR_YEARS, required=False)
	exp_months = forms.ChoiceField(choices=MONTHS, required=False)
	exp_years = forms.ChoiceField(choices=EXP_YEARS, required=False)
	vendor 		= forms.ModelChoiceField(queryset=Vendor.objects.filter(active=True), required=False)
	endclientinfo = forms.CharField(max_length=300,widget=forms.Textarea(attrs={'cols': 10, 'rows': 3}), required=False)
	partnerinfo = forms.CharField(max_length=300,widget=forms.Textarea(attrs={'cols': 10, 'rows': 3}), required=False)
	contract = forms.ChoiceField(widget = forms.Select(),choices=CONTRACT_TYPE, required=False)
	work_auth = forms.ChoiceField(widget = forms.Select(),choices=WORK_AUTHORIZATION, required=False)
	open = forms.BooleanField(widget=forms.CheckboxInput(attrs={'style':'height:20px;width:20px;'}), initial=True, required=False)
	def __init__(self, *args, **kwargs):
		super(opening_Form, self).__init__(*args, **kwargs)
		self.fields['vendor'].empty_label = '--- None ---'
	
###########################
#####  P R O F I L E  #####
###########################

class profile_applicant_Form(BaseForm):
	skills 		= forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)
	exp_months 	= forms.ChoiceField(choices=MONTHS, required=False)
	exp_years 	= forms.ChoiceField(choices=EXP_YEARS, required=False)
	salary		= forms.CharField(max_length=40,widget=forms.TextInput(attrs={'placeholder': 'Salary Expectation'}), required=False)

class profile_Form(BaseForm):
	applicant	= forms.ModelChoiceField(queryset=Applicant.objects.all().order_by('firstname','lastname'), required=True)
	skills 		= forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)
	exp_months 	= forms.ChoiceField(choices=MONTHS, required=False)
	exp_years 	= forms.ChoiceField(choices=EXP_YEARS, required=False)
	salary		= forms.CharField(max_length=40,widget=forms.TextInput(attrs={'placeholder': 'Salary Expectation'}), required=False)

class profile_edit_Form(BaseForm):
	skills 		= forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=True, widget=forms.CheckboxSelectMultiple)
	exp_months 	= forms.ChoiceField(choices=MONTHS, required=False)
	exp_years 	= forms.ChoiceField(choices=EXP_YEARS, required=False)
	salary		= forms.CharField(max_length=40,widget=forms.TextInput(attrs={'placeholder': 'Salary Expectation'}), required=False)
	
class profiledocnew_Form(BaseForm):
	DOC_TYPE = (('', "-Select Type-"),('1', "Resume"),('2', "Cover letter"),('3', "Certification"),('4', "Letter of recommendation"),('5', "Other"),)
	document  	= forms.FileField(required=True, widget=forms.FileInput(attrs={'class': 'form-control upload'}))
	type		= forms.ChoiceField(choices=DOC_TYPE, required=True)
	
class profile_skills_Form(BaseForm):
	skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)

class UserField(forms.CharField):
    def clean(self, value):
        super(UserField, self).clean(value)
        try:
            User.objects.get(username=value)
            raise forms.ValidationError("Someone is already using this Username. Please pick another one.")
        except User.DoesNotExist:
            return value
			
class EmailField(forms.CharField):
	def clean(self, value):
		super(EmailField, self).clean(value)
		oldUser = User.objects.filter(email=value)
		if oldUser.exists():
			raise forms.ValidationError("Someone is already using this email!. Please pick another one.")
		else:
			return value

##############################
#####  R E C R U I T E R #####
##############################
#111
class recruiteredit2_Form(BaseForm):
	username	= forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'Username'}),required=True)
	first_name	= forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'First name'}),required=True)
	last_name 	= forms.CharField(max_length=30,widget=forms.TextInput(attrs={'placeholder': 'First name'}),required=True)
	email		= forms.CharField(max_length=254, min_length=5 ,widget=forms.TextInput(attrs={'placeholder': 'Email'}), required=True)
			
class recruiteredit_Form(forms.ModelForm):
	username	= forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Username'}),required=True)
	first_name	= forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'First name'}),required=False)
	last_name 	= forms.CharField(max_length=30,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'First name'}),required=False)
	email		= forms.CharField(max_length=254, min_length=5 ,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email'}), required=True)
	class Meta:
		model = User
		fields = ["username","first_name","last_name","email"]
		
	def clean_email(self):
		email = self.cleaned_data.get('email')
		if email and User.objects.filter(email=email).exclude(pk=self.actual_user.id).count():
			raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
		return email

	def clean_username(self):
		username = self.cleaned_data.get('username')
		if username and User.objects.filter(username=username).exclude(pk=self.actual_user.id).count():
			raise forms.ValidationError('This username is already in use. Please supply a different username')
		return username
		
	def save(self, commit=True):
		user = super(recruiteredit_Form, self).save(commit=False)
		user.email = self.cleaned_data['email']

		if commit:
			user.save()

		return user

############################
##### R E M I N D E R ######
############################

class reminder_Form(BaseForm):
	#model_name	= forms.CharField(max_length=30)
	private		= forms.BooleanField(widget=forms.CheckboxInput(attrs={'style':'height:20px;width:20px;margin-top:10px;'}), initial=False, required=False)
	active		= forms.BooleanField(widget=forms.CheckboxInput(attrs={'style':'height:20px;width:20px;margin-top:10px;'}), initial=False, required=False)
	content 	= forms.CharField(max_length=4000,widget=forms.Textarea(attrs={'cols': 10, 'rows': 10}), required=True)

######################
##### S K I L L ######
######################

class skill_Form(BaseForm):
	name 		= forms.CharField(max_length=75,widget=forms.TextInput(attrs={'placeholder': 'Name'}),required=True)
	description = forms.CharField(max_length=4000,widget=forms.Textarea(attrs={'cols': 10, 'rows': 10}), required=False)
	def clean_name(self):
		new_name = self.data['name']
		nameExists = Skill.objects.filter(name__iexact=new_name)
		if nameExists.exists():
			raise forms.ValidationError("The name "+new_name+" already exists!")
		else:
			return new_name

class skilledit_Form(forms.ModelForm):
	name 		= forms.CharField(max_length=75,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Name'}),required=True)
	description = forms.CharField(max_length=4000,widget=forms.Textarea(attrs={'class': 'form-control','cols': 10, 'rows': 10}), required=False)
	class Meta:
		model = Skill
		fields = ["name","description"]
		
	def clean_name(self):
		name = self.cleaned_data.get('name')
		if name and Skill.objects.filter(name=name).exclude(pk=self.actual_skill.id).count():
			raise forms.ValidationError('This name already exists!')
		return name

######################
##### V E N D O R ####
######################

class vendor_Form(BaseModelForm):
	#name		= forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Vendor name'}),required=True)
	#contactname	= forms.CharField(max_length=100,widget=forms.TextInput(attrs={'placeholder': 'Contact name'}),required=False)
	#email 		= forms.EmailField(max_length=90, min_length=5,widget=forms.TextInput(attrs={'placeholder': 'Email'}), required=False)
	#phone	 	= forms.CharField(max_length=35,widget=forms.TextInput(attrs={'placeholder': 'Phone number'}), required=False)
	address 	= forms.CharField(max_length=4000,widget=forms.Textarea(attrs={'class': 'form-control','cols': 10, 'rows': 3}), required=False)
	moreinfo 	= forms.CharField(max_length=4000,widget=forms.Textarea(attrs={'class': 'form-control','cols': 10, 'rows': 3}), required=False)
	class Meta:
		model = Vendor
		fields = ['name','contactname','email','phone','address','moreinfo',]
