from webapp import app
from flask import request, make_response, abort, send_file


# static files loader route, capable of loading multiple files of either js or css but not together
@app.route("/static", methods=["GET"])
def static_loader():
	"""
	GET:
		description: single route for requesting concatenated static files, either JS or CSS

		args:
			t: type of file, either "js" or "css"
			q: filenames of requested files in order, separated by "&" in the url

		security: None required
		responses:
			200: returns the requested js or css files all concatenated together

			404: error not found if the requested filetype is neither js or css
	:authors:
		- Matt
	:returns: HTTP Response
	"""
	# lookup table for mimetypes
	mimetype_lookup = {
		"js": "text/javascript",
		"css": "text/css"
	}
	# load url args from request object
	args = request.args
	filetype = args["t"]
	if filetype == "js":
		try:
			# check the static content cache for the requested combination
			output_blob = app.static_content_cache[filetype][args["q"]]
		except KeyError:
			file_list = args["q"].split(" ")
			output = []
			for file in file_list:
				if file != '':
					# load and concatenate all of the requested files
					with open(
							str(app.root + "/webapp/static/" + filetype + "/" + file).replace("\\", "/"),
							"r") as contents:
						output.append(contents.read())
			# create http response from concatenated files
			output_blob = "\n".join(output)

		response = make_response(output_blob)
		# set correct mimetype for response
		response.mimetype = mimetype_lookup[filetype]
		return response
	elif filetype == "css":
		files = request.args.to_dict(flat=False)['q'][0].split(" ")
		output = []
		for file in files:
			# if file in app.available_css:
			# 	if (content := app.static_content_cache[filetype].get(file)) is not None:
			# 		output.append(content)
			# 	else:
			# 		with open(str(app.root + "/webapp/static/css/" + file), "r") as contents:
			# 			output.append(contents.read())
			# 			app.static_content_cache[filetype][file] = output[-1]
			if (new_file := file[:-4] + ".scss") in app.available_scss:
				if app.config["FLASK_ENV"] == "development":
					with open(str(app.root + "/webapp/static/scss/" + new_file), "r") as contents:
						output.append(app.scss_compiler.compile_string(contents.read()))
				else:
					output.append(app.static_content_cache[filetype].get(file))
			else:
				abort(404)

		output_blob = "\n".join(output)
		response = make_response(output_blob)
		# set correct mimetype for response
		response.mimetype = mimetype_lookup[filetype]
		return response
	elif filetype == "img":
		filename = args["q"]
		return send_file(app.root + "/webapp/static/" + filetype + "/" + filename, mimetype='image/jpg')
	else:
		abort(404)
