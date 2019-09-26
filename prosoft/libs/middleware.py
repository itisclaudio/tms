from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile
from django.utils.http import urlquote

EXEMPT_URLS = [compile(settings.LOGIN_URL.strip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).
    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required middleware\
 requires authentication middleware to be installed. Edit your\
 MIDDLEWARE_CLASSES setting to insert\
 'django.contrib.auth.middleware.AuthenticationMiddleware'. If that doesn't\
 work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
 'django.core.context_processors.auth'."
        if not request.user.is_authenticated():
            path = request.path_info.strip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                #return HttpResponseRedirect(settings.LOGIN_URL)
				fullURL = "%s?next=%s" % (settings.LOGIN_URL,urlquote(request.get_full_path()))
				return HttpResponseRedirect(fullURL)

class AddControlToHeader:
    """
    Middleware to add 'Access-Control-Allow-Origin' to the header
	of every request to allow 'prosoft-tms-stage.s3.amazonaws.com'
	to serve external fonts for bootstrap 	https://stackoverflow.com/questions/36099244/how-to-add-an-http-header-to-all-django-responses/36099405	https://stackoverflow.com/questions/22355540/access-control-allow-origin-in-django-app-when-accessed-with-phonegap
    """
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		response['Access-Control-Allow-Origin'] = "prosoft-tms-stage.s3.amazonaws.com"
		return response