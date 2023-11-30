"""
Used to create and pass extensions around the application
"""
from flask_pymongo import PyMongo
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap5

# For connections and integration with the MongoDB server
mongo = PyMongo()
# For logging in and handling users
login_manager = LoginManager()
# For user security
bcrypt = Bcrypt()
# For easier integration with bootstrap 5
bootstrap5 = Bootstrap5()
