from flask import render_template
from webapp import app


@app.route("/")
def landing():
	return render_template("landing.html")


@app.route("/projects")
def projects():
	return render_template("projects.html")


@app.route("/cv")
def cv():
	return render_template("cv.html")

@app.route("/test")
def test():
	return render_template("test.html")