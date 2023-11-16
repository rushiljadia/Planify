from pymongo import MongoClient
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, ".env"))

client = MongoClient(environ.get("MONGODB_CONNECTION"))
