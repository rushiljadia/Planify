from flask import request
from extensions import mongo

db = mongo.planify
users = db.users
courses = db.courses


class User:

    def sign_up(self):
        user = {
            "_id": "",
            
        }