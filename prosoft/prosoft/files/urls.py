from django.conf.urls import patterns,url
from . import views #Class Based Views URLs

urlpatterns = patterns('prosoft.files.views',
	url(r'^$','main_view',name='view_main'),
	url(r'^reports/$', 'reports_view', name='view_reports'),
	url(r'^searchquick/$','searchquick_view',name='view_searchquick'),

	### S Y S T E M ###
	#url(r'^managernew/$','managernew_view',name='view_managernew'),
	
	### A C C O U N T ###
	url(r'^login/$','login_view',name='view_login'),
	url(r'^logout/$', 'logout_view', name='view_logout'),
	url(r'^account_password/$', 'account_password_view', name='view_account_password'),
	#url(r'^history/$', 'history_view', name='view_history'),
	
	### T R A C K I N G ###
	url(r'^trackings/(?P<page>.*)/$', 'trackings_view', name='view_trackings'),
	url(r'^trackings/$', 'trackings_view', name='view_trackings'),
	url(r'^tracking/(?P<id>\d+)/$','tracking_view',name='view_tracking'),
	url(r'^trackingdelete/(?P<pk>\d+)/$',views.TrackingDelete.as_view() ,name='trackingdelete'),
	
	### A C T I V I T I E S ###
	url(r'^activities/$','activities_view',name='view_activities'),
	url(r'^activities_rpt/$','activities_rpt_view',name='view_activities_rpt'),
	url(r'^activity/(?P<id>\d+)/$','activity_view',name='view_activity'),
	url(r'^activity_rpt/(?P<id>\d+)/$','activity_rpt_view',name='view_activity_rpt'),
	url(r'^activityedit/(?P<id>\d+)/$','activityedit_view',name='view_activityedit'),
	url(r'^activitynew/(?P<application_id>\d+)/$','activitynew_view',name='view_activitynew'),
	url(r'^activitynew_application/(?P<application_id>\d+)/$','activitynew_application_view',name='view_activitynew_application'),
	url(r'^activitynew/$','activitynew_view',name='view_activitynew'),
	url(r'^activitydelete/(?P<id>\d+)/$','activity_delete_view',name='view_activity_delete'),
	url(r'^qsearch_activity/$','qsearch_activity_view',name='view_qsearch_activity'),
	
	### A P L I C A N T S ###
	url(r'^applicantnew/$','applicantnew_view',name='view_applicantnew'),
	url(r'^applicantdocnew/(?P<applicant>\d+)/$','applicantdocnew_view',name='view_applicantdocnew'),
	url(r'^applicant/(?P<id>\d+)/$','applicant_view',name='view_applicant'),
	url(r'^applicant_rpt/(?P<id>\d+)/$','applicant_rpt_view',name='view_applicant_rpt'),
	url(r'^applicants/$','applicants_view',name='view_applicants'),
	url(r'^qsearch_applicant/$','qsearch_applicant_view',name='view_qsearch_applicant'),
	url(r'^applicants_rpt/$','applicants_rpt_view',name='view_applicants_rpt'),
	url(r'^applicantedit/(?P<id>\d+)/$','applicantedit_view',name='view_applicantedit'),
	url(r'^applicantdelete/(?P<id>\d+)/$','applicantdelete_view',name='view_applicantdelete'),
	url(r'^applicantdocdelete/(?P<id>\d+)/$','applicant_doc_delete_view',name='view_applicant_doc_delete'),

	### A P P L I C A T I O N S ###
	url(r'^application/(?P<id>\d+)/$','application_view',name='view_application'),
	url(r'^application_rpt/(?P<id>\d+)/$','application_rpt_view',name='view_application_rpt'),
	url(r'^applications/$','applications_view',name='view_applications'),
	url(r'^applications/(?P<active>\d+)/(?P<mine>\d+)$','applications_view',name='view_applications'),
	url(r'^applications_rpt/$','applications_rpt_view',name='view_applications_rpt'),
	url(r'^applicationnew/(?P<profile_id>\d+)/(?P<opening_id>\d+)/$','applicationnew_view',name='view_applicationnew'),
	url(r'^applicationnew/$','applicationnew_view',name='view_applicationnew'),
	url(r'^applicationnew_pro/(?P<profile_id>\d+)/$','applicationnew_view',name='view_applicationnew'),#Still using?
	url(r'^applicationnew_profile/(?P<profile_id>\d+)/$','applicationnew_profile_view',name='view_applicationnew_profile'),
	url(r'^applicationnew_opening/(?P<opening_id>\d+)/$','applicationnew_opening_view',name='view_applicationnew_opening'),
	url(r'^applicationnew_ope/(?P<opening_id>\d+)/$','applicationnew_view',name='view_applicationnew'),
	#url(r'^applicationnew_both/(?P<profile_id>\d+)/(?P<opening_id>\d+)/$','applicationnew_view',name='view_applicationnew'),
	url(r'^applicationnew_both/(?P<profile_id>\d+)/(?P<opening_id>\d+)/$','applicationnew_both_view',name='view_applicationnew_both'),
	url(r'^qsearch_application/$','qsearch_application_view',name='view_qsearch_application'),
	#url(r'^applicationedit/(?P<id>\d+)/$','applicationedit_view',name='view_applicationedit'),
	url(r'^applicationdelete/(?P<id>\d+)/$','application_delete_view',name='view_application_delete'),

	### O P E N I N G S ###
	url(r'^openings/$','openings_view',name='view_openings'),
	url(r'^openings_rpt/$','openings_rpt_view',name='view_openings_rpt'),
	url(r'^opening/(?P<id>\d+)/$','opening_view',name='view_opening'),
	url(r'^opening_rpt/(?P<id>\d+)/$','opening_rpt_view',name='view_opening_rpt'),
	url(r'^openingnew/$','openingnew_view',name='view_openingnew'),
	url(r'^openingedit/(?P<id>\d+)/$','openingedit_view',name='view_openingedit'),
	url(r'openingdelete/(?P<id>\d+)/$','openingdelete_view',name='view_openingdelete'),
	url(r'^qsearch_opening/$','qsearch_opening_view',name='view_qsearch_opening'),
	
	### P R O F I L E S ###
	url(r'^profiledocnew/(?P<profile>\d+)/$','profiledocnew_view',name='view_profiledocnew'),
	url(r'^profilenew_appicant/(?P<applicant_id>\d+)/$','profilenew_appicant_view',name='view_profilenew_appicant'),
	url(r'^profile/(?P<id>\d+)/$','profile_view',name='view_profile'),
	url(r'^profile_rpt/(?P<id>\d+)/$','profile_rpt_view',name='view_profile_rpt'),
	url(r'^profiles/$','profiles_view',name='view_profiles'),
	url(r'^profiles_rpt/$','profiles_rpt_view',name='view_profiles_rpt'),
	url(r'^profileedit/(?P<id>\d+)/$','profileedit_view',name='view_profileedit'),
	url(r'^profiledelete/(?P<id>\d+)/$','profiledelete_view',name='view_profiledelete'),
	url(r'^profilenew/$','profilenew_view',name='view_profilenew'),
	url(r'^profilenew/(?P<applicant>\d+)/$','profilenew_view',name='view_profilenew'),
	#url(r'^profileskillsedit/(?P<profile>\d+)/$','profileskillsedit_view',name='view_profileskillsedit'),
	url(r'^profiledocdelete/(?P<id>\d+)/$','profile_doc_delete_view',name='view_profile_doc_delete'),
	url(r'^qsearch_profile/$','qsearch_profile_view',name='view_qsearch_profile'),

	### R E C R U I T E R S ###
	url(r'^recruiters/$','recruiters_view',name='view_recruiters'),
	url(r'^recruiternew/$','recruiternew_view',name='view_recruiternew'),
	url(r'^recruiter_profile/(?P<id>\d+)/$','recruiter_profile_view',name='view_recruiter_profile'),
	url(r'^recruiters_rpt/$','recruiters_rpt_view',name='view_recruiters_rpt'),
	url(r'^qsearch_recruiter/$','qsearch_recruiter_view',name='view_qsearch_recruiter'),
	url(r'^myprofile/$','myprofile_view',name='view_myprofile'),

	### R E M I N D E R S ###
	url(r'^remindernew/(?P<model_name>.*)/(?P<field_id>\d+)/$','remindernew_view',name='view_remindernew'),
	url(r'^remindernew/$','remindernew_view',name='view_remindernew'),
	url(r'^reminderedit/(?P<id>\d+)/$','reminderedit_view',name='view_reminderedit'),
	#url(r'^reminderdelete/(?P<pk>\d+)/$',views.ReminderDelete.as_view() ,name='reminderdelete'),
	url(r'^reminderdelete/(?P<id>\d+)/$','reminderdelete_view',name='view_reminderdelete'),
	url(r'^reminders/$','reminders_view',name='view_reminders'),
	url(r'^reminders/(?P<active>\d+)/$','reminders_view',name='view_reminders'),
	url(r'^reminders/(?P<private>\d+)/$','reminders_view',name='view_reminders'),
	url(r'^reminders/(?P<active>\d+)/(?P<private>\d+)/(?P<mine>\d+)$','reminders_view',name='view_reminders'),
	#url(r'^reminders_private/$','reminders_private_view',name='view_reminders_private'),
	#url(r'^reminders_private/(?P<active>\d+)/$','reminders_private_view',name='view_reminders_private'),
	url(r'^reminders_rpt/(?P<active>\d+)/(?P<private>\d+)/(?P<mine>\d+)$','reminders_rpt_view',name='view_reminders_rpt'),
	url(r'^reminders_rpt/(?P<active>\d+)/$','reminders_rpt_view',name='view_reminders_rpt'),
	url(r'^reminders_rpt/$','reminders_rpt_view',name='view_reminders_rpt'),
	url(r'^reminder/(?P<id>\d+)/$','reminder_view',name='view_reminder'),
	url(r'^reminder_rpt/(?P<id>\d+)/$','reminder_rpt_view',name='view_reminder_rpt'),
	url(r'^qsearch_reminder/$','qsearch_reminder_view',name='view_qsearch_reminder'),

	### S K I L L S ###
	url(r'^skills/(?P<page>.*)/$','skills_view',name='view_skills'),
	url(r'^skills/$','skills_view',name='view_skills'),
	url(r'^skills_rpt/$','skills_rpt_view',name='view_skills_rpt'),
	url(r'^skill/(?P<id>\d+)/$','skill_view',name='view_skill'),
	url(r'^skillnew/$','skillnew_view',name='view_skillnew'),
	url(r'^skilledit/(?P<id>\d+)/$','skilledit_view',name='view_skilledit'),
	url(r'^skilldelete/(?P<id>\d+)/$','skilldelete_view',name='view_skilldelete'),
	url(r'^qsearch_skill/$','qsearch_skill_view',name='view_qsearch_skill'),
	
	### V E N D O R ###
	url(r'^vendornew/$','vendornew_view',name='view_vendornew'),
	url(r'^vendoredit/(?P<id>\d+)/$','vendoredit_view',name='view_vendoredit'),
	url(r'^vendordelete/(?P<id>\d+)/$','vendordelete_view',name='view_vendordelete'),
	url(r'^vendor/(?P<id>\d+)/$','vendor_view',name='view_vendor'),
	url(r'^vendors/$','vendors_view',name='view_vendors'),
	url(r'^vendors_rpt/$','vendors_rpt_view',name='view_vendors_rpt'),
	url(r'^qsearch_vendor/$','qsearch_vendor_view',name='view_qsearch_vendor'),
)