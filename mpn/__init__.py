from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS
import os

from mpn.config import SECRET_KEY, MONGO_DBNAME, MONGO_URI

# initialize app
app = Flask(__name__)

# save config
app.config["SECRET_KEY"] = SECRET_KEY
app.config["MONGO_DBNAME"] = MONGO_DBNAME
app.config["MONGO_URI"] = MONGO_URI

# use cors middleware
CORS(app)

# initialize db
#mongo = PyMongo(app)
