
def parse_q_args(function):
	def wrap(request, *args, **kwargs):
		if request.GET.urlencode() != "":
			q_args = {q.split("=")[0]:q.split("=")[1] for q in request.GET.urlencode().split("&")}

			for x in q_args.items(): 
				kwargs[x[0]]=x[1]

		return function(request, *args, **kwargs)
	return wrap