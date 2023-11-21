from bcrypt import checkpw
from .extensions import mongo, login_manager


class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    @staticmethod
    def check_password(password, password_hash):
        return checkpw(password, password_hash)


# Where to redirect unaruorized user
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(username):
    u = mongo.db.users.find_one({"name": username})
    if not u:
        return None

    return User(username=u["name"])
