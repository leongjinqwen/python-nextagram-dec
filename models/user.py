from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class User(UserMixin,BaseModel):
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()

    def validate(self):
        duplicate_username = User.get_or_none(User.username==self.username)
        password_regex = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"

        if duplicate_username:
            self.errors.append("username not unique")
        if re.search(password_regex, self.password) == None:
            self.errors.append("Minimum eight characters, at least one letter and one number")
        else :
            self.password = generate_password_hash(self.password)
