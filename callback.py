def callback(*req):
	print(req)
	print(getattr(req, 'data', ''))