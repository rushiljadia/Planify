"""For managing and using database modules"""
from bcrypt import checkpw
from .extensions import mongo, login_manager


class User:
    """Class for the user module"""

    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        """To get if the user is authenticated"""
        return True

    @staticmethod
    def is_active():
        """To get if a user is active"""
        return True

    @staticmethod
    def is_anonymous():
        """To get if a user is anonymous"""
        return False

    def get_id(self):
        """To get the users id (username in this case) for the user loader"""
        return self.username

    @staticmethod
    def check_password(password, password_hash):
        """To check the users entered password against the passowrd in the
        database

        Args:
            password (bytes): The password that the user has entered
            password_hash (bytes): The password hash stored in the databse

        Returns:
            bool: Returns true if the passwords match, false otherwise
        """
        return checkpw(password, password_hash)


# Where to redirect unaruorized user
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(username):
    """Checks the user id for the current session and will load the user
    object from that id

    Args:
        username (string): The users username

    Returns:
        User: The user matching the username
    """
    # Finding the user based on the session username
    u = mongo.db.users.find_one({"name": username})
    if not u:
        return None

    return User(username=u["name"])
