import os
from os import walk
from scss.compiler import Compiler
from flask import Flask
import json

app = Flask(__name__)
app.config["FLASK_ENV"] = "development"

app.root = os.getcwd().replace("\\", "/")

with open("env.json", "r") as file:
	envs = json.load(file)

# get available scss files
app.scss_path = "static/scss/"
for (_, _, app.available_scss) in walk("webapp/" + app.scss_path):
	print(app.available_scss)
	break

scss_paths = [
	"webapp/" + app.scss_path,
	"webapp/" + app.scss_path + "partials"
]
app.scss_compiler = Compiler(search_path=scss_paths)

from webapp.routes import main_routes, support_routes
