from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.auth import views as auth_views #For Passworkd reset
from django.contrib import admin
#for error handling:
from django.conf.urls import handler500, handler404#, handler403#, handler400
from prosoft.files.views import myerror500, myerror404#, myerror403#, myerror400

urlpatterns = [
	# Examples:
	# url(r'^$', 'prosoft.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),

	url(r'^admin/', include(admin.site.urls)),
	url(r'^',include('prosoft.files.urls')),
	url(r'^media/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),
	
	#For Passworkd reset
    url(r'^user/password/reset/$','django.contrib.auth.views.password_reset',{'post_reset_redirect' : '/user/password/reset/done/'},name="password_reset"),
	url(r'^user/password/reset/done/$','django.contrib.auth.views.password_reset_done'),
	url(r'^user/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm',{'post_reset_redirect' : '/user/password/done/'}),
	url(r'^user/password/done/$','django.contrib.auth.views.password_reset_complete'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$','django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
	url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
]

#For debug_toolbar (Only production):
#if settings.DEBUG:
if 1==2:
	print "settings.DEBUG = True, Load debug_toolbar"
	import debug_toolbar
	urlpatterns = [
		url(r'^__debug__/', include(debug_toolbar.urls)),
	] + urlpatterns
	
#To handle Errors
handler500 = myerror500
handler404 = myerror404
#handler404 ='prosoft.files.views.myerror404'
#handler500 = 'prosoft.files.views.myerror500'