class AddControlToHeader:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		response['Access-Control-Allow-Origin'] = "prosoft-tms-stage.s3.amazonaws.com"
		return response