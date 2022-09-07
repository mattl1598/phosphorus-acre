import random
import os
from os import walk
from scss.compiler import Compiler
from scss.namespace import Namespace
from scss.types import Number
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


def rand(x):
	return Number(random.random()*int(x))


def mod(x, y):
	return Number(x % y)


namespace = Namespace()
namespace.set_function('random', 1, rand)
namespace.set_function('mod', 2, mod)
app.scss_compiler = Compiler(namespace=namespace, search_path=scss_paths)

from webapp.routes import main_routes, support_routes
